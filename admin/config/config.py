import os
import sys

from dotenv import load_dotenv # instalar liberia python-dotenv

load_dotenv()

# Configuración zona horaria
if sys.platform != "win32":
    import time
    time.tzset()

DB_HOST = os.getenv("DB_HOST")

DB_USER = os.getenv("DB_USER")

DB_PASS = os.getenv("DB_PASS")

DB_NAME = os.getenv("DB_NAME")