from starlette.config import Config

config = Config(".env")

APP_PORT = config("APP_PORT", cast=int, default=8000)
STAGE = config("STAGE", default="dev")
API_PREFIX = config("API_PREFIX", default="/api/v1")
DB_HOST = config("DB_HOST")
DB_NAME = config("DB_NAME")
DB_PORT = config("DB_PORT")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = config("SECRET_KEY")
TOKEN_ALGORITHM = config("TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)

ADMIN_USERNAME = config("ADMIN_USERNAME")
ADMIN_PASSWORD = config("ADMIN_PASSWORD")
ADMIN_EMAIL = config("ADMIN_EMAIL")

FERNET_KEY = config("FERNET_KEY")
ENCODING = config("ENCODING")