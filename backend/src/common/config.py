from enum import IntEnum, unique
from pathlib import Path

from pydantic import EmailStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


@unique
class RedisDB(IntEnum):
    RESULT_BACKEND = 0
    MESSAGE_BROKER = 1


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Search for .env in the parent directory
        env_file=Path(__file__).parent.parent.parent/'.env',
        frozen=True
    )

    db_host: str = 'localhost'
    db_port: PositiveInt = 5432
    db_user: str = 'postgres'
    db_pass: str = 'postgres'
    db_name: str = 'postgres'

    @property
    def db_dsn(self) -> str:
        return f'postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'

    refresh_token_key: str = 'Secret key for the refresh token'
    access_token_key: str = 'Secret key for the access token'
    token_crypt_algorithm: str = 'HS256'
    access_token_exp_sec: PositiveInt = 60*60
    refresh_token_exp_sec: PositiveInt = 60*60*24*30
    confirmation_token_exp_sec: PositiveInt = 60*60*24*5

    redis_host: str = 'localhost'
    redis_port: PositiveInt = 6379

    smtp_host: str = 'smtp.gmail.com'
    smtp_port: PositiveInt = 465
    smtp_user: EmailStr = 'user@example.com'
    smtp_pass: str = 'SMTP password'

    @property
    def email_templates_dir_path(self) -> Path:
        return Path(__file__).parent/'email_service'/'templates'


settings = _Settings()
