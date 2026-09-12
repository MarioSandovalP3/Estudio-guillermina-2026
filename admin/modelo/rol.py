from admin.config.conexion import Conexion
import re
class RolModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_rol = None
        self.__rol = None
        self.__status = None



    def validarRol(self, rol):

        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñÜü]', rol):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El rol solo puede contener letras."
            }

        return {
            "status": True
        }
    # =======================
    # ========
    # GETTERS Y SETTERS
    # ===============================
    @property
    def cod_rol(self):
        return self.__cod_rol

    @cod_rol.setter
    def cod_rol(self, valor):
        self.__cod_rol = valor

    @property
    def rol(self):
        return self.__rol

    @rol.setter
    def rol(self, valor):
        self.__rol = valor

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
        cursor.execute("SELECT * FROM seguridad.rol")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def buscar(self, rol):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM seguridad.rol
            WHERE rol = %s
        """, (rol,))

        resultado = cursor.fetchone()
        cursor.close()

        return resultado


    # ===============================
    # REGISTRAR
    # ===============================
    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.callproc(
            'seguridad.sp_registrar_rol',
            (self.__rol,)
        )
            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            self.conexion.rollback()
            print("Error al registrar rol:", e)
            return 0

    # ===============================
    # EDITAR
    # ===============================
    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE seguridad.rol 
                SET rol = %s,
                    status = %s
                WHERE cod_rol = %s
            """, (
                self.__rol,
                self.__status,
                self.__cod_rol
            ))

            self.conexion.commit()
            cursor.close()
            return 1

        except Exception as e:
            print("Error al editar rol:", e)
            return 0

    # ===============================
    # ELIMINAR  
    # ===============================
    def eliminar(self, cod_rol):
            try:
                cursor = self.conexion.cursor(dictionary=True)

                # 1. VERIFICAR SI TIENE USUARIOS ASOCIADOS
                sql_verificar = """
                    SELECT COUNT(*) AS total 
                    FROM seguridad.usuario 
                    WHERE cod_rol = %s
                """
                cursor.execute(sql_verificar, (cod_rol,))
                resultado = cursor.fetchone()

                total = resultado['total'] if resultado else 0

                # 2. SI TIENE USUARIOS → NO ELIMINA
                if total > 0:
                    cursor.close()
                    return "existe_usuarios"

                # 3. SI NO TIENE USUARIOS → ELIMINA
                sql_eliminar = """
                    DELETE FROM seguridad.rol 
                    WHERE cod_rol = %s
                """
                cursor.execute(sql_eliminar, (cod_rol,))
                self.conexion.commit()
                cursor.close()

                return "eliminado"

            except Exception as e:
                print("Error eliminar rol:", e)
                return "error"

