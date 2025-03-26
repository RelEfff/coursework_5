import requests
from typing import List, Dict


class HeadHunterAPI:
    BASE_URL = "https://api.hh.ru"

    def __init__(self, employers_ids: List[str]):
        self.employers_ids = employers_ids

    def get_employers(self) -> List[Dict]:
        employers = []
        for employer_id in self.employers_ids:
            response = requests.get(f"{self.BASE_URL}/employers/{employer_id}")
            if response.status_code == 200:
                employers.append(response.json())
            else:
                print(f"Ошибка при получении работодателя {employer_id}")
        return employers

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        vacancies = []
        page = 0
        while True:
            response = requests.get(
                f"{self.BASE_URL}/vacancies",
                params={"employer_id": employer_id, "page": page, "per_page": 100}
            )
            data = response.json()
            vacancies.extend(data.get("items", []))
            if data.get("pages") and page < data["pages"] - 1:
                page += 1
            else:
                break
        return vacancies