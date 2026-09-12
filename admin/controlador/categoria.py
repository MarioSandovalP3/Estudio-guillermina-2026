from flask import request, jsonify
from admin.modelo.categorias import CategoriaModelo


def handle_request(ruta):

    modelo = CategoriaModelo()

    # =====================================
    # BUSCAR
    # =====================================
    if request.method == "POST" and request.form.get("buscar"):

        nombre_categoria = request.form.get("buscar", "").strip()

        resultado = modelo.buscar(nombre_categoria)

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

        try:

            nombre_categoria = request.form.get("nombre_categoria", "").strip()

            # VALIDAR NOMBRE
            validacion = modelo.validarNombreCategoria(nombre_categoria)

            if not validacion["status"]:
                return jsonify(validacion)

            # VALIDAR DUPLICADO
            existe = modelo.buscar(nombre_categoria)

            if existe:
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "La categoría ya existe."
                })

            modelo.nombre_categoria = nombre_categoria

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado con éxito",
                    "text": "La categoría ha sido registrada correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar la categoría."
            })

        except Exception as e:

            return jsonify({
                "icon": "error",
                "title": "Error interno",
                "text": str(e)
            })

    # =====================================
    # ACTUALIZAR
    # =====================================
    if request.method == "POST" and request.form.get("actualizar"):

        try:

            cod_categoria = request.form.get("cod_categoria")
            nombre_categoria = request.form.get("nombre_categoria", "").strip()
            status = request.form.get("status")

            # VALIDAR NOMBRE
            validacion = modelo.validarNombreCategoria(nombre_categoria)

            if not validacion["status"]:
                return jsonify(validacion)

            # VALIDAR STATUS
            validar_status = modelo.validarStatus(status)

            if not validar_status["status"]:
                return jsonify(validar_status)

            # VALIDAR DUPLICADO
            existe = modelo.buscar(nombre_categoria)

            if existe and str(existe["cod_categoria"]) != str(cod_categoria):
                return jsonify({
                    "icon": "error",
                    "title": "Error",
                    "text": "Ya existe una categoría con este nombre."
                })

            modelo.cod_categoria = cod_categoria
            modelo.nombre_categoria = nombre_categoria
            modelo.status = int(status)

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "Los datos de la categoría han sido actualizados."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo editar la categoría."
            })

        except Exception as e:

            return jsonify({
                "icon": "error",
                "title": "Error interno",
                "text": str(e)
            })

    # =====================================
    # ELIMINAR
    # =====================================
    if request.method == "POST" and request.form.get("eliminar"):

        try:

            cod_categoria = request.form.get("cod_categoria")

            if not cod_categoria:
                return jsonify({
                    "icon": "warning",
                    "title": "Dato faltante",
                    "text": "No se recibió la categoría a eliminar."
                })

            resul = modelo.eliminar(cod_categoria)

            if resul == "eliminado":
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado con éxito",
                    "text": "La categoría ha sido eliminada correctamente."
                })

            if resul == "existe_producto":
                return jsonify({
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "La categoría tiene productos asociados."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo eliminar la categoría."
            })

        except Exception as e:

            return jsonify({
                "icon": "error",
                "title": "Error interno",
                "text": str(e)
            })

    # =====================================
    # CONSULTAR
    # =====================================

    categorias = modelo.consultar()

    return {
        "categorias": categorias
    }