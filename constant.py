from decouple import config

BASE_URL = config("BASE_URL", cast=str)
