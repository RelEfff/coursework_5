import psycopg2
from typing import List, Dict
import config

def save_companies(companies: List[Dict]) -> Dict[str, int]:
    """Сохраняет компании в БД и возвращает словарь employer_id -> company_id (из БД)"""
    connection = config.get_connection()
    cursor = connection.cursor()

    id_map = {}  # hh_id -> db_id

    for company in companies:
        name = company.get('name')
        description = company.get('description') or ''
        hh_id = company.get('id')

        cursor.execute(
            "INSERT INTO companies (name, description) VALUES (%s, %s) RETURNING id;",
            (name, description)
        )
        db_id = cursor.fetchone()[0]
        id_map[str(hh_id)] = db_id

    connection.commit()
    cursor.close()
    connection.close()
    return id_map

def save_vacancies(vacancies: List[Dict], company_id: int):
    """Сохраняет вакансии одной компании"""
    connection = config.get_connection()
    cursor = connection.cursor()

    for vacancy in vacancies:
        title = vacancy.get('name')
        url = vacancy.get('alternate_url')
        salary = vacancy.get('salary')
        salary_value = None

        if salary:
            salary_value = salary.get('from') or salary.get('to')

        cursor.execute(
            "INSERT INTO vacancies (title, salary, url, company_id) VALUES (%s, %s, %s, %s);",
            (title, salary_value, url, company_id)
        )

    connection.commit()
    cursor.close()
    connection.close()