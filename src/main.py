import json

from terminaltables import AsciiTable

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


def calculate_statistic_for_suberjob(vacancies, wanted_currency='rub'):
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


def calculate_statistic_for_headhunter(vacancies, wanted_currency='RUR'):
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


def print_statistic_table(statistic, title='Statistic'):
    statistic_fields = [
        ['Language', 'vacancies found', 'vacancies processed', 'average salary'],
    ]

    # filter out None vacancies
    statistic = {language: vacancies_statistic
                 for language, vacancies_statistic in statistic.items() if vacancies_statistic}

    for language, vacancy_statistic in statistic.items():
        statistic_fields.append([language, *(vacancy_statistic.values())])

    table = AsciiTable(statistic_fields, title)
    print(table.table)


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

    statistic_headhunter = {}
    statistic_superjob = {}
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
        statistic_headhunter.update({
            language: calculate_statistic_for_headhunter(headhunter_vacancies)
        })
        statistic_superjob.update({
            language: calculate_statistic_for_suberjob(superjob_vacancies)
        })

    print_statistic_table(statistic_headhunter,
                          f'HeadHunter')

    print_statistic_table(statistic_superjob,
                          f'SuperJob')


if __name__ == '__main__':
    main()
