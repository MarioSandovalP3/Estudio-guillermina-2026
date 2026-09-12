from admin.config.conexion import Conexion
import bcrypt  # 🔥 importante para encriptar
import re
class ClientesModelo(Conexion):
    def __init__(self):
        super().__init__()  # Llama al constructor de Conexion

        # Atributos privados
        self.__cedula = None
        self.__nombre_usuario = None
        self.__apellido_usuario = None
        self.__telefono = None
        self.__direccion = None
        self.__correo = None
        self.__cod_rol = None
        self.__status = None
        self.__password = None
       
        # CAMPOS FALTANTES
        self.__intentos_fallidos = None
        self.__ultimo_acceso = None
        self.__fecha_registro = None

    def validarCliente(self, datos):

        if re.search(r'[^0-9]', datos.get("cedula", "")):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "La cédula solo puede contener números."
            }

        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', datos.get("apellido_usuario", "")):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El apellido no puede contener números ni caracteres especiales."
            }

        if re.search(r'[^0-9]', datos.get("telefono", "")):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El teléfono solo puede contener números."
            }

        patron = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if not re.match(patron, datos.get("correo", "")):
            return {
                "status": False,
                "icon": "warning",
                "title": "Correo inválido",
                "text": "Debe ingresar un correo electrónico válido."
            }

        return {"status": True}    


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
    def password(self):
        return self.__password

    @password.setter
    def password(self, valor):
        self.__password = valor


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
    # Métodos CRUD
    # ===============================
    def consultar(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT u.*, r.rol AS rol
            FROM seguridad.usuario AS u
            INNER JOIN seguridad.rol AS r
                ON u.cod_rol = r.cod_rol
            WHERE LOWER(r.rol) IN ('cliente', 'clientes')
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
            AND cod_rol = 3
        """, (cedula,))

        resultado = cursor.fetchone()
        cursor.close()

        return resultado

    def obtener_roles(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT cod_rol, rol FROM seguridad.rol WHERE rol = 'cliente'")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            from datetime import datetime
            ahora = datetime.now()

            sql = """
                INSERT INTO seguridad.usuario
                (
                    cedula,
                    nombre_usuario,
                    apellido_usuario,
                    telefono,
                    direccion,
                    correo,
                    cod_rol,
                    status,
                    password,
                    intentos_fallidos,
                    ultimo_acceso,
                    fecha_registro
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # SI HAY PASSWORD
            if self.__password:
                hashed_password = bcrypt.hashpw(
                    self.__password.encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')
            else:
                hashed_password = ""

            cursor.execute(sql, (
                self.__cedula,
                self.__nombre_usuario,
                self.__apellido_usuario,
                self.__telefono,
                self.__direccion,
                self.__correo,
                self.__cod_rol,
                1,              # status
                hashed_password,
                0,              # intentos_fallidos
                ahora,          # ultimo_acceso
                ahora           # fecha_registro
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al registrar cliente:", e)
            return 0
    
    
    def editar(self):
        try:
            cursor = self.conexion.cursor()

            sql = """
                UPDATE seguridad.usuario 
                SET nombre_usuario = %s,
                    apellido_usuario = %s,
                    telefono = %s,
                    direccion = %s,
                    correo = %s,
                    status = %s
                WHERE cedula = %s
            """

            cursor.execute(sql, (
                self.__nombre_usuario,
                self.__apellido_usuario,
                self.__telefono,
                self.__direccion,
                self.__correo,
                self.__status,
                self.__cedula
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar cliente:", e)
            return 0


    def eliminar(self, cedula):
        cursor = None

        try:
            cursor = self.conexion.cursor()

            # =====================================================
            # 1. CONSULTAR STATUS DEL CLIENTE
            # =====================================================
            cursor.execute("""
                SELECT status
                FROM seguridad.usuario
                WHERE cedula = %s
            """, (cedula,))

            usuario = cursor.fetchone()

            if not usuario:
                return -2

            status = int(usuario[0])

            # =====================================================
            # 2. CONSULTAR RESERVAS ACTIVAS
            # =====================================================
            cursor.execute("""
                SELECT COUNT(*)
                FROM sac.servicio
                WHERE cedula = %s
                AND status = 1
            """, (cedula,))

            reservas_activas = cursor.fetchone()[0]

            # =====================================================
            # 3. STATUS = 1 + TIENE RESERVAS ACTIVAS
            # =====================================================
            if status == 1 and reservas_activas > 0:
                return -5

            # =====================================================
            # 4. STATUS = 1 + NO TIENE RESERVAS ACTIVAS
            # =====================================================
            if status == 1 and reservas_activas == 0:
                return -3

            # =====================================================
            # 5. STATUS = 0 + NO TIENE RESERVAS ACTIVAS
            # =====================================================
            if status == 0 and reservas_activas == 0:

                cursor.execute("""
                    UPDATE seguridad.usuario
                    SET status = 2
                    WHERE cedula = %s
                    AND status = 0
                """, (cedula,))

                self.conexion.commit()

                return 1

        except Exception as e:

            if self.conexion:
                self.conexion.rollback()

            print("Error al eliminar cliente:", e)
            return -2

        finally:

            if cursor:
                cursor.close()
                

    def olvidar_contrasena(self, cedula, new_password, confirm_password):

        usuario = self.consultar_por_cedula(cedula)

        if not usuario:
            return None

        hashed_password = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        cursor = self.conexion.cursor()

        sql = """
            UPDATE seguridad.usuario
            SET password = %s
            WHERE cedula = %s
        """

        cursor.execute(sql, (hashed_password, cedula))
        self.conexion.commit()

        resultado = cursor.rowcount

        cursor.close()

        return resultado > 0
    
    def consultar_por_cedula(self, cedula):
        cursor = self.conexion.cursor(dictionary=True)

        sql = """
            SELECT
                u.cedula,
                u.nombre_usuario,
                u.apellido_usuario,
                u.password,
                u.telefono AS telefono_usuario,
                u.direccion AS direccion_usuario,
                u.correo,
                u.status,
                u.cod_rol,
                r.rol
            FROM seguridad.usuario u
            INNER JOIN seguridad.rol r ON u.cod_rol = r.cod_rol
            WHERE u.cedula = %s
            LIMIT 1
        """

        cursor.execute(sql, (cedula,))
        resultado = cursor.fetchone()

        cursor.close()

        return resultado


    def consultar_por_nombre(self, valor):
        try:
            cursor = self.conexion.cursor(dictionary=True)

            sql = """
                SELECT *
                FROM seguridad.usuario
                WHERE nombre_usuario = %s
            """

            cursor.execute(sql, (valor,))
            resultado = cursor.fetchone()

            cursor.close()

            return resultado

        except Exception as e:
            print(f"Error al consultar usuario: {e}")
            return None
