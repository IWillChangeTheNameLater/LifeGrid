from datetime import datetime, timedelta, UTC
from typing import Callable

from pydantic import BaseModel, EmailStr, Field

from config import settings


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    tokens_type: str = "Bearer"


class BaseTokenPayload(BaseModel):
    sub: int


def _expiration_time_factory(seconds_to_expire: int) -> Callable[[], int]:
    expiration_datetime = datetime.now(UTC) + timedelta(
        seconds=seconds_to_expire
    )
    expiration_time = int(expiration_datetime.timestamp())
    return lambda: expiration_time


class AccessTokenPayload(BaseTokenPayload):
    email: EmailStr

    exp: int = Field(
        default_factory=_expiration_time_factory(
        settings.access_token_exp_sec
        )
    )


class RefreshTokenPayload(BaseTokenPayload):
    exp: int = Field(
        default_factory=_expiration_time_factory(
        settings.refresh_token_exp_sec
        )
    )
