from datafetch import headhunter
import json

pp = json.dumps

def main():
    search_parameters = {
        'text':'Python Germany', 
        'period': 30,
    }
    pages = headhunter.fetch_vacancies(**search_parameters)['pages']
    
    paginated_vacancies = {}
    for page in range(pages):
        vacancies_per_page = headhunter.fetch_vacancies(**search_parameters, page=page)
        paginated_vacancies[page] = vacancies_per_page
    # print(pp(paginated_vacancies, indent=4))

    counter = 1
    for vacancies_per_page in paginated_vacancies.values():
        for vacancy in vacancies_per_page['items']:
            if vacancy['salary']['currency'] == 'RUR':
                # vacancy['salary']['currency']
                print(f'{counter}: {vacancy["salary"]["from"]} - {vacancy["salary"]["to"]} -> {vacancy["name"]} -- {vacancy["alternate_url"]}' , )
                counter += 1
            # if not vacancy['department']:
            #     print(f'{counter}: {vacancy["department"]} -> {vacancy["name"]} -- {vacancy["alternate_url"]}' , )
            #     counter += 1

if __name__ == '__main__':
    main()