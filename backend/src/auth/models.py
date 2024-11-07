from datetime import datetime, timedelta, UTC
from enum import Enum
from functools import partial

from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from ulid import ULID

from config import settings


class TokenFunction(Enum):
    refresh = 'refresh_token'
    access = 'access_token'


def _calculate_expiration_time(seconds_to_expire: int) -> int:
    expiration_datetime = datetime.now(UTC) + timedelta(
        seconds=seconds_to_expire
    )
    expiration_time = int(expiration_datetime.timestamp())
    return expiration_time


class Tokens(SQLModel):
    access_token: str
    refresh_token: str
    tokens_type: str = "Bearer"


class BaseTokenPayload(SQLModel):
    sub: str


class AccessTokenPayload(BaseTokenPayload):
    email: EmailStr

    exp: int = Field(
        default_factory=partial(
        _calculate_expiration_time, settings.access_token_exp_sec
        )
    )


class RefreshTokenPayload(BaseTokenPayload):
    jti: ULID = Field(default_factory=ULID)
    exp: int = Field(
        default_factory=partial(
        _calculate_expiration_time, settings.refresh_token_exp_sec
        )
    )
    device_id: str


class IssuedTokens(SQLModel, table=True):
    __tablename__ = 'issued_tokens'

    jti: ULID = Field(default_factory=ULID, max_length=26, primary_key=True)
    sub: str = Field(index=True)
    device_id: str = Field(index=True)
    exp: int
    token: str
    is_revoked: bool = Field(default=False)
