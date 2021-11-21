import json

from requests.exceptions import ConnectionError

from datafetch import headhunter
from services import services

pp = json.dumps


def main():
    search_parameters = {
        'text': 'Python',
        'area': 1,  # Moscow
        'professional_role': 96,  # Developer
        'only_with_salary': 'true',
        'period': 30,
    }

    # fetch vacancies
    all_vacancies = []
    try:
        pages_count = headhunter.fetch_vacancies(**search_parameters)['pages']
        paginated_vacancies = {}
        for page in range(pages_count):
            vacancies_per_page = headhunter.fetch_vacancies(
                **search_parameters, page=page)
            all_vacancies += [*vacancies_per_page['items']]
    except ConnectionError as error:
        print('Something went wrong: internet connection is lost or site is not reachable')
        print("Error", error)
        exit(1)

    # calculate statistic for vacancies and group by searched text
    statistic = {}
    statistic[search_parameters['text']] = (
        services.compute_vacancies_average_salary_statistic(all_vacancies)
    )
    print(statistic)


if __name__ == '__main__':
    main()
