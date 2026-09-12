from flask import request, jsonify
from admin.modelo.promociones import PromocionModelo


def handle_request(ruta):

    modelo = PromocionModelo()


    # =====================================
    # BUSCAR
    # =====================================
    if request.method == "POST" and request.form.get("buscar"):

        nombre_promo = request.form.get("buscar")

        resultado = modelo.buscar(nombre_promo)

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


        nombre_promo = request.form.get("nombre_promo")
        descripcion_promo = request.form.get("descripcion_promo")
        descuento = request.form.get("descuento")
        inicio_promo = request.form.get("inicio_promo")
        fin_promo = request.form.get("fin_promo")


        # ===============================
        # VALIDACIONES
        # ===============================

        validacion = modelo.validarNombrePromo(nombre_promo)

        if not validacion["status"]:
            return jsonify(validacion)


        validacion = modelo.validarDescripcionPromo(descripcion_promo)

        if not validacion["status"]:
            return jsonify(validacion)


        validacion = modelo.validarDescuento(descuento)

        if not validacion["status"]:
            return jsonify(validacion)


        validacion = modelo.validarFechasPromo(
            inicio_promo,
            fin_promo
        )

        if not validacion["status"]:
            return jsonify(validacion)



        imagen = request.files.get("imagen_promo")


        validacion = modelo.validarImagenPromo(imagen)

        if not validacion["status"]:
            return jsonify(validacion)



        # ===============================
        # VALIDAR DUPLICADO
        # ===============================

        existe = modelo.buscar(nombre_promo)


        if existe:

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "La promoción ya existe."
            })



        modelo.nombre_promo = nombre_promo
        modelo.descripcion_promo = descripcion_promo
        modelo.descuento = descuento
        modelo.inicio_promo = inicio_promo
        modelo.fin_promo = fin_promo



        nombre_imagen = modelo.subir_imagen(imagen)


        if nombre_imagen:

            modelo.imagen_promo = nombre_imagen



        resul = modelo.registrar()



        if resul == 1:

            return jsonify({
                "icon": "success",
                "title": "Registrada con éxito",
                "text": "La promoción ha sido registrada correctamente."
            })


        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo registrar la promoción."
        })



    # =====================================
    # ACTUALIZAR
    # =====================================
    if request.method == "POST" and request.form.get("actualizar"):


        cod_promo = request.form.get("cod_promo")

        nombre_promo = request.form.get("nombre_promo")

        descripcion_promo = request.form.get("descripcion_promo")

        descuento = request.form.get("descuento")

        inicio_promo = request.form.get("inicio_promo")

        fin_promo = request.form.get("fin_promo")

        status = request.form.get("status")



        # ===============================
        # VALIDACIONES
        # ===============================

        validacion = modelo.validarNombrePromo(nombre_promo)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarDescripcionPromo(descripcion_promo)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarDescuento(descuento)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarFechasPromo(
            inicio_promo,
            fin_promo
        )

        if not validacion["status"]:
            return jsonify(validacion)



        # ===============================
        # VALIDAR DUPLICADO
        # ===============================

        existe = modelo.buscar(nombre_promo)


        if existe and str(existe["cod_promo"]) != str(cod_promo):

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Ya existe una promoción con este nombre."
            })



        modelo.cod_promo = cod_promo

        modelo.nombre_promo = nombre_promo

        modelo.descripcion_promo = descripcion_promo

        modelo.descuento = descuento

        modelo.inicio_promo = inicio_promo

        modelo.fin_promo = fin_promo

        modelo.status = status



        # ===============================
        # IMAGEN
        # ===============================

        imagen = request.files.get("imagen_promo")


        if imagen and imagen.filename:


            validacion = modelo.validarImagenPromo(imagen)


            if not validacion["status"]:
                return jsonify(validacion)



            nombre_imagen = modelo.subir_imagen(imagen)


            if nombre_imagen:

                modelo.imagen_promo = nombre_imagen



        else:


            datos_actuales = modelo.obtener(cod_promo)


            if datos_actuales:

                modelo.imagen_promo = datos_actuales["imagen_promo"]




        resul = modelo.editar()



        if resul == 1:

            return jsonify({
                "icon": "success",
                "title": "Editada con éxito",
                "text": "Los datos de la promoción han sido actualizados."
            })



        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo editar la promoción."
        })



    # =====================================
    # ELIMINAR
    # =====================================
    if request.method == "POST" and request.form.get("eliminar"):


        cod_promo = request.form.get("cod_promo")


        resul = modelo.eliminar(cod_promo)



        if resul == "eliminado":

            return jsonify({
                "icon": "success",
                "title": "Eliminada con éxito",
                "text": "La promoción ha sido eliminada correctamente."
            })



        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo eliminar la promoción."
        })



    # =====================================
    # CONSULTAR
    # =====================================

    promociones = modelo.consultar()


    return {
        "promociones": promociones
    }