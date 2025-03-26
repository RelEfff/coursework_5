import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config

def create_database():
    connection = psycopg2.connect(dsn=config.DB_DSN, dbname='postgres')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{config.DB_NAME}';")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f'CREATE DATABASE {config.DB_NAME};')
        print(f"База данных '{config.DB_NAME}' создана.")
    else:
        print(f"База данных '{config.DB_NAME}' уже существует.")

    cursor.close()
    connection.close()

def create_tables():
    connection = config.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            salary INTEGER,
            url TEXT,
            company_id INTEGER REFERENCES companies(id)
        );
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("Таблицы успешно созданы.")