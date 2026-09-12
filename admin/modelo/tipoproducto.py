from admin.config.conexion import Conexion
import re


class TipoProductoModelo(Conexion):

    def __init__(self):
        super().__init__()

        self.__cod_tipo_producto = None
        self.__nombre_tipo_producto = None
        self.__status = None


    # =====================================
    # VALIDACIONES
    # =====================================

    def validarNombreTipoProducto(self, nombre_tipo_producto):

        nombre_tipo_producto = nombre_tipo_producto.strip()


        if nombre_tipo_producto == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Campo vacío",
                "text": "Debe ingresar el nombre del tipo de producto."
            }


        if re.search(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]', nombre_tipo_producto):

            return {
                "status": False,
                "icon": "warning",
                "title": "Dato inválido",
                "text": "El tipo de producto no puede contener números ni caracteres especiales."
            }


        if len(nombre_tipo_producto) < 3:

            return {
                "status": False,
                "icon": "warning",
                "title": "Nombre corto",
                "text": "El nombre debe tener mínimo 3 caracteres."
            }


        if len(nombre_tipo_producto) > 50:

            return {
                "status": False,
                "icon": "warning",
                "title": "Nombre demasiado largo",
                "text": "El nombre no puede superar los 50 caracteres."
            }


        return {
            "status": True
        }



    def validarCodigo(self, codigo):

        if codigo is None or codigo == "":

            return {
                "status": False,
                "icon": "warning",
                "title": "Código vacío",
                "text": "El código del tipo de producto es obligatorio."
            }


        if not str(codigo).isdigit():

            return {
                "status": False,
                "icon": "warning",
                "title": "Código inválido",
                "text": "El código debe ser numérico."
            }


        return {
            "status": True
        }



    # =====================================
    # GETTERS Y SETTERS
    # =====================================

    @property
    def cod_tipo_producto(self):
        return self.__cod_tipo_producto

    @cod_tipo_producto.setter
    def cod_tipo_producto(self, valor):
        self.__cod_tipo_producto = valor


    @property
    def nombre_tipo_producto(self):
        return self.__nombre_tipo_producto

    @nombre_tipo_producto.setter
    def nombre_tipo_producto(self, valor):

        if valor:
            valor = valor.strip()

        self.__nombre_tipo_producto = valor



    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = valor



    # =====================================
    # CONSULTAR
    # =====================================

    def consultar(self):

        cursor = self.conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                cod_tipo_producto,
                nombre_tipo_producto,
                status
            FROM tipo_producto
        """)

        resultados = cursor.fetchall()

        cursor.close()

        return resultados



    # =====================================
    # BUSCAR
    # =====================================

    def buscar(self, nombre_tipo_producto):

        cursor = self.conexion.cursor(dictionary=True)


        cursor.execute("""
            SELECT *
            FROM tipo_producto
            WHERE nombre_tipo_producto = %s
        """, (
            nombre_tipo_producto,
        ))


        resultado = cursor.fetchone()

        cursor.close()

        return resultado



    # =====================================
    # REGISTRAR
    # =====================================

    def registrar(self):


        validacion = self.validarNombreTipoProducto(
            self.__nombre_tipo_producto
        )


        if not validacion["status"]:
            return validacion



        try:

            cursor = self.conexion.cursor()


            cursor.execute("""
                INSERT INTO tipo_producto
                (
                    nombre_tipo_producto,
                    status
                )
                VALUES
                (
                    %s,
                    1
                )
            """,(
                self.__nombre_tipo_producto,
            ))


            self.conexion.commit()

            cursor.close()


            return {
                "status": True,
                "icon": "success",
                "title": "Registrado",
                "text": "Tipo de producto registrado correctamente."
            }



        except Exception as e:


            print(
                "Error registrar tipo producto:",
                e
            )


            return {
                "status": False,
                "icon": "error",
                "title": "Error",
                "text": "No se pudo registrar el tipo de producto."
            }



    # =====================================
    # EDITAR
    # =====================================

    def editar(self):


        validacion_nombre = self.validarNombreTipoProducto(
            self.__nombre_tipo_producto
        )


        if not validacion_nombre["status"]:
            return validacion_nombre



        validacion_codigo = self.validarCodigo(
            self.__cod_tipo_producto
        )


        if not validacion_codigo["status"]:
            return validacion_codigo



        try:


            cursor = self.conexion.cursor()



            cursor.execute("""
                UPDATE tipo_producto
                SET 
                    nombre_tipo_producto = %s,
                    status = %s
                WHERE cod_tipo_producto = %s
            """,(
                self.__nombre_tipo_producto,
                self.__status,
                self.__cod_tipo_producto
            ))



            self.conexion.commit()


            cursor.close()


            return {
                "status": True,
                "icon": "success",
                "title": "Actualizado",
                "text": "Tipo de producto actualizado correctamente."
            }



        except Exception as e:


            print(
                "Error editar tipo producto:",
                e
            )


            return {
                "status": False,
                "icon": "error",
                "title": "Error",
                "text": "No se pudo actualizar."
            }



    # =====================================
    # ELIMINAR
    # =====================================

    def eliminar(self, cod_tipo_producto):

        validacion = self.validarCodigo(
            cod_tipo_producto
        )


        if not validacion["status"]:
            return validacion



        try:


            cursor = self.conexion.cursor(dictionary=True)



            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM detalle_producto
                WHERE cod_tipo_producto = %s
            """,(
                cod_tipo_producto,
            ))


            resultado = cursor.fetchone()


            total = resultado["total"] if resultado else 0



            if total > 0:


                cursor.close()


                return {
                    "status": False,
                    "icon": "warning",
                    "title": "No se puede eliminar",
                    "text": "Este tipo de producto tiene productos asociados."
                }




            cursor.execute("""
                DELETE FROM tipo_producto
                WHERE cod_tipo_producto = %s
            """,(
                cod_tipo_producto,
            ))



            self.conexion.commit()


            cursor.close()



            return {
                "status": True,
                "icon": "success",
                "title": "Eliminado",
                "text": "Registro eliminado correctamente."
            }




        except Exception as e:


            print(
                "Error eliminar tipo producto:",
                e
            )


            return {
                "status": False,
                "icon": "error",
                "title": "Error",
                "text": "No se pudo eliminar el registro."
            }