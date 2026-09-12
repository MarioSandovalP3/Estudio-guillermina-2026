from flask import request, jsonify
from admin.modelo.usuarios import UsuariosModelo


def handle_request(ruta):
        
        modelo = UsuariosModelo()

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
        # REGISTRAR 
        # ========================

        if request.method == "POST" and request.form.get("registrar"):

            cedula = request.form.get("cedula")

            validar = modelo.validarUsuario(
                cedula,
                request.form.get("nombre_usuario"),
                request.form.get("apellido_usuario"),
                request.form.get("telefono"),
                request.form.get("direccion"),
                request.form.get("correo"),
                request.form.get("password")
            )

            if not validar["status"]:
                return jsonify(validar)

            # =========================
            # VERIFICAR SI YA EXISTE
            # =========================
            dato = modelo.buscar(cedula)

            if dato:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "El usuario ya se encuentra registrado."
                })

            # =========================
            # ASIGNAR DATOS AL MODELO
            # =========================
            modelo.cedula = cedula
            modelo.nombre_usuario = request.form.get("nombre_usuario")
            modelo.apellido_usuario = request.form.get("apellido_usuario")
            modelo.telefono = request.form.get("telefono")
            modelo.direccion = request.form.get("direccion")
            modelo.correo = request.form.get("correo")
            modelo.cod_rol = request.form.get("cod_rol")
            modelo.password = request.form.get("password")

            # =========================
            # EJECUTAR REGISTRO
            # =========================
            resul = modelo.registrar()

            if resul:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado con éxito",
                    "text": "El usuario ha sido registrado correctamente."
                })
            else:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "No se pudo registrar el usuario."
                })

        if request.method == "POST" and request.form.get("actualizar"):

            try:
                
                modelo.cedula = request.form.get("cedula")
                modelo.nombre_usuario = request.form.get("nombre_usuario")
                modelo.apellido_usuario = request.form.get("apellido_usuario")
                modelo.telefono = request.form.get("telefono")
                modelo.direccion = request.form.get("direccion")
                modelo.correo = request.form.get("correo")
                modelo.cod_rol = request.form.get("cod_rol")
                modelo.status = request.form.get("status")

                # =========================
                # PASSWORD OPCIONAL
                # =========================
                password = request.form.get("password")

                if password and password.strip() != "":
                    modelo.password = password

              
                resul = modelo.editar()

                if resul:
                    return jsonify({
                        "icon": "success",
                        "title": "Éxito",
                        "text": "Datos actualizados del usuario correctamente."
                    })

                else:
                    return jsonify({
                        "icon": "error",
                        "title": "Error",
                        "text": "No se pudo editar el usuario. Verifique que el rol exista o que los datos sean válidos."
                    })

            except Exception as e:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": f"Error interno: {str(e)}"
                })

        if request.method == "POST" and request.form.get("eliminar"):

            resul = modelo.eliminar(request.form.get("cedula"))

            if resul == 1:
                return jsonify({
                    'icon': 'success',
                    'title': 'Eliminado con éxito',
                    'text': 'El usuario ha sido eliminado correctamente.'
                })

            elif resul == -2:
                return jsonify({
                    'icon': 'warning',
                    'title': 'No se puede eliminar',
                    'text': 'El usuario está activo y tiene un rol asociado.'
                })

            else:
                return jsonify({
                    'icon': 'error',
                    'title': 'Error',
                    'text': 'No se pudo eliminar el usuario.'
                })




        usuarios = modelo.consultar()
        roles = modelo.obtener_roles()

        return {
            "usuarios": usuarios,
            "roles": roles
        }
