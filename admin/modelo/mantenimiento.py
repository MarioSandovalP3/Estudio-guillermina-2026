from admin.config.conexion import Conexion
import os
import re
import datetime
from werkzeug.utils import secure_filename


class MantenimientoModelo(Conexion):
    UPLOAD_FOLDER = "static/assets/uploads/mantenimiento"
    PUBLIC_FOLDER = "assets/uploads/mantenimiento"

    def __init__(self):
        super().__init__()
        self.__cod_mantenimiento = None
        self.__nombre_archivo = None
        self.__tamano = None
        self.__fecha = None
        self.__hora = None
        self.__cedula_usuario = None

    def validarNombreArchivo(self, nombre_archivo=None):
        valor = self.__nombre_archivo if nombre_archivo is None else nombre_archivo
        if valor is None or not isinstance(valor, str) or not valor.strip():
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Archivo requerido."
            }

        nombre = os.path.basename(str(valor).strip())
        if not re.match(r'.+\.(?:jpg|jpeg|png|gif|pdf|txt)$', nombre, re.IGNORECASE):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Formato de archivo no soportado."
            }

        return {"status": True}

    def validarTamano(self, tamano=None):
        valor = self.__tamano if tamano is None else tamano
        texto = str(valor).strip() if valor is not None else ""

        if not texto or not re.match(r'^[1-9]\d*$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Tamaño inválido."
            }

        return {"status": True, "value": int(texto)}

    def validarFecha(self, fecha=None):
        valor = self.__fecha if fecha is None else fecha
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Fecha requerida."
            }

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Formato de fecha inválido (YYYY-MM-DD)."
            }

        try:
            datetime.date.fromisoformat(texto)
        except Exception:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Fecha inválida."
            }

        return {"status": True, "value": texto}

    def validarHora(self, hora=None):
        valor = self.__hora if hora is None else hora
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Hora requerida."
            }

        if not re.match(r'^\d{2}:\d{2}:\d{2}$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Formato de hora inválido (HH:MM:SS)."
            }

        return {"status": True, "value": texto}

    def validarCedulaUsuario(self, cedula_usuario=None):
        valor = self.__cedula_usuario if cedula_usuario is None else cedula_usuario
        texto = str(valor).strip() if valor is not None else ""

        if not texto or not re.match(r'^\w{3,20}$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Usuario no válido."
            }

        return {"status": True, "value": texto}

    @property
    def cod_mantenimiento(self):
        return self.__cod_mantenimiento

    @cod_mantenimiento.setter
    def cod_mantenimiento(self, valor):
        self.__cod_mantenimiento = valor

    @property
    def nombre_archivo(self):
        return self.__nombre_archivo

    @nombre_archivo.setter
    def nombre_archivo(self, valor):
        if valor is None:
            self.__nombre_archivo = None
            return
        self.__nombre_archivo = str(valor).strip()

    @property
    def tamano(self):
        return self.__tamano

    @tamano.setter
    def tamano(self, valor):
        if valor is None:
            self.__tamano = None
            return
        try:
            self.__tamano = str(int(valor))
        except Exception:
            self.__tamano = str(valor)

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, valor):
        if valor is None:
            self.__fecha = None
            return
        self.__fecha = str(valor).strip()

    @property
    def hora(self):
        return self.__hora

    @hora.setter
    def hora(self, valor):
        if valor is None:
            self.__hora = None
            return
        self.__hora = str(valor).strip()

    @property
    def cedula_usuario(self):
        return self.__cedula_usuario

    @cedula_usuario.setter
    def cedula_usuario(self, valor):
        if valor is None:
            self.__cedula_usuario = None
            return
        self.__cedula_usuario = str(valor).strip()

    def subir_archivo(self, file):
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
            ruta_destino = os.path.join(self.UPLOAD_FOLDER, filename)
            file.save(ruta_destino)
           
            self.__nombre_archivo = os.path.join(self.PUBLIC_FOLDER, filename).replace("\\", "/")
            self.__tamano = str(os.path.getsize(ruta_destino))

    def validarMantenimiento(self, nombre_archivo=None, tamano=None, fecha=None, hora=None, cedula_usuario=None):
        errors = {}
        pat_int = re.compile(r'^[1-9]\d*$')
        pat_fecha = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        pat_hora = re.compile(r'^\d{2}:\d{2}:\d{2}$')
        pat_file = re.compile(r'.+\.(?:jpg|jpeg|png|gif|pdf|txt)$', re.IGNORECASE)
        pat_cedula = re.compile(r'^\w{3,20}$')

        valor_nombre_archivo = self.__nombre_archivo if nombre_archivo is None else nombre_archivo
        valor_tamano = self.__tamano if tamano is None else tamano
        valor_fecha = self.__fecha if fecha is None else fecha
        valor_hora = self.__hora if hora is None else hora
        valor_cedula_usuario = self.__cedula_usuario if cedula_usuario is None else cedula_usuario

        if valor_nombre_archivo is None or not isinstance(valor_nombre_archivo, str):
            errors['nombre_archivo'] = 'Archivo requerido.'
        else:
            nombre = os.path.basename(valor_nombre_archivo)
            if not pat_file.match(nombre):
                errors['nombre_archivo'] = 'Formato de archivo no soportado.'

        if not valor_tamano:
            errors['tamano'] = 'Tamaño no especificado.'
        else:
            try:
                if int(valor_tamano) <= 0:
                    errors['tamano'] = 'Tamaño inválido.'
            except Exception:
                errors['tamano'] = 'Tamaño inválido.'

        if not valor_fecha:
            errors['fecha'] = 'Fecha requerida.'
        else:
            if not pat_fecha.match(str(valor_fecha)):
                errors['fecha'] = 'Formato de fecha inválido (YYYY-MM-DD).'
            else:
                try:
                    datetime.date.fromisoformat(str(valor_fecha))
                except Exception:
                    errors['fecha'] = 'Fecha inválida.'

        if not valor_hora:
            errors['hora'] = 'Hora requerida.'
        else:
            if not pat_hora.match(str(valor_hora)):
                errors['hora'] = 'Formato de hora inválido (HH:MM:SS).'

        if not valor_cedula_usuario or not pat_cedula.match(str(valor_cedula_usuario)):
            errors['cedula_usuario'] = 'Usuario no válido.'

        if errors:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Corrija los campos indicados.",
                "errors": errors
            }

        return {
            "status": True
        }

    def validar(self):
        validacion = self.validarMantenimiento()
        return validacion.get("errors", {})

    def registrar(self):
        try:
            cursor = self.conexion.cursor()
            self.conexion.start_transaction()

            try:
                cursor.callproc('sp_respaldar_mantenimiento', (
                    self.__nombre_archivo,
                    self.__tamano,
                    self.__fecha,
                    self.__hora,
                    self.__cedula_usuario
                ))
            except Exception:
                cursor.execute(
                    """
                    INSERT INTO seguridad.mantenimiento (
                        nombre_archivo,
                        tamano,
                        fecha,
                        hora,
                        cedula_usuario
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        self.__nombre_archivo,
                        self.__tamano,
                        self.__fecha,
                        self.__hora,
                        self.__cedula_usuario
                    )
                )

            self.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            self.conexion.rollback()
            print('Error al registrar mantenimiento:', e)
            return False

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT m.cod_mantenimiento, m.nombre_archivo, m.tamano, m.fecha, m.hora, m.cedula_usuario,
                   u.nombre_usuario
            FROM seguridad.mantenimiento m
            LEFT JOIN seguridad.usuario u ON m.cedula_usuario = u.cedula
            ORDER BY m.fecha DESC, m.cod_mantenimiento DESC
            """
        )
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def listar_usuarios(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT cedula, nombre_usuario FROM seguridad.usuario WHERE status = 1 ORDER BY nombre_usuario ASC")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def eliminar(self, cod):
        try:
            cursor = self.conexion.cursor()
            self.conexion.start_transaction()
            cursor.execute("DELETE FROM seguridad.mantenimiento WHERE cod_mantenimiento = %s", (cod,))
            filas = cursor.rowcount
            self.conexion.commit()
            cursor.close()
            return filas > 0
        except Exception as e:
            self.conexion.rollback()
            print('Error al eliminar mantenimiento:', e)
            return False
