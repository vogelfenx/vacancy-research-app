from dotenv import dotenv_values

config = dotenv_values('.config')
secrets = dotenv_values('.secrets')

# common settings
HEADHUNTER_API_BASE_URL = config['HEADHUNTER_API_BASE_URL']
SUPERJOB_API_BASE_URL = config['SUPERJOB_API_BASE_URL']

# secrets
SUPERJOB_API_ACCESS_TOKEN = secrets['SUPERJOB_API_ACCESS_TOKEN']

# user configuration
programming_languages = [lang for lang in config['PROGRAMMING_LANGUAGES'].split(',')]
