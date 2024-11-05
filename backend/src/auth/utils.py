from fastapi import Response

from users.models import Users

from .models import AccessTokenPayload, RefreshTokenPayload, Tokens
from .security import create_access_token, create_refresh_token


def create_tokens_from_user(user: Users) -> Tokens:
    if user.id is None:
        raise ValueError("User's id is None")

    access_token = create_access_token(
        AccessTokenPayload(sub=user.id, email=user.email)
    )
    refresh_token = create_refresh_token(RefreshTokenPayload(sub=user.id))
    return Tokens(access_token=access_token, refresh_token=refresh_token)


def set_tokens_in_cookies(response: Response, tokens: Tokens) -> None:
    response.set_cookie('access_token', tokens.access_token)
    response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)
