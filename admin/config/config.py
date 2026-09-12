import os
import sys

from dotenv import load_dotenv # instalar liberia python-dotenv

load_dotenv()

# Configuración zona horaria
if sys.platform != "win32":
    import time
    time.tzset()

DB_HOST = os.getenv("DB_HOST")

DB_PORT = int(os.getenv("DB_PORT", "3306"))

DB_USER = os.getenv("DB_USER")

DB_PASS = os.getenv("DB_PASS")

DB_NAME = os.getenv("DB_NAME")

DB_SSL_MODE = os.getenv("DB_SSL_MODE", "DISABLED").upper()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this-key")

FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"