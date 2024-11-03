from pydantic import EmailStr
from sqlmodel import SQLModel


class AccessTokenPayload(SQLModel):
    sub: int|None
    email: EmailStr


class RefreshTokenPayload(SQLModel):
    sub: int|None


class Tokens(SQLModel):
    access_token: str
    refresh_token: str
    tokens_type: str = "bearer"
