import configuration.settings
import requests

api_base_url = configuration.settings.SUPERJOB_API_BASE_URL
api_access_token = configuration.settings.SUPERJOB_API_ACCESS_TOKEN


def fetch_vacancies(keyword, town=None, catalogues=None, currency=None, period=0, page=0, count=100):
    """Fetch vacancies from SuperJob API, return in json"""
    url = f'{api_base_url}/vacancies'
    url_header = {
        'X-Api-App-Id': api_access_token
    }
    url_params = {
        'keyword': keyword,
        'town': town,
        'catalogues': catalogues,
        'currency': currency,
        'period': period,  # possible values 1 3 7 0
        'page': page,
        'count': count
    }
    response = requests.get(url, url_params, headers=url_header)
    response.raise_for_status()

    return response.json()
