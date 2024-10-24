from fastapi import APIRouter, HTTPException

from auth.security import hash_password
from users.dao import UsersDAO
from users.models import UserRegister, Users


router = APIRouter(prefix='/auth')


@router.post('/register')
async def register(user_register: UserRegister) -> None:
    user = await UsersDAO.fetch_by_email(user_register.email)
    if user: raise HTTPException(500)
    hashed_password = hash_password(user_register.password)
    await UsersDAO.add(
        Users(email=user_register.email, hashed_password=hashed_password)
    )
