from pydantic import EmailStr
from sqlmodel import select

from base_dao import BaseDAO
from database import init_session
from exceptions import *

from .models import Users


class UsersDAO(BaseDAO[Users]):
    model = Users

    @classmethod
    async def fetch_by_email(cls, email: EmailStr) -> Users|None:
        async with init_session() as session:
            statement = select(cls.model).where(cls.model.email == email)
            results = await session.exec(statement)
            return results.first()

    @classmethod
    async def verify_email(cls, user_id: str) -> None:
        async with init_session() as session:
            user = await session.get(cls.model, user_id)
            if user:
                user.is_email_verified = True
                session.add(user)
                await session.commit()
            else:
                raise UserIsNotPresentException
