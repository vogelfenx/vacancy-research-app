# CLI-Utility for getting salary statistic for IT-vacancies on HeadHunter & SuperJob   

The utility collects open jobs in the IT sector from 2 different sources and prints salary statistics grouped by search text (e.g. programming language), e.g.:
```
+HeadHunter---+-----------------+---------------------+----------------+
| Language    | vacancies found | vacancies processed | average salary |
+-------------+-----------------+---------------------+----------------+
| Python      | 686             | 60                  | 4444$          |
|  Java       | 758             | 65                  | 5296$          |
|  JavaScript | 1639            | 169                 | 4132$          |
|  C#         | 522             | 47                  | 4499$          |
|  C/C++      | 222             | 13                  | 5000$          |
|  PHP        | 877             | 50                  | 3435$          |
|  Kotlin     | 299             | 25                  | 4974$          |
|  Ruby       | 99              | 15                  | 5036$          |
+-------------+-----------------+---------------------+----------------+
+SuperJob-----+-----------------+---------------------+----------------+
| Language    | vacancies found | vacancies processed | average salary |
+-------------+-----------------+---------------------+----------------+
| Python      | 66              | 44                  | 157511₽        |
|  Java       | 61              | 42                  | 233188₽        |
|  JavaScript | 122             | 95                  | 151917₽        |
|  C#         | 40              | 24                  | 148000₽        |
|  C/C++      | 9               | 9                   | 140722₽        |
|  PHP        | 81              | 61                  | 154334₽        |
|  Kotlin     | 14              | 12                  | 260000₽        |
|  Ruby       | 9               | 8                   | 212537₽        |
+-------------+-----------------+---------------------+----------------+
```

The tool is configurable, e.g. you can specify to search vacancies by:
  - specific languages / text
  - wanted currency of vacancies  

Used sources of vacancies:
  - [HeadHunter API](https://github.com/hhru/api/blob/master/docs_eng/README.md)
  - [SuperJob API](https://api.superjob.ru/)

## First steps
1. Clone / download the repository
2. Read installation and configuration steps below
3. Read user manual

## How to install & configure
1. Install Python3 and project dependencies  
    Python3 should be already installed.   
    
    The project uses Pipenv tool, that automatically creates a virtual environment and installs all project dependencies.  
    Please refer to Pipenv [documentation](https://pypi.org/project/pipenv/) to install it.

    When Pipenv is installed, use the following command to create virtual environment and install dependencies:
    ```
    pipenv install
    ```
    To activate this project's virtual environment, run:
    ```
    pipenv shell
    ``` 

2. Generate access token for SuperJob API  
    In order to work with SuperJob API, you need to register your app and retrieve an API key.  
    To generate the API key follow the instructions in the API [documentation](https://api.superjob.ru/info/).

    Once the key is generated, place it in the file named `.secrets` like:
    ```
    SUPERJOB_API_ACCESS_TOKEN=v3.r.144447260.9765a9941232eeea1a348222c24dd5415168e901.7777c111141333924c8f48c247444453411ef831
    ```

## Usage and configuration
1. To run the module use the following command within created virtual environment:
    ```
    python3 main.py  
    ```

2. Check possible command line options, to configure the tool:
    ```
    > python3 main.py -h

    usage: main.py [-h] [--currency_hh {EUR,USD,RUR}] [--currency_sj {rub,uah,uzs}]
    
    Collect & print statistic of salaries for given programming languages
    Specify these languages in .config file.
    
    options:
      -h, --help            show this help message and exit
      --currency_hh {EUR,USD,RUR}
                            Currency of vacancies on HeadHunter to search for
      --currency_sj {rub,uah,uzs}
                            Currency of vacancies on SuperJob to search for  
    ```

2. Use user configuration file:  
    Use the configuration file `.config` to set more precise settings, e.g. programming languages to search for. 

    You can specify these programming languages by separating them with commas:   
    ````
    PROGRAMMING_LANGUAGES=Python, Java, JavaScript, C#, C/C++, PHP, Kotlin, Ruby
    ````

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
