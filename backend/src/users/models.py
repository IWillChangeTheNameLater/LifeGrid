from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Users(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    email: EmailStr
    hashed_password: str
