from flask import request, jsonify
from admin.modelo.inicio import InicioModelo
from datetime import datetime

def handle_request(ruta):
        
        modelo = InicioModelo()


# ================== REGISTRAR RESERVA ==================
        if request.method == "POST" and request.form.get("registrar"):

            cedula = request.form.get("cedula")
            fecha = request.form.get("fecha")
            hora = request.form.get("hora")

            cedula_especialista = request.form.get("cedula_especialista")

            cod_tipos_servicio = request.form.getlist("servicio[]")

            if not cod_tipos_servicio:
                return jsonify({
                    "success": False,
                    "message": "Debe seleccionar al menos un servicio"
                })

            resultado = modelo.registrarReservadeclientes(
                cedula,
                cod_tipos_servicio,
                fecha,
                hora,
                cedula_especialista   
            )

            return jsonify(resultado)




        if request.method == "POST" and request.form.get("buscar_horas"):

            fecha = request.form.get("fecha_reserva")

            print("FECHA RECIBIDA:", fecha)

            horas_ocupadas = modelo.horasOcupadas(fecha)

            print("HORAS EN BD:", horas_ocupadas)

            return jsonify({
                "success": True,
                "ocupadas": horas_ocupadas
            })
        # ================== DATOS DEL MODAL ==================

        servicios = modelo.obtenerservicios()

        estilistas = modelo.obtenerEspecialista("Estilista")

        manicuristas = modelo.obtenerEspecialista("Manicurista")

       

        return {
          
            "servicios": servicios,
            "estilistas": estilistas,
            "manicuristas": manicuristas
        }