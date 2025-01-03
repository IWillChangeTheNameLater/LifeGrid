from enum import IntEnum, unique
from pathlib import Path

from pydantic import EmailStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


def _find_relative_dir(
    dir_name: str, start_dir_path: Path|str = __file__
) -> Path:
    start_dir_path = Path(start_dir_path)

    for parent in start_dir_path.parents:
        if parent.name == dir_name:
            return parent

    for child in start_dir_path.rglob('*'):
        if child.name == dir_name and child.is_dir():
            return child

    raise ValueError('No parent or child directory found')


@unique
class RedisLogicalDB(IntEnum):
    DEFAULT = 0

    CACHE = 1

    MESSAGE_BROKER = 2
    RESULT_BACKEND = 3


class _Settings(BaseSettings):
    root_dir_path: Path = _find_relative_dir('backend')
    working_dir_path: Path = _find_relative_dir('src')

    model_config = SettingsConfigDict(
        # Search for .env in the parent directory
        env_file=root_dir_path/'.env',
        frozen=True
    )

    postgres_host: str = 'postgres'
    postgres_port: PositiveInt = 5432
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_db: str = 'postgres'

    @property
    def postgres_dsn(self) -> str:
        return f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    refresh_token_key: str = 'Secret key for the refresh token'
    access_token_key: str = 'Secret key for the access token'
    token_crypt_algorithm: str = 'HS256'
    access_token_exp_sec: PositiveInt = 60*60
    refresh_token_exp_sec: PositiveInt = 60*60*24*30
    confirmation_token_exp_sec: PositiveInt = 60*60*24*5

    redis_host: str = 'redis'
    redis_port: PositiveInt = 6379

    def get_redis_dsn(
        self, logical_db: RedisLogicalDB = RedisLogicalDB.DEFAULT
    ) -> str:
        return f'redis://{self.redis_host}:{self.redis_port}/{logical_db}'

    smtp_host: str = 'smtp.gmail.com'
    smtp_port: PositiveInt = 465
    smtp_user: EmailStr = 'user@example.com'
    smtp_pass: str = 'SMTP password'


settings = _Settings()
