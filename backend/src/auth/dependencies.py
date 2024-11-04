from fastapi import Depends, Request

from config import settings

from .models import AccessTokenPayload, RefreshTokenPayload
from .security import _extract_correct_payload_from_token


def _get_access_token(request: Request) -> str|None:
    return request.cookies.get('access_token')


def _get_refresh_token(request: Request) -> str|None:
    return request.cookies.get('refresh_token')


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
