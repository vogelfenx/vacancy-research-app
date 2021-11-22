import json
import requests

from requests.exceptions import ConnectionError, HTTPError

from datafetch import headhunter, superjob
from services import services

pp = json.dumps


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


def calculate_statistic_for_suberjob(vacancies, wanted_currency='eur'):
    vacancy_salaries = dict()
    for vacancy in vacancies:
        vacancy_salaries.update({
            vacancy['id']: {
                'salary_from': vacancy['payment_from'],
                'salary_to': vacancy['payment_to'],
                'salary_currency': vacancy['currency']
            }
        })
    return services.compute_vacancies_average_salary(vacancy_salaries, wanted_currency)


def calculate_statistic_for_headhunter(vacancies, wanted_currency='EUR'):
    vacancy_salaries = dict()

    for vacancy in vacancies:
        vacancy_salaries.update({
            vacancy['id']: {
                'salary_from': vacancy['salary']['from'],
                'salary_to': vacancy['salary']['to'],
                'salary_currency': vacancy['salary']['currency']
            }
        })
    return services.compute_vacancies_average_salary(vacancy_salaries, wanted_currency)


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
            headhunter_vacancies = fetch_headhunter_vacancies(search_parameters_headhunter)
            superjob_vacancies = fetch_superjob_vacancies(search_parameters_superjob)
        except Exception as error:
            exit(f'Something went wrong: {error}')

        # calculate statistic for vacancies and group by searched text or keyword
        get_statistic_headhunter = {}
        get_statistic_superjob = {}
        get_statistic_headhunter.update({
            language: calculate_statistic_for_headhunter(headhunter_vacancies)
        })
        get_statistic_superjob.update({
            language: calculate_statistic_for_suberjob(superjob_vacancies)
        })

        print(get_statistic_headhunter)
        print(get_statistic_superjob)


if __name__ == '__main__':
    main()
