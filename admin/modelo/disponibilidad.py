from admin.config.conexion import Conexion

class DisponibilidadModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_disponibilidad = None
        self.__fecha_disponibilidad = None
        self.__hora_disponibilidad = None
        self.__status = None
        self.__cedula_especialista = None

    # ===============================
    # GETTERS Y SETTERS
    # ===============================

    @property
    def cod_disponibilidad(self):
        return self.__cod_disponibilidad

    @cod_disponibilidad.setter
    def cod_disponibilidad(self, valor):
        self.__cod_disponibilidad = valor

    @property
    def fecha_disponibilidad(self):
        return self.__fecha_disponibilidad

    @fecha_disponibilidad.setter
    def fecha_disponibilidad(self, valor):
        self.__fecha_disponibilidad = valor

    @property
    def hora_disponibilidad(self):
        return self.__hora_disponibilidad

    @hora_disponibilidad.setter
    def hora_disponibilidad(self, valor):
        self.__hora_disponibilidad = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    @property
    def cedula_especialista(self):
        return self.__cedula_especialista

    @cedula_especialista.setter
    def cedula_especialista(self, valor):
        self.__cedula_especialista = valor


    def consultar_por_tipo(self, tipo):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                de.cod_disponibilidad,
                de.fecha_disponibilidad,
                de.hora_disponibilidad,
                de.status,

                e.cedula_especialista,
                e.especialista,

                u.nombre_usuario,
                u.apellido_usuario

            FROM disponibilidad_especialista de
            INNER JOIN especialista e 
                ON de.cedula_especialista = e.cedula_especialista
            INNER JOIN seguridad.usuario u 
                ON e.cedula_especialista = u.cedula

            WHERE e.especialista = %s
        """, (tipo,))

        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    

    def obtenerEspecialista(self, tipo):
            cursor = self.conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    e.cedula_especialista,
                    e.especialista,
                    u.nombre_usuario,
                    u.apellido_usuario
                FROM sac.especialista e
                INNER JOIN seguridad.usuario u
                    ON e.cedula_especialista = u.cedula
                WHERE e.especialista = %s
            """, (tipo,))

            resultados = cursor.fetchall()
            cursor.close()

            return resultados  