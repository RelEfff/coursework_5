import os
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Читаем переменные окружения
DB_NAME = os.getenv("DB_NAME", "default_db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Формируем строку подключения
DB_DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Функция для создания подключения к БД
def get_connection(dbname=None):
    dsn = DB_DSN if dbname is None else DB_DSN.replace(DB_NAME, dbname)
    return psycopg2.connect(dsn=dsn)
