from admin.config.conexion import Conexion
import re


class TipopagosModelo(Conexion):
    def __init__(self):
        super().__init__()

        # ===============================
        # Atributos privados
        # ===============================
        self.__cod_tipo_pago = None
        self.__nombre_tipo_pago = None
        self.__status = None

    # ===============================
    # Getters y Setters
    # ===============================

    @property
    def cod_tipo_pago(self):
        return self.__cod_tipo_pago

    @cod_tipo_pago.setter
    def cod_tipo_pago(self, valor):
        self.__cod_tipo_pago = valor

    @property
    def nombre_tipo_pago(self):
        return self.__nombre_tipo_pago

    @nombre_tipo_pago.setter
    def nombre_tipo_pago(self, valor):
        if valor is None:
            self.__nombre_tipo_pago = None
            return
        self.__nombre_tipo_pago = str(valor).strip()

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    def validarTipoPago(self, nombre_tipo_pago=None):
        nombre = self.__nombre_tipo_pago if nombre_tipo_pago is None else nombre_tipo_pago
        valor = str(nombre).strip() if nombre is not None else ""

        if not valor:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El nombre del tipo de pago es obligatorio."
            }

        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', valor):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El tipo de pago no puede contener números ni caracteres especiales."
            }

        # Validación de longitud (máximo 15 caracteres)
        if len(valor) > 15:
            return {
                "status": False,
                "icon": "warning",
                "title": "limite de caracteres alcanzado",
                "text": "limite de caracteres alcanzado"
            }

        return {
            "status": True
        }

    # ===============================
    # CRUD
    # ===============================

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipo_pago")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    

    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute(
                """
                INSERT INTO tipo_pago (
                    nombre_tipo_pago,
                    status
                )
                VALUES (%s, 1)
                """,
                (self.__nombre_tipo_pago,)
            )

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al registrar tipo de pago:", e)
            return 0




    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE tipo_pago
                SET nombre_tipo_pago = %s,
                    status = %s
                WHERE cod_tipo_pago = %s
            """, (
                self.__nombre_tipo_pago,
                self.__status,
                self.__cod_tipo_pago
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar tipo de pago:", e)
            return 0
        

    def eliminar(self, cod_tipo_pago):
        try:
            cursor = self.conexion.cursor()

            # Verificar si existe el tipo de pago
            sql = """
                SELECT status
                FROM tipo_pago
                WHERE cod_tipo_pago = %s
            """
            cursor.execute(sql, (cod_tipo_pago,))
            tipo_pago = cursor.fetchone()

            if not tipo_pago:
                cursor.close()
                return -2

            status = tipo_pago[0]

            # Verificar asociación con pagos activos
            sql_detalle_pago = """
                SELECT COUNT(*)
                FROM detalle_pago dp
                INNER JOIN pago p
                    ON dp.cod_pago = p.cod_pago
                WHERE dp.cod_tipo_pago = %s
                AND p.status = 1
            """
            cursor.execute(sql_detalle_pago, (cod_tipo_pago,))
            detalle_pago = cursor.fetchone()

            total = int(detalle_pago[0])

            # Si tiene pagos activos asociados no se elimina
            if total > 0:
                cursor.close()
                return -2

            # Si está inactivo -> eliminación lógica
            if status == 0:

                sql_update = """
                    UPDATE tipo_pago
                    SET status = 2
                    WHERE cod_tipo_pago = %s
                """

                cursor.execute(sql_update, (cod_tipo_pago,))
                self.conexion.commit()

                filas = cursor.rowcount
                cursor.close()

                return 1 if filas > 0 else -2

            # Si no tiene asociaciones -> eliminación física
            sql_delete = """
                DELETE FROM tipo_pago
                WHERE cod_tipo_pago = %s
            """

            cursor.execute(sql_delete, (cod_tipo_pago,))
            self.conexion.commit()

            filas = cursor.rowcount
            cursor.close()

            return 1 if filas > 0 else -2

        except Exception as e:
            print("Error al eliminar tipo de pago:", e)
            return -2




    def buscar(self, nombre_tipo_pago):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM tipo_pago
            WHERE nombre_tipo_pago = %s
        """, (nombre_tipo_pago,))

        resultado = cursor.fetchone()
        cursor.close()

        return resultado
