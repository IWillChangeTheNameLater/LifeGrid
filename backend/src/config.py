from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    db_host: str = 'localhost'
    db_port: int = 5432
    db_user: str = 'postgres'
    db_pass: str = 'postgres'
    db_name: str = 'postgres'

    @property
    def db_dsn(self) -> str:
        return f'postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'

    refresh_jwt_key: str = 'Secret key for the refresh token'
    access_jwt_key: str = 'Secret key for the access token'
    jwt_algorithm: str = 'HS256'
    access_jwt_exp_sec: int = 60*60
    refresh_jwt_exp_sec: int = 60*60*24*30


settings = Settings()
