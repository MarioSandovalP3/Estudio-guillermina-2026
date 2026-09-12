from flask import request, jsonify
from admin.modelo.tiposervicios import TiposervicioModelo


def handle_request(ruta):

    modelo = TiposervicioModelo()

    # =====================================
    # BUSCAR
    # =====================================
    if request.method == "POST" and request.form.get("buscar"):

        nombre_servicio = request.form.get("buscar")

        resultado = modelo.buscar(nombre_servicio)

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

        nombre_servicio = request.form.get("nombre_servicio")
        precio = request.form.get("precio")

        # VALIDAR NOMBRE
        validacion = modelo.validarNombreServicio(nombre_servicio)
        if not validacion["status"]:
            return jsonify(validacion)

        # VALIDAR PRECIO
        validacion = modelo.validarPrecio(precio)
        if not validacion["status"]:
            return jsonify(validacion)

        # VALIDAR DUPLICADO
        existe = modelo.buscar(nombre_servicio)

        if existe:
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "El tipo de servicio ya existe."
            })

        modelo.nombre_servicio = nombre_servicio
        modelo.precio = precio

        resul = modelo.registrar()

        if resul == 1:
            return jsonify({
                "icon": "success",
                "title": "Registrado con éxito",
                "text": "El tipo de servicio ha sido registrado correctamente."
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo registrar el tipo de servicio."
        })

    # =====================================
    # ACTUALIZAR
    # =====================================
    if request.method == "POST" and request.form.get("actualizar"):

        cod_tipo_servicio = request.form.get("cod_tipo_servicio")
        nombre_servicio = request.form.get("nombre_servicio")
        precio = request.form.get("precio")
        status = request.form.get("status")

        # VALIDAR NOMBRE
        validacion = modelo.validarNombreServicio(nombre_servicio)
        if not validacion["status"]:
            return jsonify(validacion)

        # VALIDAR PRECIO
        validacion = modelo.validarPrecio(precio)
        if not validacion["status"]:
            return jsonify(validacion)

        # VALIDAR DUPLICADO
        existe = modelo.buscar(nombre_servicio)

        if existe and str(existe["cod_tipo_servicio"]) != str(cod_tipo_servicio):
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Ya existe un tipo de servicio con este nombre."
            })

        modelo.cod_tipo_servicio = cod_tipo_servicio
        modelo.nombre_servicio = nombre_servicio
        modelo.precio = precio
        modelo.status = status

        resul = modelo.editar()

        if resul == 1:
            return jsonify({
                "icon": "success",
                "title": "Editado con éxito",
                "text": "Los datos del tipo de servicio han sido actualizados."
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo editar el tipo de servicio."
        })

    # =====================================
    # ELIMINAR
    # =====================================
    if request.method == "POST" and request.form.get("eliminar"):

        cod_tipo_servicio = request.form.get("cod_tipo_servicio")

        resul = modelo.eliminar(cod_tipo_servicio)

        if resul == "eliminado":
            return jsonify({
                "icon": "success",
                "title": "Eliminado con éxito",
                "text": "El tipo de servicio ha sido eliminado correctamente."
            })

        if resul == "existe_servicio":
            return jsonify({
                "icon": "warning",
                "title": "No se puede eliminar",
                "text": "Este tipo de servicio tiene servicios asociados."
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo eliminar el tipo de servicio."
        })

    # =====================================
    # CONSULTAR
    # =====================================
    tiposervicios = modelo.consultar()

    return {
        "tiposervicios": tiposervicios
    }