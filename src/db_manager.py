import psycopg2

""" класс DBManager, который подключается к БД PostgreSQL и имеет следующие методы:
    get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий у каждой компании.
    get_all_vacancies() — получает список всех вакансий с указанием названия компании,
    названия вакансии и зарплаты и ссылки на вакансию.
    get_avg_salary() — получает среднюю зарплату по вакансиям.
    get_vacancies_with_higher_salary() — получает список всех вакансий,
    у которых зарплата выше средней по всем вакансиям.
    get_vacancies_with_keyword() — получает список всех вакансий,
    в названии которых содержатся переданные в метод слова, например python.
"""


class DBManager:

    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = psycopg2.connect(database=self.database_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT employer_name, COUNT(*) AS number_of_vacancies "
                                "FROM vacancies "
                                "JOIN employers USING(employer_id) "
                                "GROUP BY employer_name")
                    rows = cur.fetchall()
                    # print(rows)
        finally:
            conn.close()
        return rows

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(database=self.database_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT employer_name, job_title, salary, vacancy_url "
                                "FROM vacancies JOIN employers USING(employer_id)")
                    rows = cur.fetchall()
                    # print(rows)
        finally:
            conn.close()
        return rows

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(database=self.database_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT AVG(salary) AS average_salary FROM vacancies")
                    rows = cur.fetchall()
                    # print(rows)
        finally:
            conn.close()
        return rows

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(database=self.database_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies"
                                "WHERE salary > (SELECT AVG(salary) FROM vacancies)")
                    rows = cur.fetchall()
                    # print(rows)
        finally:
            conn.close()
        return rows

    def get_vacancies_with_keyword(self, word):
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова.
        """
        conn = psycopg2.connect(database=self.database_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    sql = (f"SELECT * FROM vacancies JOIN employers USING (employer_id) "
                           f"WHERE job_title LIKE '%{word}%'")
                    cur.execute(sql)
                    rows = cur.fetchall()
                    # print(rows)
        finally:
            conn.close()
        return rows
