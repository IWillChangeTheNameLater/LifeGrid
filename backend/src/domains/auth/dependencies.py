from typing import Annotated

from fastapi import Depends, Request
import jwt

from common.config import settings
from common.exceptions import *

from .models import AccessTokenPayload, RefreshTokenPayload, TokenFunction


def _get_access_token(request: Request) -> str:
    token = request.cookies.get(TokenFunction.ACCESS)
    if token:
        return token
    else:
        raise TokenAbsentException


def _get_refresh_token(request: Request) -> str:
    token = request.cookies.get(TokenFunction.REFRESH)
    if token:
        return token
    else:
        raise TokenAbsentException


def _extract_valid_token_payload(token: str, key: str) -> dict:
    try:
        payload: dict = jwt.decode(
            token, key, algorithms=[settings.token_crypt_algorithm]
        )
        return payload
    except jwt.PyJWTError:
        raise TokenExpiredException
    except TypeError:
        raise IncorrectTokenFormatException


def _get_access_token_payload(
    token: str = Depends(_get_access_token)
) -> AccessTokenPayload:
    payload = _extract_valid_token_payload(token, settings.access_token_key)
    return AccessTokenPayload(**payload)


access_payload_dependency = Annotated[AccessTokenPayload,
                                      Depends(_get_access_token_payload)]


def _get_refresh_token_payload(
    token: str = Depends(_get_refresh_token)
) -> RefreshTokenPayload:
    payload = _extract_valid_token_payload(token, settings.refresh_token_key)
    return RefreshTokenPayload(**payload)


refresh_payload_dependency = Annotated[RefreshTokenPayload,
                                       Depends(_get_refresh_token_payload)]
