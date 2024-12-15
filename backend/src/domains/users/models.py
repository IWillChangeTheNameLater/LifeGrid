from datetime import date
from typing import Annotated, TYPE_CHECKING

from pydantic import EmailStr, PositiveInt, StringConstraints
from sqlmodel import Field, Relationship, SQLModel

from common.models import ULIDField, ULIDStr

from .settings.models import UsersSettings

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
    days_at_death: PositiveInt

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
    user_settings: 'UsersSettings' = Relationship(
        back_populates='user',
        cascade_delete=True,
        sa_relationship_kwargs={
            'lazy': 'selectin', 'uselist': False
        }
    )


class UserRegister(BaseUser):
    email: EmailStr
    password: PasswordStr
    birthday: date
    days_at_death: PositiveInt


class UserLogin(BaseUser):
    email: EmailStr
    password: PasswordStr
