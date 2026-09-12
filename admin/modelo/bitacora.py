from admin.config.conexion import Conexion


class BitacoraModelo(Conexion):

    def __init__(self):
        super().__init__()
        self._asegurar_esquema()

    def _asegurar_esquema(self):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SHOW COLUMNS FROM seguridad.bitacora")
            columnas = {columna["Field"] for columna in cursor.fetchall()}
            cursor.close()

            cambios = []
            if "movimiento" not in columnas and "modulo" not in columnas and "accion" not in columnas:
                cambios.append("ALTER TABLE seguridad.bitacora ADD COLUMN movimiento VARCHAR(250) NULL")
            if "status" not in columnas:
                cambios.append("ALTER TABLE seguridad.bitacora ADD COLUMN status TINYINT(1) NOT NULL DEFAULT 1")

            if cambios:
                cursor = self.conexion.cursor()
                for sql in cambios:
                    cursor.execute(sql)
                self.conexion.commit()
                cursor.close()

        except Exception as e:
            print("Error ajustando esquema de bitácora:", e)

    def _obtener_columnas(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SHOW COLUMNS FROM seguridad.bitacora")
        columnas = {columna["Field"] for columna in cursor.fetchall()}
        cursor.close()
        return columnas

    # ==========================================
    # CONSULTAR BITÁCORA
    # ==========================================
    def consultar(self, fecha=None, anio=None):

        try:
            cursor = self.conexion.cursor(dictionary=True)
            columnas = self._obtener_columnas()

            if "movimiento" in columnas:
                movimiento_sql = "COALESCE(b.movimiento, 'Sin movimiento') AS movimiento"
            elif "modulo" in columnas and "accion" in columnas:
                movimiento_sql = "CONCAT(COALESCE(b.modulo, 'general'), ' - ', COALESCE(b.accion, 'Consultar')) AS movimiento"
            else:
                movimiento_sql = "'Sin movimiento' AS movimiento"

            sql = f"""
                SELECT
                    b.cod_bitacora,
                    b.fecha,
                    b.hora,
                    {movimiento_sql},
                    u.cedula,
                    CONCAT(
                        u.nombre_usuario,
                        ' ',
                        u.apellido_usuario
                    ) AS usuario,
                    r.rol
                FROM seguridad.bitacora b

                INNER JOIN seguridad.usuario u
                    ON b.cedula = u.cedula

                LEFT JOIN seguridad.rol r
                    ON u.cod_rol = r.cod_rol

                WHERE 1=1
            """

            parametros = []

            if fecha:
                sql += " AND b.fecha = %s "
                parametros.append(fecha)

            if anio:
                sql += " AND YEAR(b.fecha) = %s "
                parametros.append(anio)

            sql += """
                ORDER BY
                    b.fecha DESC,
                    b.hora DESC
            """

            cursor.execute(sql, tuple(parametros))

            datos = cursor.fetchall()

            cursor.close()

            return datos

        except Exception as e:
            print("Error consultar bitácora:", e)
            return []

    # ==========================================
    # REGISTRAR MOVIMIENTO
    # ==========================================
    def registrar(self, cedula, modulo, accion=None, descripcion=None, ip=None):

        try:
            cursor = self.conexion.cursor()
            columnas = self._obtener_columnas()

            if descripcion:
                movimiento = f"{modulo} - {descripcion}" if modulo and descripcion else (modulo or descripcion or "Bitácora")
            elif accion:
                movimiento = f"{modulo} - {accion}" if modulo and accion else (modulo or accion or "Bitácora")
            else:
                movimiento = modulo or "Bitácora"

            if "movimiento" in columnas:
                sql = """
                    INSERT INTO seguridad.bitacora
                    (
                        cedula,
                        movimiento,
                        fecha,
                        hora,
                        status
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        CURDATE(),
                        CURTIME(),
                        1
                    )
                """
                cursor.execute(sql, (cedula, movimiento))
            elif "modulo" in columnas and "accion" in columnas:
                sql = """
                    INSERT INTO seguridad.bitacora
                    (
                        cedula,
                        modulo,
                        accion,
                        fecha,
                        hora,
                        status
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        CURDATE(),
                        CURTIME(),
                        1
                    )
                """
                cursor.execute(sql, (cedula, modulo, descripcion or accion or "BITACORA"))
            else:
                sql = """
                    INSERT INTO seguridad.bitacora
                    (
                        cedula,
                        fecha,
                        hora,
                        status
                    )
                    VALUES
                    (
                        %s,
                        CURDATE(),
                        CURTIME(),
                        1
                    )
                """
                cursor.execute(sql, (cedula,))

            self.conexion.commit()

            cursor.close()

            return True

        except Exception as e:
            print("Error registrar bitácora:", e)
            return False