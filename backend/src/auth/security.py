from datetime import datetime, timedelta, UTC

import bcrypt, jwt

from config import Settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_jwt(payload: dict, seconds_to_expire: int, key: str) -> str:
    payload = payload.copy()
    payload['exp'] = datetime.now(UTC) + timedelta(seconds=seconds_to_expire)
    encoded_jwt = jwt.encode(payload, key, Settings.jwt_algorithm)
    return encoded_jwt


def create_access_token(payload: dict) -> str:
    return create_jwt(
        payload, Settings.access_jwt_exp_sec, Settings.access_jwt_key
    )


def create_refresh_token(payload: dict) -> str:
    return create_jwt(
        payload, Settings.refresh_jwt_exp_sec, Settings.refresh_jwt_key
    )