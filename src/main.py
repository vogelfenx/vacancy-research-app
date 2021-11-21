import json
import requests

from requests.exceptions import ConnectionError, HTTPError

from datafetch import headhunter, superjob
from services import services

pp = json.dumps


CURRENCIES_SIGNS = {
    'RUR': '₽',
    'EUR': '€',
    'USD': '$',
}


def fetch_headhunter_vacancies(search_parameters):
    """Fetch HeadHunter vacancies and return it as list of dictionares"""

    vacancies = []
    page = 0
    pages_count = 1

    while page < pages_count:
        vacancies_per_page = headhunter.fetch_vacancies(
            **search_parameters, page=page)
        vacancies += [*vacancies_per_page['items']]
        pages_count = vacancies_per_page['pages']
        page += 1

    return vacancies


def fetch_superjob_vacancies(search_parameters):
    vacancies = []
    next_page = True
    page = 0

    while next_page:
        vacancies_per_page = superjob.fetch_vacancies(**search_parameters, page=page)
        vacancies += [*vacancies_per_page['objects']]
        page += 1
        next_page = vacancies_per_page['more']

    return vacancies


def main():
    popular_languages = ['Python', 'Java', 'JavaScript',
                         'C#', 'C/C++', 'PHP', 'Kotlin', 'COBOL']

    search_parameters_headhunter = {
        'area': 1,  # 1 = Moscow
        'professional_role': 96,  # 96 = Developer
        'only_with_salary': 'true',
        'period': 30,
    }
    search_parameters_superjob = {
        'town': 4,  # 4 = Moscow
        'catalogues': 48,
        'currency': 'rub',
        'period': 0,  # possible values 1 3 7 0
    }

    for language in popular_languages:
        search_parameters_headhunter['text'] = language
        search_parameters_superjob['keyword'] = language

        # fetch vacancies
        try:
            # all_vacancies = fetch_headhunter_vacancies(search_parameters_headhunter)
            all_vacancies = fetch_superjob_vacancies(search_parameters_superjob)
        except Exception as error:
            exit(f'Something went wrong: {error}')

        # calculate statistic for vacancies and group by searched text
        statistic = {}
        # statistic[search_parameters_headhunter['text']] = (
        #    services.compute_vacancies_average_salary_statistic(all_vacancies)
        # )
        vacancy_salaries = dict()
        for vacancy in all_vacancies:
            vacancy_salaries.update({
                vacancy['id']: {
                    'salary_from': vacancy['payment_from'],
                    'salary_to': vacancy['payment_to']
                }
            })
        statistic[language] = services.compute_vacancies_average_salary(vacancy_salaries)
        print(statistic)


if __name__ == '__main__':
    main()
