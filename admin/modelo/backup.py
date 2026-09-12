import datetime
import os
import subprocess

from werkzeug.utils import secure_filename

from admin.config.config import DB_PASS, DB_USER
from admin.config.conexion import Conexion


class BackupModelo(Conexion):
    CARPETA_BACKUPS = os.path.abspath("static/backups")

    def __init__(self):
        super().__init__()
        self.ultimo_archivo = None
        self.ultimo_tamano = None

    def _ejecutable(self, nombre):
        ruta_xampp = os.path.join(
            os.environ.get("XAMPP_HOME", "C:/xampp"),
            "mysql",
            "bin",
            f"{nombre}.exe"
        )
        return ruta_xampp if os.path.exists(ruta_xampp) else nombre

    def _argumentos_conexion(self, ejecutable):
        argumentos = [ejecutable, "-u", DB_USER]
        if DB_PASS:
            argumentos.append(f"-p{DB_PASS}")
        return argumentos

    def crear_backup(self, cedula_usuario=None):
        try:
            os.makedirs(self.CARPETA_BACKUPS, exist_ok=True)
            fecha = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            ruta = os.path.join(self.CARPETA_BACKUPS, f"backup_{fecha}.sql")
            comando = self._argumentos_conexion(self._ejecutable("mysqldump"))
            comando.extend(["--databases", "sac", "seguridad"])

            with open(ruta, "w", encoding="utf-8") as archivo:
                resultado = subprocess.run(
                    comando,
                    stdout=archivo,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )

            if resultado.returncode != 0:
                if os.path.exists(ruta):
                    os.remove(ruta)
                print("Error mysqldump:", resultado.stderr)
                return False

            self.ultimo_archivo = os.path.basename(ruta)
            self.ultimo_tamano = os.path.getsize(ruta)
            return True
        except Exception as error:
            print("Error backup:", error)
            return False

    def listar_backups(self):
        os.makedirs(self.CARPETA_BACKUPS, exist_ok=True)
        archivos = []
        for nombre in os.listdir(self.CARPETA_BACKUPS):
            ruta = os.path.join(self.CARPETA_BACKUPS, nombre)
            if os.path.isfile(ruta):
                archivos.append({
                    "nombre": nombre,
                    "tamaño": f"{round(os.path.getsize(ruta) / 1024, 2)} KB",
                    "fecha": datetime.datetime.fromtimestamp(
                        os.path.getctime(ruta)
                    ).strftime("%d-%m-%Y")
                })
        return archivos

    def restaurar_backup(self, archivo):
        ruta = None
        try:
            nombre = secure_filename(archivo.filename or "")
            if not nombre.lower().endswith(".sql"):
                return False

            os.makedirs(self.CARPETA_BACKUPS, exist_ok=True)
            ruta = os.path.join(self.CARPETA_BACKUPS, nombre)
            archivo.save(ruta)
            comando = self._argumentos_conexion(self._ejecutable("mysql"))

            with open(ruta, "r", encoding="utf-8") as respaldo:
                resultado = subprocess.run(
                    comando,
                    stdin=respaldo,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )
            return resultado.returncode == 0
        except Exception as error:
            print("Error restore:", error)
            return False
        finally:
            if ruta and os.path.exists(ruta):
                os.remove(ruta)

    def eliminar_backup(self, nombre):
        try:
            nombre_seguro = secure_filename(nombre or "")
            if not nombre_seguro:
                return False

            ruta = os.path.abspath(os.path.join(self.CARPETA_BACKUPS, nombre_seguro))
            if os.path.dirname(ruta) != self.CARPETA_BACKUPS or not os.path.isfile(ruta):
                return False

            os.remove(ruta)

            cursor = self.conexion.cursor()
            try:
                self.conexion.start_transaction()
                cursor.execute(
                    "DELETE FROM seguridad.mantenimiento WHERE nombre_archivo = %s OR nombre_archivo = %s",
                    (nombre_seguro, os.path.join("static/backups", nombre_seguro))
                )
                self.conexion.commit()
            except Exception:
                self.conexion.rollback()
                raise
            finally:
                cursor.close()

            return True
        except Exception as error:
            print("Error eliminar backup:", error)
            return False
