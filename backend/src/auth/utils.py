from fastapi import Response

from users.models import Users

from .dao import IssuedTokensDAO
from .dependencies import _get_refresh_token_payload
from .models import (
    AccessTokenPayload,
    RefreshTokenPayload,
    TokenFunction,
    Tokens,
)
from .security import create_access_token, create_refresh_token


def create_tokens_from_user(user: Users, device_id: str) -> Tokens:
    if user.id is None:
        raise ValueError("User's id is None")

    access_token = create_access_token(
        AccessTokenPayload(
            sub=user.id,
            email=user.email,
            email_verified=user.is_email_verified
        )
    )
    refresh_token = create_refresh_token(
        RefreshTokenPayload(sub=user.id, device_id=device_id)
    )
    return Tokens(access_token=access_token, refresh_token=refresh_token)


def set_tokens_in_cookies(response: Response, tokens: Tokens) -> None:
    response.set_cookie(TokenFunction.ACCESS, tokens.access_token)
    response.set_cookie(
        TokenFunction.REFRESH, tokens.refresh_token, httponly=True
    )


async def give_user_tokens(
    response: Response, user: Users, device_id: str
) -> Tokens:
    tokens = create_tokens_from_user(user, device_id)
    await IssuedTokensDAO.add(_get_refresh_token_payload(tokens.refresh_token))
    set_tokens_in_cookies(response, tokens)
    return tokens
