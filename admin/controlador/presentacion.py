from flask import request, jsonify
from admin.modelo.presentacion import PresentacionModelo


class PresentacionControlador:

    @staticmethod
    def handle_request(ruta):
        return PresentacionControlador.presentacion()

    @staticmethod
    def presentacion():

        modelo = PresentacionModelo()


        if request.method == "POST" and request.form.get("buscar"):

                    presentacion = request.form.get("buscar")

                    resultado = modelo.buscar(presentacion)

                    if resultado:
                        return jsonify({
                            "existe": True
                        })
                    else:
                        return jsonify({
                            "existe": False
                        })


        # =========================
        # REGISTRAR PRESENTACIÓN
        # =========================
        if request.method == "POST" and request.form.get("registrar"):

            modelo.presentacion = request.form.get("presentacion")

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado con éxito",
                    "text": "La presentación ha sido registrada correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar la presentación."
            })


        # =========================
        # EDITAR PRESENTACIÓN
        # =========================
        if request.method == "POST" and request.form.get("actualizar"):

            modelo.cod_presentacion = request.form.get("cod_presentacion")
            modelo.presentacion = request.form.get("presentacion")
            modelo.status = request.form.get("status")

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "Los datos de la presentación han sido actualizados correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo editar la presentación."
            })

        # =========================
        # ELIMINAR PRESENTACION
        # =========================
        if request.method == "POST" and request.form.get("eliminar"):

            cod_presentacion = request.form.get("cod_presentacion")

            resul = modelo.eliminar(cod_presentacion)

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado",
                    "text": "La presentación fue eliminada correctamente."
                })

            return jsonify({
                "icon": "warning",
                "title": "Advertencia",
                "text": "La presentación está asociada a una unidad  no puede eliminarse."
            })
        

        data = modelo.consultar()

        return {
            "presentacion": data
        }


def handle_request(ruta):
    return PresentacionControlador.handle_request(ruta)