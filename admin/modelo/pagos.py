from admin.config.conexion import Conexion
import os
import re
import datetime
from werkzeug.utils import secure_filename


class PagosModelo(Conexion):
    UPLOAD_FOLDER = "static/assets/uploads/comprobantes"
    PUBLIC_FOLDER = "assets/uploads/comprobantes"

    def __init__(self):
        super().__init__()

        self.__cod_pago = None
        self.__cod_servicio = None
        self.__fecha_pago = None
        self.__monto = None
        self.__status = None
        self.__cod_tipo_pago = None
        self.__cod_moneda = 1
        self.__comprobante_pago = None

    def validarCodServicio(self, cod_servicio=None):
        valor = self.__cod_servicio if cod_servicio is None else cod_servicio
        texto = str(valor).strip() if valor is not None else ""

        if not texto or not re.match(r'^[1-9]\d*$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Servicio no válido."
            }

        return {"status": True, "value": int(texto)}

    def validarFechaPago(self, fecha_pago=None):
        valor = self.__fecha_pago if fecha_pago is None else fecha_pago
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Fecha de pago requerida."
            }

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Formato de fecha inválido (YYYY-MM-DD)."
            }

        try:
            datetime.date.fromisoformat(texto)
        except Exception:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Fecha inválida."
            }

        return {"status": True, "value": texto}

    def validarMonto(self, monto=None):
        valor = self.__monto if monto is None else monto
        texto = str(valor).strip().replace(',', '.') if valor is not None else ""

        if not texto or not re.match(r'^\d+(?:\.\d{1,2})?$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Monto inválido. Use formato 1234.56"
            }

        try:
            monto_float = float(texto)
        except Exception:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Monto inválido."
            }

        if monto_float < 0:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El monto no puede ser negativo."
            }

        return {"status": True, "value": monto_float}

    def validarCodTipoPago(self, cod_tipo_pago=None):
        valor = self.__cod_tipo_pago if cod_tipo_pago is None else cod_tipo_pago
        texto = str(valor).strip() if valor is not None else ""

        if not texto or not re.match(r'^[1-9]\d*$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Tipo de pago no válido."
            }

        return {"status": True, "value": int(texto)}

    def validarCodMoneda(self, cod_moneda=None):
        valor = self.__cod_moneda if cod_moneda is None else cod_moneda
        texto = str(valor).strip() if valor is not None else ""

        if not texto or not re.match(r'^[1-9]\d*$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Moneda no válida."
            }

        return {"status": True, "value": int(texto)}

    @property
    def cod_pago(self):
        return self.__cod_pago

    @cod_pago.setter
    def cod_pago(self, valor):
        self.__cod_pago = valor

    @property
    def cod_servicio(self):
        return self.__cod_servicio

    @cod_servicio.setter
    def cod_servicio(self, valor):
        if valor is None:
            self.__cod_servicio = None
            return
        try:
            self.__cod_servicio = int(valor)
        except Exception:
            self.__cod_servicio = str(valor).strip()

    @property
    def fecha_pago(self):
        return self.__fecha_pago

    @fecha_pago.setter
    def fecha_pago(self, valor):
        if valor is None:
            self.__fecha_pago = None
            return
        self.__fecha_pago = str(valor).strip()

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, valor):
        if valor is None:
            self.__monto = None
            return
        try:
            self.__monto = float(str(valor).strip().replace(',', '.'))
        except Exception:
            self.__monto = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    @property
    def cod_tipo_pago(self):
        return self.__cod_tipo_pago

    @cod_tipo_pago.setter
    def cod_tipo_pago(self, valor):
        if valor is None:
            self.__cod_tipo_pago = None
            return
        try:
            self.__cod_tipo_pago = int(valor)
        except Exception:
            self.__cod_tipo_pago = valor

    @property
    def cod_moneda(self):
        return self.__cod_moneda

    @cod_moneda.setter
    def cod_moneda(self, valor):
        if valor is None:
            self.__cod_moneda = None
            return
        try:
            self.__cod_moneda = int(valor)
        except Exception:
            self.__cod_moneda = valor

    @property
    def comprobante_pago(self):
        return self.__comprobante_pago

    @comprobante_pago.setter
    def comprobante_pago(self, valor):
        self.__comprobante_pago = valor

    def validarPago(self, cod_servicio=None, fecha_pago=None, monto=None, cod_tipo_pago=None, cod_moneda=None, comprobante_pago=None):
        errores = {}

        pat_int = re.compile(r'^[1-9]\d*$')
        pat_fecha = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        pat_monto = re.compile(r'^\d+(?:\.\d{1,2})?$')
        pat_comprobante = re.compile(r'.+\.(?:jpg|jpeg|png|gif)$', re.IGNORECASE)

        valor_cod_servicio = self.__cod_servicio if cod_servicio is None else cod_servicio
        valor_fecha_pago = self.__fecha_pago if fecha_pago is None else fecha_pago
        valor_monto = self.__monto if monto is None else monto
        valor_cod_tipo_pago = self.__cod_tipo_pago if cod_tipo_pago is None else cod_tipo_pago
        valor_cod_moneda = self.__cod_moneda if cod_moneda is None else cod_moneda
        valor_comprobante = self.__comprobante_pago if comprobante_pago is None else comprobante_pago

        if not valor_cod_servicio or not pat_int.match(str(valor_cod_servicio)):
            errores['cod_servicio'] = "Servicio no válido."

        if not valor_fecha_pago:
            errores['fecha_pago'] = "Fecha de pago requerida."
        else:
            if not pat_fecha.match(str(valor_fecha_pago)):
                errores['fecha_pago'] = "Formato de fecha inválido (YYYY-MM-DD)."
            else:
                try:
                    datetime.date.fromisoformat(str(valor_fecha_pago))
                except Exception:
                    errores['fecha_pago'] = "Fecha inválida."

        monto_str = str(valor_monto).replace(',', '.') if valor_monto is not None else '0'
        if not pat_monto.match(monto_str):
            errores['monto'] = "Monto inválido. Use formato 1234.56"
        else:
            try:
                if float(monto_str) < 0:
                    errores['monto'] = "El monto no puede ser negativo."
            except Exception:
                errores['monto'] = "Monto inválido."

        if not valor_cod_tipo_pago or not pat_int.match(str(valor_cod_tipo_pago)):
            errores['cod_tipo_pago'] = "Tipo de pago no válido."

        if not valor_cod_moneda or not pat_int.match(str(valor_cod_moneda)):
            errores['cod_moneda'] = "Moneda no válida."

        if valor_comprobante is not None:
            if not isinstance(valor_comprobante, str):
                errores['comprobante_pago'] = "Comprobante inválido."
            else:
                nombre_archivo = os.path.basename(valor_comprobante)
                if not pat_comprobante.match(nombre_archivo):
                    errores['comprobante_pago'] = "Formato del comprobante no soportado (JPG, PNG, GIF)."

        if errores:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Corrija los campos indicados.",
                "errors": errores
            }

        return {
            "status": True
        }

    def validar(self):
        validacion = self.validarPago()
        return validacion.get("errors", {})


    def calcular_valor_cambio(self, monto, cod_moneda=None, nombre_moneda=None):
        try:
            monto_valor = float(monto or 0.0)
        except Exception:
            monto_valor = 0.0

        if monto_valor <= 0:
            return 0.0

        if nombre_moneda is None and cod_moneda is not None:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT nombre_moneda
                FROM moneda
                WHERE cod_moneda = %s
            """, (cod_moneda,))
            moneda = cursor.fetchone()
            cursor.close()
            nombre_moneda = moneda.get('nombre_moneda') if moneda else None

        nombre = (nombre_moneda or '').strip().lower()
        nombre_limpio = re.sub(r'[^a-záéíóúñ]+', '', nombre)

        if nombre_limpio in {'bolivar', 'bolivares', 'ves', 'bs', 'bsf', 'bss'}:
            return monto_valor

        if nombre_limpio in {'dolar', 'dolarves', 'usd', 'usdv', 'dolarv', 'usdves'}:
            return monto_valor

        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT COALESCE((
                SELECT c.valor
                FROM cambio c
                WHERE c.cod_moneda = %s
                ORDER BY c.fecha DESC, c.cod_cambio DESC
                LIMIT 1
            ), 0) AS valor_cambio
        """, (cod_moneda,))
        cambio = cursor.fetchone()
        cursor.close()

        tasa = float(cambio.get('valor_cambio') or 0.0) if cambio else 0.0

        if nombre_limpio in {'euro', 'eur', 'euros'}:
            return monto_valor * tasa if tasa > 0 else monto_valor

        if nombre_limpio in {'usdt', 'tether', 'stablecoin'}:
            return monto_valor * tasa if tasa > 0 else monto_valor

        return monto_valor

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)
        sql = """
            SELECT
                p.cod_pago,
                p.fecha_pago,
                p.monto,
                p.status,
                u.cedula,
                u.nombre_usuario AS nombre_cliente,
                s.cod_servicio,
                COALESCE(x.precio_total, 0) AS precio_base,
                ROUND(
                    COALESCE(x.precio_total, 0) *
                    (1 - COALESCE(pr.descuento, 0) / 100),
                    2
                ) AS precio_total,
                pr.descuento AS descuento_promocion,
                (
                    SELECT tp.nombre_tipo_pago
                    FROM detalle_pago dp
                    INNER JOIN tipo_pago tp
                        ON tp.cod_tipo_pago = dp.cod_tipo_pago
                    WHERE dp.cod_pago = p.cod_pago
                    LIMIT 1
                ) AS nombre_tipo_pago,
                (
                    SELECT m.nombre_moneda
                    FROM detalle_pago dp
                    INNER JOIN moneda m
                        ON m.cod_moneda = dp.cod_moneda
                    WHERE dp.cod_pago = p.cod_pago
                    LIMIT 1
                ) AS nombre_moneda,
                p.comprobante_pago
            FROM pago p
            INNER JOIN servicio s
                ON s.cod_servicio = p.cod_servicio
            INNER JOIN seguridad.usuario u
                ON u.cedula = s.cedula
            LEFT JOIN promocion pr
                ON pr.cod_promo = s.cod_promo
            LEFT JOIN (
                SELECT
                    cod_servicio,
                    SUM(precio_unico) AS precio_total
                FROM (
                    SELECT DISTINCT
                        ds.cod_servicio,
                        ds.cod_tipo_servicio,
                        ts.precio AS precio_unico
                    FROM detalle_servicio ds
                    LEFT JOIN tipo_servicio ts
                        ON ts.cod_tipo_servicio = ds.cod_tipo_servicio
                ) AS detalle_precios
                GROUP BY cod_servicio
            ) AS x
                ON x.cod_servicio = s.cod_servicio
            ORDER BY fecha_pago DESC
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def anular(self, cod_pago):
        try:
            cursor = self.conexion.cursor()
            if not getattr(self.conexion, 'in_transaction', False):
                self.conexion.start_transaction()

            sql = "UPDATE pago SET status = 0 WHERE cod_pago = %s"
            cursor.execute(sql, (cod_pago,))
            filas = cursor.rowcount

            self.conexion.commit()
            cursor.close()
            return filas > 0
        except Exception as e:
            self.conexion.rollback()
            return False

    def listar_clientes(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT DISTINCT
                u.cedula,
                u.nombre_usuario AS nombre_cliente
            FROM servicio s
            INNER JOIN seguridad.usuario u ON s.cedula = u.cedula
            WHERE s.status = 1
            ORDER BY u.nombre_usuario ASC
        """)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def listar_servicios(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                s.cod_servicio,
                s.fecha,
                s.descripcion,
                u.cedula,
                u.nombre_usuario AS nombre_cliente,
                COALESCE(x.precio_total, 0) AS precio_base,
                ROUND(
                    COALESCE(x.precio_total, 0) *
                    (1 - COALESCE(pr.descuento, 0) / 100),
                    2
                ) AS precio_total,
                pr.descuento AS descuento_promocion,
                GROUP_CONCAT(DISTINCT ts.precio SEPARATOR ' | ') AS precios
            FROM servicio s
            INNER JOIN seguridad.usuario u ON s.cedula = u.cedula
            LEFT JOIN promocion pr ON pr.cod_promo = s.cod_promo
            LEFT JOIN (
                SELECT
                    cod_servicio,
                    SUM(precio_unico) AS precio_total
                FROM (
                    SELECT DISTINCT
                        ds.cod_servicio,
                        ds.cod_tipo_servicio,
                        ts.precio AS precio_unico
                    FROM detalle_servicio ds
                    LEFT JOIN tipo_servicio ts ON ts.cod_tipo_servicio = ds.cod_tipo_servicio
                ) AS detalle_precios
                GROUP BY cod_servicio
            ) AS x ON x.cod_servicio = s.cod_servicio
            LEFT JOIN detalle_servicio ds ON ds.cod_servicio = s.cod_servicio
            LEFT JOIN tipo_servicio ts ON ts.cod_tipo_servicio = ds.cod_tipo_servicio
            WHERE s.status = 1
            GROUP BY s.cod_servicio, s.fecha, s.descripcion, u.cedula,
                     u.nombre_usuario, x.precio_total, pr.descuento
            ORDER BY s.fecha DESC, s.cod_servicio DESC
        """)
        resultados = cursor.fetchall()
        cursor.close()

        #  si el precio_total es 0 o nulo
        for row in resultados:
            try:
                precio_base = float(row.get('precio_base') or 0)
            except Exception:
                precio_base = 0.0

            if precio_base <= 0:
                recalculado = self._calcular_precio_desde_detalle(row.get('cod_servicio'))
                descuento = float(row.get('descuento_promocion') or 0)
                row['precio_total'] = round(recalculado * (1 - descuento / 100), 2)

        return resultados

    def obtener_monto_servicio(self, cod_servicio):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT ROUND(
                COALESCE(SUM(x.precio_unico), 0) *
                (1 - COALESCE(pr.descuento, 0) / 100),
                2
            ) AS monto
            FROM servicio s
            LEFT JOIN promocion pr ON pr.cod_promo = s.cod_promo
            LEFT JOIN (
                SELECT DISTINCT
                    ds.cod_servicio,
                    ds.cod_tipo_servicio,
                    ts.precio AS precio_unico
                FROM detalle_servicio ds
                LEFT JOIN tipo_servicio ts
                    ON ts.cod_tipo_servicio = ds.cod_tipo_servicio
            ) AS x ON x.cod_servicio = s.cod_servicio
            WHERE s.cod_servicio = %s
            GROUP BY s.cod_servicio, pr.descuento
        """, (cod_servicio,))
        resultado = cursor.fetchone()
        cursor.close()
        return float(resultado['monto'] or 0) if resultado else None

    def _calcular_precio_desde_detalle(self, cod_servicio):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT COALESCE(SUM(x.precio_unico), 0) AS total
                FROM (
                    SELECT DISTINCT
                        ds.cod_tipo_servicio,
                        ts.precio AS precio_unico
                    FROM detalle_servicio ds
                    LEFT JOIN tipo_servicio ts ON ts.cod_tipo_servicio = ds.cod_tipo_servicio
                    WHERE ds.cod_servicio = %s
                ) AS x
            """, (cod_servicio,))
            fila = cursor.fetchone()
            cursor.close()
            return float(fila.get('total') or 0.0) if fila else 0.0
        except Exception:
            try:
                cursor.close()
            except Exception:
                pass
            return 0.0

    def servicio_pertenece_a_cliente(self, cod_servicio, cedula_cliente):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT 1
            FROM servicio
            WHERE cod_servicio = %s AND cedula = %s AND status = 1
        """, (cod_servicio, cedula_cliente))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado is not None

    def registrar_con_detalle(self):
        try:
            errores = self.validar()
            if errores:
                return {"success": False, "errors": errores}

            cursor = self.conexion.cursor(dictionary=True)
            sql_existe = "SELECT cod_pago, status FROM pago WHERE cod_servicio = %s LIMIT 1"
            cursor.execute(sql_existe, (self.__cod_servicio,))
            pago_existente = cursor.fetchone()

            if pago_existente and int(pago_existente.get('status') or 0) == 1:
                cursor.close()
                return {"success": False, "error": "el pago ya está registrado"}

            if pago_existente:
                sql_update_pago = """
                    UPDATE pago
                    SET fecha_pago = %s,
                        monto = %s,
                        comprobante_pago = %s,
                        status = %s
                    WHERE cod_pago = %s
                """
                cursor.execute(sql_update_pago, (
                    self.__fecha_pago,
                    self.__monto,
                    self.__comprobante_pago,
                    self.__status,
                    pago_existente['cod_pago']
                ))

                sql_update_detalle = """
                    UPDATE detalle_pago
                    SET cantidad = 1,
                        cod_tipo_pago = %s,
                        cod_moneda = %s
                    WHERE cod_pago = %s
                """
                cursor.execute(sql_update_detalle, (
                    self.__cod_tipo_pago,
                    self.__cod_moneda,
                    pago_existente['cod_pago']
                ))
            else:
                cursor.callproc('sp_registrar_pago_completo', (
                    self.__monto,
                    self.__comprobante_pago,
                    self.__cod_servicio,
                    self.__cod_tipo_pago,
                    self.__cod_moneda,
                    "1"
                ))

            self.conexion.commit()
            cursor.close()
            return {"success": True}

        except Exception as e:
            self.conexion.rollback()
            return {"success": False, "error": str(e)}

    def consultar_por_servicio(self, cod_servicio):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pago WHERE cod_servicio = %s", (cod_servicio,))
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def listar_tipos_pago(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT cod_tipo_pago, nombre_tipo_pago FROM tipo_pago WHERE status = 1")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def listar_monedas(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT cod_moneda, nombre_moneda FROM moneda WHERE status = 1 ORDER BY nombre_moneda ASC")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados


    def subir_comprobante(self, file):
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
            ruta_destino = os.path.join(self.UPLOAD_FOLDER, filename)
            file.save(ruta_destino)
            self.__comprobante_pago = os.path.join(self.PUBLIC_FOLDER, filename).replace("\\", "/")
