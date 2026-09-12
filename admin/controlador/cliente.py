from flask import request, jsonify, session
from admin.modelo.clientes import ClientesModelo


def handle_request(ruta):

        modelo = ClientesModelo()

        if request.method == "POST" and request.form.get("buscar"):

            cedula = request.form.get("buscar")

            resultado = modelo.buscar(cedula)

            if resultado:
                return jsonify({
                    "existe": True
                })
            else:
                return jsonify({
                    "existe": False
                })
        # =========================
        # REGISTRAR (AJAX)
        # =========================

        if request.method == "POST" and request.form.get("registrar"):

            validar = modelo.validarCliente(request.form)

            if not validar["status"]:
                return jsonify(validar)

            modelo.cedula = request.form.get("cedula")
            modelo.nombre_usuario = request.form.get("nombre_usuario")
            modelo.apellido_usuario = request.form.get("apellido_usuario")
            modelo.telefono = request.form.get("telefono")
            modelo.direccion = request.form.get("direccion")
            modelo.correo = request.form.get("correo")
            modelo.cod_rol = request.form.get("cod_rol")
            modelo.password = request.form.get("password_reg") or None

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado con éxito",
                    "text": "El cliente ha sido registrado correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar el cliente."
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

         
            if session.get("cedula") == modelo.cedula:
                modelo.status = 1

            resul = modelo.editar()

            if resul == 1:

                if session.get("cedula") == modelo.cedula:

                    session["nombre_usuario"] = modelo.nombre_usuario
                    session["apellido_usuario"] = modelo.apellido_usuario
                    session["telefono"] = modelo.telefono
                    session["direccion"] = modelo.direccion
                    session["correo"] = modelo.correo

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
         # ELIMINAR CLIENTE
         # =========================
        if request.method == "POST" and request.form.get("eliminar"):

            cedula = request.form.get("cedula")

            resul = modelo.eliminar(cedula)

            if resul == 1:

                return jsonify({
                    "icon": "success",
                    "title": "Eliminado con éxito",
                    "text": "El cliente ha sido eliminado correctamente."
                })

            elif resul == -3:

                return jsonify({
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "El cliente debe estar inactivo para poder eliminarlo."
                })

            elif resul == -5:

                return jsonify({
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "El cliente tiene reservas asociadas."
                })

            else:

                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "No fue posible realizar la operación."
                })
        # =========================
        # GET (vista)
        # =========================
        registro = modelo.consultar()
        roles = modelo.obtener_roles()

        return {"registro": registro, "roles": roles}