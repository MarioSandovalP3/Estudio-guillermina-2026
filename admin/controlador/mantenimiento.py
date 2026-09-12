import datetime

from flask import request, jsonify, session
from admin.modelo.backup import BackupModelo
from admin.modelo.mantenimiento import MantenimientoModelo


def handle_request(ruta):
    if ruta == 'mantenimiento':
        return mantenimiento()
    return backup()


def backup():
    modelo = BackupModelo()

    # =========================
    # CREAR BACKUP
    # =========================
    if request.method == "POST" and request.form.get("crear_backup"):
        cedula_usuario = session.get("cedula")
        if not cedula_usuario:
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar el backup porque no se encontró el usuario." 
            })

        resul = modelo.crear_backup(cedula_usuario=cedula_usuario)

        if resul:
            registro = MantenimientoModelo()
            registro.nombre_archivo = modelo.ultimo_archivo or f"backup_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.sql"
            registro.tamano = modelo.ultimo_tamano or 0
            registro.fecha = datetime.datetime.now().strftime("%Y-%m-%d")
            registro.hora = datetime.datetime.now().strftime("%H:%M:%S")
            registro.cedula_usuario = cedula_usuario

            if registro.registrar():
                return jsonify({
                    "icon": "success",
                    "title": "Backup creado",
                    "text": "Se generó el respaldo de sac y seguridad y se registró en mantenimiento."
                })

            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Se generó el respaldo, pero no se pudo guardar en mantenimiento."
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo crear el backup."
        })

    # =========================
    # RESTAURAR BACKUP
    # =========================
    if request.method == "POST" and request.form.get("restaurar"):
        archivo = request.files.get("backup_file")

        if not archivo:
            return jsonify({
                "icon": "error",
                "title": "Error",
                "text": "Archivo de backup requerido."
            })

        resul = modelo.restaurar_backup(archivo)

        if resul:
            return jsonify({
                "icon": "success",
                "title": "Restaurado",
                "text": "Base de datos restaurada correctamente."
            })

        return jsonify({
            "icon": "error",
            "title": "Error",
            "text": "No se pudo restaurar."
        })

    # =========================
    # ELIMINAR BACKUP
    # =========================
    if request.method == 'POST' and request.form.get('eliminar_backup'):
        backup_name = request.form.get('backup_name')
        resul = modelo.eliminar_backup(backup_name)
        if resul:
            return jsonify({"icon": "success", "title": "Eliminado", "text": "Backup eliminado."})
        return jsonify({"icon": "error", "title": "Error", "text": "No se pudo eliminar el backup."})

    # =========================
    # LISTAR BACKUPS
    # =========================
    backups = modelo.listar_backups()
    return {"backups": backups}


def mantenimiento():
    modelo = MantenimientoModelo()
    mensaje = None

    # Atender backups desde la misma ruta de mantenimiento
    if request.method == 'POST' and (request.form.get('crear_backup') or request.form.get('restaurar')):
        return backup()

    # Registrar mantenimiento (archivo)
    if request.method == 'POST' and request.form.get('registrar_mantenimiento'):
        archivo = request.files.get('archivo')
        fecha = request.form.get('fecha', '').strip()
        hora = request.form.get('hora', '').strip()
        cedula = request.form.get('cedula_usuario', '').strip()

        if archivo and archivo.filename != '':
            modelo.subir_archivo(archivo)
        else:
            return jsonify({"icon": "error", "title": "Error", "text": "Archivo requerido."})

        try:
            modelo.fecha = fecha
            modelo.hora = hora or '00:00:00'
            modelo.cedula_usuario = cedula
        except ValueError as error:
            return jsonify({
                "icon": "warning",
                "title": "Dato inválido",
                "text": str(error)
            })

        validar = modelo.validarMantenimiento()
        if not validar["status"]:
            return jsonify(validar)

        if modelo.registrar():
            return jsonify({"icon": "success", "title": "Guardado", "text": "Archivo registrado."})

        return jsonify({"icon": "error", "title": "Error", "text": "No se pudo guardar."})

    # Eliminar registro
    if request.method == 'POST' and request.form.get('eliminar'):
        cod = request.form.get('cod_mantenimiento')
        if cod and modelo.eliminar(cod):
            return jsonify({"icon": "success", "title": "Eliminado", "text": "Registro eliminado."})
        return jsonify({"icon": "error", "title": "Error", "text": "No se pudo eliminar."})

    # Eliminar backup
    if request.method == 'POST' and request.form.get('eliminar_backup'):
        backup_name = request.form.get('backup_name')
        resul = BackupModelo().eliminar_backup(backup_name)
        if resul:
            return jsonify({"icon": "success", "title": "Eliminado", "text": "Backup eliminado."})
        return jsonify({"icon": "error", "title": "Error", "text": "No se pudo eliminar el backup."})

    # Listar registros y usuarios
    registros = modelo.consultar()
    usuarios = modelo.listar_usuarios()
    backups = BackupModelo().listar_backups()
    return {"registros": registros, "usuarios": usuarios, "backups": backups, "mensaje": mensaje}