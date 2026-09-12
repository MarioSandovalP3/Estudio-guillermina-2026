from flask import request, jsonify, session
from admin.modelo.inicio import InicioModelo
from datetime import datetime

def handle_request(ruta):

    modelo = InicioModelo()

    # SIEMPRE obtener la cédula primero
    cedula = session.get("cedula")

    # ================== CALENDARIO ==================

    if request.method == "GET" and request.args.get("cargar_reservas"):

        if not cedula:

            return jsonify([])

        reservas = modelo.consultarConClientes(cedula)

        reservas_unicas = {}

        for r in reservas:

            cod_reserva = r["cod_servicio"]

            servicios = modelo.obtenerServiciosDeReserva(cod_reserva)

            hora_raw = str(r["hora_reserva"]).strip()

            try:

                hora_dt = datetime.strptime(hora_raw, "%H:%M:%S")

            except:

                hora_dt = datetime.strptime(hora_raw, "%I:%M %p")

            hora_iso = hora_dt.strftime("%H:%M:%S")

            hora_12 = hora_dt.strftime("%I:%M %p")

            fecha = str(r["fecha_reserva"])

            reservas_unicas[cod_reserva] = {

                "id": cod_reserva,

                "title": f"{hora_12} - {r['nombre_cliente']} {r['apellido_cliente']}",

                "start": f"{fecha}T{hora_iso}",

                "backgroundColor": "#000",

                "borderColor": "#000",

                "textColor": "#fff",

                "extendedProps": {
                    "cedula": r["cedula_cliente"],
                    "cliente": f"{r['nombre_cliente']} {r['apellido_cliente']}",
                    "tipos_servicio": servicios,
                    "fecha": fecha,
                    "hora": hora_12,
                    "status": r["estado_reserva"] 
                }

            }

        return jsonify(list(reservas_unicas.values()))

  

    # ================== CANCELAR RESERVA ==================

    if request.method == "POST" and request.form.get("eliminar"):

        cod_servicio = request.form.get("cod_servicio")

        resultado = modelo.sp_Cancelar_Reserva(cod_servicio)

        if resultado == "cancelado":

            return jsonify({

                "icon": "success",

                "title": "Reserva cancelada",

                "text": "La reserva fue cancelada correctamente"

            })

        elif resultado == "no_existe":

            return jsonify({

                "icon": "warning",

                "title": "No encontrada",

                "text": "La reserva no existe"

            })

        else:

            return jsonify({

                "icon": "error",

                "title": "Error",

                "text": "No se pudo cancelar la reserva"

            })






    # ================== DATOS DE LA VISTA ==================



    registro = []

    if cedula:

        registro = modelo.consultarConClientes(cedula)

    return {

        "registro": registro

     

    }