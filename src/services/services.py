from collections import defaultdict


CURRENCIES_SIGNS = {
    'RUR': '₽',
    'rub': '₽',
    'EUR': '€',
    'USD': '$',
}


def compute_expected_salary(salary_from, salary_to, **kwargs):
    """Compute and return expected salary.

    Expected salary compute using the "from" & "to" salary fields of the vacancy.  
    Giving "from" and "to," fields, calculate the expected salary as an average.  
    Giving only "from", multiply by 1.2, else if only "to", multiply by 0.8.  
    If wanted currency doesn't mach with currency of the vacancy, return None.


    Args:
        salary_from (number): minimum possible salary
        salary_to (number): maximum possible salary

    Returns:
        expected_salary (number): calculated expected salary
    """
    if salary_from and salary_to:
        expected_salary = (salary_from + salary_to) / 2
        return expected_salary
    elif salary_from and not salary_to:
        expected_salary = salary_from * 1.2
    elif salary_to and not salary_from:
        expected_salary = salary_to * 0.8
    else:
        expected_salary = None

    return expected_salary


def compute_vacancies_average_salary(vacancies_salaries, wanted_currency):
    """Compute average salary and return it with statistic as dictionary.

    Args:
        vacancies_salary (dict): 
            a list of dictionaries
            containing salaries field, e.g.:
                [   
                    {
                        salary_from: 5000,
                        salary_to: 6000,
                        currency: 'EUR'
                    },
                    { ... },
                ]        

    Returns:
        A dictionary with fields vacancies_found (int), vacancies_processed (int),
        average_salary (int). If no vacancies proceeded, returns None.  

        For example:
        {        
            'vacancies_found': 10,
            'vacancies_processed': 6,
            'average_salary': 1500
        } 
    """
    vacancies_count = len(vacancies_salaries)
    cumulated_salaries = 0
    vacancies_processed = 0

    # filter vacancies by the given wanted currency
    vacancies_salaries = [vacancy for vacancy in vacancies_salaries
                          if vacancy['salary_currency'] == wanted_currency]

    for vacancy in vacancies_salaries:
        expected_salary = compute_expected_salary(**vacancy)
        if expected_salary:
            cumulated_salaries += expected_salary
            vacancies_processed += 1

    if vacancies_processed > 0:
        return {
            'vacancies_found': vacancies_count,
            'vacancies_processed': vacancies_processed,
            'average_salary': f'{int(cumulated_salaries / vacancies_processed)}'
                              f'{CURRENCIES_SIGNS[wanted_currency]}'

        }
