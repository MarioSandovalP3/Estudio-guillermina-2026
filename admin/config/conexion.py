import mysql.connector
from admin.config.config import DB_HOST, DB_USER, DB_PASS, DB_NAME

class Conexion:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )