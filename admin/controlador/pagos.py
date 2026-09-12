from flask import request, jsonify
from admin.modelo.pagos import PagosModelo
import datetime
from admin.servicios.tasa import (
    obtener_tasa_bcv,
    obtener_tasa_usdt_ves,
    obtener_tasa_usdt_binance,
    obtener_tasa_paralelo,
    obtener_tasa_euro_usd,
)


def _normalizar_nombre(nombre_moneda):
    nombre = (nombre_moneda or '').strip().lower()
    return ''.join(ch for ch in nombre if ch.isalnum())


def _calcular_valor_cambio(monto, nombre_moneda, modelo, tasa_bcv=0.0, tasa_usdt_ves=0.0, tasa_usdt_binance=0.0, tasa_paralelo=0.0, tasa_euro_usd=0.0):
    try:
        monto_valor = float(monto or 0.0)
    except Exception:
        monto_valor = 0.0

    if monto_valor <= 0:
        return 0.0

    nombre_limpio = _normalizar_nombre(nombre_moneda)

    if not tasa_bcv or tasa_bcv <= 0:
        return monto_valor

    if nombre_limpio in {'dolar', 'dolares', 'usd', 'usdves', 'dolarves', 'dolarv', 'usdv'}:
        return monto_valor * float(tasa_bcv)

    if nombre_limpio in {'bolivar', 'bolivares', 'ves', 'bs', 'bsf', 'bss'}:
        return monto_valor * float(tasa_bcv)

    if nombre_limpio in {'euro', 'eur', 'euros'}:
        if tasa_euro_usd and tasa_euro_usd > 0:
            return monto_valor * float(tasa_bcv) * float(tasa_euro_usd)
        return monto_valor * float(tasa_bcv)

    if nombre_limpio in {'usdt', 'tether', 'stablecoin'}:
        if tasa_usdt_ves and tasa_usdt_ves > 0:
            return monto_valor * float(tasa_usdt_ves)
        if tasa_paralelo and tasa_usdt_binance and tasa_paralelo > 0 and tasa_usdt_binance > 0:
            return monto_valor * float(tasa_paralelo) * float(tasa_usdt_binance)
        if tasa_usdt_binance and tasa_usdt_binance > 0:
            return monto_valor * float(tasa_bcv) * float(tasa_usdt_binance)
        return monto_valor * float(tasa_bcv)

    return monto_valor * float(tasa_bcv)


def handle_request(ruta):
    return pagos()


