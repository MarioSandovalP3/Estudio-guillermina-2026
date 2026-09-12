from flask import request, jsonify, session
from admin.modelo.empresa import EmpresaModelo


def handle_request(ruta):

        modelo = EmpresaModelo()

# =========================
# REGISTRAR EMPRESA
# =========================
        if request.method == "POST" and request.form.get("registrar"):

            validar = modelo.validarEmpresa(
                request.form.get("nombre"),
                request.form.get("direccion"),
                request.form.get("email"),
                request.form.get("telefono"),
                request.form.get("descripcion_empresa"),
                request.files.get("logo")
            )

            if not validar["status"]:
                return jsonify(validar)

            # =========================
            # ASIGNAR DATOS
            # =========================
            modelo.nombre = request.form.get("nombre")
            modelo.direccion = request.form.get("direccion")
            modelo.telefono = request.form.get("telefono")
            modelo.email = request.form.get("email")
            modelo.descripcion_empresa = request.form.get("descripcion_empresa")
            modelo.fecha_actualizacion = request.form.get("fecha_actualizacion")

            # =========================
            # LOGO
            # =========================
            file = request.files.get("logo")

            if file and file.filename != "":
                modelo.subir_logo(file)
            else:
                modelo.logo = None

            # =========================
            # REGISTRAR
            # =========================
            resul = modelo.registrar()

            if resul == 1:

                # =========================
                # OBTENER EMPRESA REGISTRADA
                # =========================
                empresa_registrada = modelo.mostrar()

                if empresa_registrada:

                    empresa = empresa_registrada[0]

                    # =========================
                    # ACTUALIZAR SESSION
                    # =========================
                    session["logo"] = empresa["logo"]
                    session["n_empresa"] = empresa["nombre"]
                    session["telefono"] = empresa["telefono"]
                    session["email"] = empresa["email"]
                    session["direccion"] = empresa["direccion"]

                    # =========================
                    # RESPUESTA AJAX
                    # =========================
                    return jsonify({
                        "icon": "success",
                        "title": "Registrado con éxito",
                        "text": "La empresa ha sido registrada correctamente.",
                        "empresa_registrada": True,
                        "data": {
                            "logo": empresa["logo"],
                            "nombre": empresa["nombre"]
                        }
                    })

                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "No se pudo obtener la empresa registrada."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar la empresa."
            })
        # =========================
        # EDITAR
        # =========================
        if request.method == "POST" and request.form.get("actualizar"):

            nombre_original = request.form.get("nombre_original")

            file = request.files.get("logo")

            # =========================
            # ASIGNAR DATOS
            # =========================
            modelo.nombre = request.form.get("nombre")
            modelo.direccion = request.form.get("direccion")
            modelo.email = request.form.get("email")
            modelo.telefono = request.form.get("telefono")
            modelo.descripcion_empresa = request.form.get("descripcion_empresa")

            # =========================
            # LOGO
            # =========================
            if file and file.filename != "":
                modelo.subir_logo(file)
            else:
                datos_actuales = modelo.mostrar()
                if datos_actuales:
                    modelo.logo = datos_actuales[0]["logo"]

            # =========================
            # ACTUALIZAR
            # =========================
            resul = modelo.editar(nombre_original)

            if resul == 1:

                empresa_actualizada = modelo.mostrar()

                if empresa_actualizada:
                    session["logo"] = empresa_actualizada[0]["logo"]
                    session["n_empresa"] = empresa_actualizada[0]["nombre"]
                    session["telefono"] = empresa_actualizada[0]["telefono"]
                    session["email"] = empresa_actualizada[0]["email"]
                    session["direccion"] = empresa_actualizada[0]["direccion"]

                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "Los datos de la empresa han sido actualizados.",
                    "data": {
                        "logo": empresa_actualizada[0]["logo"],
                        "nombre": empresa_actualizada[0]["nombre"]
                    }
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo editar la empresa."
            })
        # =========================
        # GET
        # =========================
        empresas = modelo.mostrar()

        return {
            "empresas": empresas
        }