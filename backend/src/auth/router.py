from fastapi import APIRouter, HTTPException, Response, status

from auth import security
from auth.models import Tokens
from auth.utils import create_tokens_from_user, set_tokens_in_cookies
from users.dao import UsersDAO
from users.models import UserLogin, UserRegister, Users


router = APIRouter(prefix='/auth')


@router.post('/register')
async def register(user_register: UserRegister) -> None:
    user = await UsersDAO.fetch_by_email(user_register.email)
    if user: raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    hashed_password = security.hash_password(user_register.password)
    await UsersDAO.add(
        Users(email=user_register.email, hashed_password=hashed_password)
    )


@router.post('/login')
async def login(response: Response, user_login: UserLogin) -> Tokens:
    user = await security.authenticate_user(
        user_login.email, user_login.password
    )
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    tokens = create_tokens_from_user(user)

    set_tokens_in_cookies(response, tokens)

    return tokens


@router.post('/logout')
async def logout(response: Response) -> None:
    invalid_tokens = Tokens(access_token='', refresh_token='')

    set_tokens_in_cookies(response, invalid_tokens)
