from admin.config.conexion import Conexion
import re


class TiposervicioModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_tipo_servicio = None
        self.__nombre_servicio = None
        self.__precio = None
        self.__status = None

    # =====================================
    # VALIDACIONES
    # =====================================

    def validarNombreServicio(self, nombre_servicio):

        nombre_servicio = nombre_servicio.strip()

        if nombre_servicio == "":
            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el nombre del tipo de servicio."
            }

        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', nombre_servicio):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El tipo de servicio no puede contener números ni caracteres especiales."
            }

        return {
            "status": True
        }

    def validarPrecio(self, precio):

        precio = str(precio).strip()

        if precio == "":
            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el precio."
            }

        if not re.match(r'^\d+(\.\d{1,2})?$', precio):
            return {
                "status": False,
                "icon": "warning",
                "title": "Precio inválido",
                "text": "Ingrese un precio válido."
            }

        if float(precio) <= 0:
            return {
                "status": False,
                "icon": "warning",
                "title": "Precio inválido",
                "text": "El precio debe ser mayor que cero."
            }

        return {
            "status": True
        }

    # =====================================
    # GETTERS Y SETTERS
    # =====================================

    @property
    def cod_tipo_servicio(self):
        return self.__cod_tipo_servicio

    @cod_tipo_servicio.setter
    def cod_tipo_servicio(self, valor):
        self.__cod_tipo_servicio = valor

    @property
    def nombre_servicio(self):
        return self.__nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, valor):
        self.__nombre_servicio = valor

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, valor):
        self.__precio = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    # =====================================
    # CONSULTAR
    # =====================================

    def consultar(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                cod_tipo_servicio,
                nombre_servicio,
                precio,
                status
            FROM tipo_servicio
        """)

        resultados = cursor.fetchall()

        cursor.close()

        return resultados

    # =====================================
    # BUSCAR
    # =====================================

    def buscar(self, nombre_servicio):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM tipo_servicio
            WHERE nombre_servicio = %s
        """, (nombre_servicio,))

        resultado = cursor.fetchone()

        cursor.close()

        return resultado

    # =====================================
    # REGISTRAR
    # =====================================

    def registrar(self):

        try:

            cursor = self.conexion.cursor()

            cursor.execute("""
                INSERT INTO tipo_servicio
                (nombre_servicio, precio, status)
                VALUES (%s, %s, 1)
            """, (
                self.__nombre_servicio,
                self.__precio
            ))

            self.conexion.commit()

            cursor.close()

            return 1

        except Exception as e:

            print("Error registrar tipo servicio:", e)

            return 0

    # =====================================
    # EDITAR
    # =====================================

    def editar(self):

        try:

            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE tipo_servicio
                SET nombre_servicio = %s,
                    precio = %s,
                    status = %s
                WHERE cod_tipo_servicio = %s
            """, (
                self.__nombre_servicio,
                self.__precio,
                self.__status,
                self.__cod_tipo_servicio
            ))

            self.conexion.commit()

            cursor.close()

            return 1

        except Exception as e:

            print("Error editar tipo servicio:", e)

            return 0

    # =====================================
    # ELIMINAR
    # =====================================

    def eliminar(self, cod_tipo_servicio):

        try:

            cursor = self.conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM detalle_servicio
                WHERE cod_tipo_servicio = %s
            """, (cod_tipo_servicio,))

            resultado = cursor.fetchone()

            total = resultado['total'] if resultado else 0

            if total > 0:

                cursor.close()

                return "existe_servicio"

            cursor.execute("""
                DELETE FROM tipo_servicio
                WHERE cod_tipo_servicio = %s
            """, (cod_tipo_servicio,))

            self.conexion.commit()

            cursor.close()

            return "eliminado"

        except Exception as e:

            print("Error eliminar tipo servicio:", e)

            return "error"