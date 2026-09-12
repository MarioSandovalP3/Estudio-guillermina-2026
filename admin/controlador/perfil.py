from flask import request, jsonify, session
from admin.modelo.usuarios import UsuariosModelo


def handle_request(ruta):

    modelo = UsuariosModelo()

    # =========================
    # EDITAR PERFIL USUARIO
    # =========================
    if request.method == "POST" and request.form.get("editar"):

        cedula = session.get("cedula")

        if not cedula:
            return jsonify({
                "status": "error",
                "mensaje": "No se encontró la sesión del usuario."
            })

        # datos del form
        nombre = request.form.get("nombre_usuario")
        apellido = request.form.get("apellido_usuario")
        telefono = request.form.get("telefono")
        direccion = request.form.get("direccion")
        correo = request.form.get("correo")

        # modelo
        modelo.cedula = cedula
        modelo.nombre_usuario = nombre
        modelo.apellido_usuario = apellido
        modelo.telefono = telefono
        modelo.direccion = direccion
        modelo.correo = correo
        modelo.cod_rol = session.get("cod_rol")
        modelo.status = 1  

        resul = modelo.editar()

        if resul == 1:

            #  actualizar sesión 
            session["nombre_usuario"] = nombre
            session["apellido_usuario"] = apellido
            session["telefono"] = telefono
            session["direccion"] = direccion
            session["correo"] = correo

            return jsonify({
                "status": "success",
                "mensaje": "Perfil actualizado correctamente.",
                "datos": {
                    "nombre_usuario": nombre,
                    "apellido_usuario": apellido,
                    "telefono": telefono,
                    "direccion": direccion,
                    "correo": correo
                }
            })

        else:
            return jsonify({
                "status": "error",
                "mensaje": "No se pudo actualizar el perfil."
            })

    return {}