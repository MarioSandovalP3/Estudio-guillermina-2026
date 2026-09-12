from flask import request, jsonify
from admin.modelo.marca import MarcaModelo


def handle_request(ruta):

    modelo = MarcaModelo()


    # =====================================
    # BUSCAR
    # =====================================

    if request.method == "POST" and request.form.get("buscar"):

        nombre_marca = request.form.get("buscar").strip()

        resultado = modelo.buscar(nombre_marca)


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


        nombre_marca = request.form.get("nombre_marca")


        # VALIDAR NOMBRE

        validacion = modelo.validarNombreMarca(nombre_marca)

        if not validacion["status"]:
            return jsonify(validacion)



        # VERIFICAR DUPLICADO

        existe = modelo.buscar(nombre_marca.strip())


        if existe:

            return jsonify({
                "icon": "error",
                "title": "Marca existente",
                "text": "La marca ya se encuentra registrada."
            })



        modelo.nombre_marca = nombre_marca.strip()


        resul = modelo.registrar()



        if resul == 1:

            return jsonify({
                "icon": "success",
                "title": "Registrado con éxito",
                "text": "La marca ha sido registrada correctamente."
            })



        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo registrar la marca."
        })




    # =====================================
    # ACTUALIZAR
    # =====================================

    if request.method == "POST" and request.form.get("actualizar"):


        cod_marca = request.form.get("cod_marca")

        nombre_marca = request.form.get("nombre_marca")

        status = request.form.get("status")



        # VALIDAR NOMBRE

        validacion = modelo.validarNombreMarca(nombre_marca)


        if not validacion["status"]:
            return jsonify(validacion)



        # VALIDAR STATUS BOOLEANO

        validar_status = modelo.validarStatus(status)


        if not validar_status["status"]:
            return jsonify(validar_status)




        existe = modelo.buscar(nombre_marca.strip())



        if existe and str(existe["cod_marca"]) != str(cod_marca):

            return jsonify({

                "icon": "error",

                "title": "Marca existente",

                "text": "Ya existe una marca con este nombre."

            })




        modelo.cod_marca = cod_marca

        modelo.nombre_marca = nombre_marca.strip()

        modelo.status = int(status)



        resul = modelo.editar()



        if resul == 1:

            return jsonify({

                "icon": "success",

                "title": "Actualizado con éxito",

                "text": "Los datos de la marca han sido actualizados."

            })



        return jsonify({

            "icon": "error",

            "title": "Error",

            "text": "No se pudo editar la marca."

        })





    # =====================================
    # ELIMINAR
    # =====================================

    if request.method == "POST" and request.form.get("eliminar"):


        cod_marca = request.form.get("cod_marca")



        if not cod_marca:

            return jsonify({

                "icon":"warning",

                "title":"Dato faltante",

                "text":"No se recibió la marca a eliminar."

            })



        resul = modelo.eliminar(cod_marca)




        if resul == "eliminado":

            return jsonify({

                "icon": "success",

                "title": "Eliminado con éxito",

                "text": "La marca ha sido eliminada correctamente."

            })



        if resul == "existe_producto":

            return jsonify({

                "icon":"warning",

                "title":"No se puede eliminar",

                "text":"La marca tiene productos asociados."

            })



        return jsonify({

            "icon": "error",

            "title": "Error",

            "text": "No se pudo eliminar la marca."

        })




    # =====================================
    # CONSULTAR
    # =====================================

    marcas = modelo.consultar()


    return {

        "marcas": marcas

    }