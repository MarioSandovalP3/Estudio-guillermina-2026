from flask import request, jsonify
from admin.modelo.tipoproducto import TipoProductoModelo


def handle_request(ruta):

    modelo = TipoProductoModelo()


    # =====================================
    # BUSCAR
    # =====================================

    if request.method == "POST" and request.form.get("buscar"):

        nombre = request.form.get("buscar").strip()


        resultado = modelo.buscar(nombre)


        if resultado:

            return jsonify({
                "existe": True,
                "datos": resultado
            })


        return jsonify({
            "existe": False
        })



    # =====================================
    # REGISTRAR
    # =====================================

    if request.method == "POST" and request.form.get("registrar"):


        nombre = request.form.get(
            "nombre_tipo_producto",
            ""
        ).strip()



        # Validación antes de consultar
        validacion = modelo.validarNombreTipoProducto(nombre)


        if not validacion["status"]:

            return jsonify(validacion)



        existe = modelo.buscar(nombre)


        if existe:

            return jsonify({
                "status":False,
                "icon":"error",
                "title":"Error",
                "text":"El tipo de producto ya existe."
            })



        modelo.nombre_tipo_producto = nombre



        resultado = modelo.registrar()



        return jsonify(resultado)




    # =====================================
    # ACTUALIZAR
    # =====================================

    if request.method == "POST" and request.form.get("actualizar"):


        cod = request.form.get(
            "cod_tipo_producto"
        )


        nombre = request.form.get(
            "nombre_tipo_producto",
            ""
        ).strip()



        # Validar código

        validacion_codigo = modelo.validarCodigo(cod)


        if not validacion_codigo["status"]:

            return jsonify(validacion_codigo)



        # Validar nombre

        validacion_nombre = modelo.validarNombreTipoProducto(nombre)


        if not validacion_nombre["status"]:

            return jsonify(validacion_nombre)




        existe = modelo.buscar(nombre)



        if existe and str(existe["cod_tipo_producto"]) != str(cod):

            return jsonify({
                "status":False,
                "icon":"error",
                "title":"Error",
                "text":"Ya existe un tipo de producto con ese nombre."
            })



        modelo.cod_tipo_producto = cod

        modelo.nombre_tipo_producto = nombre

        modelo.status = request.form.get(
            "status",
            1
        )



        resultado = modelo.editar()



        return jsonify(resultado)




    # =====================================
    # ELIMINAR
    # =====================================

    if request.method == "POST" and request.form.get("eliminar"):


        cod = request.form.get(
            "cod_tipo_producto"
        )



        resultado = modelo.eliminar(cod)



        return jsonify(resultado)




    # =====================================
    # CONSULTAR
    # =====================================

    tipo_productos = modelo.consultar()


    return {
        "tipo_productos": tipo_productos
    }