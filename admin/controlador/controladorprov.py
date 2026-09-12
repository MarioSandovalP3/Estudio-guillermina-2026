from flask import request, jsonify
from admin.modelo.producto import ProductoModelo


class ProductoControlador:

    @staticmethod
    def handle_request(ruta):
        return ProductoControlador.productos()


    @staticmethod
    def productos():

        modelo = ProductoModelo()

        # =========================
        # CONSULTAS PRINCIPALES
        # =========================
        productos = modelo.consultar()

        categorias = modelo.listar_categorias()
        marcas = modelo.listar_marcas()
        unidades = modelo.listar_unidades()
        presentaciones = modelo.listar_presentaciones()
        medidas = modelo.listar_medidas()
        tipos_producto = modelo.listar_tipos_producto()

        # =========================
        # BUSCAR
        # =========================
        if request.method == "POST" and request.form.get("buscar"):

            nombre_producto = request.form.get("buscar")
            resultado = modelo.buscar(nombre_producto)

            if resultado:
                return jsonify({
                    "existe": True,
                    "datos": resultado
                })

            return jsonify({
                "existe": False
            })

        # =========================
        # REGISTRAR
        # =========================
        if request.method == "POST" and request.form.get("registrar"):

            nombre_producto = request.form.get("nombre_producto")

            existe = modelo.buscar(nombre_producto)

            if existe:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "El producto ya existe."
                })

            modelo.nombre_producto = nombre_producto
            modelo.precio_producto = request.form.get("precio_producto")
            modelo.stock = request.form.get("stock")

            modelo.cod_categoria = request.form.get("cod_categoria")
            modelo.cod_marca = request.form.get("cod_marca")
            modelo.cod_unidad = request.form.get("cod_unidad")
            modelo.cod_presentacion = request.form.get("cod_presentacion")
            modelo.cod_medida = request.form.get("cod_medida")

            modelo.fecha_vencimiento = request.form.get("fecha_vencimiento")
            modelo.cod_tipo_producto = request.form.get("cod_tipo_producto")

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado",
                    "text": "Producto registrado correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar el producto."
            })

        # =========================
        # ACTUALIZAR
        # =========================
        if request.method == "POST" and request.form.get("actualizar"):

            cod_producto = request.form.get("cod_producto")
            nombre_producto = request.form.get("nombre_producto")

            existe = modelo.buscar(nombre_producto)

            if existe and str(existe["cod_producto"]) != str(cod_producto):
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "Ya existe un producto con este nombre."
                })

            modelo.cod_producto = cod_producto
            modelo.nombre_producto = nombre_producto
            modelo.precio_producto = request.form.get("precio_producto")
            modelo.stock = request.form.get("stock")

            modelo.cod_categoria = request.form.get("cod_categoria")
            modelo.cod_marca = request.form.get("cod_marca")
            modelo.cod_unidad = request.form.get("cod_unidad")
            modelo.cod_presentacion = request.form.get("cod_presentacion")
            modelo.cod_medida = request.form.get("cod_medida")

            modelo.fecha_vencimiento = request.form.get("fecha_vencimiento")
            modelo.cod_tipo_producto = request.form.get("cod_tipo_producto")
            modelo.status = request.form.get("status")

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Actualizado",
                    "text": "Producto actualizado correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo actualizar el producto."
            })

        # =========================
        # ELIMINAR
        # =========================
        if request.method == "POST" and request.form.get("eliminar"):

            cod_producto = request.form.get("cod_producto")

            resul = modelo.eliminar(cod_producto)

            if resul == "eliminado":
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado",
                    "text": "Producto eliminado correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo eliminar el producto."
            })

        # =========================
        # RESPUESTA NORMAL (GET)
        # =========================
        return {
            "productos": productos,
            "categorias": categorias,
            "marcas": marcas,
            "unidades": unidades,
            "presentaciones": presentaciones,
            "medidas": medidas,
            "tipos_producto": tipos_producto
        }