from admin.config.conexion import Conexion
import re
import bcrypt

class PersonalModelo(Conexion):

    def __init__(self):
        super().__init__()  # Llama al constructor de Conexion

        # ===============================
        # ATRIBUTOS PRIVADOS
        # ===============================
        self.__cedula = None
        self.__nombre_usuario = None
        self.__apellido_usuario = None
        self.__telefono = None
        self.__direccion = None
        self.__correo = None
        self.__cod_rol = None
        self.__status = None
        self.__password = None

        # campos para controlar intentos y accesos 
        self.__intentos_fallidos = None
        self.__ultimo_acceso = None
        self.__fecha_registro = None

    def validarCedula(self, cedula=None):
        valor = self.__cedula if cedula is None else cedula
        texto = str(valor).strip() if valor is not None else ""

        if not texto or not re.match(r'^[A-Za-z0-9\-\_]{3,20}$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Cédula no válida."
            }

        return {"status": True, "value": texto}

    def validarNombreUsuario(self, nombre_usuario=None):
        valor = self.__nombre_usuario if nombre_usuario is None else nombre_usuario
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El nombre es obligatorio."
            }

        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El nombre no puede contener caracteres especiales."
            }

        # Validación de longitud (máximo 15 caracteres)
        if len(texto) > 15:
            return {
                "status": False,
                "icon": "warning",
                "title": "limite de caracteres alcanzado",
                "text": "limite de caracteres alcanzado"
            }

        return {"status": True, "value": texto}

    def validarApellidoUsuario(self, apellido_usuario=None):
        valor = self.__apellido_usuario if apellido_usuario is None else apellido_usuario
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El apellido es obligatorio."
            }

        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El apellido no puede contener caracteres especiales."
            }

        # Validación de longitud (máximo 15 caracteres)
        if len(texto) > 15:
            return {
                "status": False,
                "icon": "warning",
                "title": "limite de caracteres alcanzado",
                "text": "limite de caracteres alcanzado"
            }

        return {"status": True, "value": texto}

    def validarTelefono(self, telefono=None):
        valor = self.__telefono if telefono is None else telefono
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            return {"status": True, "value": texto}

        if not re.match(r'^[0-9\s\+\-\(\)]{7,20}$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Teléfono no válido."
            }

        return {"status": True, "value": texto}

    def validarDireccion(self, direccion=None):
        valor = self.__direccion if direccion is None else direccion
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            return {"status": True, "value": texto}

        if len(texto) < 3:
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Dirección no válida."
            }

        return {"status": True, "value": texto}

    def validarCorreo(self, correo=None):
        valor = self.__correo if correo is None else correo
        texto = str(valor).strip() if valor is not None else ""

        if not texto:
            return {"status": True, "value": texto}

        if not re.match(r'^[a-zA-Z0-9._%+\-]+@(gmail|outlook|hotmail|yahoo)\.com$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Ingrese un correo válido como gmail.com, outlook.com, hotmail.com o yahoo.com"
            }

        return {"status": True, "value": texto}

    def validarCodRol(self, cod_rol=None):
        valor = self.__cod_rol if cod_rol is None else cod_rol
        texto = str(valor).strip() if valor is not None else ""

        if not texto or not re.match(r'^[1-9]\d*$', texto):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Rol no válido."
            }

        return {"status": True, "value": int(texto)}

    # ===============================
    # GETTERS Y SETTERS
    # ===============================

    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, valor):
        if valor is None:
            self.__cedula = None
            return
        self.__cedula = str(valor).strip()

    @property
    def nombre_usuario(self):
        return self.__nombre_usuario

    @nombre_usuario.setter
    def nombre_usuario(self, valor):
        if valor is None:
            self.__nombre_usuario = None
            return
        self.__nombre_usuario = str(valor).strip()

    @property
    def apellido_usuario(self):
        return self.__apellido_usuario

    @apellido_usuario.setter
    def apellido_usuario(self, valor):
        if valor is None:
            self.__apellido_usuario = None
            return
        self.__apellido_usuario = str(valor).strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None:
            self.__telefono = None
            return
        self.__telefono = str(valor).strip()

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        if valor is None:
            self.__direccion = None
            return
        self.__direccion = str(valor).strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None:
            self.__correo = None
            return
        self.__correo = str(valor).strip()

    @property
    def cod_rol(self):
        return self.__cod_rol

    @cod_rol.setter
    def cod_rol(self, valor):
        if valor is None:
            self.__cod_rol = None
            return
        try:
            self.__cod_rol = int(valor)
        except Exception:
            self.__cod_rol = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    @property
    def password(self):
        return getattr(self, '_PersonalModelo__password', None)

    @password.setter
    def password(self, valor):
        if valor is None:
            self.__password = None
            return
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
    # CONSULTAR
    # ===============================

    def consultar(self):

        cursor = self.conexion.cursor(dictionary=True)

        try:

            cursor.execute("""
                SELECT
                    u.cedula,
                    u.nombre_usuario,
                    u.apellido_usuario,
                    u.telefono,
                    u.direccion,
                    u.correo,
                    u.status,
                    u.cod_rol,
                    r.rol
                FROM seguridad.usuario u
                INNER JOIN seguridad.rol r ON r.cod_rol = u.cod_rol
                WHERE r.rol IN ('gerente', 'empleado')
                  AND u.status IN (0, 1)
                ORDER BY u.nombre_usuario ASC
            """)

            resultados = cursor.fetchall()

            cursor.close()

            return resultados

        except Exception as e:

            print("Error consultar personal:", e)

            cursor.close()

            return []

    # ===============================
    # REGISTRAR
    # ===============================

    def registrar(self):

        cursor = self.conexion.cursor()

        try:

            from datetime import datetime
            ahora = datetime.now()

            # prepare hashed password if provided
            if getattr(self, '_PersonalModelo__password', None):
                try:
                    hashed_password = bcrypt.hashpw(
                        self.__password.encode('utf-8'),
                        bcrypt.gensalt()
                    ).decode('utf-8')
                except Exception:
                    hashed_password = ''
            else:
                hashed_password = ''

            cursor.execute("""
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
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                self.cedula,
                self.nombre_usuario,
                self.apellido_usuario,
                self.telefono,
                self.direccion,
                self.correo,
                self.cod_rol,
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

            print("Error registrar personal:", e)

            self.conexion.rollback()

            cursor.close()

            return False

    # ===============================
    # EDITAR
    # ===============================

    def editar(self):

        cursor = self.conexion.cursor()

        try:

            cursor.execute("""
                UPDATE seguridad.usuario
                SET
                    nombre_usuario = %s,
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

            return 1

        except Exception as e:

            print("Error editar personal:", e)

            self.conexion.rollback()

            cursor.close()

            return False

    # ===============================
    # ELIMINAR
    # ===============================

    def eliminar(self, cedula):

        cursor = self.conexion.cursor()

        try:

            cursor.execute("""
                SELECT COUNT(*)
                FROM especialista
                WHERE cedula_especialista = %s
            """, (cedula,))

            especialista_asociado = cursor.fetchone()[0]

            if especialista_asociado > 0:
                cursor.close()
                return -2

            cursor.execute("""
                UPDATE seguridad.usuario
                SET status = 2
                WHERE cedula = %s
            """, (cedula,))

            self.conexion.commit()

            cursor.close()

            return 1

        except Exception as e:

            print("Error eliminar personal:", e)

            self.conexion.rollback()

            cursor.close()

            return False

    # ===============================
    # OBTENER ROLES
    # ===============================

    def obtener_roles(self):

        cursor = self.conexion.cursor(dictionary=True)

        try:

            cursor.execute("""
                SELECT 
                    cod_rol,
                    rol
                FROM seguridad.rol
                WHERE rol IN ('gerente','empleado')
            """)

            resultados = cursor.fetchall()

            cursor.close()

            return resultados

        except Exception as e:

            print("Error obtener roles:", e)

            cursor.close()

            return []

    # ===============================
    # BUSCAR
    # ===============================

    def buscar(self, cedula):

        cursor = self.conexion.cursor(dictionary=True)

        try:

            cursor.execute("""
                SELECT *
                FROM seguridad.usuario
                WHERE cedula = %s
            """, (cedula,))

            resultado = cursor.fetchone()

            cursor.close()

            return resultado

        except Exception as e:

            print("Error buscar personal:", e)

            cursor.close()

            return None