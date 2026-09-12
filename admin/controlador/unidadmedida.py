from flask import request, jsonify
from admin.modelo.unidadmedida import UnidadmedidaModelo

def handle_request(ruta):
        
        modelo = UnidadmedidaModelo()

        if request.method == "POST" and request.form.get("buscar"):
            medida = request.form.get("buscar")

            resultado = modelo.buscar(medida)

            if resultado:
                return jsonify({
                    "existe": True
                })
            else:
                return jsonify({
                    "existe": False
                })

        # =========================
        # REGISTRAR  MEDIDA
        # =========================
# =========================
# REGISTRAR MEDIDA
# =========================
        if request.method == "POST" and request.form.get("registrar"):

            medida = request.form.get("medida")

            validar = modelo.validarMedida(medida)

            if not validar["status"]:
                return jsonify(validar)

            modelo.medida = medida

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado con éxito",
                    "text": "La medida ha sido registrada correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar la medida."
            })


        # =========================
        # EDITAR
        # =========================
        if request.method == "POST" and request.form.get("actualizar"):

            medida = request.form.get("medida")

            validar = modelo.validarMedida(medida)

            if not validar["status"]:
                return jsonify(validar)

            modelo.cod_medida = request.form.get("cod_medida")
            modelo.medida = medida
            modelo.status = request.form.get("status")

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "Los datos de la medida han sido actualizados correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo editar la medida."
            })

        # =========================
        # ELIMINAR MEDIDA
        # =========================
        if request.method == "POST" and request.form.get("eliminar"):

            cod_medida = request.form.get("cod_medida")

            resul = modelo.eliminar(cod_medida)

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado",
                    "text": "La medida fue eliminada correctamente."
                })

            return jsonify({
                "icon": "warning",
                "title": "No se puede eliminar",
                "text": "La medida está asociada a una unidad y no se puede eliminar ."
            })



        data = modelo.consultar()

        return {
            "unidadmedida": data
        }