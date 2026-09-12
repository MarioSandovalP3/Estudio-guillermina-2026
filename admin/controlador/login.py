from flask import request, jsonify, session
from admin.modelo.clientes import ClientesModelo
from admin.modelo.usuarios import UsuariosModelo
from admin.modelo.empresa import EmpresaModelo
from admin.servicios.bitacora_logger import guardar_bitacora
import bcrypt
from datetime import datetime
import random

def cerrar_sesion():
    session.clear()
    return True



def handle_request(ruta):

    # =========================================================
    # GENERAR CAPTCHA
    # =========================================================
    if request.method == "POST" and request.form.get("generar_captcha"):

        numero1 = random.randint(1, 9)
        numero2 = random.randint(1, 9)

        session["captcha_respuesta"] = numero1 + numero2
        session["captcha_verificado"] = False

        return jsonify({
            "status": True,
            "numero1": numero1,
            "numero2": numero2
        })


    # =========================================================
    # VERIFICAR CAPTCHA
    # =========================================================
    if request.method == "POST" and request.form.get("verificar_captcha"):

        respuesta_usuario = request.form.get("respuesta")
        respuesta_correcta = session.get("captcha_respuesta")

        if respuesta_usuario == str(respuesta_correcta):

            session["captcha_verificado"] = True
            session.pop("captcha_respuesta", None)

            return jsonify({
                "status": True,
                "verificado": True
            })

        session["captcha_verificado"] = False

        return jsonify({
            "status": False,
            "verificado": False
        })






    # ==========================
    # MODELOS
    # ==========================
    modelo_cliente = ClientesModelo()
    modelo_usuario = UsuariosModelo()
    modelo_empresa = EmpresaModelo()

        # ==========================
        # MAPEO MODULOS -> RUTAS FLASK
        # ==========================
    MAPEO_MODULOS = {

        "inicio": "inicio",

        "panel_principal": "panel",

        "cliente": "cliente",

        "reserva": "reserva",

        "disponibilidad_especialista": "disponibilidad",

        "tipo_de_servicio": "tiposervicio",

        "promocion": "promocion",

        "compra": "compra",

        "proveedor": "proveedor",

        "producto": "producto",

        "tipo_producto": "tipoproducto",

        "marca": "marca",

        "categoria": "categoria",

        "unidad_de_medida": "unidadmedida",

    

        "presentacion": "presentacion",

        "unidad": "unidad",

        "mi_dato": "misdatos",

        "historial_de_reserva": "misreservas",

        "personal": "personal",

        "pago": "pagos",

        "pago_personal": "pagospersonal",

        "reporte_cliente": "reporte_cliente",

        "reporte_reserva": "reporte_reserva",


        "reporte_pago": "reporte_pago",

        "reporte_pago_estadistico": "reporte_pago_estadistico",

        "reporte_producto": "reporte_producto",

        "reporte_producto_estadistico": "reporte_producto_estadistico",

        "reporte_reserva_estadistico": "reporte_reserva_estadistico",

        "empresa": "empresa",

        "usuario": "usuarios",

        "rol": "rol",

        "permiso": "permisos",

        "especialista": "especialidad",

        "tipo_de_pago": "tipopagos",

        "moneda": "moneda",

        "mantenimiento": "mantenimiento",

        "bitacora": "bitacora"

    }
    # ==========================
    # RECUPERAR CONTRASEÑA
    # ==========================
    if "cedula" in request.form and "new_password" in request.form:

        cedula = request.form.get("cedula")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Las contraseñas no coinciden"
            })

        resultado = modelo_cliente.olvidar_contrasena(
            cedula,
            new_password,
            confirm_password
        )

        if resultado:
            return jsonify({
                "icon": "success",
                "title": "Éxito",
                "text": "Contraseña actualizada correctamente"
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "Usuario no encontrado"
        })

    # ==========================
    # LOGIN
    # ==========================

    if request.method == "POST" and request.form.get("login"):

            # VALIDAR CAPTCHA
            if session.get("captcha_verificado") is not True:
                return jsonify({
                    "icon": "warning",
                    "title": "CAPTCHA requerido",
                    "text": "Verifica el CAPTCHA primero"
                })

            cedula = request.form.get("cedula")
            password = request.form.get("password")

            usuario = modelo_usuario.consultar_por_cedula(cedula)

            # VALIDAR USUARIO
            if not usuario:
                guardar_bitacora(
                    modulo="Login",
                    accion="INTENTO_FALLIDO",
                    descripcion="Intento de inicio de sesión con usuario inexistente",
                    cedula=cedula or 0,
                    ip=request.remote_addr,
                )
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "Usuario no existe"
                })

            if usuario["status"] != 1:
                guardar_bitacora(
                    modulo="Login",
                    accion="INTENTO_FALLIDO",
                    descripcion="Intento de inicio de sesión con usuario inactivo",
                    cedula=usuario.get("cedula") or cedula,
                    ip=request.remote_addr,
                )
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "Usuario inactivo"
                })

            # ==========================
            # VALIDAR BLOQUEO
            # ==========================
            if modelo_usuario.usuario_bloqueado(cedula):
                guardar_bitacora(
                    modulo="Login",
                    accion="INTENTO_FALLIDO",
                    descripcion="Intento de inicio de sesión en usuario bloqueado",
                    cedula=cedula,
                    ip=request.remote_addr,
                )
                return jsonify({
                    "icon": "warning",
                    "title": "Usuario bloqueado",
                    "text": "Ha superado el número máximo de intentos. Espere 5 minutos."
                })
            
            password_db = usuario["password"]

            if not bcrypt.checkpw(
                password.encode("utf-8"),
                password_db.encode("utf-8")
            ):

                modelo_usuario.aumentar_intentos(cedula)

                usuario = modelo_usuario.consultar_por_cedula(cedula)

                guardar_bitacora(
                    modulo="Login",
                    accion="INTENTO_FALLIDO",
                    descripcion=f"Contraseña incorrecta. Intento {usuario['intentos_fallidos']} de 3.",
                    cedula=cedula,
                    ip=request.remote_addr,
                )

                if usuario["intentos_fallidos"] >= 3:

                    return jsonify({
                        "icon": "warning",
                        "title": "Usuario bloqueado",
                        "text": "Ha superado el número máximo de intentos. Espere 5 minutos."
                    })

                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": f"Contraseña incorrecta. Intento {usuario['intentos_fallidos']} de 3."
                })
            
            # ==========================
            modelo_usuario.reiniciar_intentos(cedula)
            # ==========================
            # SESIÓN
            # ==========================
            session.clear()

            session.permanent = True
            session["iniciarsesion"] = "ok"
            session["cedula"] = usuario["cedula"]
            session["nombre_usuario"] = usuario["nombre_usuario"]
            session["apellido_usuario"] = usuario["apellido_usuario"]
            session["correo"] = usuario["correo"]
            session["telefono"] = usuario["telefono"]
            session["direccion"] = usuario["direccion"]
            session["cod_rol"] = usuario["cod_rol"]
            session["rol"] = usuario["rol"]

            session["ultimo_acceso"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            logo = modelo_empresa.mostrar()

            if logo:
                session["logo"] = logo[0]["logo"]
                session["n_empresa"] = logo[0]["nombre"]
                session["telefono_empresa"] = logo[0]["telefono"]
                session["email_empresa"] = logo[0]["email"]
                session["direccion_empresa"] = logo[0]["direccion"]
            # ==========================
            # PERMISOS 
            # ==========================
            permisos = modelo_usuario.consultar_permisos_rol(usuario["cod_rol"])

            session["modulos"] = {}

            for permiso in permisos:

                raw = permiso["nombre_modulo"].strip().lower()

                ruta_modulo = MAPEO_MODULOS.get(raw)

                if ruta_modulo:
                    session["modulos"][ruta_modulo] = True

                        

            print("MODULOS:", session["modulos"])

            # ==========================
            # REDIRECCIÓN POR ROL
            # ==========================
            if usuario["rol"] == "administrador":
                redirect_url = "/admin?ruta=inicio"

            elif usuario["rol"] == "cliente":
                redirect_url = "/admin?ruta=reservacliente"

            else:
                redirect_url = "/admin?ruta=inicio"

            guardar_bitacora(
                modulo="Login",
                accion="INICIO_SESION",
                descripcion=f"Inicio de sesión exitoso de {usuario['nombre_usuario']} {usuario['apellido_usuario']}",
                cedula=usuario["cedula"],
                ip=request.remote_addr,
            )

            return jsonify({
                "icon": "success",
                "title": "Bienvenido",
                "text": usuario["nombre_usuario"],
                "redirect": redirect_url
            })

    return {}