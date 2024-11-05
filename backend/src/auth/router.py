from fastapi import APIRouter, Depends, Response

from exceptions import *
from users.dao import UsersDAO
from users.models import UserLogin, UserRegister, Users

from .dependencies import get_refresh_token_payload
from .models import RefreshTokenPayload, Tokens
from .security import authenticate_user, hash_text
from .utils import create_tokens_from_user, set_tokens_in_cookies


router = APIRouter(prefix='/auth')


@router.post('/register')
async def register(response: Response, user_register: UserRegister) -> Tokens:
    user = await UsersDAO.fetch_by_email(user_register.email)
    if user:
        raise UserAlreadyExistsException

    hashed_password = hash_text(user_register.password)
    user = Users(email=user_register.email, hashed_password=hashed_password)
    await UsersDAO.add(user)

    new_user = await UsersDAO.fetch_by_email(user_register.email)
    assert new_user
    tokens = create_tokens_from_user(new_user)
    set_tokens_in_cookies(response, tokens)

    return tokens


@router.post('/login')
async def login(response: Response, user_login: UserLogin) -> Tokens:
    user = await authenticate_user(user_login.email, user_login.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    tokens = create_tokens_from_user(user)
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
    tokens = create_tokens_from_user(user)

    set_tokens_in_cookies(response, tokens)

    return tokens


@router.post('/logout')
async def logout(response: Response) -> None:
    invalid_tokens = Tokens(access_token='', refresh_token='')

    set_tokens_in_cookies(response, invalid_tokens)
