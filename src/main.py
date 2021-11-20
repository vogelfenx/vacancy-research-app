from datafetch import headhunter
import json

pp = json.dumps

def main():
    pages = headhunter.fetch_vacancies('Python', currency='EUR')['pages']
    
    paginated_vacancies = {}
    for page in range(pages):
        vacancies_per_page = headhunter.fetch_vacancies('Python', currency='EUR', page=page)
        paginated_vacancies[page] = vacancies_per_page
    # print(pp(paginated_vacancies, indent=4))

    counter = 1
    for vacancies_per_page in paginated_vacancies.values():
        for vacancy in vacancies_per_page['items']:
            if vacancy['salary']['currency'] == 'EUR':
                print(f'{counter}: {vacancy["name"]} -- {vacancy["alternate_url"]}' , )
                counter += 1

if __name__ == '__main__':
    main()