from admin.config.conexion import Conexion


class PanelModelo(Conexion):

    def __init__(self):
        super().__init__()


    def consultar_clientes_activos(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute(
            """SELECT * FROM seguridad.vista_clientes_activos"""
        )

        resultado = cursor.fetchone()

        cursor.close()

        return resultado


    def consultar_total_reservas_activas(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute(
            """SELECT * FROM vista_total_reservas_activas"""
        )

        resultado = cursor.fetchone()

        cursor.close()

        return resultado


    def reservas_por_dia(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM vista_reservas_por_dia
        """)

        datos = cursor.fetchall()

        cursor.close()

        return datos


    def reservas_por_mes(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM vista_reservas_por_mes
        """)

        datos = cursor.fetchall()

        cursor.close()

        return datos



    def reservas_por_hora(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM vista_reservas_por_hora
        """)

        datos = cursor.fetchall()

        cursor.close()

        return datos       
    



    def ingresos_por_mes(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM vista_ingresos_mes
        """)

        datos = cursor.fetchall()

        cursor.close()

        return datos



    def ingresos_por_dia(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM vista_ingresos_dia
        """)

        datos = cursor.fetchall()

        cursor.close()

        return datos    



    def servicios_populares(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                CASE
                    WHEN DAY(s.fecha) BETWEEN 1 AND 15 THEN 'Primera quincena'
                    ELSE 'Segunda quincena'
                END AS quincena,
                ts.nombre_servicio,
                COUNT(DISTINCT ds.cod_servicio) AS cantidad_reservas
            FROM sac.detalle_servicio ds
            INNER JOIN sac.tipo_servicio ts
                ON ds.cod_tipo_servicio = ts.cod_tipo_servicio
            INNER JOIN sac.servicio s
                ON ds.cod_servicio = s.cod_servicio
            WHERE s.status = 1
                AND MONTH(s.fecha) = MONTH(CURDATE())
                AND YEAR(s.fecha) = YEAR(CURDATE())
            GROUP BY
                CASE
                    WHEN DAY(s.fecha) BETWEEN 1 AND 15 THEN 'Primera quincena'
                    ELSE 'Segunda quincena'
                END,
                ts.cod_tipo_servicio,
                ts.nombre_servicio
            HAVING COUNT(DISTINCT ds.cod_servicio) >= 2
            ORDER BY
                CASE
                    WHEN DAY(s.fecha) BETWEEN 1 AND 15 THEN 1
                    ELSE 2
                END,
                cantidad_reservas DESC
        """)
        datos = cursor.fetchall()
        cursor.close()
        return datos





    def productos_stock(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                nombre_producto,
                stock
            FROM producto
            WHERE status = 1
                AND stock >= 50
            ORDER BY stock DESC
        """)

        datos = cursor.fetchall()

        cursor.close()

        return datos        