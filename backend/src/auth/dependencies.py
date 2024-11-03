from fastapi import Depends, Request
from jwt import PyJWTError

from auth.models import AccessTokenPayload, RefreshTokenPayload
from auth.security import _extract_payload_from_jwt
from config import settings
from exceptions import *


def _get_access_jwt(request: Request) -> str|None:
    return request.cookies.get('access_jwt')


def _get_refresh_jwt(request: Request) -> str|None:
    return request.cookies.get('refresh_jwt')


def get_access_jwt_payload(
    token: str = Depends(_get_access_jwt)
) -> AccessTokenPayload:
    if not token:
        raise TokenAbsentException
    try:
        payload = _extract_payload_from_jwt(token, settings.access_jwt_key)
        return AccessTokenPayload(**payload)
    except PyJWTError:
        raise TokenExpiredException
    except TypeError:
        raise IncorrectTokenFormatException


def get_refresh_jwt_payload(
    token: str = Depends(_get_refresh_jwt)
) -> RefreshTokenPayload:
    if not token:
        raise TokenAbsentException
    try:
        payload = _extract_payload_from_jwt(token, settings.refresh_jwt_key)
        return RefreshTokenPayload(**payload)
    except PyJWTError:
        raise TokenExpiredException
    except TypeError:
        raise IncorrectTokenFormatException
