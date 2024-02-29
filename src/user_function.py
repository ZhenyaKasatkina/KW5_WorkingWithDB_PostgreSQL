from src.hh_api import HeadHunterAPI
from src.config import config
from src.create_databases import create_database, save_data_to_database
from src.db_manager import DBManager


def check_range_and_num(range_from: int, range_to: int):
    """
    Проверка введенных данных на значение - число и диапазон
    """
    while True:
        number = input("Введи номер(число) своего выбора:  ")
        if not number.isdigit():
            print(f"Должно быть число, попробуй еще раз")
        elif int(number) < range_from or int(number) > range_to:
            print(f"Такого числа в диапазоне нет, попробуй еще раз")
        else:
            break
    return number


def user_func(companies):
    print('Привет! Получаем данные о вакансиях на hh.ru,\n'
          'где работодателями являются следующие организации:\n'
          '"Планетра", "ЛАНИТ", "Фабрика решений", "InlyIT", "Тензор", "Инспектор Клауд",\n'
          '"ВЕБ Инфраструктура", "БИЗНЕС КОНТЕНТ", "Syntella", "ANA BAR", "Wanted",\n'
          '"НИИ Масштаб", "SberTech", "Тинькофф", "Банк ВТБ (ПАО)", "Сбер. IT",\n'
          '"МГТС", "Совкомбанк Технологии", "Эвотор"\n'
          'и формируем БД "vacancies_with_hh"\n'
          'ЖДЁМ...\n')
    hh_data = HeadHunterAPI(companies)
    ads_data = hh_data.get_vacancies_data()
    # print(ads_data)

    params = config()
    create_database("vacancies_with_hh", params)
    save_data_to_database(ads_data, "vacancies_with_hh", params)
    print('БД "vacancies_with_hh" сформирована.')
    while True:
        print('\nВыбери параметр для работы с БД:\n'
              '1. получить список всех компаний и количество вакансий у каждой компании.\n'
              '2. получить список всех вакансий с указанием названия компании, '
              'названия вакансии и зарплаты и ссылки на вакансию.\n'
              '3. получить среднюю зарплату по вакансиям.\n'
              '4. получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n'
              '5. получить список всех вакансий, в названии которых содержатся переданные в метод слово.\n'
              '6. завершить работу программы\n')
        choice = ['1. список всех компаний и количество вакансий у каждой компании.\n',
                  '2. список всех вакансий с указанием названия компании, '
                  'названия вакансии и зарплаты и ссылки на вакансию.\n',
                  '3. средняя заработная плата по вакансиям.\n',
                  '4. список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n',
                  '5. список всех вакансий, в названии которых содержатся введенное пользователем слово.\n',
                  '6. завершить работу программы\n']
        number_choice = int(check_range_and_num(1, 6))
        print(f"\nTвой выбор: {choice[int(number_choice) - 1]}")
        manager = DBManager("vacancies_with_hh", params)
        if number_choice == 1:
            data = manager.get_companies_and_vacancies_count()
            for item in data:
                print(item)

        elif number_choice == 2:
            data = manager.get_all_vacancies()
            for item in data:
                print(item)

        elif number_choice == 3:
            data = manager.get_avg_salary()
            print(data)

        elif number_choice == 4:
            data = manager.get_vacancies_with_higher_salary()
            for item in data:
                print(item)

        elif number_choice == 5:
            word_user = str(input("Введите слово для фильтрации: ").lower())
            data = manager.get_vacancies_with_keyword(word_user)
            if not data:
                print("Нет данных, соответствующих заданным критериям")
            else:
                for item in data:
                    print(item)

        else:
            print('Программа завершена. БД "vacancies_with_hh" закрыта')
            break
