from flask import request, jsonify
from admin.modelo.personal import PersonalModelo

def handle_request(ruta):
        
        modelo = PersonalModelo()

   
        if request.method == "POST" and request.form.get("buscar"):
            cedula = request.form.get("buscar")
            resultado = modelo.buscar(cedula)
            if resultado:
                return jsonify({"existe": True})
            else:
                return jsonify({"existe": False})

        # =========================
        # REGISTRAR (AJAX)
        # =========================
        if request.method == "POST" and request.form.get("registrar"):
            modelo.cedula = request.form.get("cedula")
            modelo.nombre_usuario = request.form.get("nombre_usuario")
            modelo.apellido_usuario = request.form.get("apellido_usuario")
            modelo.telefono = request.form.get("telefono")
            modelo.direccion = request.form.get("direccion")
            modelo.correo = request.form.get("correo")
            modelo.cod_rol = request.form.get("cod_rol")
            modelo.password = request.form.get("password_reg") or None

            validaciones = (
                modelo.validarNombreUsuario(),
                modelo.validarApellidoUsuario(),
                modelo.validarCorreo(),
            )
            for validacion in validaciones:
                if not validacion["status"]:
                    return jsonify(validacion)

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado con éxito",
                    "text": "El personal ha sido registrado correctamente."
                })
            else:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "No se pudo registrar el personal."
                })

        # =========================
        # EDITAR (AJAX)
        # =========================
        if request.method == "POST" and request.form.get("actualizar"):

            modelo.cedula = request.form.get("cedula")
            modelo.nombre_usuario = request.form.get("nombre_usuario")
            modelo.apellido_usuario = request.form.get("apellido_usuario")
            modelo.telefono = request.form.get("telefono")
            modelo.direccion = request.form.get("direccion")
            modelo.correo = request.form.get("correo")
            modelo.cod_rol = request.form.get("cod_rol")
            modelo.status = request.form.get("status")

            validaciones = (
                modelo.validarNombreUsuario(),
                modelo.validarApellidoUsuario(),
                modelo.validarCorreo(),
            )
            for validacion in validaciones:
                if not validacion["status"]:
                    return jsonify(validacion)

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "Los datos del cliente fueron actualizados correctamente."
                })
            else:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "No se pudo actualizar el cliente."
                })

        # =========================
        # ELIMINAR PERSONAL
        # =========================
        if request.method == "POST" and request.form.get("eliminar"):
            cedula = request.form.get("cedula")
            resul = modelo.eliminar(cedula)

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado con éxito",
                    "text": "El personal ha sido eliminado correctamente."
                })
            else:
                return jsonify({
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "Este personal tiene un especialista  asociado."
                })

        # =========================
        # GET (vista)
        # =========================
        registro = modelo.consultar()
        roles = modelo.obtener_roles()

        return {"registro": registro, "roles": roles}