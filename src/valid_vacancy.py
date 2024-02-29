

class Vacancies:

    def __init__(self, job_title: str, salary_from: int | None, salary_to: int | None,
                 town: str, url: str) -> None:

        self.job_title = job_title                              # должность
        self.salary_from = self._is_valid_salary(salary_from)   # зарплата ОТ
        self.salary_to = self._is_valid_salary(salary_to)       # зарплата ДО
        self.salary = self.compare_salary()                     # максимальная ЗП из указанной в объявлении
        self.town = self._is_valid_town(town)                   # город
        self.url = self._is_valid_url(url)                      # ссылка на объявление

    @staticmethod
    def _is_valid_salary(salary):
        """Проверка заработной платы на предмет указания ее размера"""
        if not salary:
            salary = 0
        return int(salary)

    @staticmethod
    def _is_valid_town(town):
        """Проверка города на предмет его указания"""
        if not town:
            town = "Город не указан"
        return town

    @staticmethod
    def _is_valid_url(url):
        """Проверка ссылки на объявление на предмет её указания"""
        if not url:
            url = "Ссылка на объявление не указана"
        return url

    def compare_salary(self):
        """Сравниваем указанную в одном объявлении заработную плату
        от ... с до ..., и выводим большую по значению ЗП"""
        if self.salary_from > self.salary_to:
            return self.salary_from
        else:
            return self.salary_to
