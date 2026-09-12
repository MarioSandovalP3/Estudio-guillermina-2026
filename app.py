from flask import Flask, render_template, request, session, redirect, url_for ,send_from_directory,jsonify
from datetime import datetime, timedelta
from admin.controlador import controladores
from admin.controlador.login import cerrar_sesion
from admin.servicios.bitacora_logger import registrar_cierre_sesion, registrar_movimiento_sistema
from admin.servicios.tasa import obtener_tasa_bcv
from admin.controlador.notificaciones import handle_request as notificaciones_controller
from admin.modelo.notificaciones import NotificacionesModelo

import threading
import time
import os

from admin.modelo.inicio import InicioModelo
from admin.config.config import FLASK_DEBUG, SECRET_KEY, SESSION_COOKIE_SECURE
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Mantener sesión aunque cierre navegador
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)


app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = SESSION_COOKIE_SECURE


# ==============================
# RUTAS PÚBLICAS
# ==============================

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/quienesomos")
def quienesomos():
    return render_template("quienesomos.html")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html")


@app.route("/promociones")
def promociones():
    return render_template("promociones.html")


@app.route("/preguntas")
def preguntas():
    return render_template("preguntas.html")


# ==============================
# NOTIFICACIONES
# ==============================
@app.route("/notificaciones", methods=["GET"])
def notificaciones():

    if session.get("iniciarsesion") != "ok":

        return jsonify({
            "status": False,
            "mensaje": "Sesión no iniciada"
        }), 401

    return notificaciones_controller()


# ==============================
# LOGIN NO DESTRUYE SESIÓN SI YA EXISTE
# ==============================
@app.route("/login")
def login():

    if session.get("iniciarsesion") == "ok":

        cod_rol = session.get("cod_rol")

        if cod_rol in [1, 2]:
            return redirect(url_for("admin_index", ruta="inicio"))

        if cod_rol == 3:
            return redirect(url_for("admin_index", ruta="reservacliente"))

    session.clear()
    return redirect(url_for("admin_index", ruta="login"))


# ==============================
# ACCESO DESDE BOTÓN WEB
# ==============================
@app.route("/acceder")
def acceder():

    if session.get("iniciarsesion") == "ok":

        cod_rol = session.get("cod_rol")

        if cod_rol in [1, 2]:
            return redirect(url_for("admin_index", ruta="inicio"))

        if cod_rol == 3:
            return redirect(url_for("admin_index", ruta="reservacliente"))

    return redirect(url_for("admin_index", ruta="login"))


# ==============================
# CONTROL TIEMPO FUERA DEL SISTEMA
# ==============================

def sesion_expirada():

    ultimo = session.get("ultimo_acceso")


    if not ultimo:
        return True


    try:

        ultimo_dt = datetime.strptime(
            ultimo,
            "%Y-%m-%d %H:%M:%S"
        )


    except:

        return True



    diferencia = datetime.now() - ultimo_dt


    # Si pasan más de 20 minutos sin entrar al sistema
    if diferencia > timedelta(minutes=20):

        return True


    return False
# ==============================
# FRONT CONTROLLER ADMIN
# ==============================
@app.route("/admin", methods=["GET", "POST"])
def admin_index():

    ruta = request.args.get("ruta")
    datos = {}


    modelo_notificaciones = NotificacionesModelo()
    empresa_configurada = modelo_notificaciones.consultarEmpresaRegistrada()

    if not ruta:
        ruta = "login"

    # ==========================
    # CONTROL DE SESIÓN
    # ==========================
    
    rutas_publicas = ["login"]

    # Permitir registrar y buscar clientes sin iniciar sesión
    if (
        ruta == "cliente"
        and request.method == "POST"
        and (
            request.form.get("registrar")
            or request.form.get("buscar")
        )
    ):
        pass

    elif ruta not in rutas_publicas and session.get("iniciarsesion") != "ok":
        ruta = "login"

# ==========================
# VALIDAR EXPIRACIÓN
# ==========================

    if session.get("iniciarsesion") == "ok":


        if sesion_expirada():

            session.clear()

            return redirect(
                url_for("login")
            )


        # renovar tiempo cuando vuelve al sistema
        session["ultimo_acceso"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    controlador = controladores.get(ruta)

    if controlador:
        respuesta = controlador.handle_request(ruta)

        if hasattr(respuesta, "get_json"):
            return respuesta

        if isinstance(respuesta, dict):
            datos = respuesta

    # ==========================
    # PERMISOS
    # ==========================
    acceso_permitido = False

    if session.get("iniciarsesion") == "ok":

        if ruta in ["reservacliente", "misreservas", "misdatos", "inicio"]:
            acceso_permitido = True
        else:
            modulos = session.get("modulos", {})
            acceso_permitido = modulos.get(ruta, False)


    datos["tasa_bcv"] = obtener_tasa_bcv()

    # ==========================
    # RENDER
    # ==========================
    return render_template(
        "admin/vista/plantilla.html",
        ruta=ruta,
        acceso_permitido=acceso_permitido,
        empresa_configurada=empresa_configurada,
        **datos
    )
@app.route("/admin/descargar-backup/<path:filename>")
def descargar_backup(filename):
    return send_from_directory("static/backups", filename, as_attachment=True)


@app.route("/descargar/<path:filename>")
def descargar_backup_alias(filename):
    return send_from_directory("static/backups", filename, as_attachment=True)


# ==============================
# CERRAR SESIÓN
# ==============================
@app.route("/cerrarsesion")
def cerrarsesion():
    registrar_cierre_sesion()
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    registrar_cierre_sesion()
    return redirect(url_for("admin_index"))

@app.after_request
def registrar_movimiento_despues_de_request(response):
    if (
        session.get("iniciarsesion") == "ok"
        and request.path.startswith("/admin")
        and request.endpoint not in {"cerrarsesion", "logout"}
    ):
        registrar_movimiento_sistema(request.args.get("ruta"), response)

    return response


def proceso_automatico_8pm():

    with app.app_context():

        modelo = InicioModelo()

        while True:

            if datetime.now().hour == 20 and datetime.now().minute == 0:

                modelo.procesar_reservas_8pm()

                time.sleep(60)

            time.sleep(30)


if __name__ == "__main__":

    threading.Thread(
        target=proceso_automatico_8pm,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=FLASK_DEBUG,
    )