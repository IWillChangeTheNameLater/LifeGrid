from fastapi import Response

from users.models import Users

from .models import AccessTokenPayload, RefreshTokenPayload, TokenFunction, Tokens
from .security import create_access_token, create_refresh_token


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
