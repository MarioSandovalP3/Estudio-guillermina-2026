from flask import request, jsonify
from admin.modelo.especialidad import EspecialidadModelo

def handle_request(ruta):
        
        modelo = EspecialidadModelo()

        if request.method == "POST" and request.form.get("buscar"):

            especialidad = request.form.get("especialista")
            cedula = request.form.get("cedula")

            resultado = modelo.buscar(especialidad, cedula)

            if resultado:
                return jsonify({
                    "existe": True
                })

            return jsonify({
                "existe": False
            })      

        if request.method == "POST" and request.form.get("registrar"):

            especialista = request.form.get("especialista")

            validar = modelo.validarEspecialidad(especialista)

            if not validar["status"]:
                return jsonify(validar)

            modelo.especialista = especialista
            modelo.cedula = request.form.get("cedula")

            resul = modelo.registrar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Registrado con éxito",
                    "text": "El especialista ha sido registrado."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar."
            })

        if request.method == "POST" and request.form.get("actualizar"):

            modelo.cedula = request.form.get("cedula")
            modelo.especialista = request.form.get("especialista")
            modelo.status = request.form.get("status")

            resul = modelo.editar()

            if resul == 1:
                return jsonify({
                    "icon": "success",
                    "title": "Editado con éxito",
                    "text": "Los datos del especialista han sido actualizados correctamente."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo actualizar."
            })



        if request.method == "POST" and request.form.get("eliminar"):

            modelo.cedula_especialista = request.form.get("cedula_especialista")
            resul = modelo.eliminar(modelo.cedula_especialista)

            if resul == "eliminado":
                return jsonify({
                    "icon": "success",
                    "title": "Eliminado con éxito",
                    "text": "La especialista ha sido eliminada correctamente."
                })

            if resul == "tiene_reservas":
                return jsonify({
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "La especialista tiene reservas asociadas."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo eliminar la especialista."
            })


        especialidad = modelo.consultar()
        usuarios = modelo.obtener_usuario()

        return {
        "especialidad": especialidad,
        "usuarios": usuarios
}