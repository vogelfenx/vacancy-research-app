from collections import defaultdict


def compute_expected_salary(salary_from, salary_to):
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


def compute_vacancies_average_salary(vacancies_salary):
    """Compute average salary and return it with statistic as dictionary.

    Args:
        vacancies (list): List of vacancies. Each vacancy has fields listed here
        https://github.com/hhru/api/blob/master/docs_eng/vacancies.md#short-description-of-the-vacancy
        wanted_currency (str): wanted currency of the salary

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
    cumulated_salaries = 0
    vacancies_processed = 0
    for vacancy in vacancies_salary.values():
        expected_salary = compute_expected_salary(**vacancy)
        if expected_salary:
            cumulated_salaries += expected_salary
            vacancies_processed += 1

    if vacancies_processed > 0:
        return {
            'vacancies_found': len(vacancies_salary),
            'vacancies_processed': vacancies_processed,
            'average_salary': int(cumulated_salaries / vacancies_processed)

        }
