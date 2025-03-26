from utils.api import HeadHunterAPI
from utils.db_create import create_database, create_tables
from utils.data_loader import save_companies, save_vacancies
from utils.db_manager import DBManager

# Создание базы данных и таблиц
create_database()
create_tables()

# Список компаний по ID с hh.ru
employers = [
    "1740",     # Яндекс
    "3529",     # Сбер
    "78638",    # Тинькофф
    "80",       # Газпром
    "15478",    # VK
    "1122462",  # Ozon
    "4181",     # Альфа-Банк
    "39305",    # МТС
    "3776",     # РЖД
    "183"       # Ростелеком
]

# Получение данных с API
api = HeadHunterAPI(employers)
companies = api.get_employers()
print(f"\nНайдено компаний: {len(companies)}")

# Сохранение компаний и вакансий
id_map = save_companies(companies)
for hh_id in id_map:
    vacancies = api.get_vacancies(hh_id)  # max_vacancies=50 по умолчанию
    save_vacancies(vacancies, id_map[hh_id])
    print(f"Сохранено вакансий для компании {hh_id}: {len(vacancies)}")

# Работа с базой через DBManager
db = DBManager()

def show_menu():
    print("\n🔸 Что вы хотите сделать?")
    print("1 — Показать компании и количество вакансий")
    print("2 — Показать все вакансии (по 5)")
    print("3 — Показать среднюю зарплату")
    print("4 — Показать вакансии с зарплатой выше средней")
    print("5 — Показать вакансии по ключевому слову")
    print("0 — Выйти")

while True:
    show_menu()
    choice = input("Введите номер действия: ")

    if choice == "1":
        print("\n▶️ Компании и количество вакансий:")
        for row in db.get_companies_and_vacancies_count():
            print(f"{row[0]} — {row[1]} вакансий")

    elif choice == "2":
        print("\n▶️ Все вакансии (по 5 штук):")
        all_vacancies = db.get_all_vacancies()
        index = 0
        while index < len(all_vacancies):
            for row in all_vacancies[index:index+5]:
                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
            index += 5
            if index >= len(all_vacancies):
                print("\n🔚 Конец списка.")
                break
            if input("Enter — продолжить, 'q' — выйти: ").lower() == 'q':
                break

    elif choice == "3":
        print("\n▶️ Средняя зарплата:")
        print(db.get_avg_salary())

    elif choice == "4":
        print("\n▶️ Вакансии с зарплатой выше средней:")
        for row in db.get_vacancies_with_higher_salary():
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

    elif choice == "5":
        keyword = input("Введите ключевое слово для поиска: ")
        print(f"\n▶️ Вакансии по ключу '{keyword}':")
        for row in db.get_vacancies_with_keyword(keyword):
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

    elif choice == "0":
        print("До свидания!")
        break

    else:
        print("Неверный выбор, попробуйте снова.")

db.close()