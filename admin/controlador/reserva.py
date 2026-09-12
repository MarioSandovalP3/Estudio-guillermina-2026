from flask import request, jsonify
from admin.modelo.reservas import ReservasModelo
from datetime import datetime

def handle_request(ruta):

        modelo = ReservasModelo()

        if request.method == "POST" and request.form.get("actualizar"):

            modelo.cod_servicio = request.form.get("cod_servicio")
            modelo.fecha_reserva = request.form.get("fecha")
            modelo.hora_reserva = request.form.get("hora")
            modelo.status = request.form.get("status")

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "La reserva fue actualizada correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo actualizar la reserva."
            })


        if request.method == "POST" and request.form.get("buscar_horas"):

                    fecha = request.form.get("fecha_reserva")

                    horas_ocupadas = modelo.horasOcupadas(fecha)

                    return jsonify({
                        "success": True,
                        "ocupadas": horas_ocupadas
                    })
            
        if request.method == "POST" and request.form.get("eliminar"):

            cod_servicio = request.form.get("cod_servicio")
            resul = modelo.eliminar(cod_servicio)

            if resul == 'eliminado':
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado con éxito",
                    "text": "La reserva ha sido eliminada correctamente."
                })

            if resul == 'activo':
                return jsonify({
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "La reserva está activa y no puede ser eliminada."
                })

            if resul == 'ya_eliminado':
                return jsonify({
                    "icon": "info",
                    "title": "Sin cambios",
                    "text": "La reserva ya estaba eliminada."
                })

            if resul == 'no_existe':
                return jsonify({
                    "icon": "error",
                    "title": "No encontrada",
                    "text": "La reserva no existe."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo eliminar la reserva."
            })          
            
        reservas = modelo.consultar()
        return {"reservas": reservas}