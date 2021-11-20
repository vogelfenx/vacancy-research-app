
def compute_expected_salary(vacancy, wanted_currency):
    """Compute and return expected salary

    Expected salary compute using the "from" & "to" salary fields of the vacancy.  
    Giving "from" and "to," fields, calculate the expected salary as an average.  
    Giving only "from", multiply by 1.2, else if only "to", multiply by 0.8.  
    If wanted currency doesn't mach with currency of the vacancy, return None.

    Args:
        vacancy (json): vacancy with relevant fields
        https://github.com/hhru/api/blob/master/docs_eng/vacancies.md#short-description-of-the-vacancy 
        wanted_currency (str): wanted currency of the salary

    Return:
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
