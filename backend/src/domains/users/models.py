from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from common import ULIDField, ULIDStr

if TYPE_CHECKING:
    from domains.auth.models import (
        IssuedConfirmationTokens,
        IssuedRefreshTokens,
    )


class BaseUser(SQLModel):
    ...


class Users(BaseUser, table=True):
    id: ULIDStr = ULIDField(primary_key=True)
    email: EmailStr = Field(index=True)
    is_email_verified: bool = False
    hashed_password: str

    issued_refresh_tokens: list['IssuedRefreshTokens'] = Relationship(
        back_populates='user',
        cascade_delete=True,
        sa_relationship_kwargs={'lazy': 'selectin'}
    )
    issued_confirmation_tokens: list[
        'IssuedConfirmationTokens'] = Relationship(
            back_populates='user',
            cascade_delete=True,
            sa_relationship_kwargs={'lazy': 'selectin'}
        )


class UserRegister(BaseUser):
    email: EmailStr
    password: str


class UserLogin(BaseUser):
    email: EmailStr
    password: str
