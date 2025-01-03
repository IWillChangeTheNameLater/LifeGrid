from fastapi import APIRouter, Request, Response

from common.database import session_dependency
from common.exceptions import *
from common.task_queue.tasks import email_service as email_tasks
from domains.auth.dao import IssuedConfirmationTokensDAO
from domains.users.dao import UsersDAO
from domains.users.models import UserLogin, UserRegister, Users

from . import security
from .dao import IssuedTokensDAO
from .dependencies import access_payload_dependency, refresh_payload_dependency
from .models import Tokens
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

    hashed_password = security.hash_text(user_register.password)
    new_user = Users(
        email=user_register.email,
        hashed_password=hashed_password,
        birthday=user_register.birthday,
        days_at_death=user_register.days_at_death
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return await give_user_tokens(response, new_user, device_id)


@router.post('/login')
async def login(
    response: Response, user_login: UserLogin, device_id: str
) -> Tokens:
    user = await security.authenticate_user(
        user_login.email, user_login.password
    )
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


@router.patch('/change_password')
async def change_password(
    old_password: str,
    new_password: str,
    access_token_payload: access_payload_dependency,
    session: session_dependency
) -> None:
    user = await UsersDAO.fetch_by_primary_key(access_token_payload.sub)

    if not user:
        raise UserIsNotPresentException
    elif not security.verify_hashed_text(old_password, user.hashed_password):
        raise IncorrectPasswordException

    user.hashed_password = security.hash_text(new_password)
    session.add(user)
    await session.commit()


@router.post('/request_confirmation_email')
async def request_confirmation_email(
    request: Request, access_token_payload: access_payload_dependency
) -> None:
    if access_token_payload.email_verified:
        raise EmailAlreadyVerified

    token_id = await IssuedConfirmationTokensDAO.issue_token(
        access_token_payload.sub
    )

    confirmation_link = str(
        request.url_for(confirm_email.__name__, confirmation_token=token_id)
    )

    email_tasks.request_confirmation_email.delay(
        access_token_payload.email, confirmation_link
    )


@router.get('/confirm_email/{confirmation_token}')
async def confirm_email(confirmation_token: str) -> None:
    await security.confirm_email(confirmation_token)
