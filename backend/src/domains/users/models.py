from datetime import date
from enum import StrEnum
from typing import Annotated, TYPE_CHECKING

from pydantic import EmailStr, StringConstraints
from sqlmodel import Field, Relationship, SQLModel

from common.models import ULIDField, ULIDStr

if TYPE_CHECKING:
    from domains.auth.models import (
        IssuedConfirmationTokens,
        IssuedRefreshTokens,
    )


PasswordStr = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=8, max_length=64)]


class BaseUser(SQLModel):
    ...


class Users(BaseUser, table=True):
    id: ULIDStr = ULIDField(primary_key=True)
    email: EmailStr = Field(index=True, max_length=254)
    is_email_verified: bool = False
    hashed_password: str
    birthday: date
    days_at_death: int = Field(ge=1)

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

    user_settings: 'UserSettings' = Relationship(
        back_populates='id',
        cascade_delete=True,
        sa_relationship_kwargs={
            'lazy': 'selectin', 'uselist': False
        }
    )


class UserRegister(BaseUser):
    email: EmailStr
    password: PasswordStr
    birthday: date
    days_at_death: int = Field(ge=1)


class UserLogin(BaseUser):
    email: EmailStr
    password: PasswordStr


class Theme(StrEnum):
    LIGHT = 'light'
    DARK = 'dark'


class UserSettings(BaseUser, table=True):
    __tablename__ = 'user_settings'

    id: ULIDStr = ULIDField(primary_key=True)
    accent_color: str|None = Field(min_length=3, max_length=6)
    theme: Theme|None

    user: Users = Relationship(
        back_populates='user_settings',
        sa_relationship_kwargs={
            'lazy': 'selectin', 'uselist': False
        }
    )
