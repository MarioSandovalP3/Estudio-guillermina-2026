from flask import request, jsonify

from admin.modelo.moneda import MonedaModelo
from admin.servicios.tasa import (
    obtener_tasa_bcv,
    obtener_tasa_usdt_binance,
    obtener_tasa_usdt_ves,
    obtener_tasa_paralelo,
    obtener_tasa_euro_usd,
)



def handle_request(ruta):
    modelo = MonedaModelo()

    if request.method == "POST" and request.form.get("buscar"):
        nombre_moneda = request.form.get("buscar")
        resultado = modelo.buscar(nombre_moneda)

        return jsonify({"existe": bool(resultado)})

    # =========================
    # REGISTRAR MONEDA
    # =========================
    if request.method == "POST" and request.form.get("registrar"):
        nombre_moneda = request.form.get("nombre_moneda", "").strip()
        validar = modelo.validarMoneda(nombre_moneda)

        if not validar["status"]:
            return jsonify(validar)

        if modelo.buscar(nombre_moneda):
            return jsonify({
                "icon": "warning",
                "title": "Advertencia",
                "text": "Esta moneda ya está registrada."
            })

        try:
            modelo.nombre_moneda = nombre_moneda
        except ValueError as error:
            return jsonify({
                "icon": "warning",
                "title": "Dato inválido",
                "text": str(error)
            })

        resul = modelo.registrar()

        if resul == 1:
            tasa_bcv = obtener_tasa_bcv()
            tasa_usdt_ves = obtener_tasa_usdt_ves()
            tasa_usdt_binance = obtener_tasa_usdt_binance()
            tasa_paralelo = obtener_tasa_paralelo()
            tasa_euro_usd = obtener_tasa_euro_usd()
            if tasa_bcv and tasa_bcv > 0:
                modelo.actualizar_tasas_automaticas(
                    tasa_bcv,
                    tasa_usdt_ves,
                    tasa_usdt_binance,
                    tasa_paralelo,
                    tasa_euro_usd,
                )
            return jsonify({
                "icon": "success",
                "title": "Registrado con éxito",
                "text": "La moneda ha sido registrada correctamente."
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo registrar la moneda."
        })

    # =========================
    # EDITAR
    # =========================
    if request.method == "POST" and request.form.get("actualizar"):
        nombre_moneda = request.form.get("nombre_moneda", "").strip()
        validar = modelo.validarMoneda(nombre_moneda)

        if not validar["status"]:
            return jsonify(validar)

        modelo.cod_moneda = request.form.get("cod_moneda")

        try:
            modelo.nombre_moneda = nombre_moneda
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
                "text": "Los datos de la moneda han sido actualizados correctamente."
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo editar la moneda."
        })

    # =========================
    # ELIMINAR MONEDA
    # =========================
    if request.method == "POST" and request.form.get("eliminar"):
        cod_moneda = request.form.get("cod_moneda")
        resul = modelo.eliminar(cod_moneda)

        if resul == 1:
            return jsonify({
                "icon": "success",
                "title": "Eliminado",
                "text": "La moneda fue eliminada correctamente."
            })

        return jsonify({
            "icon": "warning",
            "title": "No se puede eliminar",
            "text": "La moneda está asociada a un pago activo y no se puede eliminar."
        })

    # Obtener tasa oficial (USD -> BS) para referencia y calcular equivalencias
    tasa_bcv = obtener_tasa_bcv()
    tasa_usdt_ves = obtener_tasa_usdt_ves()
    tasa_usdt_binance = obtener_tasa_usdt_binance()
    tasa_paralelo = obtener_tasa_paralelo()
    tasa_euro_usd = obtener_tasa_euro_usd()
    modelo.actualizar_tasas_automaticas(
        tasa_bcv,
        tasa_usdt_ves,
        tasa_usdt_binance,
        tasa_paralelo,
        tasa_euro_usd,
    )
    data = modelo.consultar()

    for moneda in data:
        # `valor_cambio` viene de la tabla cambio (último valor registrado para esa moneda)
        try:
            valor_cambio = float(moneda.get('valor_cambio') or 0.0)
        except Exception:
            valor_cambio = 0.0

        #  valor_cambio es la cantidad de Bs por 1 unidad de la moneda.
        moneda['valor_bs'] = valor_cambio
        moneda['valor_usd'] = 1.00

    return {
        "monedas": data,
        "tasa_bcv": tasa_bcv
    }

