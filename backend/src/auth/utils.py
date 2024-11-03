from fastapi import Response

from auth.models import AccessTokenPayload, RefreshTokenPayload, Tokens
from auth.security import create_access_jwt, create_refresh_jwt
from users.models import Users


def create_tokens_from_user(user: Users) -> Tokens:
    access_jwt = create_access_jwt(
        AccessTokenPayload(sub=user.id, email=user.email)
    )
    refresh_jwt = create_refresh_jwt(RefreshTokenPayload(sub=user.id))
    return Tokens(access_token=access_jwt, refresh_token=refresh_jwt)


def set_tokens_in_cookies(response: Response, tokens: Tokens) -> None:
    response.set_cookie('access_jwt', tokens.access_token)
    response.set_cookie('refresh_jwt', tokens.refresh_token, httponly=True)
