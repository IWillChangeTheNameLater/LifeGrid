from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from ulid import ULID


class BaseUser(SQLModel):
    ...


class Users(BaseUser, table=True):
    id: str = Field(default_factory=ULID, primary_key=True, max_length=26)
    email: EmailStr = Field(index=True)
    hashed_password: str


class UserRegister(BaseUser):
    email: EmailStr
    password: str


class UserLogin(BaseUser):
    email: EmailStr
    password: str
