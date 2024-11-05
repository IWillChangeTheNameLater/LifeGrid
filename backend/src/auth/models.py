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


def _calculate_expiration_time(seconds: int) -> Callable[[], int]:
    expiration_datetime = datetime.now(UTC) + timedelta(seconds=seconds)
    expiration_time = int(expiration_datetime.timestamp())
    return lambda: expiration_time


class AccessTokenPayload(BaseTokenPayload):
    email: EmailStr

    exp: int = Field(
        default_factory=_calculate_expiration_time(
        settings.access_token_exp_sec
        )
    )


class RefreshTokenPayload(BaseTokenPayload):
    exp: int = Field(
        default_factory=_calculate_expiration_time(
        settings.refresh_token_exp_sec
        )
    )
