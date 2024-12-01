from pathlib import Path

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Search for .env in the parent directory
        env_file=Path(__file__).parent.parent/'.env'
    )

    db_host: str = 'localhost'
    db_port: int = 5432
    db_user: str = 'postgres'
    db_pass: str = 'postgres'
    db_name: str = 'postgres'

    @property
    def db_dsn(self) -> str:
        return f'postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'

    refresh_token_key: str = 'Secret key for the refresh token'
    access_token_key: str = 'Secret key for the access token'
    token_crypt_algorithm: str = 'HS256'
    access_token_exp_sec: int = 60*60
    refresh_token_exp_sec: int = 60*60*24*30

    redis_host: str = 'localhost'
    redis_port: int = 6379

    smtp_host: str = 'smtp.gmail.com'
    smtp_port: int = 465
    smtp_user: EmailStr = 'user@example.com'
    smtp_pass: str = 'SMTP password'


settings = _Settings()
