from admin.config.conexion import Conexion

class ReservasModelo(Conexion):
    def __init__(self):
        super().__init__()  # Llama al constructor de Conexion

        # Atributos privados
   
        self.__fecha_reserva = None
        self.__hora_reserva = None
        self.__cantidad_reserva = None
        self.__status = None
        self.__cod_servicio = None
        self.__cod_especialista = None
        self.__especialista = None
        self.__precio = None

    # ===============================
    # Getters y Setters
    # ===============================

    @property
    def cod_reserva(self):
        return self.__cod_reserva

    @cod_reserva.setter
    def cod_reserva(self, valor):
        self.__cod_reserva = valor

    @property
    def fecha_reserva(self):
        return self.__fecha_reserva

    @fecha_reserva.setter
    def fecha_reserva(self, valor):
        self.__fecha_reserva = valor

    @property
    def hora_reserva(self):
        return self.__hora_reserva

    @hora_reserva.setter
    def hora_reserva(self, valor):
        self.__hora_reserva = valor

    @property
    def cantidad_reserva(self):
        return self.__cantidad_reserva

    @cantidad_reserva.setter
    def cantidad_reserva(self, valor):
        self.__cantidad_reserva = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    @property
    def cod_servicio(self):
        return self.__cod_servicio

    @cod_servicio.setter
    def cod_servicio(self, valor):
        self.__cod_servicio = valor

    @property
    def cod_especialista(self):
        return self.__cod_especialista

    @cod_especialista.setter
    def cod_especialista(self, valor):
        self.__cod_especialista = valor

    @property
    def especialista(self):
        return self.__especialista

    @especialista.setter
    def especialista(self, valor):
        self.__especialista = valor

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, valor):
        self.__precio = valor

        

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                s.cod_servicio,
                s.fecha AS fecha_reserva,
                s.hora AS hora_reserva,
                s.status AS estado_reserva,

                u.cedula AS cedula_cliente,
                u.nombre_usuario AS nombre_cliente,
                u.apellido_usuario AS apellido_cliente,

                e.cedula_especialista,
                e.especialista AS nombre_especialista,
                u2.nombre_usuario AS nombre_usuario_especialista,
                u2.apellido_usuario AS apellido_usuario_especialista,

                GROUP_CONCAT(
                    DISTINCT ts.nombre_servicio
                    SEPARATOR ' | '
                ) AS servicios,

                GROUP_CONCAT(
                    DISTINCT ts.precio
                    SEPARATOR ' | '
                ) AS precios,

                r.rol AS rol_usuario

            FROM sac.servicio s

            INNER JOIN seguridad.usuario u
                ON s.cedula = u.cedula

            INNER JOIN sac.especialista e
                ON s.cedula_especialista = e.cedula_especialista

            LEFT JOIN seguridad.usuario u2
                ON u2.cedula = e.cedula_especialista

            LEFT JOIN sac.detalle_servicio ds
                ON ds.cod_servicio = s.cod_servicio

            LEFT JOIN sac.tipo_servicio ts
                ON ds.cod_tipo_servicio = ts.cod_tipo_servicio

            LEFT JOIN seguridad.usuario su
                ON su.cedula = u.cedula

            LEFT JOIN seguridad.rol r
                ON su.cod_rol = r.cod_rol

            WHERE s.status IN (0, 1)

            GROUP BY
                s.cod_servicio,
                u.cedula,
                e.cedula_especialista,
                r.rol,
                s.fecha,
                s.hora,
                s.status,
                e.especialista,
                u2.nombre_usuario,
                u2.apellido_usuario

            ORDER BY
                s.fecha ASC,
                s.hora ASC
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados

    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE servicio
                SET fecha = %s,
                    hora = %s,
                    status = %s
                WHERE cod_servicio = %s
            """, (
                self.__fecha_reserva,
                self.__hora_reserva,
                self.__status,
                self.__cod_servicio
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar reserva:", e)
            return 0
        


    def editar(self):
        cursor = None
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                SELECT fecha, hora, cedula_especialista, status
                FROM sac.servicio
                WHERE cod_servicio = %s
            """, (self.__cod_servicio,))

            actual = cursor.fetchone()

            if not actual:
                return 0

            fecha_anterior = actual[0]
            hora_anterior = actual[1]
            especialista = actual[2]

            fecha_nueva = self.__fecha_reserva
            hora_nueva = self.__hora_reserva
            status_nuevo = int(self.__status)

            cursor.execute("""
                UPDATE sac.disponibilidad_especialista
                SET fecha_disponibilidad = %s,
                    hora_disponibilidad = %s,
                    status = %s
                WHERE fecha_disponibilidad = %s
                AND hora_disponibilidad = %s
                AND cedula_especialista = %s
            """, (
                fecha_nueva,
                hora_nueva,
                status_nuevo,
                fecha_anterior,
                hora_anterior,
                especialista
            ))

            cursor.execute("""
                UPDATE sac.servicio
                SET fecha = %s,
                    hora = %s,
                    status = %s
                WHERE cod_servicio = %s
            """, (
                fecha_nueva,
                hora_nueva,
                status_nuevo,
                self.__cod_servicio
            ))

            self.conexion.commit()
            return 1

        except Exception:
            if self.conexion:
                self.conexion.rollback()
            return 0

        finally:
            if cursor:
                cursor.close()



        # ===============================
        # ELIMINAR  
        # ===============================
    
    def eliminar(self, cod_servicio):
        cursor = None

        try:
            cursor = self.conexion.cursor(dictionary=True)

            # =====================================================
            # 1. CONSULTAR LA RESERVA
            # =====================================================
            cursor.execute("""
                SELECT 
                    fecha,
                    hora,
                    cedula_especialista,
                    status
                FROM sac.servicio
                WHERE cod_servicio = %s
            """, (cod_servicio,))

            servicio = cursor.fetchone()

            if not servicio:
                return "no_existe"

            status_actual = int(servicio["status"])

            fecha_reserva = servicio["fecha"]
            hora_reserva = servicio["hora"]
            especialista = servicio["cedula_especialista"]

            # =====================================================
            # 2. SI ESTÁ ACTIVA NO SE PUEDE ELIMINAR
            # =====================================================
            if status_actual == 1:
                return "activo"

            # =====================================================
            # 3. SI YA ESTÁ ELIMINADA
            # =====================================================
            if status_actual == 2:
                return "ya_eliminado"

            # =====================================================
            # 4. SOLO SE PUEDE ELIMINAR SI ESTÁ CANCELADA (0)
            # =====================================================
            if status_actual == 0:

                # -------------------------------------------------
                # 4.1 ELIMINAR LA DISPONIBILIDAD DE LA RESERVA
                # -------------------------------------------------
                cursor.execute("""
                    DELETE FROM sac.disponibilidad_especialista
                    WHERE fecha_disponibilidad = %s
                    AND hora_disponibilidad = %s
                    AND cedula_especialista = %s
                """, (
                    fecha_reserva,
                    hora_reserva,
                    especialista
                ))

                # -------------------------------------------------
                # 4.2 CAMBIAR STATUS DE 0 → 2
                # -------------------------------------------------
                cursor.execute("""
                    UPDATE sac.servicio
                    SET status = 2
                    WHERE cod_servicio = %s
                    AND status = 0
                """, (cod_servicio,))

              
                self.conexion.commit()

                return "eliminado"

            return "error"

        except Exception as e:
            if self.conexion:
                self.conexion.rollback()

            print("Error eliminar servicio:", e)
            return "error"

        finally:
            if cursor:
                cursor.close()

    def consultarfiltradofecha(self, fecha_inicio=None, fecha_fin=None):

        cursor = self.conexion.cursor(dictionary=True)

        sql = """
            SELECT
                s.cod_servicio,
                s.fecha AS fecha_reserva,
                s.hora AS hora_reserva,
                s.status AS estado_reserva,

                u.cedula AS cedula_cliente,
                u.nombre_usuario AS nombre_cliente,
                u.apellido_usuario AS apellido_cliente,

                e.cedula_especialista,
                e.especialista AS nombre_especialista,
                u2.nombre_usuario AS nombre_usuario_especialista,
                u2.apellido_usuario AS apellido_usuario_especialista,

                GROUP_CONCAT(
                    DISTINCT ts.nombre_servicio
                    SEPARATOR ' | '
                ) AS servicios,

                GROUP_CONCAT(
                    DISTINCT ts.precio
                    SEPARATOR ' | '
                ) AS precios,

                r.rol AS rol_usuario

            FROM sac.servicio s

            INNER JOIN seguridad.usuario u
                ON s.cedula = u.cedula

            INNER JOIN sac.especialista e
                ON s.cedula_especialista = e.cedula_especialista

            LEFT JOIN seguridad.usuario u2
                ON u2.cedula = e.cedula_especialista

            LEFT JOIN sac.detalle_servicio ds
                ON ds.cod_servicio = s.cod_servicio

            LEFT JOIN sac.tipo_servicio ts
                ON ds.cod_tipo_servicio = ts.cod_tipo_servicio

            LEFT JOIN seguridad.usuario su
                ON su.cedula = u.cedula

            LEFT JOIN seguridad.rol r
                ON su.cod_rol = r.cod_rol

            WHERE s.status IN (0, 1)
        """

        parametros = []

        if fecha_inicio and fecha_fin:
            sql += """
                AND s.fecha BETWEEN %s AND %s
            """
            parametros.extend([
                fecha_inicio,
                fecha_fin
            ])

        elif fecha_inicio:
            sql += """
                AND s.fecha >= %s
            """
            parametros.append(fecha_inicio)

        elif fecha_fin:
            sql += """
                AND s.fecha <= %s
            """
            parametros.append(fecha_fin)

        sql += """
            GROUP BY
                s.cod_servicio,
                u.cedula,
                e.cedula_especialista,
                r.rol,
                s.fecha,
                s.hora,
                s.status,
                e.especialista,
                u2.nombre_usuario,
                u2.apellido_usuario

            ORDER BY
                s.fecha ASC,
                s.hora ASC
        """

        cursor.execute(sql, parametros)

        resultados = cursor.fetchall()

        cursor.close()

        return resultados


    def consultar_especialistas(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                e.cedula_especialista,
                e.especialista,
                e.status,
                u.nombre_usuario,
                u.apellido_usuario
            FROM sac.especialista e
            INNER JOIN seguridad.usuario u
                ON u.cedula = e.cedula_especialista
            WHERE e.status = 1
        """)

        resultados = cursor.fetchall()

        print(resultados)  

        cursor.close()
        return resultados
    


    def consultarEspecialista(self, cedula_especialista=None):

        cursor = self.conexion.cursor(dictionary=True)

        sql = """
            SELECT
                s.cod_servicio,
                s.fecha AS fecha_reserva,
                s.hora AS hora_reserva,
                s.status AS estado_reserva,

                u.cedula AS cedula_cliente,
                u.nombre_usuario AS nombre_cliente,
                u.apellido_usuario AS apellido_cliente,

                e.cedula_especialista,
                e.especialista AS nombre_especialista,

                servicios.servicios,
                servicios.precios,

                r.rol AS rol_usuario

            FROM sac.servicio s

            INNER JOIN seguridad.usuario u
                ON s.cedula = u.cedula

            INNER JOIN sac.especialista e
                ON s.cedula_especialista = e.cedula_especialista

            LEFT JOIN seguridad.rol r
                ON u.cod_rol = r.cod_rol

            LEFT JOIN (
                SELECT
                    ds.cod_servicio,

                    GROUP_CONCAT(
                        DISTINCT ts.nombre_servicio
                        SEPARATOR ' | '
                    ) AS servicios,

                    GROUP_CONCAT(
                        DISTINCT ts.precio
                        SEPARATOR ' | '
                    ) AS precios

                FROM sac.detalle_servicio ds

                INNER JOIN sac.tipo_servicio ts
                    ON ds.cod_tipo_servicio = ts.cod_tipo_servicio

                GROUP BY ds.cod_servicio

            ) AS servicios
                ON servicios.cod_servicio = s.cod_servicio
        """

        parametros = []

        if cedula_especialista:
            sql += """
                WHERE s.cedula_especialista = %s
            """
            parametros.append(cedula_especialista)

        sql += """
            ORDER BY
                s.fecha ASC,
                s.hora ASC
        """

        cursor.execute(sql, parametros)

        datos = cursor.fetchall()

        cursor.close()

        return datos


    def consultar_clientes(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                u.cedula,
                u.nombre_usuario,
                u.apellido_usuario
            FROM seguridad.usuario u
            INNER JOIN seguridad.rol r
                ON r.cod_rol = u.cod_rol
            WHERE u.status = 1
            AND LOWER(r.rol) LIKE 'cliente%'
        """)

        resultados = cursor.fetchall()

        print(resultados)

        cursor.close()

        return resultados
    

    def consultar_especialistasreporte(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                e.cedula_especialista,
                e.especialista,
                u.nombre_usuario,
                u.apellido_usuario
            FROM sac.especialista e
            INNER JOIN seguridad.usuario u
                ON u.cedula = e.cedula_especialista
            WHERE e.status = 1
            AND u.status = 1
            AND e.especialista IN ('Manicurista', 'Estilista')
        """)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    
    def consultar_reporte_especialista(self, cedula_especialista):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                e.cedula_especialista,
                u.nombre_usuario,
                u.apellido_usuario,
                e.especialista
            FROM sac.especialista e
            INNER JOIN seguridad.usuario u
                ON u.cedula = e.cedula_especialista
            WHERE e.cedula_especialista = %s
            AND e.status = 1
            AND u.status = 1
        """, (cedula_especialista,))

        especialista = cursor.fetchone()

        if not especialista:
            cursor.close()
            return None

        cursor.execute("""
            SELECT
                COUNT(DISTINCT s.cod_servicio) AS total_reservas
            FROM sac.servicio s
            WHERE s.cedula_especialista = %s
            AND s.status IN (0, 1)
        """, (cedula_especialista,))

        resultado = cursor.fetchone()

        especialista["total_reservas"] = (
            resultado["total_reservas"]
            if resultado
            else 0
        )

        cursor.execute("""
            SELECT
                CONCAT(
                    u.nombre_usuario,
                    ' ',
                    u.apellido_usuario
                ) AS cliente,
                COUNT(DISTINCT s.cod_servicio) AS cantidad
            FROM sac.servicio s
            INNER JOIN seguridad.usuario u
                ON u.cedula = s.cedula
            WHERE s.cedula_especialista = %s
            AND s.status IN (0, 1)
            GROUP BY
                s.cedula,
                u.nombre_usuario,
                u.apellido_usuario
            ORDER BY
                cantidad DESC,
                cliente ASC
            LIMIT 1
        """, (cedula_especialista,))

        resultado = cursor.fetchone()

        especialista["cliente_mas_atendido"] = (
            resultado["cliente"]
            if resultado
            else "No disponible"
        )

        cursor.execute("""
            SELECT
                TRIM(ts.nombre_servicio) AS servicio,
                COUNT(DISTINCT s.cod_servicio) AS cantidad
            FROM sac.servicio s
            INNER JOIN sac.detalle_servicio ds
                ON ds.cod_servicio = s.cod_servicio
            INNER JOIN sac.tipo_servicio ts
                ON ts.cod_tipo_servicio = ds.cod_tipo_servicio
            WHERE s.cedula_especialista = %s
            AND s.status IN (0, 1)
            GROUP BY
                ts.cod_tipo_servicio,
                ts.nombre_servicio
            ORDER BY
                cantidad DESC,
                ts.nombre_servicio ASC
            LIMIT 1
        """, (cedula_especialista,))

        resultado = cursor.fetchone()

        especialista["servicio_mas_solicitado"] = (
            resultado["servicio"]
            if resultado
            else "No disponible"
        )

        cursor.execute("""
            SELECT
                s.cod_servicio,
                CONCAT(
                    u.nombre_usuario,
                    ' ',
                    u.apellido_usuario
                ) AS cliente,
                DATE_FORMAT(
                    s.fecha,
                    '%d/%m/%Y'
                ) AS fecha,
                s.hora,
                CASE
                    WHEN p.cod_promo IS NOT NULL THEN
                        CONCAT(
                            p.nombre_promo,
                            ' (',
                            p.descuento,
                            '% descuento)'
                        )
                    ELSE
                        'NO'
                END AS promocion,
                GROUP_CONCAT(
                    DISTINCT CONCAT(
                        TRIM(ts.nombre_servicio),
                        '###',
                        FORMAT(ts.precio, 2)
                    )
                    ORDER BY TRIM(ts.nombre_servicio)
                    SEPARATOR '@@'
                ) AS servicios_precios,
                (
                    SELECT
                        COALESCE(
                            SUM(ts2.precio),
                            0
                        )
                    FROM (
                        SELECT DISTINCT
                            cod_servicio,
                            cod_tipo_servicio
                        FROM sac.detalle_servicio
                    ) ds2
                    INNER JOIN sac.tipo_servicio ts2
                        ON ts2.cod_tipo_servicio = ds2.cod_tipo_servicio
                    WHERE ds2.cod_servicio = s.cod_servicio
                    GROUP BY ds2.cod_servicio
                ) AS total
            FROM sac.servicio s
            INNER JOIN seguridad.usuario u
                ON u.cedula = s.cedula
            INNER JOIN sac.detalle_servicio ds
                ON ds.cod_servicio = s.cod_servicio
            INNER JOIN sac.tipo_servicio ts
                ON ts.cod_tipo_servicio = ds.cod_tipo_servicio
            LEFT JOIN sac.promocion p
                ON p.cod_promo = s.cod_promo
            WHERE s.cedula_especialista = %s
            AND s.status IN (0, 1)
            GROUP BY
                s.cod_servicio,
                u.nombre_usuario,
                u.apellido_usuario,
                s.fecha,
                s.hora,
                p.cod_promo,
                p.nombre_promo,
                p.descuento
            ORDER BY
                s.fecha DESC,
                s.hora DESC
        """, (cedula_especialista,))

        especialista["reservas"] = cursor.fetchall()

        cursor.close()

        return especialista