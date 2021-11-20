import json

from requests.exceptions import ConnectionError

from datafetch import headhunter
from services import services

pp = json.dumps

CURRENCIES_SIGNS = {
    'RUR': '₽',
    'EUR': '€',
    'USD': '$',
}


def main():
    search_parameters = {
        'text': 'Python',
        'area': 1,  # Moscow
        'professional_role': 96,  # Developer
        'only_with_salary': 'true',
        'period': 30,
    }

    try:
        pages_count = headhunter.fetch_vacancies(**search_parameters)['pages']
        paginated_vacancies = {}
        for page in range(pages_count):
            vacancies_per_page = headhunter.fetch_vacancies(**search_parameters, page=page)
            paginated_vacancies[page] = vacancies_per_page
        # print(pp(paginated_vacancies, indent=4))
    except ConnectionError as error:
        print('Something went wrong: internet connection is lost or site is not reachable')
        print("Error", error)
        exit(1)

    counter = 1
    for vacancies_per_page in paginated_vacancies.values():
        for vacancy in vacancies_per_page['items']:
            wanted_currency = 'EUR'
            expected_salary = services.compute_expected_salary(vacancy, wanted_currency)
            if expected_salary:
                print(f'{counter}:'
                      f'{expected_salary} {CURRENCIES_SIGNS[wanted_currency]}'
                      f'-> {vacancy["name"]} -- {vacancy["alternate_url"]}')
                counter += 1


if __name__ == '__main__':
    main()
