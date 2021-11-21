from collections import defaultdict

CURRENCIES_SIGNS = {
    'RUR': '₽',
    'EUR': '€',
    'USD': '$',
}


def compute_expected_salary(vacancy, wanted_currency):
    """Compute and return expected salary

    Expected salary compute using the "from" & "to" salary fields of the vacancy.  
    Giving "from" and "to," fields, calculate the expected salary as an average.  
    Giving only "from", multiply by 1.2, else if only "to", multiply by 0.8.  
    If wanted currency doesn't mach with currency of the vacancy, return None.

    Args:
        vacancy (json): 
          vacancy with relevant fields
          https://github.com/hhru/api/blob/master/docs_eng/vacancies.md#short-description-of-the-vacancy 
        wanted_currency (str): 
          wanted currency of the salary

    Returns:
        calculated expected salary or None.
    """
    vacancy_salary_from = vacancy['salary']['from']
    vacancy_salary_to = vacancy['salary']['to']
    vacancy_salary_currency = vacancy['salary']['currency']

    if vacancy_salary_currency == wanted_currency:
        if vacancy_salary_from and vacancy_salary_to:
            expected_salary = (vacancy_salary_from + vacancy_salary_to) / 2
            return expected_salary
        elif vacancy_salary_from and not vacancy_salary_to:
            expected_salary = vacancy_salary_from * 1.2
        elif vacancy_salary_to and not vacancy_salary_from:
            expected_salary = vacancy_salary_to * 0.8
        else:
            expected_salary = None

        return expected_salary


def compute_vacancies_average_salary_statistic(vacancies, wanted_currency='RUR'):
    """Compute average salary and return it with statistic as dictionary.

    Args:
        vacancies (list): List of vacancies. Each vacancy has fields listed here
        https://github.com/hhru/api/blob/master/docs_eng/vacancies.md#short-description-of-the-vacancy
        wanted_currency (str): wanted currency of the salary

    Returns:
        A dictionary with fields vacancies_found (int), vacancies_processed (int),
        average_salary (dict).

        For example:
        {        
            'vacancies_found': 10,
            'vacancies_processed': 6,
            'average_salary': {
                'average_salary': 1500,
                'currency': '$'
                }
        } 
    """
    cumulated_salaries = 0
    vacancies_processed = 0
    for vacancy in vacancies:
        expected_salary = compute_expected_salary(vacancy, wanted_currency)
        if expected_salary:
            # print(vacancy['alternate_url'])
            cumulated_salaries += expected_salary
            vacancies_processed += 1

    if vacancies_processed > 0:
        return {
            'vacancies_found': len(vacancies),
            'vacancies_processed': vacancies_processed,
            'average_salary': {
                'average_salary': int(cumulated_salaries / vacancies_processed),
                'currency': CURRENCIES_SIGNS[wanted_currency]
            }
        }
