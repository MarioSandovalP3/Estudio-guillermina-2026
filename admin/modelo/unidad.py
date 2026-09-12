from admin.config.conexion import Conexion
import re

class UnidadModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_unidad = None
        self.__nombre_unidad = None
        self.__cod_presentacion = None
        self.__cod_medida = None
        self.__status = None


    def validarNombreUnidad(self, nombre_unidad):

        if re.search(r'[^0-9]', nombre_unidad):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "La unidad solo puede contener números."
            }

        return {
            "status": True
        }


    # =====================================
    # GETTERS Y SETTERS
    # =====================================

    @property
    def cod_unidad(self):
        return self.__cod_unidad

    @cod_unidad.setter
    def cod_unidad(self, valor):
        self.__cod_unidad = valor

    @property
    def nombre_unidad(self):
        return self.__nombre_unidad

    @nombre_unidad.setter
    def nombre_unidad(self, valor):
        self.__nombre_unidad = valor

    @property
    def cod_presentacion(self):
        return self.__cod_presentacion

    @cod_presentacion.setter
    def cod_presentacion(self, valor):
        self.__cod_presentacion = valor

    @property
    def cod_medida(self):
        return self.__cod_medida

    @cod_medida.setter
    def cod_medida(self, valor):
        self.__cod_medida = valor

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
            SELECT 
                u.cod_unidad,
                u.nombre_unidad,
                u.cod_presentacion,
                u.cod_medida,
                u.status,
                p.presentacion,
                m.medida
            FROM unidad AS u
            INNER JOIN presentacion AS p
                ON u.cod_presentacion = p.cod_presentacion
            INNER JOIN medida AS m
                ON u.cod_medida = m.cod_medida
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados    


    # ===============================
    # OBTENER PRESENTACIONES
    # ===============================

    def obtener_presentaciones(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                cod_presentacion,
                presentacion
            FROM presentacion
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados


    # ===============================
    # OBTENER MEDIDAS
    # ===============================

    def obtener_medidas(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                cod_medida,
                medida
            FROM medida
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados       
    

    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                INSERT INTO unidad (
                    nombre_unidad,
                    cod_presentacion,
                    cod_medida,
                    status
                ) VALUES (%s, %s, %s, 1)
            """, (
                self.__nombre_unidad,
                self.__cod_presentacion,
                self.__cod_medida
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al registrar unidad:", e)
            return 0


    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE unidad
                SET nombre_unidad = %s,
                    cod_presentacion = %s,
                    cod_medida = %s,
                    status = %s
                WHERE cod_unidad = %s
            """, (
                self.__nombre_unidad,
                self.__cod_presentacion,
                self.__cod_medida,
                self.__status,
                self.__cod_unidad
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar unidad:", e)
            return 0   



    def sp_eliminar_unidad(self, cod_unidad):

        try:

            cursor = self.conexion.cursor()

            self.conexion.start_transaction()

            # 1. Verificar si la unidad existe
            sql = """
                SELECT status
                FROM unidad
                WHERE cod_unidad = %s
            """

            cursor.execute(sql, (cod_unidad,))
            unidad = cursor.fetchone()

            if not unidad:
                self.conexion.rollback()
                cursor.close()
                return -2

            status = unidad[0]

            # 2. Verificar si tiene productos activos asociados
            sql = """
                SELECT COUNT(*)
                FROM producto
                WHERE cod_unidad = %s
                AND status = 1
            """

            cursor.execute(sql, (cod_unidad,))
            total = cursor.fetchone()[0]

            # 3. Si está inactiva, eliminación lógica
            if status == 0:

                sql = """
                    UPDATE unidad
                    SET status = 2
                    WHERE cod_unidad = %s
                """

                cursor.execute(sql, (cod_unidad,))
                filas = cursor.rowcount

                self.conexion.commit()
                cursor.close()

                return 1 if filas > 0 else -2

            # 4. Si está activa y tiene productos, no eliminar
            if status == 1 and total > 0:

                self.conexion.rollback()
                cursor.close()

                return -2

            # 5. Si está activa y no tiene productos, eliminar físicamente
            if status == 1 and total == 0:

                sql = """
                    DELETE FROM unidad
                    WHERE cod_unidad = %s
                """

                cursor.execute(sql, (cod_unidad,))
                filas = cursor.rowcount

                self.conexion.commit()
                cursor.close()

                return 1 if filas > 0 else -2

        except Exception as e:

            self.conexion.rollback()

            print("Error al eliminar unidad:", e)

            return -2
        


    def buscar(self, unidad, cod_presentacion, cod_medida, cod_unidad=None):
        cursor = self.conexion.cursor(dictionary=True)

        if cod_unidad:
            cursor.execute("""
                SELECT cod_unidad
                FROM unidad
                WHERE nombre_unidad = %s
                AND cod_presentacion = %s
                AND cod_medida = %s
                AND cod_unidad != %s
            """, (unidad, cod_presentacion, cod_medida, cod_unidad))
        else:
            cursor.execute("""
                SELECT cod_unidad
                FROM unidad
                WHERE nombre_unidad = %s
                AND cod_presentacion = %s
                AND cod_medida = %s
            """, (unidad, cod_presentacion, cod_medida))

        resultado = cursor.fetchone()
        cursor.close()

        return resultado