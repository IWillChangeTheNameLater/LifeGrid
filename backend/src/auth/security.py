from datetime import datetime, timedelta, UTC

import bcrypt, jwt
from pydantic import EmailStr

from config import settings
from users.dao import UsersDAO
from users.models import Users


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_jwt(payload: dict, seconds_to_expire: int, key: str) -> str:
    payload = payload.copy()
    payload['exp'] = datetime.now(UTC) + timedelta(seconds=seconds_to_expire)
    encoded_jwt = jwt.encode(payload, key, settings.jwt_algorithm)
    return encoded_jwt


def create_access_jwt(payload: dict) -> str:
    return create_jwt(
        payload, settings.access_jwt_exp_sec, settings.access_jwt_key
    )


def create_refresh_jwt(payload: dict) -> str:
    return create_jwt(
        payload, settings.refresh_jwt_exp_sec, settings.refresh_jwt_key
    )


def extract_jwt_payload(token: str, key: str) -> dict:
    payload: dict = jwt.decode(token, key, algorithms=[settings.jwt_algorithm])
    return payload


def extract_access_jwt_payload(token: str) -> dict:
    return extract_jwt_payload(token, settings.access_jwt_key)


def extract_refresh_jwt_payload(token: str) -> dict:
    return extract_jwt_payload(token, settings.refresh_jwt_key)


async def authenticate_user(email: EmailStr, password: str) -> Users|None:
    user = await UsersDAO.fetch_by_email(email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
