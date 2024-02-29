from src.hh_api import HeadHunterAPI

companies = ["Планетра", "ЛАНИТ", "Фабрика решений", "InlyIT", "Тензор", "Инспектор Клауд",
             "ВЕБ Инфраструктура", "БИЗНЕС КОНТЕНТ", "Syntella", "ANA BAR", "Wanted",
             "НИИ Масштаб", "SberTech", "Тинькофф", "Банк ВТБ (ПАО)", "Сбер. IT",
             "МГТС", "Совкомбанк Технологии", "Эвотор"]


def main():
    hh_data = HeadHunterAPI(companies)
    ads_data = hh_data.get_vacancies_data()
    print(ads_data)


if __name__ == '__main__':
    main()
