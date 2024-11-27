from starlette.config import Config

config = Config(".env")

APP_PORT = config("APP_PORT", cast=int, default=8000)
STAGE = config("STAGE", default="dev")
API_PREFIX = config("API_PREFIX", default="/api/v1")
DATABASE_URL = config("DATABASE_URL")

SECRET_KEY = config("SECRET_KEY")
TOKEN_ALGORITHM = config("TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)

ADMIN_USERNAME = config("ADMIN_USERNAME")
ADMIN_PASSWORD = config("ADMIN_PASSWORD")
ADMIN_EMAIL = config("ADMIN_EMAIL")
