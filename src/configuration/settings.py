from dotenv import dotenv_values

config = dotenv_values('.config')

HEADHUNTER_API_BASE_URL = config['HEADHUNTER_API_BASE_URL']
