import bcrypt, jwt
from pydantic import EmailStr

from config import settings
from exceptions import *
from users.dao import UsersDAO
from users.models import Users

from .models import AccessTokenPayload, BaseTokenPayload, RefreshTokenPayload


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def _create_token(payload: BaseTokenPayload, key: str) -> str:
    encoded_token = jwt.encode(
        payload.model_dump(), key, settings.token_crypt_algorithm
    )
    return encoded_token


def create_access_token(payload: AccessTokenPayload) -> str:
    return _create_token(payload, settings.access_token_key)


def create_refresh_token(payload: RefreshTokenPayload) -> str:
    return _create_token(payload, settings.refresh_token_key)


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
