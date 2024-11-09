from datetime import datetime, timedelta, UTC
from enum import Enum
from functools import partial

from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from ulid import ULID

from config import settings


class TokenFunction(str, Enum):
    REFRESH = 'refresh_token'
    ACCESS = 'access_token'


class Tokens(SQLModel):
    access_token: str
    refresh_token: str
    tokens_type: str = "Bearer"


class BaseTokenPayload(SQLModel):
    sub: str


def _calculate_expiration_time(seconds_to_expire: int) -> int:
    expiration_datetime = datetime.now(UTC) + timedelta(
        seconds=seconds_to_expire
    )
    expiration_time = int(expiration_datetime.timestamp())
    return expiration_time


class AccessTokenPayload(BaseTokenPayload):
    email: EmailStr

    exp: int = Field(
        default_factory=partial(
        _calculate_expiration_time, settings.access_token_exp_sec
        )
    )


class RefreshTokenPayload(BaseTokenPayload):
    jti: str = Field(default_factory=lambda: str(ULID()), max_length=26)
    exp: int = Field(
        default_factory=partial(
        _calculate_expiration_time, settings.refresh_token_exp_sec
        )
    )
    device_id: str


class IssuedRefreshTokens(SQLModel, table=True):
    __tablename__ = 'issued_refresh_tokens'

    jti: str = Field(
        default_factory=lambda: str(ULID()), max_length=26, primary_key=True
    )
    sub: str = Field(index=True)
    device_id: str = Field(index=True)
    exp: int
    hashed_token: str
    is_revoked: bool = Field(default=False)
