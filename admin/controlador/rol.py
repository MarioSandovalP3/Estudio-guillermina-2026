from flask import request, jsonify
from admin.modelo.rol import RolModelo


def handle_request(ruta):

        modelo = RolModelo()

        if request.method == "POST" and request.form.get("buscar"):

            rol = request.form.get("buscar")

            resultado = modelo.buscar(rol)

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
        # =========================
        if request.method == "POST" and request.form.get("registrar"):

            rol = request.form.get("rol")

            validar = modelo.validarRol(rol)

            if not validar["status"]:
                return jsonify(validar)

            modelo.rol = rol

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado con éxito",
                    "text": "El rol ha sido registrado correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar el rol."
            })
        # =========================
        # EDITAR
        # =========================
        if request.method == "POST" and request.form.get("actualizar"):

            modelo.cod_rol = request.form.get("cod_rol")
            modelo.rol = request.form.get("rol")
            modelo.status = request.form.get("status")

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "Los datos del rol han sido actualizados correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo editar el rol."
            })

        # =========================
        # ELIMINAR
        # =========================
        if request.method == "POST" and request.form.get("eliminar"):

            modelo.cod_rol = request.form.get("cod_rol")
            resul = modelo.eliminar(modelo.cod_rol)

            if resul == 'eliminado':
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado con éxito",
                    "text": "El rol ha sido eliminado correctamente."
                })

            if resul == 'existe_usuarios':
                return jsonify({
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "Este rol tiene usuarios asociados."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo eliminar el rol."
            })
                

                
        roles = modelo.consultar()
        return {"roles": roles}