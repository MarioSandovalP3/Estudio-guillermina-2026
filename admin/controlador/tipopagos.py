from flask import request, jsonify
from admin.modelo.tipopagos import TipopagosModelo


def handle_request(ruta):
        
        modelo = TipopagosModelo()


        if request.method == "POST" and request.form.get("buscar"):

            nombre_tipo_pago = request.form.get("buscar")

            resultado = modelo.buscar(nombre_tipo_pago)

            if resultado:
                return jsonify({
                    "existe": True
                })
            else:
                return jsonify({
                    "existe": False
                })

        # =========================
        # REGISTRAR TIPO DE PAGO
        # =========================
        if request.method == "POST" and request.form.get("registrar"):

            nombre_tipo_pago = request.form.get("nombre_tipo_pago", "").strip()
            validar = modelo.validarTipoPago(nombre_tipo_pago)

            if not validar["status"]:
                return jsonify(validar)

            try:
                modelo.nombre_tipo_pago = nombre_tipo_pago
            except ValueError as error:
                return jsonify({
                    "icon": "warning",
                    "title": "Dato inválido",
                    "text": str(error)
                })

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado",
                    "text": "El tipo de pago ha sido registrado correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar el tipo de pago."
            })

        # =========================
        # EDITAR TIPO DE PAGO
        # =========================
        if request.method == "POST" and request.form.get("actualizar"):

            nombre_tipo_pago = request.form.get("nombre_tipo_pago", "").strip()
            validar = modelo.validarTipoPago(nombre_tipo_pago)

            if not validar["status"]:
                return jsonify(validar)

            modelo.cod_tipo_pago = request.form.get("cod_tipo_pago")

            try:
                modelo.nombre_tipo_pago = nombre_tipo_pago
            except ValueError as error:
                return jsonify({
                    "icon": "warning",
                    "title": "Dato inválido",
                    "text": str(error)
                })

            modelo.status = request.form.get("status")

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "Los datos del tipo de pago han sido actualizados correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo editar el tipo de pago."
            })



        if request.method == "POST" and request.form.get("eliminar"):

            cod_tipo_pago = request.form.get("cod_tipo_pago")

            resul = modelo.eliminar(cod_tipo_pago)

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado",
                    "text": "El tipo de pago fue eliminado correctamente."
                })

            return jsonify({
                "icon": "warning",
                "title": "No se puede eliminar",
                "text": "El tipo de pago está asociado a pagos activos y no se puede eliminar."
            })

        tipopagos = modelo.consultar()
        
        return {"tipopagos": tipopagos}
