from admin.config.conexion import Conexion
import re

class ProveedorModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_proveedor = None
        self.__cedula = None
        self.__nombre = None
        self.__apellido = None
        self.__rif = None
        self.__telefono = None
        self.__correo = None
        self.__status = None

    # ===============================
    # VALIDACIONES
    # ===============================

    def validarCedula(self, cedula):

        cedula = str(cedula).strip()


        if cedula == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar la cédula del proveedor."
            }


        if not re.match(r'^\d{6,8}$', cedula):

            return {
                "status": False,
                "icon": "warning",
                "title": "Cédula inválida",
                "text": "La cédula debe contener entre 6 y 8 números."
            }


        return {
            "status": True
        }



    def validarNombre(self, nombre):

        nombre = nombre.strip()


        if nombre == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el nombre del proveedor."
            }



        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', nombre):

            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El nombre solo puede contener letras."
            }


        return {
            "status": True
        }



    def validarApellido(self, apellido):

        apellido = apellido.strip()


        if apellido == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el apellido del proveedor."
            }



        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', apellido):

            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El apellido solo puede contener letras."
            }


        return {
            "status": True
        }



    def validarRif(self, rif):

        rif = rif.strip()


        if rif == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el RIF."
            }



        # Ejemplo: J123456789 / V123456789
        if not re.match(r'^[VEJPGvejpg]\d{8,9}$', rif):

            return {
                "status": False,
                "icon": "warning",
                "title": "RIF inválido",
                "text": "El RIF debe tener formato válido (Ej: J123456789)."
            }



        return {
            "status": True
        }



    def validarTelefono(self, telefono):

        telefono = str(telefono).strip()


        if telefono == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el teléfono."
            }



        if not re.match(r'^\d{10,11}$', telefono):

            return {
                "status": False,
                "icon": "warning",
                "title": "Teléfono inválido",
                "text": "El teléfono debe contener entre 10 y 11 números."
            }



        return {
            "status": True
        }




    def validarCorreo(self, correo):

        correo = correo.strip()


        if correo == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el correo."
            }



        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'


        if not re.match(patron, correo):

            return {
                "status": False,
                "icon": "warning",
                "title": "Correo inválido",
                "text": "Ingrese un correo electrónico válido."
            }



        return {
            "status": True
        }
    # ===============================
    # GETTERS Y SETTERS
    # ===============================

    @property
    def cod_proveedor(self):
        return self.__cod_proveedor

    @cod_proveedor.setter
    def cod_proveedor(self, valor):
        self.__cod_proveedor = valor

    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, valor):
        self.__cedula = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        self.__apellido = valor

    @property
    def rif(self):
        return self.__rif

    @rif.setter
    def rif(self, valor):
        self.__rif = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        self.__correo = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor

    # ===============================
    # CONSULTAR
    # ===============================

    def consultar(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM proveedor")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    # ===============================
    # BUSCAR
    # ===============================

    def buscar(self, cedula):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM proveedor
            WHERE cedula = %s
        """, (cedula,))

        resultado = cursor.fetchone()
        cursor.close()

        return resultado

    # ===============================
    # REGISTRAR
    # ===============================

    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                INSERT INTO proveedor (cedula, nombre, apellido, rif, telefono, correo, status)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
            """, (
                self.__cedula,
                self.__nombre,
                self.__apellido,
                self.__rif,
                self.__telefono,
                self.__correo
            ))

            self.conexion.commit()
            cursor.close()
            return 1

        except Exception as e:
            print("Error al registrar proveedor:", e)
            return 0

    # ===============================
    # EDITAR
    # ===============================

    def editar(self):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE proveedor 
                SET cedula = %s,
                    nombre = %s,
                    apellido = %s,
                    rif = %s,
                    telefono = %s,
                    correo = %s,
                    status = %s
                WHERE cod_proveedor = %s
            """, (
                self.__cedula,
                self.__nombre,
                self.__apellido,
                self.__rif,
                self.__telefono,
                self.__correo,
                self.__status,
                self.__cod_proveedor
            ))

            self.conexion.commit()
            cursor.close()
            return 1

        except Exception as e:
            print("Error al editar proveedor:", e)
            return 0

    # ===============================
    # ELIMINAR
    # ===============================

    def eliminar(self, cod_proveedor):
        try:
            cursor = self.conexion.cursor()

            cursor.execute("""
                DELETE FROM proveedor
                WHERE cod_proveedor = %s
            """, (cod_proveedor,))

            self.conexion.commit()
            cursor.close()

            return "eliminado"

        except Exception as e:
            print("Error eliminar proveedor:", e)
            return "error"