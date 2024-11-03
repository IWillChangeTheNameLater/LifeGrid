from fastapi import Depends, Request
import jwt

from auth.models import AccessTokenPayload, RefreshTokenPayload
from config import settings
from exceptions import *


def _get_access_jwt(request: Request) -> str|None:
    return request.cookies.get('access_jwt')


def _get_refresh_jwt(request: Request) -> str|None:
    return request.cookies.get('refresh_jwt')


def _extract_correct_payload_from_jwt(token: str|None, key: str) -> dict:
    if not token:
        raise TokenAbsentException
    try:
        payload: dict = jwt.decode(
            token, key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except jwt.PyJWTError:
        raise TokenExpiredException
    except TypeError:
        raise IncorrectTokenFormatException


def get_access_jwt_payload(
    token: str|None = Depends(_get_access_jwt)
) -> AccessTokenPayload:
    payload = _extract_correct_payload_from_jwt(token, settings.access_jwt_key)
    return AccessTokenPayload(**payload)


def get_refresh_jwt_payload(
    token: str|None = Depends(_get_refresh_jwt)
) -> RefreshTokenPayload:
    payload = _extract_correct_payload_from_jwt(
        token, settings.refresh_jwt_key
    )
    return RefreshTokenPayload(**payload)
