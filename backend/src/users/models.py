from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from ulid import ULID

if TYPE_CHECKING:
    from auth.models import IssuedRefreshTokens


class BaseUser(SQLModel):
    ...


class Users(BaseUser, table=True):
    id: str = Field(
        default_factory=lambda: str(ULID()), primary_key=True, max_length=26
    )

    email: EmailStr = Field(index=True)
    is_email_verified: bool = False
    hashed_password: str

    issued_refresh_tokens: list['IssuedRefreshTokens'] = Relationship(
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
