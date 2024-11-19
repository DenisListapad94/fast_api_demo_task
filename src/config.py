import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
from dotenv import dotenv_values, find_dotenv,load_dotenv
#
# env_cfg = dotenv_values(find_dotenv(raise_error_if_not_found=True))
load_dotenv(os.path.join(BASE_DIR, '.env'))

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

TOKEN_TYPE = os.getenv("TOKEN_TYPE")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
