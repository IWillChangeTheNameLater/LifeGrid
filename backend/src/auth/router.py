from fastapi import APIRouter, Response

from database import session_dependency
from exceptions import *
from users.dao import UsersDAO
from users.models import UserLogin, UserRegister, Users

from .dao import IssuedTokensDAO
from .dependencies import refresh_payload_dependency
from .models import Tokens
from .security import authenticate_user, confirm_email_with_token, hash_text
from .utils import give_user_tokens, set_tokens_in_cookies


router = APIRouter(prefix='/auth')


@router.post('/register')
async def register(
        response: Response,
        user_register: UserRegister,
        device_id: str,
        session: session_dependency
) -> Tokens:
    user = await UsersDAO.fetch_by_email(user_register.email)
    if user:
        raise UserAlreadyExistsException

    hashed_password = hash_text(user_register.password)
    new_user = Users(
        email=user_register.email, hashed_password=hashed_password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return await give_user_tokens(response, new_user, device_id)


@router.post('/login')
async def login(
        response: Response, user_login: UserLogin, device_id: str
) -> Tokens:
    user = await authenticate_user(user_login.email, user_login.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    return await give_user_tokens(response, user, device_id)


@router.post('/refresh')
async def refresh(
        response: Response, refresh_token_payload: refresh_payload_dependency
) -> Tokens:
    user = await UsersDAO.fetch_by_primary_key(refresh_token_payload.sub)
    if not user:
        raise UserIsNotPresentException

    await IssuedTokensDAO.revoke_token(refresh_token_payload)

    return await give_user_tokens(
        response, user, refresh_token_payload.device_id
    )


@router.post('/logout')
async def logout(
        response: Response, refresh_token_payload: refresh_payload_dependency
) -> None:
    await IssuedTokensDAO.revoke_token(refresh_token_payload)

    invalid_tokens = Tokens(access_token='', refresh_token='')
    set_tokens_in_cookies(response, invalid_tokens)


@router.post('/confirm_email')
async def confirm_email(confirmation_token: str) -> None:
    await confirm_email_with_token(confirmation_token)
