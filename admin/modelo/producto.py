from admin.config.conexion import Conexion
import re
from datetime import datetime


class ProductoModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_producto = None
        self.__nombre_producto = None
        self.__precio_producto = None
        self.__stock = None

        self.__cod_categoria = None
        self.__cod_marca = None
        self.__cod_unidad = None
        self.__cod_presentacion = None
        self.__cod_medida = None

        self.__fecha_vencimiento = None
        self.__cod_tipo_producto = None

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

    def validarNombreProducto(self, nombre):

        nombre = str(nombre).strip()


        if nombre == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el nombre del producto."
            }


        # Permite letras, números, espacios y algunos caracteres comunes
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s\-\.]+$', nombre):

            return {
                "status": False,
                "icon": "warning",
                "title": "Nombre inválido",
                "text": "El nombre del producto contiene caracteres no permitidos."
            }


        return {
            "status": True
        }



    def validarPrecio(self, precio):

        precio = str(precio).strip()


        if precio == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el precio del producto."
            }



        if not re.match(r'^\d+(\.\d{1,2})?$', precio):

            return {
                "status": False,
                "icon": "warning",
                "title": "Precio inválido",
                "text": "El precio debe ser un número válido con máximo 2 decimales."
            }



        if float(precio) <= 0:

            return {
                "status": False,
                "icon": "warning",
                "title": "Precio inválido",
                "text": "El precio debe ser mayor a cero."
            }


        return {
            "status": True
        }




    def validarStock(self, stock):

        stock = str(stock).strip()


        if stock == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el stock del producto."
            }



        if not stock.isdigit():

            return {
                "status": False,
                "icon": "warning",
                "title": "Stock inválido",
                "text": "El stock debe contener solamente números."
            }



        return {
            "status": True
        }




    def validarSelects(self, cod_categoria, cod_marca, cod_unidad, cod_presentacion, cod_medida, cod_tipo_producto):


        campos = [
            cod_categoria,
            cod_marca,
            cod_unidad,
            cod_tipo_producto
        ]


        if any(campo is None or str(campo) == "" for campo in campos):

            return {
                "status": False,
                "icon": "warning",
                "title": "Datos incompletos",
                "text": "Debe seleccionar todos los datos del producto."
            }


        return {
            "status": True
        }




    def validarFechaVencimiento(self, fecha):


        if not fecha:

            return {
                "status": False,
                "icon": "warning",
                "title": "Fecha requerida",
                "text": "Debe ingresar la fecha de vencimiento."
            }



        try:

            fecha_convertida = datetime.strptime(
                fecha,
                "%Y-%m-%d"
            )


            if fecha_convertida.date() < datetime.now().date():

                return {
                    "status": False,
                    "icon": "warning",
                    "title": "Fecha vencida",
                    "text": "La fecha de vencimiento no puede ser anterior a la fecha actual."
                }



        except:

            return {
                "status": False,
                "icon": "warning",
                "title": "Fecha inválida",
                "text": "La fecha de vencimiento no tiene un formato válido."
            }



        return {
            "status": True
        }
    # =========================
    # PROPIEDADES
    # =========================
    @property
    def cod_producto(self):
        return self.__cod_producto

    @cod_producto.setter
    def cod_producto(self, v):
        self.__cod_producto = v

    @property
    def nombre_producto(self):
        return self.__nombre_producto

    @nombre_producto.setter
    def nombre_producto(self, v):
        self.__nombre_producto = v

    @property
    def precio_producto(self):
        return self.__precio_producto

    @precio_producto.setter
    def precio_producto(self, v):
        self.__precio_producto = v

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, v):
        self.__stock = v

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, v):
        self.__status = v

    # =========================
    # SETTERS FALTANTES
    # =========================
    @property
    def cod_categoria(self):
        return self.__cod_categoria

    @cod_categoria.setter
    def cod_categoria(self, v):
        self.__cod_categoria = v

    @property
    def cod_marca(self):
        return self.__cod_marca

    @cod_marca.setter
    def cod_marca(self, v):
        self.__cod_marca = v

    @property
    def cod_unidad(self):
        return self.__cod_unidad

    @cod_unidad.setter
    def cod_unidad(self, v):
        self.__cod_unidad = v

    @property
    def cod_presentacion(self):
        return self.__cod_presentacion

    @cod_presentacion.setter
    def cod_presentacion(self, v):
        self.__cod_presentacion = v

    @property
    def cod_medida(self):
        return self.__cod_medida

    @cod_medida.setter
    def cod_medida(self, v):
        self.__cod_medida = v

    @property
    def fecha_vencimiento(self):
        return self.__fecha_vencimiento

    @fecha_vencimiento.setter
    def fecha_vencimiento(self, v):
        self.__fecha_vencimiento = v

    @property
    def cod_tipo_producto(self):
        return self.__cod_tipo_producto

    @cod_tipo_producto.setter
    def cod_tipo_producto(self, v):
        self.__cod_tipo_producto = v

    # =========================
    # CONSULTAR (SEGURA)
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
                p.cod_categoria,
                p.cod_marca,
                p.cod_unidad,
                dp.fecha_vencimiento,
                dp.cod_tipo_producto,

                m.nombre_marca,
                c.nombre_categoria,
                u.nombre_unidad,
                u.cod_presentacion AS cod_presentacion,
                u.cod_medida AS cod_medida,
                pr.presentacion AS nombre_presentacion,
                me.medida AS nombre_medida,
                tp.nombre_tipo_producto

            FROM producto p

            INNER JOIN marca m ON p.cod_marca = m.cod_marca
            INNER JOIN categoria c ON p.cod_categoria = c.cod_categoria
            INNER JOIN unidad u ON p.cod_unidad = u.cod_unidad
            LEFT JOIN presentacion pr ON u.cod_presentacion = pr.cod_presentacion
            LEFT JOIN medida me ON u.cod_medida = me.cod_medida
            LEFT JOIN detalle_producto dp ON p.cod_producto = dp.cod_producto
            LEFT JOIN tipo_producto tp ON dp.cod_tipo_producto = tp.cod_tipo_producto

            ORDER BY p.cod_producto DESC
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
            SELECT p.*, dp.fecha_vencimiento, dp.cod_tipo_producto
            FROM producto p
            LEFT JOIN detalle_producto dp ON p.cod_producto = dp.cod_producto
            WHERE p.cod_producto = %s
        """, (cod,))

        datos = cursor.fetchone()
        cursor.close()

        return datos

    # =========================
    # BUSCAR 
    # =========================
    def buscar(self, nombre):

        cursor = self.conn().cursor(dictionary=True)

        cursor.execute("""
            SELECT cod_producto, nombre_producto
            FROM producto
            WHERE nombre_producto = %s
        """, (nombre,))

        datos = cursor.fetchone()
        cursor.close()

        return datos

    # =========================
    # REGISTRAR 
    # =========================
    def registrar(self):

        try:
            conn = self.conn()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO producto (
                    nombre_producto,
                    precio_producto,
                    stock,
                    cod_categoria,
                    cod_marca,
                    cod_unidad,
                    status
                )
                VALUES (%s,%s,%s,%s,%s,%s,1)
            """, (
                self.__nombre_producto,
                self.__precio_producto,
                self.__stock,
                self.__cod_categoria,
                self.__cod_marca,
                self.__cod_unidad
            ))

            cod_producto = cursor.lastrowid

            cursor.execute("""
                INSERT INTO detalle_producto (
                    fecha_vencimiento,
                    cod_producto,
                    cod_tipo_producto
                )
                VALUES (%s,%s,%s)
            """, (
                self.__fecha_vencimiento,
                cod_producto,
                self.__cod_tipo_producto
            ))

            conn.commit()
            cursor.close()

            return 1

        except Exception as e:
            self.conn().rollback()
            print(" ERROR MYSQL COMPLETO:", repr(e))
            return 0

    # =========================
    # EDITAR
    # =========================
    def editar(self):

        try:
            conn = self.conn()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE producto
                SET nombre_producto=%s,
                    precio_producto=%s,
                    stock=%s,
                    cod_categoria=%s,
                    cod_marca=%s,
                    cod_unidad=%s,
                    status=%s
                WHERE cod_producto=%s
            """, (
                self.__nombre_producto,
                self.__precio_producto,
                self.__stock,
                self.__cod_categoria,
                self.__cod_marca,
                self.__cod_unidad,
                self.__status,
                self.__cod_producto
            ))

            cursor.execute("""
                UPDATE detalle_producto
                SET fecha_vencimiento=%s,
                    cod_tipo_producto=%s
                WHERE cod_producto=%s
            """, (
                self.__fecha_vencimiento,
                self.__cod_tipo_producto,
                self.__cod_producto
            ))

            conn.commit()
            cursor.close()

            return 1

        except Exception as e:
            self.conn().rollback()
            print("ERROR EDITAR:", repr(e))
            return 0

    # =========================
    # ELIMINAR
    # =========================
    def eliminar(self, cod):

        try:
            cursor = self.conn().cursor()

            cursor.execute("""
                DELETE FROM producto
                WHERE cod_producto = %s
            """, (cod,))

            self.conn().commit()
            cursor.close()

            return "eliminado"

        except Exception as e:
            print(" ERROR ELIMINAR:", repr(e))
            return "error"

    # =========================
    # COMBOS
    # =========================
    def listar_categorias(self):
        cursor = self.conn().cursor(dictionary=True)
        cursor.execute("SELECT * FROM categoria WHERE status=1")
        return cursor.fetchall()

    def listar_marcas(self):
        cursor = self.conn().cursor(dictionary=True)
        cursor.execute("SELECT * FROM marca WHERE status=1")
        return cursor.fetchall()

    def listar_unidades(self):
        cursor = self.conn().cursor(dictionary=True)
        cursor.execute("SELECT * FROM unidad WHERE status=1")
        return cursor.fetchall()

    def obtener_relacion_unidad(self, cod_unidad):
        cursor = self.conn().cursor(dictionary=True)
        cursor.execute("""
            SELECT cod_presentacion, cod_medida
            FROM unidad
            WHERE cod_unidad = %s AND status = 1
            LIMIT 1
        """, (cod_unidad,))
        datos = cursor.fetchone()
        cursor.close()
        return datos or {}

    def listar_presentaciones(self):
        cursor = self.conn().cursor(dictionary=True)
        cursor.execute("SELECT * FROM presentacion WHERE status=1")
        return cursor.fetchall()

    def listar_medidas(self):
        cursor = self.conn().cursor(dictionary=True)
        cursor.execute("SELECT * FROM medida WHERE status=1")
        return cursor.fetchall()

    def listar_tipos_producto(self):
        cursor = self.conn().cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipo_producto WHERE status=1")
        return cursor.fetchall()