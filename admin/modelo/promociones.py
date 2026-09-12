import os
from werkzeug.utils import secure_filename
from admin.config.conexion import Conexion


class PromocionModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_promo = None
        self.__descuento = None
        self.__nombre_promo = None
        self.__descripcion_promo = None
        self.__imagen_promo = None
        self.__inicio_promo = None
        self.__fin_promo = None
        self.__status = None

    # ===============================
    # GETTERS Y SETTERS
    # ===============================

    @property
    def cod_promo(self):
        return self.__cod_promo

    @cod_promo.setter
    def cod_promo(self, valor):
        self.__cod_promo = valor

    @property
    def descuento(self):
        return self.__descuento

    @descuento.setter
    def descuento(self, valor):
        self.__descuento = valor

    @property
    def nombre_promo(self):
        return self.__nombre_promo

    @nombre_promo.setter
    def nombre_promo(self, valor):
        self.__nombre_promo = valor

    @property
    def descripcion_promo(self):
        return self.__descripcion_promo

    @descripcion_promo.setter
    def descripcion_promo(self, valor):
        self.__descripcion_promo = valor

    @property
    def imagen_promo(self):
        return self.__imagen_promo

    @imagen_promo.setter
    def imagen_promo(self, valor):
        self.__imagen_promo = valor

    @property
    def inicio_promo(self):
        return self.__inicio_promo

    @inicio_promo.setter
    def inicio_promo(self, valor):
        self.__inicio_promo = valor

    @property
    def fin_promo(self):
        return self.__fin_promo

    @fin_promo.setter
    def fin_promo(self, valor):
        self.__fin_promo = valor

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

        cursor.execute("""
            SELECT *
            FROM promocion
        """)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados

    # ===============================
    # OBTENER POR ID
    # ===============================

    def obtener(self, cod_promo):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM promocion
            WHERE cod_promo = %s
        """, (cod_promo,))

        resultado = cursor.fetchone()
        cursor.close()

        return resultado

    # ===============================
    # BUSCAR
    # ===============================

    def buscar(self, nombre_promo):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM promocion
            WHERE nombre_promo = %s
        """, (nombre_promo,))

        resultado = cursor.fetchone()
        cursor.close()

        return resultado

    # ===============================
    # VALIDACIONES
    # ===============================

    def validarNombrePromo(self, nombre_promo):
        nombre_promo = str(nombre_promo).strip() if nombre_promo is not None else ""

        if nombre_promo == "":
            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el nombre de la promoción."
            }

        if len(nombre_promo) > 100:
            return {
                "status": False,
                "icon": "warning",
                "title": "Nombre muy largo",
                "text": "El nombre de la promoción no puede superar los 100 caracteres."
            }

        if not all(car.isalnum() or car.isspace() for car in nombre_promo):
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "Solo se aceptan letras, números y espacios."
            }

        return {"status": True}

    def validarDescripcionPromo(self, descripcion_promo):
        descripcion_promo = str(descripcion_promo).strip() if descripcion_promo is not None else ""

        if len(descripcion_promo) > 250:
            return {
                "status": False,
                "icon": "warning",
                "title": "Descripción muy larga",
                "text": "La descripción no puede superar los 250 caracteres."
            }

        return {"status": True}

    def validarDescuento(self, descuento):
        descuento = str(descuento).strip() if descuento is not None else ""

        if descuento == "":
            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar un descuento."
            }

        if not descuento.isdigit():
            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El descuento solo debe contener números."
            }

        if len(descuento) > 3:
            return {
                "status": False,
                "icon": "warning",
                "title": "Descuento inválido",
                "text": "El descuento no puede superar 3 dígitos."
            }

        if int(descuento) > 100:
            return {
                "status": False,
                "icon": "warning",
                "title": "Descuento inválido",
                "text": "El descuento no puede ser mayor a 100%."
            }

        return {"status": True}

    def validarFechasPromo(self, inicio_promo, fin_promo):
        from datetime import datetime

        if not inicio_promo or not fin_promo:
            return {
                "status": False,
                "icon": "warning",
                "title": "Fechas requeridas",
                "text": "Debe seleccionar la fecha de inicio y la fecha final."
            }

        try:
            fecha_inicio = datetime.strptime(str(inicio_promo), "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(str(fin_promo), "%Y-%m-%d").date()
        except ValueError:
            return {
                "status": False,
                "icon": "warning",
                "title": "Fechas inválidas",
                "text": "Las fechas ingresadas no tienen un formato válido."
            }

        hoy = datetime.today().date()

        if fecha_inicio < hoy:
            return {
                "status": False,
                "icon": "warning",
                "title": "Fecha inválida",
                "text": "La fecha de inicio no puede ser anterior a hoy."
            }

        if fecha_fin < fecha_inicio:
            return {
                "status": False,
                "icon": "warning",
                "title": "Fecha inválida",
                "text": "La fecha final no puede ser anterior a la fecha de inicio."
            }

        return {"status": True}

    def validarImagenPromo(self, imagen):
        if imagen is None or getattr(imagen, "filename", None) in [None, ""]:
            return {"status": True}

        extensiones_permitidas = {"jpg", "jpeg", "png", "webp"}
        nombre_archivo = str(imagen.filename).lower()
        extension = nombre_archivo.rsplit(".", 1)[-1] if "." in nombre_archivo else ""

        if extension not in extensiones_permitidas:
            return {
                "status": False,
                "icon": "warning",
                "title": "Formato inválido",
                "text": "La imagen solo puede ser JPG, JPEG, PNG o WEBP."
            }

        return {"status": True}

    # ===============================
    # SUBIR IMAGEN
    # ===============================

    def subir_imagen(self, archivo):

        try:

            carpeta = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "static",
                "assets",
                "img",
                "promociones"
            ))

            os.makedirs(carpeta, exist_ok=True)

            nombre_archivo = secure_filename(archivo.filename)

            ruta = os.path.join(carpeta, nombre_archivo)

            archivo.save(ruta)

            return nombre_archivo

        except Exception as e:
            print("Error al subir imagen:", e)
            return None

    # ===============================
    # REGISTRAR
    # ===============================

    def registrar(self):

        try:

            cursor = self.conexion.cursor()

            cursor.execute("""
                INSERT INTO promocion
                (
                    descuento,
                    nombre_promo,
                    descripcion_promo,
                    imagen_promo,
                    inicio_promo,
                    fin_promo,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    1
                )
            """, (
                self.__descuento,
                self.__nombre_promo,
                self.__descripcion_promo,
                self.__imagen_promo,
                self.__inicio_promo,
                self.__fin_promo
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al registrar promoción:", e)
            return 0

    # ===============================
    # EDITAR
    # ===============================

    def editar(self):

        try:

            cursor = self.conexion.cursor()

            cursor.execute("""
                UPDATE promocion
                SET descuento = %s,
                    nombre_promo = %s,
                    descripcion_promo = %s,
                    imagen_promo = %s,
                    inicio_promo = %s,
                    fin_promo = %s,
                    status = %s
                WHERE cod_promo = %s
            """, (
                self.__descuento,
                self.__nombre_promo,
                self.__descripcion_promo,
                self.__imagen_promo,
                self.__inicio_promo,
                self.__fin_promo,
                self.__status,
                self.__cod_promo
            ))

            self.conexion.commit()
            cursor.close()

            return 1

        except Exception as e:
            print("Error al editar promoción:", e)
            return 0

    # ===============================
    # ELIMINAR
    # ===============================

    def eliminar(self, cod_promo):

        try:

            cursor = self.conexion.cursor()

            cursor.execute("""
                DELETE FROM promocion
                WHERE cod_promo = %s
            """, (cod_promo,))

            self.conexion.commit()
            cursor.close()

            return "eliminado"

        except Exception as e:
            print("Error eliminar promoción:", e)
            return "error"