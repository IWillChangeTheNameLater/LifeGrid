from fastapi import APIRouter, HTTPException, Response, status

from auth import security
from auth.models import AccessTokenPayload, RefreshTokenPayload, Tokens
from auth.utils import set_tokens_in_cookies
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

    access_jwt = security.create_access_jwt(
        AccessTokenPayload(sub=user.id, email=user.email)
    )
    refresh_jwt = security.create_refresh_jwt(RefreshTokenPayload(sub=user.id))
    tokens = Tokens(access_token=access_jwt, refresh_token=refresh_jwt)

    set_tokens_in_cookies(response, tokens)

    return tokens
