from datetime import datetime, UTC

import bcrypt, jwt
from pydantic import EmailStr

from config import settings
from exceptions import *
from users.dao import UsersDAO
from users.models import Users

from .dao import IssuedConfirmationTokensDAO
from .models import AccessTokenPayload, BaseTokenPayload, RefreshTokenPayload


def hash_text(text: str) -> str:
    return bcrypt.hashpw(text.encode(), bcrypt.gensalt()).decode()


def verify_hashed_text(text: str, hashed_text: str) -> bool:
    return bcrypt.checkpw(text.encode(), hashed_text.encode())


def _create_token(payload: BaseTokenPayload, key: str) -> str:
    encoded_token = jwt.encode(
        payload.model_dump(), key, settings.token_crypt_algorithm
    )
    return encoded_token


def create_access_token(payload: AccessTokenPayload) -> str:
    return _create_token(payload, settings.access_token_key)


def create_refresh_token(payload: RefreshTokenPayload) -> str:
    return _create_token(payload, settings.refresh_token_key)


async def authenticate_user(email: EmailStr, password: str) -> Users|None:
    user = await UsersDAO.fetch_by_email(email)
    if user and verify_hashed_text(password, user.hashed_password):
        return user
    return None


async def confirm_email_with_token(token_id: str) -> None:
    token = await IssuedConfirmationTokensDAO.extract_token(token_id)
    if token.expire_at < int(datetime.now(UTC).timestamp()):
        raise TokenExpiredException

    await UsersDAO.verify_email(token.user_id)
