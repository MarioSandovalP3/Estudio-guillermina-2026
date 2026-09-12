
from flask import request, jsonify

from admin.modelo.panel import PanelModelo


def handle_request(ruta):

    modelo = PanelModelo()

    clientes = modelo.consultar_clientes_activos()

    reservas = modelo.consultar_total_reservas_activas()
    reservas_mes = modelo.reservas_por_mes()
    reservas_dia = modelo.reservas_por_dia()
    ingresos_mes = modelo.ingresos_por_mes()

    ingresos_dia = modelo.ingresos_por_dia()

    servicios_populares = modelo.servicios_populares()
    productos_stock = modelo.productos_stock()

    return {

        "reservas_mes": reservas_mes,

        "reservas_dia": reservas_dia,


        "ingresos_mes": ingresos_mes,

        "ingresos_dia": ingresos_dia,

        "productos_stock": productos_stock,

        "clientes": clientes,

        "reservas": reservas,

        "servicios_populares": servicios_populares

    }