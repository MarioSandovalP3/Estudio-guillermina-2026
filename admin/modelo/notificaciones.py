from datetime import datetime
from admin.config.conexion import Conexion


class NotificacionesModelo(Conexion):

    def __init__(self):
        super().__init__()

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)

        try:
            fecha_hoy = datetime.now().date()

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM seguridad.usuario
                WHERE cod_rol = 3
                AND fecha_registro = %s
                AND status = 1
            """, (fecha_hoy,))
            total_clientes = int(cursor.fetchone()["total"] or 0)

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM sac.servicio
                WHERE fecha = %s
                AND status = 1
            """, (fecha_hoy,))
            total_reservas = int(cursor.fetchone()["total"] or 0)

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM sac.compra
                WHERE fecha_compra = %s
                AND status = 1
            """, (fecha_hoy,))
            total_compras = int(cursor.fetchone()["total"] or 0)

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM sac.pago
                WHERE fecha_pago = %s
                AND status = 1
            """, (fecha_hoy,))
            total_pagos = int(cursor.fetchone()["total"] or 0)

            cursor.execute("""
                SELECT cod_producto, nombre_producto, stock
                FROM sac.producto
                WHERE status = 1
                AND stock < 3
                ORDER BY stock ASC, nombre_producto ASC
            """)
            productos_bajo_stock = [
                {
                    "cod_producto": int(producto["cod_producto"]),
                    "nombre_producto": producto["nombre_producto"],
                    "stock": int(producto["stock"] or 0)
                }
                for producto in cursor.fetchall()
            ]

            return {
                "status": True,
                "fecha": str(fecha_hoy),
                "clientes": total_clientes,
                "reservas": [{
                    "fecha": str(fecha_hoy),
                    "total": total_reservas
                }],
                "compras": total_compras,
                "pagos": total_pagos,
                "productos_bajo_stock": productos_bajo_stock
            }

        except Exception as error:
            print("Error al consultar notificaciones:", error)

            return {
                "status": False,
                "fecha": str(datetime.now().date()),
                "clientes": 0,
                "reservas": [],
                "compras": 0,
                "pagos": 0,
                "productos_bajo_stock": []
            }

        finally:
            cursor.close()

    def consultarUltimaCancelacion(self):
        cursor = self.conexion.cursor(dictionary=True)

        try:
            sql = """
                SELECT s.cod_servicio, s.fecha, s.hora,
                       u.nombre_usuario, u.apellido_usuario
                FROM sac.servicio s
                INNER JOIN seguridad.usuario u
                    ON u.cedula = s.cedula
                WHERE s.status = 0
                ORDER BY s.cod_servicio DESC
                LIMIT 1
            """

            cursor.execute(sql)
            resultado = cursor.fetchone()

            if not resultado:
                return None

            return {
                "cod_servicio": int(resultado["cod_servicio"]),
                "fecha": resultado["fecha"].strftime("%Y-%m-%d")
                    if resultado["fecha"] else "",
                "hora": str(resultado["hora"])
                    if resultado["hora"] else "",
                "cliente": f'{resultado["nombre_usuario"]} '
                           f'{resultado["apellido_usuario"]}'.strip()
            }

        except Exception as error:
            print("Error consultando última cancelación:", error)
            return None

        finally:
            cursor.close()

    def consultarCancelacionesHoy(self):
        cursor = self.conexion.cursor(dictionary=True)

        try:
            fecha_hoy = datetime.now().date()

            sql = """
                SELECT s.cod_servicio, s.fecha, s.hora,
                       u.nombre_usuario, u.apellido_usuario
                FROM sac.servicio s
                INNER JOIN seguridad.usuario u
                    ON u.cedula = s.cedula
                WHERE s.status = 0
                AND s.fecha = %s
                ORDER BY s.cod_servicio DESC
            """

            cursor.execute(sql, (fecha_hoy,))
            resultados = cursor.fetchall()

            cancelaciones = []

            for resultado in resultados:
                cancelaciones.append({
                    "cod_servicio": int(resultado["cod_servicio"]),
                    "fecha": resultado["fecha"].strftime("%Y-%m-%d")
                        if resultado["fecha"] else "",
                    "hora": str(resultado["hora"])
                        if resultado["hora"] else "",
                    "cliente": f'{resultado["nombre_usuario"]} '
                               f'{resultado["apellido_usuario"]}'.strip()
                })

            return cancelaciones

        except Exception as error:
            print("Error consultando cancelaciones del día:", error)
            return []

        finally:
            cursor.close()


    def consultarEmpresaRegistrada(self):
        cursor = self.conexion.cursor(dictionary=True)

        try:
            sql = """
                SELECT COUNT(*) AS total
                FROM sac.empresa
            """

            cursor.execute(sql)
            resultado = cursor.fetchone()

            return resultado["total"] > 0

        except Exception as error:
            print("Error verificando empresa registrada:", error)
            return False

        finally:
            cursor.close()
