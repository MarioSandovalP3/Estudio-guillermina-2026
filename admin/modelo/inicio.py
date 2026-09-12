from admin.config.conexion import Conexion

class InicioModelo(Conexion):
    def __init__(self):
        super().__init__()

 # Atributos privados
        self.__cod_reserva = None
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





    def consultarconlientesini(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
                SELECT 
                    s.cod_servicio,
                    s.fecha AS fecha_servicio,
                    s.hora AS hora_servicio,
                    s.status,

                    -- CLIENTE
                    u.cedula,
                    u.nombre_usuario,
                    u.apellido_usuario,

                    -- SERVICIOS SIN DUPLICADOS
                    GROUP_CONCAT(DISTINCT ts.nombre_servicio SEPARATOR ' | ') AS nombre_servicio

                FROM sac.servicio s

                JOIN seguridad.usuario u
                    ON s.cedula = u.cedula

                JOIN sac.detalle_servicio ds
                    ON ds.cod_servicio = s.cod_servicio

                JOIN sac.tipo_servicio ts
                    ON ts.cod_tipo_servicio = ds.cod_tipo_servicio

                WHERE s.status = 1

                GROUP BY 
                    s.cod_servicio,
                    s.fecha,
                    s.hora,
                    s.status,
                    u.cedula,
                    u.nombre_usuario,
                    u.apellido_usuario
        """)

        resultados = cursor.fetchall()
        cursor.close()
        return resultados


    def obtenerServiciosDeReserva(self, cod_servicio):
        cursor = self.conexion.cursor()

        cursor.execute("""
           SELECT 
            GROUP_CONCAT(DISTINCT ts.nombre_servicio SEPARATOR ' | ') AS servicios
        FROM detalle_servicio ds
        INNER JOIN tipo_servicio ts 
            ON ds.cod_tipo_servicio = ts.cod_tipo_servicio
        WHERE ds.cod_servicio = %s
        """, (cod_servicio,))

        resultados = cursor.fetchall()
        cursor.close()

     
        return [r[0] for r in resultados]
    
    def obtenerservicios(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                cod_tipo_servicio,
                nombre_servicio,
                precio
            FROM tipo_servicio
            WHERE status = 1
        """)

        resultados = cursor.fetchall()

        cursor.close()

        return resultados
    
    def obtenerRoles(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                cod_rol,
                rol
            FROM seguridad.rol
            WHERE rol = 'cliente'
        """)

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
            AND e.status = 1
        """, (tipo,))

        resultados = cursor.fetchall()

        cursor.close()

        return resultados

    def obtenerPromocionesActivas(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                cod_promo,
                descuento,
                nombre_promo,
                descripcion_promo,
                imagen_promo,
                inicio_promo,
                fin_promo
            FROM promocion
            WHERE status = 1
            ORDER BY cod_promo DESC
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados   


    def obtenerProductosDisponibles(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.cod_producto,
                p.nombre_producto,
                p.precio_producto,
                p.stock,
                c.nombre_categoria,
                m.nombre_marca,
                u.nombre_unidad

            FROM sac.producto p
            INNER JOIN sac.categoria c ON p.cod_categoria = c.cod_categoria
            INNER JOIN sac.marca m ON p.cod_marca = m.cod_marca
            INNER JOIN sac.unidad u ON p.cod_unidad = u.cod_unidad

            WHERE p.status = 1
            AND p.stock > 0
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados



    def actualizarStockProductos(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                cod_producto,
                stock
            FROM sac.producto
            WHERE status = 1
        """)

        resultados = cursor.fetchall()

        cursor.close()

        return resultados




    def buscarClientePorNombre(self, nombre):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                cedula,
                nombre_usuario,
                apellido_usuario
            FROM seguridad.usuario
            WHERE CONCAT(nombre_usuario, ' ', apellido_usuario) LIKE %s
            AND status = 1
            LIMIT 10
        """, (f"%{nombre}%",))

        resultados = cursor.fetchall()

        cursor.close()

        return resultados     
    

# ================== REGISTRAR PARA ADMIN ==================

    def registrarReserva(
            self,
            cedula,
            cod_tipos_servicio,
            fecha,
            hora,
            cedula_especialista,
            cod_promo=None,
            cod_productos=None,
            descripcion=None
    ):
        try:

            cursor = self.conexion.cursor()

            # ==========================================================
            # TIPOS DE SERVICIO
            # ==========================================================

            tipos_servicio = ",".join(
                str(cod_tipo)
                for cod_tipo in cod_tipos_servicio
            )

            # ==========================================================
            # PRODUCTOS
            # ==========================================================

            productos = None
            cantidades = None

            if cod_productos:

                productos = ",".join(
                    str(producto["cod_producto"])
                    for producto in cod_productos
                )

                cantidades = ",".join(
                    str(producto["cantidad"])
                    for producto in cod_productos
                )

            # ==========================================================
            # LLAMAR PROCEDIMIENTO
            # ==========================================================

            cursor.callproc(
                "sp_registrar_reserva",
                (
                    cedula,
                    tipos_servicio,
                    fecha,
                    hora,
                    cedula_especialista,
                    cod_promo,
                    productos,
                    cantidades,
                    descripcion
                )
            )

            # ==========================================================
            # OBTENER RESULTADO
            # ==========================================================

            resultado = None

            for result in cursor.stored_results():
                resultado = result.fetchone()

            cursor.close()

            if resultado:

                # ======================================================
                # GUARDAR JSON SOLO SI HAY PRODUCTOS
                # ======================================================

                if cod_productos:

                    self.guardarStockJSON(
                        resultado[0],
                        fecha,
                        cod_productos,
                        resultado[6]
                    )

                return {
                    "success": True,
                    "cod_servicio": resultado[0],
                    "cliente": f"{resultado[1]} {resultado[2]}",
                    "especialista": resultado[3],
                    "fecha": resultado[4],
                    "hora": resultado[5]
                }

            return {
                "success": False,
                "message": "No se pudo registrar la reserva."
            }

        except Exception as e:

            self.conexion.rollback()

            return {
                "success": False,
                "message": str(e)
            }


    # ==============================================================
    # GUARDAR STOCK EN JSON
    # ==============================================================

    def guardarStockJSON(
            self,
            cod_servicio,
            fecha,
            cod_productos,
            cod_conteos
    ):

        import json
        import os
        from flask import current_app

        archivo = os.path.join(
            current_app.root_path,
            "static",
            "assets",
            "js",
            "modulos-js",
            "json-js",
            "reservas_stock.json"
        )

        datos = {}

        if os.path.exists(archivo):

            try:

                with open(
                    archivo,
                    "r",
                    encoding="utf-8"
                ) as f:

                    datos = json.load(f)

            except Exception:

                datos = {}

        conteos = str(cod_conteos).split(",")

        productos = {}

        for i, producto in enumerate(cod_productos or []):

            if i >= len(conteos):
                continue

            productos[str(
                producto["cod_producto"]
            )] = {
                "cantidad": int(
                    producto["cantidad"]
                ),
                "cod_conteo": int(
                    conteos[i]
                )
            }

        datos[str(cod_servicio)] = {
            "fecha": str(fecha),
            "productos": productos
        }

        with open(
            archivo,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                datos,
                f,
                indent=4,
                ensure_ascii=False
            )


    def procesar_reservas_8pm(self):

        import json
        import os
        from datetime import date
        from flask import current_app

        archivo = os.path.join(
            current_app.root_path,
            "static",
            "assets",
            "js",
            "modulos-js",
            "json-js",
            "reservas_stock.json"
        )

        if not os.path.exists(archivo):
            return []

        try:

            with open(
                archivo,
                "r",
                encoding="utf-8"
            ) as f:

                datos = json.load(f)

        except Exception as error:

            print(
                "Error leyendo reservas_stock.json:",
                error
            )

            return []

        cursor = self.conexion.cursor(
            dictionary=True
        )

        procesadas = []

        try:

         
            for cod_servicio, reserva in datos.items():

                if str(
                    reserva.get("fecha")
                ) != str(
                    date.today()
                ):
                    continue

                # ======================================================
                # BUSCAR RESERVA ACTIVA
                # ======================================================

                cursor.execute("""
                    SELECT
                        s.cod_servicio,
                        s.fecha,
                        s.hora,
                        u.nombre_usuario,
                        u.apellido_usuario
                    FROM sac.servicio s
                    INNER JOIN seguridad.usuario u
                        ON u.cedula = s.cedula
                    WHERE s.cod_servicio = %s
                    AND s.fecha = CURDATE()
                    AND s.status = 1
                """, (cod_servicio,))

                resultado = cursor.fetchone()

                if not resultado:
                    continue

                # ======================================================
                # VERIFICAR PAGO
                # ======================================================

                cursor.execute("""
                    SELECT COUNT(*) AS total
                    FROM sac.pago
                    WHERE cod_servicio = %s
                    AND status = 1
                """, (cod_servicio,))

                pago = cursor.fetchone()

                if pago["total"] > 0:
                    continue

                # ======================================================
                # DEVOLVER PRODUCTOS
                # ======================================================

                productos = reserva.get(
                    "productos",
                    {}
                )

                productos_devueltos = {}

                for cod_producto, producto in productos.items():

                    cursor.execute("""
                        UPDATE sac.conteo_stock
                        SET status = 0
                        WHERE cod_conteo = %s
                        AND cod_producto = %s
                        AND status = 1
                    """, (
                        producto["cod_conteo"],
                        cod_producto
                    ))

                    if cursor.rowcount == 1:

                        cursor.execute("""
                            UPDATE sac.producto
                            SET stock = stock + %s
                            WHERE cod_producto = %s
                        """, (
                            producto["cantidad"],
                            cod_producto
                        ))

                        productos_devueltos[
                            str(cod_producto)
                        ] = {
                            "cantidad": int(
                                producto["cantidad"]
                            ),
                            "cod_conteo": int(
                                producto["cod_conteo"]
                            )
                        }

                # ======================================================
                # GUARDAR RESERVA PARA EL ALERT
                # ======================================================

                procesadas.append({
                    "cod_servicio": int(
                        resultado["cod_servicio"]
                    ),
                    "fecha": (
                        resultado["fecha"].strftime(
                            "%Y-%m-%d"
                        )
                        if resultado["fecha"]
                        else ""
                    ),
                    "hora": (
                        str(
                            resultado["hora"]
                        )
                        if resultado["hora"]
                        else ""
                    ),
                    "cliente": (
                        f'{resultado["nombre_usuario"]} '
                        f'{resultado["apellido_usuario"]}'
                    ).strip(),
                    "productos": productos_devueltos
                })

            # ==========================================================
            # SI HAY RESERVAS, EJECUTAR PROCEDIMIENTO
            # ==========================================================

            if procesadas:

                cursor.callproc(
                    "sp_procesar_reservas_8pm"
                )

                for result in cursor.stored_results():
                    result.fetchall()

            # ==========================================================
            # CONFIRMAR
            # ==========================================================

            self.conexion.commit()

            return procesadas

        except Exception as error:

            self.conexion.rollback()

            print(
                "Error procesando reservas de las 08:00 PM:",
                error
            )

            return []

        finally:

            cursor.close()


    def horasOcupadas(self, fecha):

        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                SELECT hora
                FROM servicio
                WHERE fecha = %s
                AND status = 1
                ORDER BY hora
            """, (fecha,))

            horas = cursor.fetchall()

            cursor.close()

            return [fila[0] for fila in horas]

        except Exception as e:
            print("Error horasOcupadas:", e)
            return []
                


    def consultarConClientes(self, cedula):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT

                s.cod_servicio,
                s.cod_promo,
                s.fecha AS fecha_reserva,
                s.hora AS hora_reserva,
                s.descripcion,
                s.status AS estado_reserva,

                u.cedula AS cedula_cliente,
                u.nombre_usuario AS nombre_cliente,
                u.apellido_usuario AS apellido_cliente,
                r.rol AS rol_cliente,

                e.cedula_especialista,
                e.especialista,

                ue.nombre_usuario AS nombre_especialista,
                ue.apellido_usuario AS apellido_especialista,

                servicios.servicios,
                servicios.precios

            FROM sac.servicio s

            INNER JOIN seguridad.usuario u
                ON s.cedula = u.cedula

            INNER JOIN seguridad.rol r
                ON u.cod_rol = r.cod_rol

            INNER JOIN sac.especialista e
                ON s.cedula_especialista = e.cedula_especialista

            LEFT JOIN seguridad.usuario ue
                ON ue.cedula = e.cedula_especialista

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

            WHERE s.cedula = %s
            AND s.status IN (0, 1)

            ORDER BY
                s.fecha ASC,
                s.hora ASC

        """, (cedula,))

        resultados = cursor.fetchall()

        cursor.close()

        return resultados


    def sp_Cancelar_Reserva(self, cod_servicio):

        cursor = None

        try:
            cursor = self.conexion.cursor(dictionary=True)
            self.conexion.start_transaction()

            cursor.execute("""
                SELECT fecha, hora, cedula_especialista, status
                FROM sac.servicio
                WHERE cod_servicio = %s
            """, (cod_servicio,))

            reserva = cursor.fetchone()

            if not reserva:
                self.conexion.rollback()
                return "no_existe"

            if reserva["status"] == 0:
                self.conexion.rollback()
                return "ya_cancelado"

            cursor.execute("""
                UPDATE sac.servicio
                SET status = 0
                WHERE cod_servicio = %s
            """, (cod_servicio,))

            cursor.execute("""
                UPDATE sac.disponibilidad_especialista
                SET status = 0
                WHERE fecha_disponibilidad = %s
                AND hora_disponibilidad = %s
                AND cedula_especialista = %s
                AND status = 1
            """, (
                reserva["fecha"],
                reserva["hora"],
                reserva["cedula_especialista"]
            ))

            self.conexion.commit()

            return "cancelado"

        except Exception as e:
            self.conexion.rollback()
            print("Error cancelar reserva:", e)
            return "error"

        finally:
            if cursor:
                cursor.close()


    def registrarReservadeclientes(
        self,
        cedula,
        cod_tipos_servicio,
        fecha,
        hora,
        cedula_especialista,
        cod_promo=None,
        descripcion=None
    ):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                SELECT nombre_usuario, apellido_usuario
                FROM seguridad.usuario
                WHERE cedula=%s
            """, (cedula,))

            cliente = cursor.fetchone()

            if not cliente:
                return {
                    "success": False,
                    "message": "Debe ingresar la cedula de un cliente existente."
                }

            cursor.execute("""
                SELECT especialista
                FROM sac.especialista
                WHERE cedula_especialista=%s
            """, (cedula_especialista,))

            especialista = cursor.fetchone()

            if not especialista:
                return {
                    "success": False,
                    "message": "Debe seleccionar un especialista existente."
                }

            cursor.execute("""
                SELECT cod_servicio
                FROM sac.servicio
                WHERE cedula_especialista=%s
                AND fecha=%s
                AND hora=%s
                AND status IN (0,1)
            """, (
                cedula_especialista,
                fecha,
                hora
            ))

            conflicto_especialista = cursor.fetchone()

            if conflicto_especialista:
                return {
                    "success": False,
                    "message": "El especialista ya tiene una reserva en esa fecha y hora."
                }

            cursor.execute("""
                SELECT cod_servicio
                FROM sac.servicio
                WHERE cedula=%s
                AND fecha=%s
                AND hora=%s
                AND cedula_especialista=%s
                AND status IN (0,1)
            """, (
                cedula,
                fecha,
                hora,
                cedula_especialista
            ))

            cliente_ocupado = cursor.fetchone()

            if cliente_ocupado:
                return {
                    "success": False,
                    "message": "El cliente ya tiene una reserva con ese especialista en esa fecha y hora."
                }

            cursor.execute("""
                INSERT INTO sac.servicio(
                    cod_promo,
                    cedula,
                    descripcion,
                    fecha,
                    hora,
                    status,
                    cedula_especialista
                )
                VALUES(%s,%s,%s,%s,%s,1,%s)
            """, (
                cod_promo,
                cedula,
                descripcion,
                fecha,
                hora,
                cedula_especialista
            ))

            cod_servicio = cursor.lastrowid

            for codTipo in cod_tipos_servicio:

                cursor.execute("""
                    INSERT INTO sac.detalle_servicio(
                        cantidad_servicio,
                        cod_servicio,
                        cod_tipo_servicio,
                        cod_producto
                    )
                    VALUES(%s,%s,%s,NULL)
                """, (
                    1,
                    cod_servicio,
                    codTipo
                ))

            cursor.execute("""
                INSERT INTO sac.disponibilidad_especialista(
                    fecha_disponibilidad,
                    hora_disponibilidad,
                    status,
                    cedula_especialista
                )
                VALUES(%s,%s,1,%s)
            """, (
                fecha,
                hora,
                cedula_especialista
            ))

            self.conexion.commit()

            cursor.close()

            return {
                "success": True,
                "cod_servicio": cod_servicio,
                "cliente": f"{cliente[0]} {cliente[1]}",
                "especialista": especialista[0],
                "fecha": fecha,
                "hora": hora
            }

        except Exception as e:

            self.conexion.rollback()

            return {
                "success": False,
                "message": str(e)
            }