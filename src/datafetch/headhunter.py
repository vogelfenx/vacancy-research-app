import configuration.settings
import requests

api_base_url = configuration.settings.HEADHUNTER_API_BASE_URL


def fetch_vacancies(text, area=None, professional_role=None, currency=None, only_with_salary=None, period=30, page=0, per_page=100):
    """Fetch vacancies from HeadHunter API, return there in json.

    Args:
        text (str): 
            search the specific vacancies by text
        area (int, optional): 
            search vacancies by area. 
            Possible ids: https://api.hh.ru/areas/
            Defaults to None.
        professional_role (int, optional): 
            search vacancies by profession. 
            Possible ids: https://api.hh.ru/professional_roles
            Defaults to None.
        currency (str, optional): 
            search vacancies by currency. 
            Make sense only with salary parameter.
            Defaults to None.
        only_with_salary (boolean, optional): 
            returns vacancies only with salary. Defaults to None.
        period (int, optional): 
            search vacancies for given period. 
            Possible values from 0 to 30. Defaults to 30.
        page (int, optional): 
            page number of the response. Defaults to 0.
        per_page (int, optional): 
            number of vacancies per page. Defaults to 100.

        The args correspondent the fields of the vacancy described 
        in the api documentation 
        https://github.com/hhru/api/blob/master/docs_eng/vacancies.md#short-description-of-the-vacancy 

    Returns:
        Response (json): page with the vacancies in json
    """
    url = f'{api_base_url}/vacancies'
    url_params = {
        'text': text,
        'area': area,
        'professional_role': professional_role,
        'currency': currency,
        'only_with_salary': only_with_salary,
        'period': period,
        'page': page,
        'per_page': per_page,
    }

    response = requests.get(url, url_params)
    # print(response.url)
    response.raise_for_status()

    return response.json()
