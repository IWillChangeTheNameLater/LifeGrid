from datetime import datetime, UTC
from typing import cast

from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import select

from base_dao import BaseDAO
from database import init_session
from exceptions import *

from .models import IssuedRefreshTokens, RefreshTokenPayload


class IssuedTokensDAO(BaseDAO):
    model = IssuedRefreshTokens

    @classmethod
    async def add(cls, token: RefreshTokenPayload) -> None:
        async with init_session() as session:
            issued_token = IssuedRefreshTokens(
                jti=token.jti,
                sub=token.sub,
                device_id=token.device_id,
                exp=token.exp,
            )
            session.add(issued_token)
            await session.commit()

    @classmethod
    async def revoke_token(cls, token: RefreshTokenPayload) -> None:
        async with init_session() as session:
            statement = select(cls.model).where(cls.model.jti == token.jti)
            current_token = (await session.exec(statement)).one()
            if current_token.is_revoked:
                raise TokenAlreadyRevoked
            else:
                current_token.is_revoked = True
                session.add(current_token)
                await session.commit()

    @classmethod
    async def delete_expired(cls) -> None:
        current_time = int(datetime.now(UTC).timestamp())
        condition = cast(BinaryExpression, cls.model.exp < current_time)
        await cls.delete_by_condition(condition)
