from admin.config.conexion import Conexion
import re

class UnidadmedidaModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_medida = None
        self.__medida = None
        self.__status = None

    # =====================================
    # VALIDACIONES
    # =====================================

    def validarMedida(self, medida):

        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', medida):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "La unidad de medida no puede contener números."
            }

        return {
            "status": True
        }
    # =====================================
    # GETTERS Y SETTERS
    # =====================================

    @property
    def cod_medida(self):
        return self.__cod_medida

    @cod_medida.setter
    def cod_medida(self, valor):
        self.__cod_medida = valor

    @property
    def medida(self):
        return self.__medida

    @medida.setter
    def medida(self, valor):
        self.__medida = valor

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

        cursor.execute("SELECT cod_medida, medida, status FROM medida")

        resultados = cursor.fetchall()
        cursor.close()

        return resultados


 # ===============================
    # registrar
    # ===============================
    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute(
                "INSERT INTO medida (medida, status) VALUES (%s, 1)",
                (self.__medida,)
            )

            self.conexion.commit()
            cursor.close()
            return 1

        except Exception as e:
            print("Error al registrar medida:", e)
            return 0

    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE medida
                SET medida = %s,
                    status = %s
                WHERE cod_medida = %s
            """, (
                self.__medida,
                self.__status,
                self.__cod_medida
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar  medida:", e)
            return 0        


    def eliminar(self, cod_medida):
        try:
            cursor = self.conexion.cursor()

            # Verificar si existe la medida
            sql = """
                SELECT status
                FROM medida
                WHERE cod_medida = %s
            """
            cursor.execute(sql, (cod_medida,))
            medida = cursor.fetchone()

            if not medida:
                cursor.close()
                return -2

            status = medida[0]

            # Verificar si está asociada a una unidad
            sql_unidad = """
                SELECT COUNT(*)
                FROM unidad
                WHERE cod_medida = %s
            """
            cursor.execute(sql_unidad, (cod_medida,))
            unidad = cursor.fetchone()

            total = int(unidad[0])

            # Si tiene unidades asociadas no se elimina
            if total > 0:
                cursor.close()
                return -2

            # Si está inactiva -> eliminación lógica
            if status == 0:
                sql_update = """
                    UPDATE medida
                    SET status = 2
                    WHERE cod_medida = %s
                """
                cursor.execute(sql_update, (cod_medida,))
                self.conexion.commit()

                filas = cursor.rowcount
                cursor.close()

                return 1 if filas > 0 else -2

            # Si no está asociada y está activa -> eliminar físicamente
            sql_delete = """
                DELETE FROM medida
                WHERE cod_medida = %s
            """
            cursor.execute(sql_delete, (cod_medida,))
            self.conexion.commit()

            filas = cursor.rowcount
            cursor.close()

            return 1 if filas > 0 else -2

        except Exception as e:
            print("Error al eliminar medida:", e)
            return -2


    def buscar(self, medida):
                cursor = self.conexion.cursor(dictionary=True)

                cursor.execute("""
                    SELECT *
                    FROM medida
                    WHERE medida = %s
                """, (medida,))

                resultado = cursor.fetchone()
                cursor.close()

                return resultado            
           