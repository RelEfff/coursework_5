import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

    def get_companies_and_vacancies_count(self):
        """Список компаний и количество вакансий у каждой"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, COUNT(vacancies.id) 
                FROM companies
                LEFT JOIN vacancies ON companies.id = vacancies.company_id
                GROUP BY companies.name;
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """Список всех вакансий с указанием компании, зарплаты и ссылки"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """Средняя зарплата по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;")
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Вакансии с зарплатой выше средней"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
                WHERE salary > (
                    SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL
                );
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Вакансии по ключевому слову"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
                WHERE LOWER(vacancies.title) LIKE %s;
            """, (f'%{keyword.lower()}%',))
            return cur.fetchall()

    def close(self):
        self.conn.close()