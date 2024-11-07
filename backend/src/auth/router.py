from fastapi import APIRouter, Depends, Response

from exceptions import *
from users.dao import UsersDAO
from users.models import UserLogin, UserRegister, Users

from .dao import IssuedTokensDAO
from .dependencies import get_refresh_token_payload
from .models import RefreshTokenPayload, Tokens
from .security import (
    authenticate_user,
    create_tokens_from_user,
    hash_text,
    set_tokens_in_cookies,
)


router = APIRouter(prefix='/auth')


@router.post('/register')
async def register(
    response: Response, user_register: UserRegister, device_id: str
) -> Tokens:
    user = await UsersDAO.fetch_by_email(user_register.email)
    if user:
        raise UserAlreadyExistsException

    hashed_password = hash_text(user_register.password)
    user = Users(email=user_register.email, hashed_password=hashed_password)
    await UsersDAO.add(user)

    new_user = await UsersDAO.fetch_by_email(user_register.email)
    assert new_user

    tokens = create_tokens_from_user(new_user, device_id)
    await IssuedTokensDAO.add(get_refresh_token_payload(tokens.refresh_token))
    set_tokens_in_cookies(response, tokens)

    return tokens


@router.post('/login')
async def login(
    response: Response, user_login: UserLogin, device_id: str
) -> Tokens:
    user = await authenticate_user(user_login.email, user_login.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    tokens = create_tokens_from_user(user, device_id)
    await IssuedTokensDAO.add(get_refresh_token_payload(tokens.refresh_token))
    set_tokens_in_cookies(response, tokens)

    return tokens


@router.post('/refresh')
async def refresh(
    response: Response,
    refresh_token_payload: RefreshTokenPayload = Depends(
    get_refresh_token_payload
    )
) -> Tokens:
    user = await UsersDAO.fetch_by_primary_key(refresh_token_payload.sub)
    if not user:
        raise UserIsNotPresentException

    try:
        await IssuedTokensDAO.revoke_current_token(refresh_token_payload)
    except TokenAlreadyRevoked:
        assert user.id
        await IssuedTokensDAO.revoke_user_device_tokens(
            refresh_token_payload.sub, refresh_token_payload.device_id
        )
        raise

    tokens = create_tokens_from_user(user, refresh_token_payload.device_id)
    await IssuedTokensDAO.add(get_refresh_token_payload(tokens.refresh_token))
    set_tokens_in_cookies(response, tokens)

    return tokens


@router.post('/logout')
async def logout(
    response: Response,
    refresh_token_payload: RefreshTokenPayload = Depends(
    get_refresh_token_payload
    )
) -> None:
    await IssuedTokensDAO.revoke_current_token(refresh_token_payload)

    invalid_tokens = Tokens(access_token='', refresh_token='')
    set_tokens_in_cookies(response, invalid_tokens)
