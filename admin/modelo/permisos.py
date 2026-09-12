from admin.config.conexion import Conexion

class PermisosModelo(Conexion):

    def __init__(self):
        super().__init__()

        # ===============================
        # ATRIBUTOS PRIVADOS
        # ===============================

        self.__cod_permiso = None
        self.__cod_modulo = None
        self.__cod_accion = None
        self.__status = None

    
        self.__nombre_accion = None

    # ===============================
    # GETTERS Y SETTERS
    # ===============================

    @property
    def cod_permiso(self):
        return self.__cod_permiso

    @cod_permiso.setter
    def cod_permiso(self, valor):
        self.__cod_permiso = valor


    @property
    def cod_modulo(self):
        return self.__cod_modulo

    @cod_modulo.setter
    def cod_modulo(self, valor):
        self.__cod_modulo = valor


    @property
    def cod_accion(self):
        return self.__cod_accion

    @cod_accion.setter
    def cod_accion(self, valor):
        self.__cod_accion = valor


    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor


    @property
    def nombre_accion(self):
        return self.__nombre_accion

    @nombre_accion.setter
    def nombre_accion(self, valor):
        self.__nombre_accion = valor

        
    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT  
                u.cedula, 
                u.nombre_usuario, 
                u.apellido_usuario, 
                u.status AS status_usuario, 
                u.cod_rol, 
                r.rol, 

                GROUP_CONCAT(
                    DISTINCT p.cod_permiso
                    SEPARATOR '|'
                ) AS cod_permiso,

                GROUP_CONCAT( 
                    DISTINCT CONCAT(p.cod_modulo, '-', p.cod_accion) 
                    SEPARATOR '|' 
                ) AS permisos, 

                MAX(p.status) AS status_permisos 

            FROM seguridad.usuario u 

            INNER JOIN seguridad.rol r 
                ON u.cod_rol = r.cod_rol 

            INNER JOIN seguridad.rol_permiso rp 
                ON r.cod_rol = rp.cor_rol 

            INNER JOIN seguridad.permiso p 
                ON rp.cod_permiso = p.cod_permiso 

            GROUP BY 
                u.cedula, 
                u.nombre_usuario, 
                u.apellido_usuario, 
                u.status, 
                u.cod_rol, 
                r.rol 
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados
    

    def registrar(self, cod_rol, permisos):
        cursor = self.conexion.cursor()

        try:
            # =========================
            # RECORRER PERMISOS
            # =========================
            for cod_modulo, acciones in permisos.items():

                for cod_accion in acciones.keys():

                    # =========================
                    # VALIDAR / BUSCAR PERMISO
                    # =========================
                    cursor.execute("""
                        SELECT cod_permiso
                        FROM seguridad.permiso
                        WHERE cod_modulo = %s AND cod_accion = %s
                    """, (
                        cod_modulo,
                        cod_accion
                    ))

                    permiso = cursor.fetchone()

                    # =========================
                    # INSERTAR PERMISO SI NO EXISTE
                    # =========================
                    if permiso is None:
                        cursor.execute("""
                            INSERT INTO seguridad.permiso (
                                cod_modulo,
                                cod_accion,
                                status
                            )
                            VALUES (%s, %s, %s)
                        """, (
                            cod_modulo,
                            cod_accion,
                            1
                        ))

                        cod_permiso = cursor.lastrowid
                    else:
                        cod_permiso = permiso[0]

                    # =========================
                    # VALIDAR RELACIÓN ROL_PERMISO
                    # =========================
                    cursor.execute("""
                        SELECT cod_rol_permiso
                        FROM seguridad.rol_permiso
                        WHERE cor_rol = %s AND cod_permiso = %s
                    """, (
                        cod_rol,
                        cod_permiso
                    ))

                    existe = cursor.fetchone()

                    # =========================
                    # INSERTAR RELACIÓN SI NO EXISTE
                    # =========================
                    if existe is None:
                        cursor.execute("""
                            INSERT INTO seguridad.rol_permiso (
                                cor_rol,
                                cod_permiso
                            )
                            VALUES (%s, %s)
                        """, (
                            cod_rol,
                            cod_permiso
                        ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error registrar permiso:", e)
            self.conexion.rollback()
            cursor.close()
            return False


    def editar(self, cod_rol, permisos_nuevos, status):

        cursor = self.conexion.cursor()

        try:

            # ==========================================
            # 1. OBTENER TODOS LOS PERMISOS DEL ROL
            # ==========================================
            cursor.execute("""
                SELECT cod_permiso
                FROM seguridad.rol_permiso
                WHERE cor_rol = %s
            """, (cod_rol,))

            permisos_actuales = set()

            for row in cursor.fetchall():
                permisos_actuales.add(row[0])

            # ==========================================
            # 2. RECORRER LOS CHECKBOX SELECCIONADOS
            # ==========================================
            permisos_nuevos_ids = set()

            for permiso in permisos_nuevos:

                # permiso viene: "2-1"
                cod_modulo, cod_accion = permiso.split("-")

                # ==========================================
                # BUSCAR SI YA EXISTE EN TABLA permiso
                # ==========================================
                cursor.execute("""
                    SELECT cod_permiso
                    FROM seguridad.permiso
                    WHERE cod_modulo = %s
                    AND cod_accion = %s
                """, (cod_modulo, cod_accion))

                permiso_bd = cursor.fetchone()

                # ==========================================
                # SI NO EXISTE → CREARLO
                # ==========================================
                if not permiso_bd:

                    cursor.execute("""
                        INSERT INTO seguridad.permiso
                        (
                            cod_modulo,
                            cod_accion,
                            status
                        )
                        VALUES (%s, %s, %s)
                    """, (cod_modulo, cod_accion, status))

                    cod_permiso = cursor.lastrowid

                else:

                    cod_permiso = permiso_bd[0]

                    # ==========================================
                    # ACTUALIZAR STATUS
                    # ==========================================
                    cursor.execute("""
                        UPDATE seguridad.permiso
                        SET status = %s
                        WHERE cod_permiso = %s
                    """, (status, cod_permiso))

                permisos_nuevos_ids.add(cod_permiso)

            # ==========================================
            # 3. PERMISOS A INSERTAR
            # ==========================================
            permisos_insertar = permisos_nuevos_ids - permisos_actuales

            # ==========================================
            # 4. INSERTAR NUEVOS AL ROL
            # ==========================================
            for cod_permiso in permisos_insertar:

                cursor.execute("""
                    INSERT INTO seguridad.rol_permiso
                    (
                        cor_rol,
                        cod_permiso
                    )
                    VALUES (%s, %s)
                """, (cod_rol, cod_permiso))

            # ==========================================
            # 5. PERMISOS A ELIMINAR
            # ==========================================
            permisos_eliminar = permisos_actuales - permisos_nuevos_ids

            # ==========================================
            # 6. ELIMINAR SOLO LOS DESELECCIONADOS
            # ==========================================
            for cod_permiso in permisos_eliminar:

                cursor.execute("""
                    DELETE FROM seguridad.rol_permiso
                    WHERE cor_rol = %s
                    AND cod_permiso = %s
                """, (cod_rol, cod_permiso))

            # ==========================================
            # 7. GUARDAR CAMBIOS
            # ==========================================
            self.conexion.commit()

            cursor.close()

            return True

        except Exception as e:

            print("Error editar permisos:", e)

            self.conexion.rollback()

            cursor.close()

            return False   


    def obtener_acciones(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT cod_accion, nombre_accion, status
            FROM seguridad.acciones
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados

    def obtener_roles(self):
            cursor = self.conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT cod_rol, rol 
                FROM seguridad.rol
            """)

            resultados = cursor.fetchall()
            cursor.close()

            return resultados
    

    def obtener_modulos(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
           SELECT
            cod_modulo,
            REPLACE(nombre_modulo, '_', ' ') AS nombre_modulo,
            status
        FROM seguridad.modulos
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados




    def tiene_permiso(self, cod_rol, modulo, accion):

        cursor = self.conexion.cursor()

        sql = """
            SELECT COUNT(*)
            FROM seguridad.rol_permiso rp
            INNER JOIN seguridad.permiso p ON rp.cod_permiso = p.cod_permiso
            INNER JOIN seguridad.modulos m ON p.cod_modulo = m.cod_modulo
            INNER JOIN seguridad.acciones a ON p.cod_accion = a.cod_accion
            WHERE rp.cor_rol = %s
            AND m.nombre_modulo = %s
            AND a.nombre_accion = %s
            AND p.status = 1
        """

        cursor.execute(sql, (cod_rol, modulo, accion))
        resultado = cursor.fetchone()

        cursor.close()

        return resultado[0] > 0
    

    def buscar_permisos(self, cod_rol, permisos):
        cursor = self.conexion.cursor(dictionary=True)

        if not permisos:
            cursor.close()
            return False

        cursor.execute("""
            SELECT CONCAT(p.cod_modulo, '-', p.cod_accion) AS permiso
            FROM seguridad.rol_permiso rp
            INNER JOIN seguridad.permiso p
                ON rp.cod_permiso = p.cod_permiso
            WHERE rp.cor_rol = %s
        """, (cod_rol,))

        resultados = cursor.fetchall()
        cursor.close()

        permisos_bd = {
            str(resultado["permiso"]).strip()
            for resultado in resultados
        }

        permisos_recibidos = {
            str(permiso).strip()
            for permiso in permisos
        }

        return permisos_bd == permisos_recibidos

    def eliminar(self, cod_permiso):
        try:
            cursor = self.conexion.cursor(dictionary=True)

            sql = """
                SELECT
                    p.status,
                    COUNT(rp.cod_rol_permiso) AS asociaciones
                FROM seguridad.permiso p
                LEFT JOIN seguridad.rol_permiso rp
                    ON rp.cod_permiso = p.cod_permiso
                WHERE p.cod_permiso = %s
                GROUP BY p.cod_permiso, p.status
            """

            cursor.execute(sql, (cod_permiso,))
            resultado = cursor.fetchone()

            if not resultado:
                cursor.close()
                return "error"

            status = resultado["status"]
            asociaciones = resultado["asociaciones"] or 0

            if status == 1 and asociaciones > 0:
                cursor.close()
                return "tiene_permisos"

            sql = """
                DELETE FROM seguridad.permiso
                WHERE cod_permiso = %s
            """

            cursor.execute(sql, (cod_permiso,))
            self.conexion.commit()
            cursor.close()

            return "eliminado"

        except Exception:
            self.conexion.rollback()
            return "error"