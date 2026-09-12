from admin.config.conexion import Conexion
import datetime
import re


class PagospersonalModelo(Conexion):
    def __init__(self):
        super().__init__()

        self.__cod_pago_personal = None
        self.__fecha_pago = None
        self.__hora_pago = None
        self.__porcentaje = None
        self.__status = None
        self.__cod_servicio = None
        self.ultimo_error = None

    def validarFechaPago(self, fecha_pago=None):
        valor = self.__fecha_pago if fecha_pago is None else fecha_pago
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Debe indicar la fecha del pago."
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

    def validarHoraPago(self, hora_pago=None):
        valor = self.__hora_pago if hora_pago is None else hora_pago
        texto = str(valor).strip() if valor is not None else ""

        if texto == "":
            return {"status": True, "value": None}

        # Acepta HH:MM 
        if not re.match(r'^\d{2}:\d{2}(:\d{2})?$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Formato de hora inválido (HH:MM o HH:MM:SS)."
            }

        if len(texto) == 5:
            texto = texto + ':00'

        return {"status": True, "value": texto}

    def validarPorcentaje(self, porcentaje=None):
        valor = self.__porcentaje if porcentaje is None else porcentaje
        texto = str(valor).strip() if valor is not None else ""

        if not texto or not re.match(r'^[1-9]\d*$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El porcentaje debe ser mayor a cero."
            }

        return {"status": True, "value": int(texto)}

    def validarCodServicio(self, cod_servicio=None):
        valor = self.__cod_servicio if cod_servicio is None else cod_servicio
        texto = str(valor).strip() if valor is not None else ""

        if not texto or not re.match(r'^[1-9]\d*$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Debe seleccionar un servicio válido."
            }

        return {"status": True, "value": int(texto)}

    def validarPagoPersonal(self, cod_servicio=None, fecha_pago=None, hora_pago=None, porcentaje=None):
        errores = {}
        pat_int = re.compile(r'^[1-9]\d*$')
        pat_fecha = re.compile(r'^\d{4}-\d{2}-\d{2}$')

        valor_cod_servicio = self.__cod_servicio if cod_servicio is None else cod_servicio
        valor_fecha_pago = self.__fecha_pago if fecha_pago is None else fecha_pago
        valor_hora_pago = self.__hora_pago if hora_pago is None else hora_pago
        valor_porcentaje = self.__porcentaje if porcentaje is None else porcentaje

        if not valor_cod_servicio or not pat_int.match(str(valor_cod_servicio)):
            errores['cod_servicio'] = "Debe seleccionar un servicio válido."

        if not valor_fecha_pago:
            errores['fecha_pago'] = "Debe indicar la fecha del pago."
        elif not pat_fecha.match(str(valor_fecha_pago)):
            errores['fecha_pago'] = "Formato de fecha inválido (YYYY-MM-DD)."
        else:
            try:
                datetime.date.fromisoformat(str(valor_fecha_pago))
            except Exception:
                errores['fecha_pago'] = "Fecha inválida."

        if valor_hora_pago is not None and str(valor_hora_pago).strip() != '':
            hora_str = str(valor_hora_pago).strip()
            if len(hora_str) == 5:
                hora_str = hora_str + ':00'
            if not re.match(r'^\d{2}:\d{2}:\d{2}$', hora_str):
                errores['hora_pago'] = "Formato de hora inválido (HH:MM o HH:MM:SS)."

        if not valor_porcentaje or not pat_int.match(str(valor_porcentaje)):
            errores['porcentaje'] = "El porcentaje debe ser mayor a cero."

        if errores:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Corrija los campos indicados.",
                "errors": errores
            }

        return {"status": True}

    @property
    def cod_pago_personal(self):
        return self.__cod_pago_personal

    @cod_pago_personal.setter
    def cod_pago_personal(self, valor):
        self.__cod_pago_personal = valor

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
    def hora_pago(self):
        return self.__hora_pago

    @hora_pago.setter
    def hora_pago(self, valor):
      
        if valor is None:
            self.__hora_pago = None
            return
        self.__hora_pago = str(valor).strip()

    @property
    def porcentaje(self):
        return self.__porcentaje

    @porcentaje.setter
    def porcentaje(self, valor):
      
        if valor is None:
            self.__porcentaje = None
            return
        try:
            self.__porcentaje = int(valor)
        except Exception:
            self.__porcentaje = valor

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
     
        if valor is None:
            self.__cod_servicio = None
            return
        try:
            self.__cod_servicio = int(valor)
        except Exception:
            self.__cod_servicio = valor

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)
        sql = """
            SELECT
                pp.cod_pago_personal,
                pp.fecha_pago,
                pp.hora_pago,
                pp.porcentaje,
                pp.status,
                s.cod_servicio,
                s.descripcion AS servicio,
                s.fecha AS fecha_servicio,
                u.cedula,
                u.nombre_usuario AS nombre_cliente,
                ue.cedula AS cedula_especialista,
                CONCAT(COALESCE(ue.nombre_usuario, ''), ' ', COALESCE(ue.apellido_usuario, '')) AS nombre_especialista,
                COALESCE(x.precio_total, 0) AS monto_servicio,
                COALESCE(
                    fn_calcular_comision_servicio(x.precio_total, pp.porcentaje),
                    0
                ) AS monto_a_pagar,
                fn_calcular_total_pago_personal(ue.cedula, pp.fecha_pago) AS total_pago_dia
            FROM pago_personal pp
            INNER JOIN servicio s ON pp.cod_servicio = s.cod_servicio
            INNER JOIN seguridad.usuario u ON s.cedula = u.cedula
            LEFT JOIN seguridad.usuario ue ON ue.cedula = s.cedula_especialista
            LEFT JOIN (
                SELECT
                    ds.cod_servicio,
                    SUM(GREATEST(CAST(ds.cantidad_servicio AS DECIMAL(10,2)), 1) * ts.precio) AS precio_total
                FROM detalle_servicio ds
                LEFT JOIN tipo_servicio ts ON ts.cod_tipo_servicio = ds.cod_tipo_servicio
                GROUP BY ds.cod_servicio
            ) AS x ON x.cod_servicio = s.cod_servicio
            GROUP BY pp.cod_pago_personal, pp.fecha_pago, pp.hora_pago, pp.porcentaje, pp.status,
                     s.cod_servicio, s.descripcion, s.fecha, u.cedula, u.nombre_usuario,
                     ue.cedula, ue.nombre_usuario, ue.apellido_usuario, x.precio_total
            ORDER BY pp.fecha_pago DESC, pp.cod_pago_personal DESC
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def listar_servicios(self):
        cursor = self.conexion.cursor(dictionary=True)
        sql = """
            SELECT
                s.cod_servicio,
                s.fecha,
                s.descripcion,
                s.cedula_especialista,
                u.cedula,
                u.nombre_usuario AS nombre_cliente,
                CONCAT(COALESCE(ue.nombre_usuario, ''), ' ', COALESCE(ue.apellido_usuario, '')) AS nombre_especialista,
                COALESCE(SUM(GREATEST(CAST(ds.cantidad_servicio AS DECIMAL(10,2)), 1) * ts.precio), 0) AS precio_total
            FROM servicio s
            INNER JOIN seguridad.usuario u ON s.cedula = u.cedula
            LEFT JOIN seguridad.usuario ue ON ue.cedula = s.cedula_especialista
            LEFT JOIN detalle_servicio ds ON ds.cod_servicio = s.cod_servicio
            LEFT JOIN tipo_servicio ts ON ts.cod_tipo_servicio = ds.cod_tipo_servicio
            WHERE s.status = 1
            GROUP BY s.cod_servicio, s.fecha, s.descripcion, s.cedula_especialista, u.cedula, u.nombre_usuario, ue.nombre_usuario, ue.apellido_usuario
            ORDER BY s.fecha DESC, s.cod_servicio DESC
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def listar_personal(self):
        cursor = self.conexion.cursor(dictionary=True)
        sql = """
            SELECT
                u.cedula,
                u.nombre_usuario,
                u.apellido_usuario,
                esp.cedula_especialista,
                esp.especialista
            FROM seguridad.usuario u
            INNER JOIN especialista esp ON esp.cedula_especialista = u.cedula
            WHERE u.status = 1
            ORDER BY u.nombre_usuario ASC
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def registrar(self):
        try:
            cursor = self.conexion.cursor()
            self.conexion.rollback()
            self.conexion.start_transaction()

            cursor.callproc('sp_guardar_pago_personal', (
                self.__fecha_pago,
                self.__hora_pago or '00:00:00',
                self.__porcentaje,
                self.__status,
                self.__cod_servicio,
            ))

            self.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            self.conexion.rollback()
            self.ultimo_error = str(e)
            print("Error al registrar pago personal:", e)
            return False

    def existe_pago_activo(self, cod_servicio):
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM pago_personal WHERE cod_servicio = %s AND status = 1",
            (cod_servicio,)
        )
        existe = cursor.fetchone()[0] > 0
        cursor.close()
        return existe

    def obtener_pago_activo(self, cod_servicio):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT cod_pago_personal, fecha_pago, hora_pago FROM pago_personal WHERE cod_servicio = %s AND status = 1 ORDER BY fecha_pago DESC, hora_pago DESC LIMIT 1",
            (cod_servicio,)
        )
        pago = cursor.fetchone()
        cursor.close()
        return pago

    def procesar_nomina(self):
        try:
            cursor = self.conexion.cursor()

            cursor.callproc('sp_procesar_nomina_personal', (
                self.__fecha_pago,
                self.__hora_pago or '00:00:00',
                self.__porcentaje,
                self.__status,
                self.__cod_servicio,
            ))

            cursor.close()
            return True
        except Exception as e:
            print("Error al procesar nómina personal:", e)
            return False

    def anular(self, cod_pago_personal):
        try:
            cursor = self.conexion.cursor()
            self.conexion.start_transaction()

            sql = "UPDATE pago_personal SET status = 0 WHERE cod_pago_personal = %s"
            cursor.execute(sql, (cod_pago_personal,))
            filas = cursor.rowcount

            self.conexion.commit()
            cursor.close()
            return filas > 0
        except Exception as e:
            self.conexion.rollback()
            print("Error al anular pago personal:", e)
            return False