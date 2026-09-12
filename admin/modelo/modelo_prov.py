from admin.config.conexion import Conexion


class ProductoModelo(Conexion):

    def __init__(self):
        super().__init__()

    def conn(self):
        try:
            if self.conexion is None or not self.conexion.is_connected():
                self.conexion.reconnect()
        except:
            self.conexion.reconnect()

        return self.conexion

    # =========================
    # CONSULTAR PRODUCTOS
    # =========================
    def consultar(self):

        cursor = self.conn().cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                p.cod_producto,
                p.nombre_producto,
                p.precio_producto,
                p.stock,
                p.status,

                m.nombre_marca,
                c.nombre_categoria,
                u.nombre_unidad,
                pr.presentacion,
                me.medida

            FROM producto p
            INNER JOIN marca m ON p.cod_marca = m.cod_marca
            INNER JOIN categoria c ON p.cod_categoria = c.cod_categoria
            INNER JOIN unidad u ON p.cod_unidad = u.cod_unidad
            INNER JOIN presentacion pr ON p.cod_presentacion = pr.cod_presentacion
            INNER JOIN medida me ON p.cod_medida = me.cod_medida

            ORDER BY p.cod_producto DESC
        """)

        datos = cursor.fetchall()
        cursor.close()

        return datos