from admin.config.conexion import Conexion
import re

class EspecialidadModelo(Conexion):

    def __init__(self):
        super().__init__()

        # ===============================
        # ATRIBUTOS PRIVADOS
        # ===============================
      
        self.__especialista = None
        self.__nombre_usuario = None
        self.__cedula = None
        self.__status = None

    def validarEspecialidad(self, especialista):

        if re.search(r'\d', especialista):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "La especialidad solo puede contener letras."
            }

        return {
            "status": True
        }

    # ===============================
    # GETTERS Y SETTERS
    # ===============================

    @property
    def especialista(self):
        return self.__especialista

    @especialista.setter
    def especialista(self, valor):
        self.__especialista = valor


    @property
    def nombre_usuario(self):
        return self.__nombre_usuario

    @nombre_usuario.setter
    def nombre_usuario(self, valor):
        self.__nombre_usuario = valor


    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, valor):
        self.__cedula = valor


    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    # ===============================
    # CONSULTAS
    # ===============================

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT e.*, u.nombre_usuario, u.apellido_usuario
            FROM especialista AS e
            INNER JOIN seguridad.usuario AS u
            ON e.cedula_especialista = u.cedula
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados


    def obtener_usuario(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT u.cedula, u.nombre_usuario, u.apellido_usuario, r.cod_rol, r.rol
            FROM seguridad.usuario AS u
            INNER JOIN seguridad.rol AS r ON u.cod_rol = r.cod_rol
            WHERE r.rol != 'cliente'
            AND u.status = 1
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados

    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.callproc(
                'sac.sp_guardar_especialista',
                (
                    self.__especialista,
                    self.__cedula
                )
            )

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            self.conexion.rollback()
            print("Error al registrar especialista:", e)
            return 0


    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE especialista 
                SET especialista = %s,
                    status = %s
                WHERE cedula_especialista = %s
            """, (
                self.__especialista,
                self.__status,
                self.__cedula
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar especialista:", e)
            return 0      


    def buscar(self, especialidad, cedula):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM especialista
            WHERE especialista = %s
            AND cedula_especialista = %s
        """, (especialidad, cedula))

        resultado = cursor.fetchone()

        cursor.close()

        return resultado


    def eliminar(self, cedula_especialista):
        try:
            cursor = self.conexion.cursor(dictionary=True)

            sql = """
                SELECT e.status,
                    COUNT(s.cod_servicio) AS reservas,
                    SUM(CASE WHEN s.status = 1 THEN 1 ELSE 0 END) AS reservas_activas
                FROM sac.especialista e
                LEFT JOIN sac.servicio s
                    ON s.cedula_especialista = e.cedula_especialista
                WHERE e.cedula_especialista = %s
                GROUP BY e.status
            """
            cursor.execute(sql, (cedula_especialista,))
            resultado = cursor.fetchone()

            if resultado:
                status = resultado["status"]
                reservas = resultado["reservas"] or 0
                reservas_activas = resultado["reservas_activas"] or 0

                if status == 1 and reservas_activas > 0:
                    cursor.close()
                    return "tiene_reservas"

                if status == 0 and reservas > 0:
                    cursor.close()
                    return "tiene_reservas"

            sql = """
                DELETE FROM sac.especialista
                WHERE cedula_especialista = %s
            """
            cursor.execute(sql, (cedula_especialista,))
            self.conexion.commit()
            cursor.close()

            return "eliminado"

        except Exception as e:
            print("Error eliminar especialista:", e)
            return "error"