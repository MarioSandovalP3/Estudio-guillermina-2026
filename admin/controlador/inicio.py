from flask import request, jsonify
from admin.modelo.inicio import InicioModelo
from datetime import datetime

def handle_request(ruta):
        
        modelo = InicioModelo()

        if request.method == "GET" and request.args.get("cargar_reservas"):

            reservas = modelo.consultarconlientesini()

            reservas_unicas = {}

            for r in reservas:

                cod_reserva = r["cod_servicio"]

                servicios = modelo.obtenerServiciosDeReserva(cod_reserva)

                hora_raw = str(r["hora_servicio"]).strip()

                hora_dt = datetime.strptime(hora_raw, "%I:%M %p")

                hora_iso = hora_dt.strftime("%H:%M:%S")
                hora_12 = hora_dt.strftime("%I:%M %p")

                fecha = str(r["fecha_servicio"])

                reservas_unicas[cod_reserva] = {
                    "id": cod_reserva,
                    "title": f"{hora_12} - {r['nombre_usuario']} {r['apellido_usuario']}",
                    "start": f"{fecha}T{hora_iso}",
                    "backgroundColor": "#000",
                    "borderColor": "#000",
                    "textColor": "#fff",
                    "extendedProps": {
                        "cedula": r["cedula"],
                        "cliente": f"{r['nombre_usuario']} {r['apellido_usuario']}",
                        "tipos_servicio": servicios,
                        "fecha": fecha,
                        "hora": hora_12
                    }
                }

            return jsonify(list(reservas_unicas.values()))


        # ================== ACTUALIZAR STOCK ==================
        if request.method == "GET" and request.args.get("actualizar_stock"):

            productos = modelo.actualizarStockProductos()

            return jsonify(productos)


# ================== REGISTRAR RESERVA ==================
        if request.method == "POST" and request.form.get("registrar"):

            cedula = request.form.get("cedula")

            fecha = request.form.get("fecha")

            hora = request.form.get("hora")

            cedula_especialista = request.form.get("cedula_especialista")

            cod_tipos_servicio = request.form.getlist("servicio[]")

            cod_promo = request.form.get("promocion")

            productos_seleccionados = request.form.getlist("producto[]")


            cod_productos = []

            for cod_producto in productos_seleccionados:


                cantidad = request.form.get(
                    f"cantidad_producto[{cod_producto}]"
                )


                cod_productos.append({

                    "cod_producto": cod_producto,

                    "cantidad": int(cantidad)

                })

            resultado = modelo.registrarReserva(

                cedula,

                cod_tipos_servicio,

                fecha,

                hora,

                cedula_especialista,

                cod_promo,

                cod_productos

            )

            return jsonify(resultado)
        
        # ================== BUSCAR CLIENTE POR NOMBRE ==================
        if request.method == "POST" and request.form.get("buscar_cliente"):

            nombre = request.form.get("nombre_usuario", "").strip()

            if not nombre:
                return jsonify({
                    "success": False,
                    "clientes": []
                })

            resultados = modelo.buscarClientePorNombre(nombre)

            if resultados:
                return jsonify({
                    "success": True,
                    "clientes": resultados
                })

            return jsonify({
                "success": False,
                "clientes": []
            })

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

        promociones = modelo.obtenerPromocionesActivas()

        productos = modelo.obtenerProductosDisponibles()

        return {
            "servicios": servicios,
            "estilistas": estilistas,
            "manicuristas": manicuristas,
            "promociones": promociones,
            "productos": productos
        }