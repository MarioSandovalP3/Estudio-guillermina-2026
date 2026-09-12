from admin.config.conexion import Conexion
import os
from werkzeug.utils import secure_filename     
import re
from os.path import splitext

class EmpresaModelo(Conexion):

    def __init__(self):
        super().__init__()
       

        # Atributos privados
        self.__nombre = None
        self.__direccion = None
        self.__email = None
        self.__telefono = None
        self.__descripcion_empresa = None
        self.__logo = None
        self.__fecha_actualizacion = None


    def validarEmpresa(self, nombre, direccion, email, telefono, descripcion, logo):

        errores = []

        # Nombre (letras, espacios y signos. No números)
        if nombre and re.search(r'\d', nombre):
            errores.append("• El nombre de la empresa no puede contener números.")

        # Email
        if email and not re.fullmatch(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            email
        ):
            errores.append("• El correo electrónico no es válido.")

        # Teléfono
        if telefono and not telefono.isdigit():
            errores.append("• El teléfono solo puede contener números.")

        # Logo
        if logo and logo.filename:

            extension = splitext(logo.filename)[1].lower()

            if extension not in (".png", ".jpg", ".jpeg"):
                errores.append("• El logo debe ser una imagen PNG, JPG o JPEG.")

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
    # GETTERS Y SETTERS
    # ===============================

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor


    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        self.__direccion = valor


    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        self.__email = valor


    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor


    @property
    def descripcion_empresa(self):
        return self.__descripcion_empresa

    @descripcion_empresa.setter
    def descripcion_empresa(self, valor):
        self.__descripcion_empresa = valor


    @property
    def logo(self):
        return self.__logo

    @logo.setter
    def logo(self, valor):
        self.__logo = valor

    @property
    def fecha_actualizacion(self):
        return self.__fecha_actualizacion

    @fecha_actualizacion.setter
    def fecha_actualizacion(self, valor):
        self.__fecha_actualizacion = valor

  
  # ===============================
    # CRUD
    # ===============================

    def mostrar(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empresa")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

  # ===============================
    # SUBIR LOGO
    # ===============================
    def subir_logo(self, file):
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            ruta = os.path.join("static/assets/img/", filename)

            file.save(ruta)
            self.__logo = ruta

    def buscar(self):
        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(*) as total 
            FROM empresa
        """)

        resultado = cursor.fetchone()
        cursor.close()

        return resultado

    def registrar(self):
        try:
            cursor = self.conexion.cursor()

            sql = """
                INSERT INTO empresa
                (nombre, direccion, telefono, email, descripcion_empresa, logo, fecha_actualizacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                self.__nombre,
                self.__direccion,
                self.__telefono,
                self.__email,
                self.__descripcion_empresa,
                self.__logo,
                self.__fecha_actualizacion
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al registrar empresa:", e)
            return 0
        
  # ===============================
    # EDITAR
    # ===============================
    def editar(self, nombre_original):
        try:
            cursor = self.conexion.cursor()

            sql = """
                UPDATE empresa 
                SET nombre=%s, direccion=%s, telefono=%s, email=%s, descripcion_empresa=%s, logo=%s
                WHERE nombre=%s
            """

            cursor.execute(sql, (
                self.__nombre,
                self.__direccion,
                self.__telefono,
                self.__email,
                self.__descripcion_empresa,
                self.__logo,
                nombre_original
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar empresa:", e)
            return 0