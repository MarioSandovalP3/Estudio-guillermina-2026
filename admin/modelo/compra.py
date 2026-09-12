from admin.config.conexion import Conexion
import json
import re
from datetime import datetime


class CompraModelo(Conexion):

    def __init__(self):
        super().__init__()
        self.ultimo_error = None

        self.__cod_compra = None
        self.__fecha_compra = None
        self.__total = None
        self.__cod_proveedor = None
        self.__status = None

    def conn(self):
        try:
            if self.conexion is None or not self.conexion.is_connected():
                self.conexion.reconnect()
        except:
            self.conexion.reconnect()

        return self.conexion
        # =========================
    # VALIDACIONES
    # =========================

    def validarFechaCompra(self, fecha):

        if not fecha or fecha.strip() == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Fecha requerida",
                "text": "Debe ingresar la fecha de compra."
            }


        try:

            fecha_compra = datetime.strptime(
                fecha,
                "%Y-%m-%d"
            )


        except:

            return {
                "status": False,
                "icon": "warning",
                "title": "Fecha inválida",
                "text": "La fecha de compra no tiene un formato válido."
            }


        return {
            "status": True
        }



    def validarProveedor(self, cod_proveedor):

        if not cod_proveedor:

            return {
                "status": False,
                "icon": "warning",
                "title": "Proveedor requerido",
                "text": "Debe seleccionar un proveedor."
            }


        try:

            cod_proveedor = int(cod_proveedor)


        except:

            return {
                "status": False,
                "icon": "warning",
                "title": "Proveedor inválido",
                "text": "El proveedor seleccionado no es válido."
            }


        return {
            "status": True
        }




    def validarTotal(self, total):

        try:

            total = float(total)


        except:

            return {
                "status": False,
                "icon": "warning",
                "title": "Total inválido",
                "text": "El total debe ser un valor numérico."
            }



        if total <= 0:

            return {
                "status": False,
                "icon": "warning",
                "title": "Total inválido",
                "text": "El total debe ser mayor que cero."
            }



        return {
            "status": True
        }




    def validarProductos(self, productos):

        if not productos or len(productos) == 0:

            return {
                "status": False,
                "icon": "warning",
                "title": "Productos requeridos",
                "text": "Debe agregar al menos un producto a la compra."
            }



        for producto in productos:


            if not producto:

                continue


            cantidad = int(
                producto.get("cantidad",0) or 0
            )


            precio = float(
                producto.get("precio",0) or 0
            )



            if cantidad <= 0:

                return {
                    "status": False,
                    "icon": "warning",
                    "title": "Cantidad inválida",
                    "text": "La cantidad de los productos debe ser mayor que cero."
                }



            if precio <= 0:

                return {
                    "status": False,
                    "icon": "warning",
                    "title": "Precio inválido",
                    "text": "El precio de los productos debe ser mayor que cero."
                }



        return {
            "status": True
        }


    # =========================
    # PROPIEDADES
    # =========================
    @property
    def cod_compra(self):
        return self.__cod_compra

    @cod_compra.setter
    def cod_compra(self, v):
        self.__cod_compra = v

    @property
    def fecha_compra(self):
        return self.__fecha_compra

    @fecha_compra.setter
    def fecha_compra(self, v):
        self.__fecha_compra = v

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, v):
        self.__total = v

    @property
    def cod_proveedor(self):
        return self.__cod_proveedor

    @cod_proveedor.setter
    def cod_proveedor(self, v):
        self.__cod_proveedor = v

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, v):
        self.__status = v

    # =========================
    # CONSULTAR
    # =========================
    def consultar(self):

        cursor = self.conn().cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                c.cod_compra,
                c.fecha_compra,
                c.total,
                c.status,
                CONCAT(p.nombre, ' ', p.apellido) AS proveedor,
                COALESCE(
                    GROUP_CONCAT(
                        DISTINCT CONCAT(dp.cantidad, 'x ', pr.nombre_producto)
                        SEPARATOR ', '
                    ),
                    'Sin productos'
                ) AS productos
            FROM compra c
            INNER JOIN proveedor p ON c.cod_proveedor = p.cod_proveedor
            LEFT JOIN detalle_compra dp ON c.cod_compra = dp.cod_compra
            LEFT JOIN producto pr ON dp.cod_producto = pr.cod_producto
            GROUP BY c.cod_compra, c.fecha_compra, c.total, c.status, proveedor
            ORDER BY c.cod_compra DESC
        """)

        datos = cursor.fetchall()
        cursor.close()

        return datos

    # =========================
    # OBTENER
    # =========================
    def obtener(self, cod):

        cursor = self.conn().cursor(dictionary=True)

        cursor.execute("""
            SELECT
                c.cod_compra,
                c.fecha_compra,
                c.total,
                c.cod_proveedor,
                c.status,
                CONCAT(p.nombre, ' ', p.apellido) AS proveedor,
                p.rif AS rif
            FROM compra c
            INNER JOIN proveedor p ON c.cod_proveedor = p.cod_proveedor
            WHERE c.cod_compra = %s
        """, (cod,))

        datos = cursor.fetchone()
        cursor.close()

        return datos

    def obtener_detalle_compra(self, cod_compra):

        cursor = self.conn().cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                dc.cod_producto,
                dc.cantidad,
                dc.precio_unitario,
                p.nombre_producto,
                p.precio_producto,
                m.nombre_marca AS marca,
                c.nombre_categoria AS categoria,
                tp.nombre_tipo_producto AS tipo
            FROM detalle_compra dc
            INNER JOIN producto p ON dc.cod_producto = p.cod_producto
            LEFT JOIN marca m ON p.cod_marca = m.cod_marca
            LEFT JOIN categoria c ON p.cod_categoria = c.cod_categoria
            LEFT JOIN detalle_producto dp ON p.cod_producto = dp.cod_producto
            LEFT JOIN tipo_producto tp ON dp.cod_tipo_producto = tp.cod_tipo_producto
            WHERE dc.cod_compra = %s
        """, (cod_compra,))

        datos = cursor.fetchall()
        cursor.close()

        return datos

    # =========================
    # REGISTRAR COMPRA
    # =========================
    def registrar(self):

        try:
            conn = self.conn()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO compra (
                    fecha_compra,
                    total,
                    cod_proveedor,
                    status
                )
                VALUES (%s, %s, %s, 1)
            """, (
                self.__fecha_compra,
                self.__total,
                self.__cod_proveedor
            ))

            cod_compra = cursor.lastrowid

            conn.commit()
            cursor.close()

            return cod_compra

        except Exception as e:
            self.conn().rollback()
            print("ERROR REGISTRAR COMPRA:", repr(e))
            return 0

    # =========================
    # REGISTRAR DETALLE
    # =========================
    def registrar_detalle(self, cod_compra, productos):

        try:
            conn = self.conn()
            cursor = conn.cursor()

            for p in productos:
                if not p:
                    continue

                cod_producto = int(p.get("cod_producto", 0) or 0)
                cantidad = int(p.get("cantidad", 0) or 0)
                precio = float(p.get("precio", 0) or 0)

                if cod_producto <= 0 or cantidad <= 0:
                    continue

                cursor.execute("""
                    INSERT INTO detalle_compra (
                        cod_compra,
                        cod_producto,
                        cantidad,
                        precio_unitario
                    )
                    VALUES (%s, %s, %s, %s)
                """, (
                    cod_compra,
                    cod_producto,
                    cantidad,
                    precio
                ))

            conn.commit()
            cursor.close()

            return 1

        except Exception as e:
            self.conn().rollback()
            print("ERROR DETALLE COMPRA:", repr(e))
            return 0

    def registrar_completa(self, fecha_compra, cod_proveedor, productos, cedula=None):
        try:
            self.ultimo_error = None
            conn = self.conn()
            cursor = conn.cursor()
            detalles = [
                {
                    "cod_producto": int(producto.get("cod_producto", 0) or 0),
                    "cantidad": int(producto.get("cantidad", 0) or 0),
                    "precio_unitario": float(
                        producto.get("precio_unitario", producto.get("precio", 0)) or 0
                    )
                }
                for producto in productos
                if producto
            ]
            argumentos = (
                fecha_compra,
                int(cod_proveedor),
                json.dumps(detalles),
                cedula,
                None
            )
            resultado = cursor.callproc(
                "sp_registrar_compra_completa",
                argumentos
            )
            cursor.close()
            return resultado[-1]
        except Exception as e:
            self.conn().rollback()
            self.ultimo_error = str(e)
            print("ERROR REGISTRAR COMPRA COMPLETA:", repr(e))
            return 0

    # =========================
    # EDITAR COMPRA
    # =========================
    def editar(self, cod_compra, productos):

        try:
            conn = self.conn()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT cod_producto, cantidad
                FROM detalle_compra
                WHERE cod_compra = %s
            """, (cod_compra,))
            detalle_actual = cursor.fetchall()

            for item in detalle_actual:
                cursor.execute("""
                    UPDATE producto
                    SET stock = stock - %s
                    WHERE cod_producto = %s
                """, (item[1], item[0]))

            cursor.execute("""
                DELETE FROM detalle_compra
                WHERE cod_compra = %s
            """, (cod_compra,))

            cursor.execute("""
                UPDATE compra
                SET fecha_compra = %s,
                    total = %s,
                    cod_proveedor = %s,
                    status = %s
                WHERE cod_compra = %s
            """, (
                self.__fecha_compra,
                self.__total,
                self.__cod_proveedor,
                self.__status,
                cod_compra
            ))

            for p in productos:
                if not p:
                    continue

                cod_producto = int(p.get("cod_producto", 0) or 0)
                cantidad = int(p.get("cantidad", 0) or 0)
                precio = float(p.get("precio", 0) or 0)

                if cod_producto <= 0 or cantidad <= 0:
                    continue

                cursor.execute("""
                    INSERT INTO detalle_compra (
                        cod_compra,
                        cod_producto,
                        cantidad,
                        precio_unitario
                    )
                    VALUES (%s, %s, %s, %s)
                """, (
                    cod_compra,
                    cod_producto,
                    cantidad,
                    precio
                ))

                cursor.execute("""
                    UPDATE producto
                    SET stock = stock + %s
                    WHERE cod_producto = %s
                """, (cantidad, cod_producto))

            conn.commit()
            cursor.close()

            return 1

        except Exception as e:
            self.conn().rollback()
            print("ERROR EDITAR COMPRA:", repr(e))
            return 0

    # =========================
    # CANCELAR COMPRA
    # =========================
    def eliminar(self, cod, cedula=None):

        try:
            conn = self.conn()
            cursor = conn.cursor()
            cursor.callproc(
                "sp_cancelar_compra",
                (int(cod), cedula)
            )
            cursor.close()

            return "cancelado"

        except Exception as e:
            self.conn().rollback()
            print("ERROR CANCELAR COMPRA:", repr(e))
            return "error"

    # =========================
    # SELECT PROVEEDORES
    # =========================
    def listar_proveedores(self):

        cursor = self.conn().cursor(dictionary=True)
        cursor.execute("""
            SELECT cod_proveedor, nombre, apellido
            FROM proveedor
            WHERE status = 1
        """)
        datos = cursor.fetchall()
        cursor.close()
        return datos

    # =========================
    # SELECT PRODUCTOS
    # =========================
    def listar_productos(self):

        cursor = self.conn().cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                p.cod_producto,
                p.nombre_producto,
                p.precio_producto,
                m.nombre_marca AS marca,
                c.nombre_categoria AS categoria,
                tp.nombre_tipo_producto AS tipo
            FROM producto p
            LEFT JOIN marca m ON p.cod_marca = m.cod_marca
            LEFT JOIN categoria c ON p.cod_categoria = c.cod_categoria
            LEFT JOIN detalle_producto dp ON p.cod_producto = dp.cod_producto
            LEFT JOIN tipo_producto tp ON dp.cod_tipo_producto = tp.cod_tipo_producto
            WHERE p.status = 1
            GROUP BY p.cod_producto, p.nombre_producto, p.precio_producto, m.nombre_marca, c.nombre_categoria, tp.nombre_tipo_producto
        """)
        datos = cursor.fetchall()
        cursor.close()
        return datos