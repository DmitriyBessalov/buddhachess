import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    database_url: str

    jwt_secret: str
    # jwt_algorithm: str = 'HS256'
    # jwt_expires_s: int = 3600

    debug: bool

    SECRET_KEY = "{{cookiecutter.secret_key}}"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
