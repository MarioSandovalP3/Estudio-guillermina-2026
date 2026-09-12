from admin.config.conexion import Conexion
import re

class CategoriaModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_categoria = None
        self.__nombre_categoria = None
        self.__status = None


# ===============================
    # VALIDACIONES
    # ===============================

    def validarNombreCategoria(self, nombre_categoria):

        nombre_categoria = str(nombre_categoria).strip()

        if nombre_categoria == "":
            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el nombre de la categoría."
            }

        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', nombre_categoria):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "La categoría no puede contener números ni caracteres especiales."
            }

        if len(nombre_categoria) < 3:
            return {
                "status": False,
                "icon": "warning",
                "title": "Nombre inválido",
                "text": "La categoría debe tener al menos 3 caracteres."
            }

        if len(nombre_categoria) > 50:
            return {
                "status": False,
                "icon": "warning",
                "title": "Nombre muy largo",
                "text": "La categoría no puede superar los 50 caracteres."
            }

        return {
            "status": True
        }


    def validarStatus(self, status):

        if str(status) not in ["0", "1"]:
            return {
                "status": False,
                "icon": "warning",
                "title": "Estado inválido",
                "text": "El estado recibido no es válido."
            }

        return {
            "status": True
        }
    # ===============================
    # GETTERS Y SETTERS
    # ===============================

    @property
    def cod_categoria(self):
        return self.__cod_categoria

    @cod_categoria.setter
    def cod_categoria(self, valor):
        self.__cod_categoria = valor

    @property
    def nombre_categoria(self):
        return self.__nombre_categoria

    @nombre_categoria.setter
    def nombre_categoria(self, valor):
        self.__nombre_categoria = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    # ===============================
    # CONSULTAR
    # ===============================

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categoria")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    # ===============================
    # BUSCAR
    # ===============================

    def buscar(self, nombre_categoria):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM categoria
            WHERE nombre_categoria = %s
        """, (nombre_categoria,))

        resultado = cursor.fetchone()
        cursor.close()

        return resultado

    # ===============================
    # REGISTRAR
    # ===============================

    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                INSERT INTO categoria (nombre_categoria, status)
                VALUES (%s, 1)
            """, (
                self.__nombre_categoria,
            ))

            self.conexion.commit()
            cursor.close()
            return 1

        except Exception as e:
            print("Error al registrar categoría:", e)
            return 0

    # ===============================
    # EDITAR
    # ===============================

    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE categoria
                SET nombre_categoria = %s,
                    status = %s
                WHERE cod_categoria = %s
            """, (
                self.__nombre_categoria,
                self.__status,
                self.__cod_categoria
            ))

            self.conexion.commit()
            cursor.close()
            return 1

        except Exception as e:
            print("Error al editar categoría:", e)
            return 0

        # ===============================
    # ELIMINAR
    # ===============================

    def eliminar(self, cod_categoria):

        try:

            cursor = self.conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM producto
                WHERE cod_categoria = %s
            """, (cod_categoria,))

            resultado = cursor.fetchone()

            if resultado["total"] > 0:

                cursor.close()

                return "existe_producto"

            cursor.execute("""
                DELETE FROM categoria
                WHERE cod_categoria = %s
            """, (cod_categoria,))

            self.conexion.commit()

            cursor.close()

            return "eliminado"

        except Exception as e:

            print("Error eliminar categoría:", e)

            return "error"