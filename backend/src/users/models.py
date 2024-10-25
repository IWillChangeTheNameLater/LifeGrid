from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class BaseUser(SQLModel):
    ...


class Users(BaseUser, table=True):
    id: int|None = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True)
    hashed_password: str


class UserRegister(BaseUser):
    email: EmailStr
    password: str


class UserLogin(BaseUser):
    email: EmailStr
    password: str
