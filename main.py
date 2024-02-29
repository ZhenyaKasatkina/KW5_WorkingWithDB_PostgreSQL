from src.hh_api import HeadHunterAPI
from src.config import config
from src.create_databases import create_database, save_data_to_database
from src.db_manager import DBManager

companies = ["Планетра", "ЛАНИТ", "Фабрика решений", "InlyIT", "Тензор", "Инспектор Клауд",
             "ВЕБ Инфраструктура", "БИЗНЕС КОНТЕНТ", "Syntella", "ANA BAR", "Wanted",
             "НИИ Масштаб", "SberTech", "Тинькофф", "Банк ВТБ (ПАО)", "Сбер. IT",
             "МГТС", "Совкомбанк Технологии", "Эвотор"]


def main():
    hh_data = HeadHunterAPI(companies)
    ads_data = hh_data.get_vacancies_data()
    # print(ads_data)

    params = config()

    create_database("vacancies_with_hh", params)
    save_data_to_database(ads_data, "vacancies_with_hh", params)

    manager = DBManager("vacancies_with_hh", params)
    # y = manager.get_companies_and_vacancies_count()
    # y = manager.get_all_vacancies()
    # y = manager.get_avg_salary()
    # y = manager.get_vacancies_with_higher_salary()
    y = manager.get_vacancies_with_keyword('python')
    print(y)


if __name__ == '__main__':
    main()
