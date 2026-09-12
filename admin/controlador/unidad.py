from flask import request, jsonify
from admin.modelo.unidad import UnidadModelo

def handle_request(ruta):
        
        modelo = UnidadModelo()

        if request.method == "POST" and request.form.get("buscar"):
            unidad = request.form.get("buscar")
            cod_presentacion = request.form.get("cod_presentacion")
            cod_medida = request.form.get("cod_medida")
            cod_unidad = request.form.get("cod_unidad")

            resultado = modelo.buscar(
                unidad,
                cod_presentacion,
                cod_medida,
                cod_unidad
            )

            return jsonify({
                "existe": resultado is not None
            })
            
      # =========================
        # REGISTRAR UNIDAD
        # =========================

        if request.method == "POST" and request.form.get("registrar"):

            nombre_unidad = request.form.get("nombre_unidad")

            validar = modelo.validarNombreUnidad(nombre_unidad)

            if not validar["status"]:
                return jsonify(validar)

            modelo.nombre_unidad = nombre_unidad
            modelo.cod_presentacion = request.form.get("cod_presentacion")
            modelo.cod_medida = request.form.get("cod_medida")

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado con éxito",
                    "text": "La unidad ha sido registrada correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar la unidad."
            })

        # =========================
        # EDITAR UNIDAD
        # =========================
        if request.method == "POST" and request.form.get("actualizar"):

            nombre_unidad = request.form.get("nombre_unidad")

            validar = modelo.validarNombreUnidad(nombre_unidad)

            if not validar["status"]:
                return jsonify(validar)

            modelo.cod_unidad = request.form.get("cod_unidad")
            modelo.nombre_unidad = nombre_unidad
            modelo.cod_presentacion = request.form.get("cod_presentacion")
            modelo.cod_medida = request.form.get("cod_medida")
            modelo.status = request.form.get("status")

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "La unidad ha sido actualizada correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo editar la unidad."
            })


        # ==========================================
        # ELIMINAR UNIDAD
        # ==========================================

        if request.method == "POST" and request.form.get("eliminar"):

            cod_unidad = request.form.get("cod_unidad")

            resul = modelo.sp_eliminar_unidad(cod_unidad)

            if resul == 1:

                return jsonify({
                    "icon": "success",
                    "title": "Eliminado con éxito",
                    "text": "La unidad fue eliminada correctamente."
                })

            else:

                return jsonify({
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "La unidad no puede ser eliminada porque tiene productos asociados ."
                })

        unidad = modelo.consultar()
        presentaciones = modelo.obtener_presentaciones()
        medidas = modelo.obtener_medidas()

        return {
            "unidad": unidad,
            "presentaciones": presentaciones,
            "medidas": medidas
        }