from flask import request, jsonify
from admin.modelo.producto import ProductoModelo


def handle_request(ruta):

    modelo = ProductoModelo()

    # =========================
    # CONSULTAR (GET)
    # =========================
    if request.method == "GET":

        productos = modelo.consultar()

        return {
            "productos": productos,
            "categorias": modelo.listar_categorias(),
            "marcas": modelo.listar_marcas(),
            "unidades": modelo.listar_unidades(),
            "presentaciones": modelo.listar_presentaciones(),
            "medidas": modelo.listar_medidas(),
            "tipos_producto": modelo.listar_tipos_producto()
        }

    # =========================
    # BUSCAR
    # =========================
    if request.method == "POST" and request.form.get("buscar"):

        nombre = request.form.get("buscar")

        resultado = modelo.buscar(nombre)

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

        try:

            modelo.nombre_producto = request.form.get("nombre_producto")
            modelo.precio_producto = request.form.get("precio_producto")
            modelo.stock = request.form.get("stock")

            modelo.cod_categoria = request.form.get("cod_categoria")
            modelo.cod_marca = request.form.get("cod_marca")
            modelo.cod_unidad = request.form.get("cod_unidad")
            modelo.cod_presentacion = request.form.get("cod_presentacion")
            modelo.cod_medida = request.form.get("cod_medida")

            modelo.fecha_vencimiento = request.form.get("fecha_vencimiento")
            modelo.cod_tipo_producto = request.form.get("cod_tipo_producto")

            existe = modelo.buscar(modelo.nombre_producto)

            if existe:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "El producto ya existe."
                })

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

        except Exception as e:

            return jsonify({
                "icon": "error",
                "title": "Error interno",
                "text": str(e)
            })

    # =========================
    # ACTUALIZAR
    # =========================
    if request.method == "POST" and request.form.get("actualizar"):

        try:

            modelo.cod_producto = request.form.get("cod_producto")
            modelo.nombre_producto = request.form.get("nombre_producto")
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

            cod = request.form.get("cod_producto")

            resul = modelo.eliminar(cod)

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

        except Exception as e:

            return jsonify({
                "icon": "error",
                "title": "Error interno",
                "text": str(e)
            })