# from pydantic import AnyHttpUrl, EmailStr, HttpUrl, PostgresDsn, validator
from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str = '127.0.0.1'
    SERVER_PORT: int = 8000
    DATABASE_URL: str

    JWT_SECRET: str = 'SECRET'
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    EMAIL_HOST: str = 'localhost'
    EMAIL_PORT: int = 25
    EMAIL_FROM_NAME: str = ''
    EMAIL_FROM_EMAIL: str = 'mail@example.com'

    DEBUG: bool


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
