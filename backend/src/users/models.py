from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from ulid import ULID


class BaseUser(SQLModel):
    ...


class Users(BaseUser, table=True):
    id: str = Field(
        default_factory=lambda: str(ULID()), primary_key=True, max_length=26
    )

    email: EmailStr = Field(index=True)
    is_email_verified: bool = False
    hashed_password: str


class UserRegister(BaseUser):
    email: EmailStr
    password: str


class UserLogin(BaseUser):
    email: EmailStr
    password: str
