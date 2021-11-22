import configuration.settings
import requests

api_base_url = configuration.settings.SUPERJOB_API_BASE_URL
api_access_token = configuration.settings.SUPERJOB_API_ACCESS_TOKEN


def fetch_vacancies(keyword, town=None, catalogues=None, currency=None, period=0, page=0, count=100):
    """Fetch vacancies from SuperJob API, return in json.

    Args:
        keyword (str): 
            search the specific vacancies by keyword
        town (int, optional): 
            search vacancies by area. Defaults to None.
            Possible ids: https://api.superjob.ru/2.0/towns/
        catalogues (int, optional): 
            search vacancies by profession. Defaults to None.
            Possible ids: https://api.superjob.ru/2.0/catalogues/
        currency (str, optional): 
            search vacancies by currency. 
            Possible values:
                - rub — russian ruble
                - uah — ukrainian hryvnia
                - uzs — uzbekistan som 
            Defaults to None.
        period (int, optional): 
            search vacancies for given period. 
            Possible values are 
                - 1 — for last 1 day
                - 3 — for last 3 days
                - 7 — for last week
                - 0 — for all time 
            Defaults to 0.
        page (int, optional): 
            page number of the response. Defaults to 0.
        count (int, optional): 
            number of vacancies per page. Defaults to 100.

        The args correspondent the fields of the vacancy described 
        in the api documentation https://api.superjob.ru/#vacancy

    Returns:
        Response (json): page with the vacancies in json
    """
    url = f'{api_base_url}/vacancies'
    url_header = {
        'X-Api-App-Id': api_access_token
    }
    url_params = {
        'keyword': keyword,
        'town': town,
        'catalogues': catalogues,
        'currency': currency,
        'period': period,
        'page': page,
        'count': count
    }
    response = requests.get(url, url_params, headers=url_header)
    response.raise_for_status()

    return response.json()
