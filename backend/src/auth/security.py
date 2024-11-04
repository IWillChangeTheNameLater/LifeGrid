from datetime import datetime, timedelta, UTC

import bcrypt, jwt
from pydantic import EmailStr
from sqlmodel import SQLModel

from config import settings
from exceptions import *
from users.dao import UsersDAO
from users.models import Users


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def _create_token(
    payload: dict|SQLModel, seconds_to_expire: int, key: str
) -> str:
    if isinstance(payload, SQLModel):
        payload = payload.model_dump()
    else:
        payload = payload.copy()
    payload['exp'] = datetime.now(UTC) + timedelta(seconds=seconds_to_expire)
    encoded_token = jwt.encode(payload, key, settings.token_crypt_algorithm)
    return encoded_token


def create_access_token(payload: dict|SQLModel) -> str:
    return _create_token(
        payload, settings.access_token_exp_sec, settings.access_token_key
    )


def create_refresh_token(payload: dict|SQLModel) -> str:
    return _create_token(
        payload, settings.refresh_token_exp_sec, settings.refresh_token_key
    )


def _extract_correct_payload_from_token(token: str|None, key: str) -> dict:
    if not token:
        raise TokenAbsentException
    try:
        payload: dict = jwt.decode(
            token, key, algorithms=[settings.token_crypt_algorithm]
        )
        return payload
    except jwt.PyJWTError:
        raise TokenExpiredException
    except TypeError:
        raise IncorrectTokenFormatException


async def authenticate_user(email: EmailStr, password: str) -> Users|None:
    user = await UsersDAO.fetch_by_email(email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
