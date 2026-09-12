from flask import request, jsonify
from admin.modelo.pagospersonal import PagospersonalModelo


def handle_request(ruta):
    return pagospersonal()


def pagospersonal():
    modelo = PagospersonalModelo()
    mensaje = None

    if request.method == "POST" and request.form.get("registrar"):
        errores = []

        cod_servicio = int(request.form.get("cod_servicio", 0) or 0)
        fecha_pago = request.form.get("fecha_pago", "").strip()
        hora_pago = request.form.get("hora_pago", "").strip()
        if hour := hora_pago:
            hora_pago = hour if len(hour) == 8 else (hour + ':00' if len(hour) == 5 else hour)
        porcentaje = int(request.form.get("porcentaje", 0) or 0)

        if cod_servicio <= 0:
            errores.append("Debe seleccionar un servicio.")
        if not fecha_pago:
            errores.append("Debe indicar la fecha del pago.")
        if porcentaje <= 0:
            errores.append("El porcentaje debe ser mayor a cero.")

        validar = modelo.validarPagoPersonal(
            cod_servicio=cod_servicio,
            fecha_pago=fecha_pago,
            hora_pago=hora_pago,
            porcentaje=porcentaje
        )

        if not validar["status"]:
            return jsonify(validar)

        if errores:
            return jsonify({
                "icon": "error",
                "title": "Error de validación",
                "text": " ".join(errores)
            })

        if modelo.existe_pago_activo(cod_servicio):
            return jsonify({
                "icon": "warning",
                "title": "Pago personal ya registrado",
                "text": "anule el anterior para registrarlo nuevamente"
            })

        try:
            modelo.cod_servicio = cod_servicio
            modelo.fecha_pago = fecha_pago
            modelo.hora_pago = hora_pago or "00:00:00"
            modelo.porcentaje = porcentaje
            modelo.status = 1
        except ValueError as error:
            return jsonify({
                "icon": "warning",
                "title": "Dato inválido",
                "text": str(error)
            })

        if modelo.registrar():
            return jsonify({
                "icon": "success",
                "title": "Pago personal registrado",
                "text": "El pago del personal se registró correctamente.",
                "notificacion": True
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": modelo.ultimo_error or "No se pudo registrar el pago del personal."
        })

    if request.method == "POST" and request.form.get("anular"):
        cod_pago_personal = request.form.get("cod_pago_personal_a_anular")
        if cod_pago_personal:
            resultado = modelo.anular(cod_pago_personal)
            if resultado:
                return jsonify({
                    "icon": "success",
                    "title": "Pago anulado con éxito",
                    "text": "El pago personal se anuló correctamente."
                })
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo anular el pago del personal."
            })

    registro = modelo.consultar()
    servicios = modelo.listar_servicios()
    return {"registro": registro, "servicios": servicios, "mensaje": mensaje}
