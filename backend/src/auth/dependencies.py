from fastapi import Depends, Request
import jwt

from config import settings
from exceptions import *

from .models import AccessTokenPayload, RefreshTokenPayload


def _get_access_token(request: Request) -> str|None:
    return request.cookies.get('access_token')


def _get_refresh_token(request: Request) -> str|None:
    return request.cookies.get('refresh_token')


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


def get_access_token_payload(
    token: str|None = Depends(_get_access_token)
) -> AccessTokenPayload:
    payload = _extract_correct_payload_from_token(
        token, settings.access_token_key
    )
    return AccessTokenPayload(**payload)


def get_refresh_token_payload(
    token: str|None = Depends(_get_refresh_token)
) -> RefreshTokenPayload:
    payload = _extract_correct_payload_from_token(
        token, settings.refresh_token_key
    )
    return RefreshTokenPayload(**payload)
