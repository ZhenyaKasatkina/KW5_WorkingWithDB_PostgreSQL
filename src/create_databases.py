import psycopg2

from src.valid_vacancy import Vacancies
from typing import Any


def create_database(database_name: str, params: dict):
    """
    Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях.
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    # cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:          # таблица работодателей
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL
            )
        """)
    with conn.cursor() as cur:          # таблица вакансий
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                job_title VARCHAR(255) NOT NULL,
                salary INT,
                town VARCHAR(100),
                vacancy_url TEXT NOT NULL
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """
    Сохранение данных о работодателях и вакансиях в базу данных.
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for item in data:
            # print(item)
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name)
                VALUES (%s, %s)
                RETURNING employer_id
                """,
                (item["employer"]["id"], item["employer"]["name"])
            )
            # vacancy_id = cur.fetchone()[0]
            vacancies_data = item['vacancies']
            for vacancy in vacancies_data:
                valid_vacancy = Vacancies(vacancy["name"], vacancy["salary"]["from"],
                                          vacancy["salary"]["to"], vacancy["area"]["name"],
                                          vacancy["alternate_url"])         # валидация данных вакансии
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, employer_id, job_title, salary,
                    town, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy['id'], vacancy["employer"]["id"], valid_vacancy.job_title.lower(),
                     valid_vacancy.salary,
                     valid_vacancy.town.capitalize(), valid_vacancy.url)
                )

    conn.commit()
    conn.close()
