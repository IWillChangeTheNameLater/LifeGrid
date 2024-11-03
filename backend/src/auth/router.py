from fastapi import APIRouter, Depends, HTTPException, Response, status

from auth.dependencies import get_refresh_jwt_payload
from auth.models import RefreshTokenPayload, Tokens
from auth.security import authenticate_user, hash_password
from auth.utils import create_tokens_from_user, set_tokens_in_cookies
from users.dao import UsersDAO
from users.models import UserLogin, UserRegister, Users


router = APIRouter(prefix='/auth')


@router.post('/register')
async def register(user_register: UserRegister) -> None:
    user = await UsersDAO.fetch_by_email(user_register.email)
    if user: raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    hashed_password = hash_password(user_register.password)
    await UsersDAO.add(
        Users(email=user_register.email, hashed_password=hashed_password)
    )


@router.post('/login')
async def login(response: Response, user_login: UserLogin) -> Tokens:
    user = await authenticate_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    tokens = create_tokens_from_user(user)

    set_tokens_in_cookies(response, tokens)

    return tokens


@router.post('/refresh')
async def refresh(
    response: Response,
    refresh_token_payload: RefreshTokenPayload = Depends(
    get_refresh_jwt_payload
    )
) -> Tokens:
    user = await UsersDAO.fetch_by_primary_key(refresh_token_payload.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    tokens = create_tokens_from_user(user)

    set_tokens_in_cookies(response, tokens)

    return tokens


@router.post('/logout')
async def logout(response: Response) -> None:
    invalid_tokens = Tokens(access_token='', refresh_token='')

    set_tokens_in_cookies(response, invalid_tokens)
