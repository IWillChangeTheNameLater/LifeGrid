from fastapi import APIRouter, HTTPException, Response, status

from auth import security
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
async def login(response: Response, user_login: UserLogin) -> None:
    user = await security.authenticate_user(
        user_login.email, user_login.password
    )
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    access_jwt = security.create_access_jwt({
        'sub': user.id,
        'email': user.email
    })
    refresh_jwt = security.create_refresh_jwt({'sub': user.id})

    response.set_cookie('access_jwt', access_jwt)
    response.set_cookie('refresh_jwt', refresh_jwt, httponly=True)
