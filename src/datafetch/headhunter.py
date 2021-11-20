import requests
import configuration.settings

api_base_url = configuration.settings.HEADHUNTER_API_BASE_URL

def fetch_vacancies(text, area=1, professional_role=96, currency='RUR', only_with_salary='true', period=30, page=0, per_page=100):
    """Fetch vacancies from HeadHunter API, return in json"""
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
