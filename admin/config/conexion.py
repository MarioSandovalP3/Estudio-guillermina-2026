import mysql.connector
from admin.config.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASS,
    DB_NAME,
    DB_SSL_MODE,
)

class Conexion:
    def __init__(self):
        parametros = {
            "host": DB_HOST,
            "port": DB_PORT,
            "user": DB_USER,
            "password": DB_PASS,
            "database": DB_NAME,
        }

        if DB_SSL_MODE == "REQUIRED":
            parametros["ssl_disabled"] = False

        self.conexion = mysql.connector.connect(**parametros)