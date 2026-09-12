from flask import request, jsonify
from admin.modelo.notificaciones import NotificacionesModelo


def handle_request():

    modelo = NotificacionesModelo()


    # =====================================================
    # VERIFICAR EMPRESA REGISTRADA
    # =====================================================

    if request.args.get("empresa") == "1":

        empresa_registrada = modelo.consultarEmpresaRegistrada()

        return jsonify({
            "status": True,
            "empresa_registrada": empresa_registrada
        })


    # =====================================================
    # CANCELACIONES
    # =====================================================

    if request.args.get("cancelacion") == "1":

        ultima = modelo.consultarUltimaCancelacion()

        cancelaciones_hoy = modelo.consultarCancelacionesHoy()

        return jsonify({
            "status": True,
            "ultima": ultima,
            "cancelaciones": cancelaciones_hoy
        })


    # =====================================================
    # NOTIFICACIONES GENERALES
    # =====================================================

    datos = modelo.consultar()

    if datos:

        return jsonify({
            "status": True,
            "fecha": datos["fecha"],
            "reservas": datos["reservas"],
            "clientes": datos["clientes"],
            "pagos": datos["pagos"],
            "compras": datos["compras"],
            "productos_bajo_stock": datos["productos_bajo_stock"]
        })


    return jsonify({
        "status": False,
        "mensaje": "No se pudieron consultar las notificaciones."
    }), 500