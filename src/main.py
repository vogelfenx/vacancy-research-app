import json
import requests

from requests.exceptions import ConnectionError, HTTPError

from datafetch import headhunter
from services import services

pp = json.dumps


def fetch_headhunter_vacancies(search_parameters):
    """Fetch HeadHunter vacancies and return it as list of dictionares"""

    headhunter_vacancies = []
    page = 0
    pages_count = 1

    while page < pages_count:
        vacancies_per_page = headhunter.fetch_vacancies(
            **search_parameters, page=page)

        headhunter_vacancies += [*vacancies_per_page['items']]
        pages_count = vacancies_per_page['pages']
        page += 1

    return headhunter_vacancies


def main():
    popular_languages = ['Python', 'Java', 'JavaScript',
                         'C#', 'C/C++', 'PHP', 'Kotlin', 'COBOL']

    search_parameters = {
        'area': 1,  # 1 = Moscow
        'professional_role': 96,  # 96 = Developer
        'only_with_salary': 'true',
        'period': 30,
    }

    for language in popular_languages:
        search_parameters['text'] = language

        # fetch vacancies
        try:
            all_vacancies = fetch_headhunter_vacancies(search_parameters)
        except Exception as error:
            exit(f'Something went wrong: {error}')

        # calculate statistic for vacancies and group by searched text
        statistic = {}
        statistic[search_parameters['text']] = (
            services.compute_vacancies_average_salary_statistic(all_vacancies)
        )
        print(statistic)


if __name__ == '__main__':
    main()
