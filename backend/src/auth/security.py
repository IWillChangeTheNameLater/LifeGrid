import bcrypt, jwt
from fastapi import Response
from pydantic import EmailStr

from config import settings
from users.dao import UsersDAO
from users.models import Users

from .dao import IssuedTokensDAO
from .dependencies import get_refresh_token_payload
from .models import (
    AccessTokenPayload,
    BaseTokenPayload,
    RefreshTokenPayload,
    TokenFunction,
    Tokens,
)


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


def create_tokens_from_user(user: Users, device_id: str) -> Tokens:
    if user.id is None:
        raise ValueError("User's id is None")

    access_token = create_access_token(
        AccessTokenPayload(sub=user.id, email=user.email)
    )
    refresh_token = create_refresh_token(
        RefreshTokenPayload(sub=user.id, device_id=device_id)
    )
    return Tokens(access_token=access_token, refresh_token=refresh_token)


def set_tokens_in_cookies(response: Response, tokens: Tokens) -> None:
    response.set_cookie(TokenFunction.access.value, tokens.access_token)
    response.set_cookie(
        TokenFunction.refresh.value, tokens.refresh_token, httponly=True
    )


async def give_user_tokens(
    response: Response, user: Users, device_id: str
) -> Tokens:
    tokens = create_tokens_from_user(user, device_id)
    await IssuedTokensDAO.add(get_refresh_token_payload(tokens.refresh_token))
    set_tokens_in_cookies(response, tokens)
    return tokens
