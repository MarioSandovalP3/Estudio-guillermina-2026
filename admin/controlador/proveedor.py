from flask import request, jsonify
from admin.modelo.proveedor import ProveedorModelo


def handle_request(ruta):

    modelo = ProveedorModelo()


    # =====================================
    # BUSCAR
    # =====================================
    if request.method == "POST" and request.form.get("buscar"):

        cedula = request.form.get("buscar")

        resultado = modelo.buscar(cedula)

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


        cedula = request.form.get("cedula")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        rif = request.form.get("rif")
        telefono = request.form.get("telefono")
        correo = request.form.get("correo")



        # ===============================
        # VALIDACIONES
        # ===============================

        validacion = modelo.validarCedula(cedula)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarNombre(nombre)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarApellido(apellido)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarRif(rif)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarTelefono(telefono)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarCorreo(correo)

        if not validacion["status"]:
            return jsonify(validacion)



        # ===============================
        # DUPLICADO
        # ===============================

        existe = modelo.buscar(cedula)


        if existe:

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "El proveedor ya existe."
            })



        modelo.cedula = cedula
        modelo.nombre = nombre
        modelo.apellido = apellido
        modelo.rif = rif
        modelo.telefono = telefono
        modelo.correo = correo



        resul = modelo.registrar()



        if resul == 1:

            return jsonify({
                "icon": "success",
                "title": "Registrado con éxito",
                "text": "El proveedor ha sido registrado correctamente."
            })



        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo registrar el proveedor."
        })




    # =====================================
    # ACTUALIZAR
    # =====================================
    if request.method == "POST" and request.form.get("actualizar"):


        cod = request.form.get("cod_proveedor")

        cedula = request.form.get("cedula")

        nombre = request.form.get("nombre")

        apellido = request.form.get("apellido")

        rif = request.form.get("rif")

        telefono = request.form.get("telefono")

        correo = request.form.get("correo")

        status = request.form.get("status")



        # ===============================
        # VALIDACIONES
        # ===============================

        validacion = modelo.validarCedula(cedula)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarNombre(nombre)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarApellido(apellido)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarRif(rif)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarTelefono(telefono)

        if not validacion["status"]:
            return jsonify(validacion)



        validacion = modelo.validarCorreo(correo)

        if not validacion["status"]:
            return jsonify(validacion)



        # ===============================
        # DUPLICADO
        # ===============================

        existe = modelo.buscar(cedula)


        if existe and str(existe["cod_proveedor"]) != str(cod):

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Ya existe un proveedor con esta cédula."
            })



        modelo.cod_proveedor = cod

        modelo.cedula = cedula

        modelo.nombre = nombre

        modelo.apellido = apellido

        modelo.rif = rif

        modelo.telefono = telefono

        modelo.correo = correo

        modelo.status = status



        resul = modelo.editar()



        if resul == 1:

            return jsonify({
                "icon": "success",
                "title": "Editado con éxito",
                "text": "Los datos del proveedor han sido actualizados."
            })



        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo editar el proveedor."
        })




    # =====================================
    # ELIMINAR
    # =====================================
    if request.method == "POST" and request.form.get("eliminar"):


        cod = request.form.get("cod_proveedor")


        resul = modelo.eliminar(cod)



        if resul == "eliminado":

            return jsonify({
                "icon": "success",
                "title": "Eliminado con éxito",
                "text": "El proveedor ha sido eliminado correctamente."
            })



        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo eliminar el proveedor."
        })



    # =====================================
    # CONSULTAR
    # =====================================
    proveedores = modelo.consultar()


    return {
        "proveedores": proveedores
    }