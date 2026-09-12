import json
from datetime import date

from flask import request, jsonify, session
from admin.modelo.compra import CompraModelo


def handle_request(ruta):

    modelo = CompraModelo()


    # =========================
    # CONSULTA (GET)
    # =========================

    if request.method == "GET":

        if request.args.get("detalle_compra"):
            cod = request.args.get("cod_compra")
            compra = modelo.obtener(cod)
            detalle = modelo.obtener_detalle_compra(cod)
            return jsonify({
                "compra": compra,
                "detalle": detalle
            })

        compras = modelo.consultar()

        return {
            "compras": compras,
            "proveedores": modelo.listar_proveedores(),
            "productos": modelo.listar_productos()
        }



    def obtener_fecha_compra():

        fecha = request.form.get(
            "fecha_compra",
            ""
        ).strip()

        return fecha or date.today().strftime("%Y-%m-%d")



    def obtener_productos():

        raw_productos = request.form.get("productos")


        if raw_productos:

            try:

                productos = json.loads(raw_productos)

                if isinstance(productos, list):

                    return productos

            except:

                pass



        if request.is_json:

            datos = request.get_json(
                silent=True
            ) or {}


            if isinstance(datos, dict):

                productos = datos.get(
                    "productos",
                    []
                )


                if isinstance(productos, list):

                    return productos



        return []



    # =========================
    # REGISTRAR COMPRA
    # =========================

    if request.method == "POST" and request.form.get("registrar"):


        try:


            fecha = obtener_fecha_compra()

            total = request.form.get("total")

            proveedor = request.form.get("cod_proveedor")

            productos = obtener_productos()



            # =========================
            # VALIDACIONES
            # =========================


            validacion = modelo.validarFechaCompra(fecha)

            if not validacion["status"]:
                return jsonify(validacion)



            validacion = modelo.validarProveedor(proveedor)

            if not validacion["status"]:
                return jsonify(validacion)



            validacion = modelo.validarTotal(total)

            if not validacion["status"]:
                return jsonify(validacion)



            validacion = modelo.validarProductos(productos)

            if not validacion["status"]:
                return jsonify(validacion)



            cod_compra = modelo.registrar_completa(
                fecha,
                proveedor,
                productos,
                session.get("cedula")
            )

            if cod_compra:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado",
                    "cod_compra": cod_compra,
                    "text": "Compra registrada correctamente."
                })



            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": modelo.ultimo_error or "No se pudo registrar la compra."
            })


        except Exception as e:


            return jsonify({
                "icon": "error",
                "title": "Error interno",
                "text": str(e)
            })




    # =========================
    # EDITAR
    # =========================

    if request.method == "POST" and (
        request.form.get("editar")
        or request.form.get("actualizar")
    ):


        try:


            cod = request.form.get("cod_compra")

            fecha = obtener_fecha_compra()

            total = request.form.get("total")

            proveedor = request.form.get("cod_proveedor")

            productos = obtener_productos()

            status = request.form.get(
                "status",
                1
            )



            # =========================
            # VALIDACIONES
            # =========================


            validacion = modelo.validarFechaCompra(fecha)

            if not validacion["status"]:
                return jsonify(validacion)



            validacion = modelo.validarProveedor(proveedor)

            if not validacion["status"]:
                return jsonify(validacion)



            validacion = modelo.validarTotal(total)

            if not validacion["status"]:
                return jsonify(validacion)



            validacion = modelo.validarProductos(productos)

            if not validacion["status"]:
                return jsonify(validacion)



            modelo.fecha_compra = fecha

            modelo.total = total

            modelo.cod_proveedor = proveedor

            modelo.status = status



            resultado = modelo.editar(
                cod,
                productos
            )



            if resultado:


                return jsonify({
                    "icon": "success",
                    "title": "Actualizado",
                    "text": "Compra actualizada correctamente."
                })



            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo actualizar la compra."
            })



        except Exception as e:


            return jsonify({
                "icon": "error",
                "title": "Error interno",
                "text": str(e)
            })




    # =========================
    # ELIMINAR
    # =========================

    if request.method == "POST" and request.form.get("eliminar"):


        try:


            cod = request.form.get("cod_compra")


            resul = modelo.eliminar(cod, session.get("cedula"))



            if resul == "cancelado":

                return jsonify({
                    "icon": "success",
                    "title": "Cancelada",
                    "text": "Compra cancelada correctamente."
                })



            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo cancelar la compra."
            })



        except Exception as e:


            return jsonify({
                "icon": "error",
                "title": "Error interno",
                "text": str(e)
            })



    # =========================
    # DEFAULT
    # =========================

    return {
        "compras": modelo.consultar(),
        "proveedores": modelo.listar_proveedores(),
        "productos": modelo.listar_productos()
    }