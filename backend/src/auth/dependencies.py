from fastapi import Depends, Request

from config import settings
from exceptions import *

from .models import AccessTokenPayload, RefreshTokenPayload, TokenFunction
from .security import _extract_valid_token_payload


def _get_access_token(request: Request) -> str:
    token = request.cookies.get(TokenFunction.access.value)
    if token:
        return token
    else:
        raise TokenAbsentException


def _get_refresh_token(request: Request) -> str:
    token = request.cookies.get(TokenFunction.refresh.value)
    if token:
        return token
    else:
        raise TokenAbsentException


def get_access_token_payload(
    token: str = Depends(_get_access_token)
) -> AccessTokenPayload:
    payload = _extract_valid_token_payload(token, settings.access_token_key)
    return AccessTokenPayload(**payload)


def get_refresh_token_payload(
    token: str = Depends(_get_refresh_token)
) -> RefreshTokenPayload:
    payload = _extract_valid_token_payload(token, settings.refresh_token_key)
    return RefreshTokenPayload(**payload)
