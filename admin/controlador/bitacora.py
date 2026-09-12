from flask import request, jsonify
from admin.modelo.bitacora import BitacoraModelo


def handle_request(ruta):

    modelo = BitacoraModelo()

    # =====================================
    # REGISTRAR
    # =====================================

    if request.method == "POST" and request.form.get("registrar"):

        cedula = request.form.get("cedula")
        modulo = request.form.get("modulo") or ruta or "bitacora"
        accion = request.form.get("accion") or "Registrar"

        resul = modelo.registrar(cedula, modulo, accion)

        if resul:

            return jsonify({
                "icon": "success",
                "title": "Registrado",
                "text": "Movimiento registrado correctamente."
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo registrar el movimiento."
        })

    # =====================================
    # CONSULTAR
    # =====================================

    bitacora = modelo.consultar()

    return {
        "bitacora": bitacora
    }