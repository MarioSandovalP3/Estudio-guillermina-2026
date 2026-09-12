from admin.config.conexion import Conexion
import datetime
import re


class MonedaModelo(Conexion):

    def __init__(self):
        super().__init__()

        # ===============================
        # ATRIBUTOS PRIVADOS
        # ===============================
        self.__cod_moneda = None
        self.__nombre_moneda = None
        self.__status = None

    def validarMoneda(self, nombre_moneda=None):
        nombre = self.__nombre_moneda if nombre_moneda is None else nombre_moneda
        valor = str(nombre).strip() if nombre is not None else ""

        if not valor:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El nombre de la moneda es obligatorio."
            }

        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', valor):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "La moneda no puede contener números ni caracteres especiales."
            }

        # Validación de longitud (máximo 15 caracteres)
        if len(valor) > 15:
            return {
                "status": False,
                "icon": "warning",
                "title": "limite de caracteres alcanzado",
                "text": "limite de caracteres alcanzado"
            }

        return {
            "status": True,
            "value": valor
        }

    # ===============================
    # GETTERS Y SETTERS
    # ===============================

    @property
    def cod_moneda(self):
        return self.__cod_moneda

    @cod_moneda.setter
    def cod_moneda(self, valor):
        self.__cod_moneda = valor


    @property
    def nombre_moneda(self):
        return self.__nombre_moneda

    @nombre_moneda.setter
    def nombre_moneda(self, valor):
        if valor is None:
            self.__nombre_moneda = None
            return
        self.__nombre_moneda = str(valor).strip()


    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    # ===============================
    # CONSULTAR MONEDA
    # ===============================

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                m.cod_moneda,
                m.nombre_moneda,
                m.status,
                (
                    SELECT c.valor
                    FROM cambio c
                    WHERE c.cod_moneda = m.cod_moneda
                    ORDER BY c.fecha DESC, c.cod_cambio DESC
                    LIMIT 1
                ) AS valor_cambio,
                (
                    SELECT c.fecha
                    FROM cambio c
                    WHERE c.cod_moneda = m.cod_moneda
                    ORDER BY c.fecha DESC, c.cod_cambio DESC
                    LIMIT 1
                ) AS fecha_cambio
            FROM moneda m
            ORDER BY cod_moneda DESC
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados        

    # ===============================
    # REGISTRAR
    # ===============================
    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute(
                "INSERT INTO moneda (nombre_moneda, status) VALUES (%s, 1)",
                (self.__nombre_moneda,)
            )

            # Obtener id insertado
            try:
                cod_moneda = cursor.lastrowid
            except Exception:
                cursor.execute("SELECT LAST_INSERT_ID()")
                cod_moneda = cursor.fetchone()[0]

            self.conexion.commit()
            # Registrar un cambio inicial 
            try:
                fecha_hoy = datetime.date.today().strftime('%Y-%m-%d')
                self.registrar_cambio(0, fecha_hoy, cod_moneda)
            except Exception:
                pass

            cursor.close()
            return 1

        except Exception as e:
            print("Error al registrar moneda:", e)
            return 0




    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE moneda
                SET nombre_moneda = %s,
                    status = %s
                WHERE cod_moneda = %s
            """, (
                self.__nombre_moneda,
                self.__status,
                self.__cod_moneda
            ))

            self.conexion.commit()
            # Registrar cambio 
            try:
                fecha_hoy = datetime.date.today().strftime('%Y-%m-%d')
                self.registrar_cambio(0, fecha_hoy, self.__cod_moneda)
            except Exception:
                pass

            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar moneda:", e)
            return 0  

    def eliminar(self, cod_moneda):
        try:
            cursor = self.conexion.cursor()

            # Verificar si existe la moneda
            sql = """
                SELECT status
                FROM moneda
                WHERE cod_moneda = %s
            """
            cursor.execute(sql, (cod_moneda,))
            moneda = cursor.fetchone()

            if not moneda:
                cursor.close()
                return -2

            status = moneda[0]

            # Bloquear solo si existe un pago activo asociado.
            sql_detalle_pago = """
                SELECT COUNT(*)
                FROM detalle_pago dp
                INNER JOIN pago p
                    ON dp.cod_pago = p.cod_pago
                WHERE dp.cod_moneda = %s
                AND p.status = 1
            """
            cursor.execute(sql_detalle_pago, (cod_moneda,))
            detalle_pago = cursor.fetchone()

            total = int(detalle_pago[0])

            # Los pagos anulados no impiden eliminar la moneda.
            if total > 0:
                cursor.close()
                return -2

            # Si está inactiva -> eliminación lógica
            if status == 0:

                sql_update = """
                    UPDATE moneda
                    SET status = 2
                    WHERE cod_moneda = %s
                """

                cursor.execute(sql_update, (cod_moneda,))
                self.conexion.commit()

                filas = cursor.rowcount
                cursor.close()

                return 1 if filas > 0 else -2

            # Si no tiene asociaciones -> eliminación física
            sql_delete = """
                DELETE FROM moneda
                WHERE cod_moneda = %s
            """

            cursor.execute(sql_delete, (cod_moneda,))
            self.conexion.commit()

            filas = cursor.rowcount
            cursor.close()

            return 1 if filas > 0 else -2

        except Exception as e:
            print("Error al eliminar moneda:", e)
            return -2        


    def buscar(self, nombre_moneda):
            cursor = self.conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT *
                FROM moneda
                WHERE LOWER(nombre_moneda) = LOWER(%s)
            """, (nombre_moneda,))

            resultado = cursor.fetchone()
            cursor.close()

            return resultado

    def registrar_cambio(self, valor, fecha, cod_moneda):
        try:
            cursor = self.conexion.cursor()
           
            try:
                if not getattr(self.conexion, 'in_transaction', False):
                    self.conexion.start_transaction()
            except Exception:
              
                pass

            cursor.execute(
                "SELECT cod_cambio FROM cambio WHERE cod_moneda = %s AND fecha = %s",
                (cod_moneda, fecha)
            )
            cambio_existente = cursor.fetchone()

            if cambio_existente:
                cursor.execute(
                    "UPDATE cambio SET valor = %s WHERE cod_cambio = %s",
                    (valor, cambio_existente[0])
                )
            else:
                cursor.execute(
                    "INSERT INTO cambio (valor, fecha, cod_moneda) VALUES (%s, %s, %s)",
                    (valor, fecha, cod_moneda)
                )

            self.conexion.commit()
            cursor.close()
            return 1

        except Exception as e:
            self.conexion.rollback()
            print("Error al registrar cambio:", e)
            return 0

    def actualizar_tasas_automaticas(
        self,
        tasa_bcv,
        tasa_usdt_ves=0.0,
        tasa_usdt_binance=0.0,
        tasa_paralelo=0.0,
        tasa_euro_usd=0.0,
    ):
        try:
            if not tasa_bcv or tasa_bcv <= 0:
                return 0

            fecha_hoy = datetime.date.today().strftime('%Y-%m-%d')
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT cod_moneda, nombre_moneda FROM moneda WHERE status != 2")
            monedas = cursor.fetchall()
            cursor.close()

            eur_usd = 0.0
            if tasa_euro_usd and tasa_euro_usd > 0:
                eur_usd = float(tasa_euro_usd)

            actualizadas = 0
            for moneda in monedas:
                nombre = (moneda.get('nombre_moneda') or '').strip().lower()
                nombre_limpio = re.sub(r'[^a-záéíóúñ]+', '', nombre)
                if nombre_limpio in {'bcv', 'dolar', 'dolarves', 'usd', 'usdv', 'dolarv'}:
              
                    valor = float(tasa_bcv)
                elif nombre_limpio in {'usdt', 'tether', 'stablecoin'}:
                    
                    if tasa_usdt_ves and tasa_usdt_ves > 0:
                        valor = float(tasa_usdt_ves)
                    elif tasa_paralelo and tasa_paralelo > 0 and tasa_usdt_binance and tasa_usdt_binance > 0:
                        valor = float(tasa_paralelo) * float(tasa_usdt_binance)
                    elif tasa_usdt_binance and tasa_usdt_binance > 0:
                        valor = float(tasa_bcv) * float(tasa_usdt_binance)
                    else:
                        valor = float(tasa_bcv)
                elif nombre_limpio in {'euro', 'eur', 'euros'}:
                    if eur_usd and tasa_bcv and tasa_bcv > 0:
                        valor = float(tasa_bcv) * eur_usd
                    else:
                        valor = float(tasa_bcv) * 1.08
                elif nombre_limpio in {'bolivar', 'bolivares', 'ves', 'bs', 'bsf', 'bss'}:
                    valor = 1.0
                else:
                    continue

                if self.registrar_cambio(valor, fecha_hoy, moneda['cod_moneda']) == 1:
                    actualizadas += 1

            return actualizadas

        except Exception as e:
            print("Error al actualizar tasas automáticas:", e)
            return 0
