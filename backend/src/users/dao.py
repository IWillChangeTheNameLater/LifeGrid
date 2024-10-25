from pydantic import EmailStr
from sqlmodel import select

from base_dao import BaseDAO
from database import init_session
from users.models import Users


class UsersDAO(BaseDAO[Users]):
    model = Users

    @classmethod
    async def fetch_by_email(cls, email: EmailStr) -> Users|None:
        async with init_session() as session:
            statement = select(cls.model).where(cls.model.email == email)
            results = await session.exec(statement)
            return results.first()
