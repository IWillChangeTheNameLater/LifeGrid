from fastapi import Depends, HTTPException, Request, status
import jwt

from auth.models import AccessTokenPayload, RefreshTokenPayload
from auth.security import _extract_payload_from_jwt
from config import settings


def _get_access_jwt(request: Request) -> str|None:
    return request.cookies.get('access_jwt')


def _get_refresh_jwt(request: Request) -> str|None:
    return request.cookies.get('refresh_jwt')


def get_access_jwt_payload(
    token: str = Depends(_get_access_jwt)
) -> AccessTokenPayload:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = _extract_payload_from_jwt(token, settings.access_jwt_key)
        return AccessTokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except TypeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_refresh_jwt_payload(
    token: str = Depends(_get_refresh_jwt)
) -> RefreshTokenPayload:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = _extract_payload_from_jwt(token, settings.refresh_jwt_key)
        return RefreshTokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except TypeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
