from admin.config.conexion import Conexion
import re


class MarcaModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_marca = None
        self.__nombre_marca = None
        self.__status = None


    # ===============================
    # VALIDACIONES
    # ===============================

    def validarNombreMarca(self, nombre_marca):

        nombre_marca = str(nombre_marca).strip()

        if nombre_marca == "":
            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el nombre de la marca."
            }


        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', nombre_marca):

            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "La marca no puede contener números ni caracteres especiales."
            }


        if len(nombre_marca) < 3:

            return {
                "status": False,
                "icon": "warning",
                "title": "Nombre inválido",
                "text": "El nombre de la marca debe tener mínimo 3 caracteres."
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
    def cod_marca(self):
        return self.__cod_marca

    @cod_marca.setter
    def cod_marca(self, valor):
        self.__cod_marca = valor


    @property
    def nombre_marca(self):
        return self.__nombre_marca

    @nombre_marca.setter
    def nombre_marca(self, valor):
        self.__nombre_marca = valor


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

        cursor.execute("""
            SELECT *
            FROM marca
        """)

        resultados = cursor.fetchall()

        cursor.close()

        return resultados



    # ===============================
    # BUSCAR
    # ===============================

    def buscar(self, nombre_marca):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM marca
            WHERE nombre_marca = %s
        """, (nombre_marca,))


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
                INSERT INTO marca
                (
                    nombre_marca,
                    status
                )
                VALUES (%s,1)
            """,(
                self.__nombre_marca,
            ))


            self.conexion.commit()

            cursor.close()

            return 1


        except Exception as e:

            print("Error al registrar marca:", e)

            return 0



    # ===============================
    # EDITAR
    # ===============================

    def editar(self):

        try:

            cursor = self.conexion.cursor()


            cursor.execute("""
                UPDATE marca
                SET nombre_marca = %s,
                    status = %s
                WHERE cod_marca = %s
            """,(
                self.__nombre_marca,
                self.__status,
                self.__cod_marca
            ))


            self.conexion.commit()

            cursor.close()

            return 1


        except Exception as e:

            print("Error al editar marca:", e)

            return 0



    # ===============================
    # ELIMINAR
    # ===============================

    def eliminar(self,cod_marca):

        try:

            cursor = self.conexion.cursor(dictionary=True)


            # Verificar si la marca está asociada a productos
            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM producto
                WHERE cod_marca = %s
            """,(cod_marca,))


            resultado = cursor.fetchone()


            if resultado["total"] > 0:

                cursor.close()

                return "existe_producto"



            cursor.execute("""
                DELETE FROM marca
                WHERE cod_marca = %s
            """,(cod_marca,))


            self.conexion.commit()

            cursor.close()


            return "eliminado"


        except Exception as e:

            print("Error eliminar marca:", e)

            return "error"