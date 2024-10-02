from starlette.config import Config
from starlette.datastructures import Secret

# load .env file to get database URL 
try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

# define secret by cast ( cast = Secret )
DATABASE_URL = config("DATABASE_URL", cast=Secret)