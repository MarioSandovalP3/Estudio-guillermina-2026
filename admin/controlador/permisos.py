from flask import request, jsonify
from admin.modelo.permisos import PermisosModelo

def handle_request(ruta):
        
        modelo = PermisosModelo()

        if request.method == "POST" and request.form.get("buscar"):
            cod_rol = request.form.get("cod_rol")
            permisos = request.form.getlist("permisos")
            resultado = modelo.buscar_permisos(cod_rol, permisos)
            return jsonify({"existe": resultado})

        if request.method == "POST" and request.form.get("registrar"):

            cod_rol = request.form.get("cod_rol")

            if not cod_rol:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "Seleccione un rol"
                })

            # OBTENER CHECKBOX MARCADOS
            permisos_form = request.form.getlist("permisos")

            print(permisos_form)

            if not permisos_form:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "Seleccione permisos"
                })

            # CONSTRUIR DICCIONARIO
            permisos = {}

            for permiso in permisos_form:

                datos = permiso.split("-")

                cod_modulo = datos[0]
                cod_accion = datos[1]

                if cod_modulo not in permisos:
                    permisos[cod_modulo] = {}

                permisos[cod_modulo][cod_accion] = True

            print(permisos)

            # REGISTRAR
            resul = modelo.registrar(cod_rol, permisos)

            if resul:
                return jsonify({
                    "icon": "success",
                    "title": "Correcto",
                    "text": "Permisos registrados"
                })

            else:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "No se pudo registrar"
                })

        if request.method == "POST" and request.form.get("actualizar"):

            try:

                cod_rol = request.form.get("cod_rol")
                status = request.form.get("status")

                permisos = request.form.getlist("permisos[]")

                if not permisos:
                    permisos = []

                resultado = modelo.editar(cod_rol, permisos, status)

                if resultado:

                    return jsonify({
                        "icon": "success",
                        "title": "Éxito",
                        "text": "Permisos actualizados correctamente."
                    })

                else:

                    return jsonify({
                        "icon": "error",
                        "title": "Error",
                        "text": "No se pudieron actualizar los permisos."
                    })

            except Exception as e:

                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": f"Error interno: {str(e)}"
                })


        if request.method == "POST" and request.form.get("eliminar"):

            cod_permiso = request.form.get("cod_permiso")

            resultado = modelo.eliminar(cod_permiso)

            if resultado == "eliminado":
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado con éxito",
                    "text": "El permiso ha sido eliminado correctamente."
                })

            if resultado == "tiene_permisos":
                return jsonify({
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "El permiso está asociado a uno o más roles."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo eliminar el permiso."
            })


        # ==========================
        # MOSTRAR DATOS (GET)
        # ==========================
        permisos = modelo.consultar()
        acciones = modelo.obtener_acciones()
        roles = modelo.obtener_roles()
        modulos = modelo.obtener_modulos()

        return {
            "permisos": permisos,
            "acciones": acciones,
            "roles": roles,
            "modulos": modulos
        }