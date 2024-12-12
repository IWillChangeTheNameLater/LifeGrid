from datetime import datetime, timedelta, UTC
from enum import StrEnum
from typing import Callable, TYPE_CHECKING

from pydantic import EmailStr, PositiveInt
from sqlmodel import Field, Relationship, SQLModel

from common.config import settings
from common.models import ULIDField, ULIDStr

if TYPE_CHECKING:
    from domains.users.models import Users


class TokenFunction(StrEnum):
    REFRESH = 'refresh_token'
    ACCESS = 'access_token'


class Tokens(SQLModel):
    access_token: str
    refresh_token: str
    tokens_type: str = "Bearer"


class BaseTokenPayload(SQLModel):
    sub: ULIDStr


def _calculate_expiration_time(seconds_to_live: int) -> int:
    expiration_datetime = datetime.now(UTC) + timedelta(
        seconds=seconds_to_live
    )
    return int(expiration_datetime.timestamp())


def exp_time_factory(seconds_to_live: int) -> Callable[[], int]:
    return lambda: _calculate_expiration_time(seconds_to_live)


class AccessTokenPayload(BaseTokenPayload):
    email: EmailStr
    email_verified: bool
    exp: PositiveInt = Field(
        default_factory=exp_time_factory(settings.access_token_exp_sec)
    )


class RefreshTokenPayload(BaseTokenPayload):
    jti: ULIDStr = ULIDField()
    exp: PositiveInt = Field(
        default_factory=exp_time_factory(settings.refresh_token_exp_sec)
    )
    device_id: str


class IssuedRefreshTokens(SQLModel, table=True):
    __tablename__ = 'issued_refresh_tokens'

    jti: ULIDStr = ULIDField(primary_key=True)
    sub: ULIDStr = Field(
        foreign_key='users.id', ondelete='CASCADE', index=True
    )
    device_id: str = Field(index=True)
    exp: PositiveInt
    is_revoked: bool = Field(default=False)

    user: 'Users' = Relationship(
        back_populates='issued_refresh_tokens',
        sa_relationship_kwargs={'lazy': 'selectin'}
    )


class IssuedConfirmationTokens(SQLModel, table=True):
    __tablename__ = 'issued_confirmation_tokens'

    id: ULIDStr = ULIDField(primary_key=True)
    user_id: ULIDStr = Field(
        foreign_key='users.id', ondelete='CASCADE', unique=True
    )
    expire_at: PositiveInt = Field(
        default_factory=exp_time_factory(settings.confirmation_token_exp_sec)
    )

    user: 'Users' = Relationship(
        back_populates='issued_confirmation_tokens',
        sa_relationship_kwargs={'lazy': 'selectin'}
    )
