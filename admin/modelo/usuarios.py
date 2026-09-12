from admin.config.conexion import Conexion
import bcrypt
from datetime import datetime, timedelta
import re

class UsuariosModelo(Conexion):
    def __init__(self):
        super().__init__() # Llama al constructor de Conexion

        # Atributos privados
        self.__cedula = None
        self.__nombre_usuario = None
        self.__apellido_usuario = None
        self.__telefono = None
        self.__direccion = None
        self.__correo = None
        self.__password = None
        self.__cod_rol = None
        self.__status = None

        # CAMPOS FALTANTES
        self.__intentos_fallidos = None
        self.__ultimo_acceso = None
        self.__fecha_registro = None

 

    def validarUsuario(self, cedula, nombre, apellido, telefono, direccion, correo, password):

        errores = []

        # Cédula: solo números
        if cedula and not cedula.isdigit():
            errores.append("• La cédula solo puede contener números.")

        # Nombre: solo letras, espacios y signos
        if nombre and re.search(r'\d', nombre):
            errores.append("• El nombre no puede contener números.")

        # Apellido: solo letras, espacios y signos
        if apellido and re.search(r'\d', apellido):
            errores.append("• El apellido no puede contener números.")

        # Teléfono: solo números
        if telefono and not telefono.isdigit():
            errores.append("• El teléfono solo puede contener números.")

        # Dirección: cualquier contenido (no se valida)

        # Correo
        if correo and not re.fullmatch(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            correo
        ):
            errores.append("• El correo electrónico no es válido.")

        # Contraseña: sin validación

        if errores:
            return {
                "status": False,
                "icon": "warning",
                "title": "Datos inválidos",
                "text": "<br>".join(errores)
            }

        return {
            "status": True
        }




    # ===============================
    # Getters y Setters
    # ===============================

    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, valor):
        self.__cedula = valor


    @property
    def nombre_usuario(self):
        return self.__nombre_usuario

    @nombre_usuario.setter
    def nombre_usuario(self, valor):
        self.__nombre_usuario = valor


    @property
    def apellido_usuario(self):
        return self.__apellido_usuario

    @apellido_usuario.setter
    def apellido_usuario(self, valor):
        self.__apellido_usuario = valor


    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor


    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        self.__direccion = valor


    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        self.__correo = valor


    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, valor):
        self.__password = valor


    @property
    def cod_rol(self):
        return self.__cod_rol

    @cod_rol.setter
    def cod_rol(self, valor):
        self.__cod_rol = valor


    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor




    @property
    def intentos_fallidos(self):
        return self.__intentos_fallidos

    @intentos_fallidos.setter
    def intentos_fallidos(self, valor):
        self.__intentos_fallidos = valor


    @property
    def ultimo_acceso(self):
        return self.__ultimo_acceso

    @ultimo_acceso.setter
    def ultimo_acceso(self, valor):
        self.__ultimo_acceso = valor


    @property
    def fecha_registro(self):
        return self.__fecha_registro

    @fecha_registro.setter
    def fecha_registro(self, valor):
        self.__fecha_registro = valor
    # ===============================
    # Métodos
    # ===============================

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                u.cedula,
                u.nombre_usuario,
                u.apellido_usuario,
                u.password,
                u.telefono,
                u.direccion,
                u.correo,
                u.status,
                u.cod_rol,
                r.rol
            FROM seguridad.usuario u
            JOIN seguridad.rol r 
                ON u.cod_rol = r.cod_rol
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
    
    def buscar(self, cedula):
            cursor = self.conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT *
                FROM seguridad.usuario
                WHERE cedula = %s
            """, (cedula,))

            resultado = cursor.fetchone()
            cursor.close()

            return resultado


    def registrar(self):
        cursor = self.conexion.cursor()

        try:
            # =========================
            # ENCRIPTAR PASSWORD
            # =========================
            hashedPassword = bcrypt.hashpw(
                self.password.encode('utf-8'),
                bcrypt.gensalt()
            )

            # =========================
            # FECHA ACTUAL
            # =========================
            from datetime import datetime
            ahora = datetime.now()

            # =========================
            # INSERTAR USUARIO
            # =========================
            sql = """
                INSERT INTO seguridad.usuario (
                    cedula,
                    nombre_usuario,
                    apellido_usuario,
                    password,
                    telefono,
                    direccion,
                    correo,
                    status,
                    cod_rol,
                    intentos_fallidos,
                    ultimo_acceso,
                    fecha_registro
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                self.cedula,
                self.nombre_usuario,
                self.apellido_usuario,
                hashedPassword,
                self.telefono,
                self.direccion,
                self.correo,
                1,
                self.cod_rol,
                0,          # intentos_fallidos
                ahora,      # ultimo_acceso
                ahora       # fecha_registro
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error registrar usuario:", e)
            cursor.close()
            return False

    def editar(self):
        cursor = self.conexion.cursor()

        try:
            # =========================
            # SI VIENE PASSWORD → ENCRIPTAR
            # =========================
            if hasattr(self, "password") and self.password:
                hashedPassword = bcrypt.hashpw(
                    self.password.encode('utf-8'),
                    bcrypt.gensalt()
                )

                cursor.execute("""
                    UPDATE seguridad.usuario
                    SET nombre_usuario = %s,
                        apellido_usuario = %s,
                        password = %s,
                        telefono = %s,
                        direccion = %s,
                        correo = %s,
                        status = %s,
                        cod_rol = %s
                    WHERE cedula = %s
                """, (
                    self.nombre_usuario,
                    self.apellido_usuario,
                    hashedPassword,
                    self.telefono,
                    self.direccion,
                    self.correo,
                    self.status,
                    self.cod_rol,
                    self.cedula
                ))

            else:
                # SIN CAMBIAR PASSWORD
                cursor.execute("""
                    UPDATE seguridad.usuario
                    SET nombre_usuario = %s,
                        apellido_usuario = %s,
                        telefono = %s,
                        direccion = %s,
                        correo = %s,
                        status = %s,
                        cod_rol = %s
                    WHERE cedula = %s
                """, (
                    self.nombre_usuario,
                    self.apellido_usuario,
                    self.telefono,
                    self.direccion,
                    self.correo,
                    self.status,
                    self.cod_rol,
                    self.cedula
                ))

            self.conexion.commit()
            cursor.close()
            return True

        except Exception as e:
            print("Error editar usuario:", e)
            cursor.close()
            return False
  

    def eliminar(self, cedula):
        try:
            cursor = self.conexion.cursor()

            sql = """
                SELECT status, cod_rol
                FROM seguridad.usuario
                WHERE cedula = %s
            """
            cursor.execute(sql, (cedula,))
            usuario = cursor.fetchone()

            # Usuario no existe
            if not usuario:
                cursor.close()
                return 0

            status, cod_rol = usuario

            # Usuario inactivo con rol → eliminación lógica
            if status == 0 and cod_rol is not None:
                sql_update = """
                    UPDATE seguridad.usuario
                    SET status = 2
                    WHERE cedula = %s
                """
                cursor.execute(sql_update, (cedula,))
                self.conexion.commit()

                filas = cursor.rowcount
                cursor.close()

                return 1 if filas > 0 else 0

            # Usuario activo con rol → no se elimina
            if status == 1 and cod_rol is not None:
                cursor.close()
                return -2

            cursor.close()
            return -1

        except Exception as e:
            print("Error eliminar usuario:", e)
            return 0


    def consultar_por_cedula(self, cedula):

        sql = """
        SELECT
            u.cedula,
            u.nombre_usuario,
            u.apellido_usuario,
            u.password,
            u.telefono,
            u.direccion,
            u.correo,
            u.status,
            u.cod_rol,
            u.intentos_fallidos,
            u.ultimo_acceso,
            u.fecha_registro,
            r.rol
        FROM seguridad.usuario u
        INNER JOIN seguridad.rol r
            ON u.cod_rol = r.cod_rol
        WHERE u.cedula = %s
        LIMIT 1
        """

        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute(sql, (cedula,))
        resultado = cursor.fetchone()
        cursor.close()

        return resultado
    

    def consultar_permisos_rol(self, cod_rol):

        sql = """
        SELECT
            m.nombre_modulo,
            a.nombre_accion
        FROM seguridad.rol_permiso rp
        INNER JOIN seguridad.permiso p
            ON rp.cod_permiso = p.cod_permiso
        INNER JOIN seguridad.modulos m
            ON p.cod_modulo = m.cod_modulo
        INNER JOIN seguridad.acciones a
            ON p.cod_accion = a.cod_accion
        WHERE rp.cor_rol = %s
        """

        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute(sql, (cod_rol,))
        resultados = cursor.fetchall()
        cursor.close()

        return resultados
        






    # =====================================
    # AUMENTAR INTENTOS FALLIDOS
    # =====================================
    def aumentar_intentos(self, cedula):

        cursor = self.conexion.cursor()

        sql = """
            UPDATE seguridad.usuario
            SET intentos_fallidos = intentos_fallidos + 1,
                ultimo_acceso = NOW()
            WHERE cedula = %s
        """

        cursor.execute(sql, (cedula,))
        self.conexion.commit()
        cursor.close()


    # =====================================
    # REINICIAR INTENTOS
    # =====================================
    def reiniciar_intentos(self, cedula):

        cursor = self.conexion.cursor()

        sql = """
            UPDATE seguridad.usuario
            SET intentos_fallidos = 0,
                ultimo_acceso = NOW()
            WHERE cedula = %s
        """

        cursor.execute(sql, (cedula,))
        self.conexion.commit()
        cursor.close()


    # =====================================
    # VERIFICAR BLOQUEO DE 5 MINUTOS
    # =====================================
    def usuario_bloqueado(self, cedula):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT intentos_fallidos,
                ultimo_acceso
            FROM seguridad.usuario
            WHERE cedula = %s
        """, (cedula,))

        usuario = cursor.fetchone()

        cursor.close()

        if not usuario:
            return False

        if usuario["intentos_fallidos"] < 3:
            return False

       
        if datetime.now() >= usuario["ultimo_acceso"] + timedelta(minutes=5):

            self.reiniciar_intentos(cedula)

            return False

        # Sigue bloqueado
        return True        