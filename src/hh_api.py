import requests

"""
Получает данные о работодателях и их вакансиях с сайта hh.ru. 
Для этого используйте публичный API hh.ru и библиотеку requests.
"""


class HeadHunterAPI:

    def __init__(self, companies: list[str]):
        self.companies = companies

    def get_employers_data(self):
        """
        Получает данные о работодателях
        с сайта HH через API по названию компаний
        """
        list_employers = []
        for company in self.companies:
            params = {
                "found": 1,
                "per_page": 50,
                "page": 0,
                "text": str(company),
                "only_with_vacancies": "true",
                "items": [{}]
            }
            bases_url = 'https://api.hh.ru/'
            method_name = "employers"
            response = requests.get(f"{bases_url}{method_name}", params=params)
            # print(response.json(), len(response.json()))
            # print(response.status_code)
            list_employers.extend(response.json()["items"])
        return list_employers

    def get_vacancies_data(self):
        """
        Получает вакансии
        с сайта HH через API (по id работодателя)
        и возвращает список словарей: работодатель и данные по его вакансиям
        """
        employers = self.get_employers_data()
        data = []

        for employer in employers:
            count_page = 0
            vacancies_data = []
            while count_page < 15:
                params = {
                    "per_page": 100,
                    "page": count_page,
                    "employer_id": employer["id"],
                    "only_with_salary": "true",
                    "items": [{}]
                }

                bases_url = 'https://api.hh.ru/'
                method_name = "vacancies"
                response = requests.get(f"{bases_url}{method_name}", params=params)
                # print(response.json(), len(response.json()), count_page)
                # print(response.status_code)
                if response.json()["items"]:
                    vacancies_data.extend(response.json()["items"])
                    count_page += 1
                else:
                    break
            data.append({'employer': employer,
                         'vacancies': vacancies_data})
        return data