def pagos():
    modelo = PagosModelo()
    mensaje = None

    if request.method == "POST" and request.form.get("registrar"):
        errores = []

        cod_servicio = int(request.form.get("cod_servicio", 0) or 0)
        cedula_cliente = request.form.get("cedula_cliente", "").strip()
        fecha_pago = request.form.get("fecha_pago", "").strip()
        monto = float(request.form.get("monto", 0) or 0)
        cod_tipo_pago = int(request.form.get("cod_tipo_pago", 0) or 0)
        cod_moneda = int(request.form.get("cod_moneda", 1) or 1)
        archivo_comprobante = request.files.get("comprobante_pago")
        comprobante_pago_texto = request.form.get("comprobante_pago", "").strip()

        if not cedula_cliente:
            errores.append("Debe seleccionar un cliente.")
        if cod_servicio <= 0:
            errores.append("Servicio no válido.")
        if not fecha_pago:
            errores.append("Debe indicar la fecha del pago.")
        if cod_tipo_pago <= 0:
            errores.append("Debe seleccionar un tipo de pago.")
        if cedula_cliente and cod_servicio > 0 and not modelo.servicio_pertenece_a_cliente(cod_servicio, cedula_cliente):
            errores.append("El servicio seleccionado no pertenece al cliente indicado.")

        monto_servicio = modelo.obtener_monto_servicio(cod_servicio) if cod_servicio > 0 else None
        if monto_servicio is None:
            errores.append("No se pudo calcular el monto del servicio seleccionado.")
        else:
            monto = monto_servicio

        if archivo_comprobante and archivo_comprobante.filename != "":
            if not archivo_comprobante.mimetype.startswith("image/"):
                errores.append("El comprobante debe ser una imagen.")

            archivo_comprobante.seek(0, 2)
            size = archivo_comprobante.tell()
            archivo_comprobante.seek(0)

            if size > 5 * 1024 * 1024:
                errores.append("El comprobante no puede superar 5MB.")

            if archivo_comprobante.mimetype not in ["image/jpeg", "image/png", "image/gif"]:
                errores.append("Formato no permitido. Use JPG, PNG o GIF.")

        # permitir fecha de pago solo si es hoy o la fecha del servicio
        try:
            fecha_hoy = datetime.date.today().isoformat()
            if fecha_pago and fecha_pago != fecha_hoy:
                # buscar la fecha del servicio seleccionado
                servicios_list = modelo.listar_servicios()
                servicio_fecha = None
                for s in servicios_list:
                    if int(s.get('cod_servicio') or 0) == int(cod_servicio or 0):
                        servicio_fecha = str(s.get('fecha') or '')
                        break

                if not servicio_fecha:
                    errores.append("No se encontró la fecha del servicio para validar la fecha de pago.")
                else:
                    if fecha_pago != servicio_fecha:
                        errores.append("La fecha de pago debe ser la fecha actual o la fecha del servicio.")
        except Exception:
            
            pass

        validar = modelo.validarPago(
            cod_servicio=cod_servicio,
            fecha_pago=fecha_pago,
            monto=monto,
            cod_tipo_pago=cod_tipo_pago,
            cod_moneda=cod_moneda,
            comprobante_pago=(archivo_comprobante.filename if archivo_comprobante and archivo_comprobante.filename != "" else comprobante_pago_texto or None)
        )

        if not validar["status"]:
            return jsonify(validar)

        if errores:
            return jsonify({
                "icon": "error",
                "title": "Error de validación",
                "text": " ".join(errores)
            })

        try:
            modelo.cod_servicio = cod_servicio
            modelo.fecha_pago = fecha_pago
            modelo.monto = monto
            modelo.status = 1
            modelo.cod_tipo_pago = cod_tipo_pago
            modelo.cod_moneda = cod_moneda
        except ValueError as error:
            return jsonify({
                "icon": "warning",
                "title": "Dato inválido",
                "text": str(error)
            })

        if archivo_comprobante and archivo_comprobante.filename != "":
            modelo.subir_comprobante(archivo_comprobante)
        else:
            modelo.comprobante_pago = comprobante_pago_texto or None

        resultado = modelo.registrar_con_detalle()

        if resultado.get("success"):
            return jsonify({
                "icon": "success",
                "title": "Pago registrado",
                "text": "el pago se ha registrado con éxito"
            })
        # Si el modelo devolvió errores por campo
        if resultado.get('errors'):
            return jsonify({
                "icon": "error",
                "title": "Error de validación",
                "text": "Corrija los campos indicados.",
                "errors": resultado.get('errors')
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": resultado.get("error", "No se pudo registrar el pago ni el detalle.")
        })

    if request.method == "POST" and request.form.get("listar"):
        cod_servicio = int(request.form.get("cod_servicio", 0) or 0)
        data = modelo.consultar_por_servicio(cod_servicio)
        return jsonify({"success": True, "data": data})

    if request.method == "POST" and request.form.get("listar_tipos_pago"):
        tipos = modelo.listar_tipos_pago()
        return jsonify({"success": True, "data": tipos})

    if request.method == "POST" and request.form.get("anular"):
        cod_pago = request.form.get("cod_pago_a_anular")

        if cod_pago:
            resultado = modelo.anular(cod_pago)
            if resultado:
                return jsonify({
                    "icon": "success",
                    "title": "Pago anulado con éxito",
                    "text": "El pago se anuló correctamente."
                })
            else:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "No se pudo anular el pago"
                })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se indicó el pago a anular"
        })

    tasa_bcv = obtener_tasa_bcv()
    tasa_usdt_ves = obtener_tasa_usdt_ves()
    tasa_usdt_binance = obtener_tasa_usdt_binance()
    tasa_paralelo = obtener_tasa_paralelo()
    tasa_euro_usd = obtener_tasa_euro_usd()
    registro = modelo.consultar()
    for pago in registro:
        pago['valor'] = _calcular_valor_cambio(
            pago.get('monto'),
            pago.get('nombre_moneda'),
            modelo,
            tasa_bcv,
            tasa_usdt_ves,
            tasa_usdt_binance,
            tasa_paralelo,
            tasa_euro_usd,
        )
    tipopagos = modelo.listar_tipos_pago()
    monedas = modelo.listar_monedas()
    servicios = modelo.listar_servicios()
    clientes = modelo.listar_clientes()
    
    for s in servicios:
        try:
            precio_val = float(s.get('precio_total') or 0)
        except Exception:
            precio_val = 0.0

        if not precio_val or precio_val <= 0:
            precios_raw = s.get('precios') or ''
            if precios_raw:
                suma = 0.0
                for part in precios_raw.split(' | '):
                    try:
                        v = float(part)
                        suma += v
                    except Exception:
                        continue
                if suma > 0:
                    s['precio_total'] = suma
    return {"registro": registro, "tipopagos": tipopagos, "monedas": monedas, "servicios": servicios, "clientes": clientes, "mensaje": mensaje}
