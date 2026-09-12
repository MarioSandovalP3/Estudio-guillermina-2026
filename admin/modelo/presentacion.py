from admin.config.conexion import Conexion


class PresentacionModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_presentacion = None
        self.__presentacion = None
        self.__status = None

    # =====================================
    # GETTERS Y SETTERS
    # =====================================

    @property
    def cod_presentacion(self):
        return self.__cod_presentacion

    @cod_presentacion.setter
    def cod_presentacion(self, valor):
        self.__cod_presentacion = valor

    @property
    def presentacion(self):
        return self.__presentacion

    @presentacion.setter
    def presentacion(self, valor):
        self.__presentacion = valor

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
            SELECT cod_presentacion, presentacion, status
            FROM presentacion
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados


    def buscar(self, presentacion, cod_presentacion=None):
        cursor = self.conexion.cursor(dictionary=True)

        if cod_presentacion:
            cursor.execute("""
                SELECT *
                FROM sac.presentacion
                WHERE presentacion = %s
                AND cod_presentacion != %s
            """, (presentacion, cod_presentacion))
        else:
            cursor.execute("""
                SELECT *
                FROM sac.presentacion
                WHERE presentacion = %s
            """, (presentacion,))

        resultado = cursor.fetchone()
        cursor.close()

        return resultado   





    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute(
                "INSERT INTO presentacion (presentacion, status) VALUES (%s, 1)",
                (self.__presentacion,)
            )

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al registrar presentación:", e)
            return 0
        

    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE presentacion
                SET presentacion = %s,
                    status = %s
                WHERE cod_presentacion = %s
            """, (
                self.__presentacion,
                self.__status,
                self.__cod_presentacion
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar presentación:", e)
            return 0

    def eliminar(self, cod_presentacion):
        try:
            cursor = self.conexion.cursor()

            # Verificar si existe la presentación
            sql = """
                SELECT status
                FROM presentacion
                WHERE cod_presentacion = %s
            """
            cursor.execute(sql, (cod_presentacion,))
            presentacion = cursor.fetchone()

            if not presentacion:
                cursor.close()
                return -2

            status = presentacion[0]

            # Verificar si está asociada a una unidad
            sql_unidad = """
                SELECT COUNT(*)
                FROM unidad
                WHERE cod_presentacion = %s
            """
            cursor.execute(sql_unidad, (cod_presentacion,))
            unidad = cursor.fetchone()

            total = int(unidad[0])

            # Si tiene unidades asociadas no se elimina
            if total > 0:
                cursor.close()
                return -2

            # Si está inactiva -> eliminación lógica
            if status == 0:
                sql_update = """
                    UPDATE presentacion
                    SET status = 2
                    WHERE cod_presentacion = %s
                """
                cursor.execute(sql_update, (cod_presentacion,))
                self.conexion.commit()

                filas = cursor.rowcount
                cursor.close()

                return 1 if filas > 0 else -2

            # Si no está asociada y está activa -> eliminar físicamente
            sql_delete = """
                DELETE FROM presentacion
                WHERE cod_presentacion = %s
            """
            cursor.execute(sql_delete, (cod_presentacion,))
            self.conexion.commit()

            filas = cursor.rowcount
            cursor.close()

            return 1 if filas > 0 else -2

        except Exception as e:
            print("Error al eliminar presentación:", e)
            return -2