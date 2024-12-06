from datetime import datetime, UTC
from typing import cast

from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import select

from base_dao import BaseDAO
from database import init_session
from exceptions import *

from .models import (
    IssuedConfirmationTokens,
    IssuedRefreshTokens,
    RefreshTokenPayload,
)


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


class IssuedConfirmationTokensDAO(BaseDAO):
    model = IssuedConfirmationTokens

    @classmethod
    async def delete_user_tokens(cls, user_id: str) -> None:
        condition = cast(BinaryExpression, cls.model.user_id == user_id)
        await cls.delete_by_condition(condition)

    @classmethod
    async def issue_token(cls, user_id: str) -> str:
        async with init_session() as session:
            await cls.delete_user_tokens(user_id)

            issued_token = cls.model(user_id=user_id)
            token_id = issued_token.id
            session.add(issued_token)
            await session.commit()
            return token_id

    @classmethod
    async def delete_expired(cls) -> None:
        current_time = int(datetime.now(UTC).timestamp())
        condition = cast(BinaryExpression, cls.model.expire_at < current_time)
        await cls.delete_by_condition(condition)

    @classmethod
    async def extract_token(cls, token_id: str) -> IssuedConfirmationTokens:
        async with init_session() as session:
            if token := await session.get(cls.model, token_id):
                await session.delete(token)
                await session.commit()
                return token
            else:
                raise TokenAbsentException
