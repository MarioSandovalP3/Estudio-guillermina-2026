from flask import request, jsonify
from admin.modelo.disponibilidad import DisponibilidadModelo


def handle_request(ruta):

        modelo = DisponibilidadModelo()


                      
        estilistas = modelo.consultar_por_tipo("Estilista")
        manicuristas = modelo.consultar_por_tipo("Manicurista")

        return {
            "estilistas": estilistas,
            "manicuristas": manicuristas
        }