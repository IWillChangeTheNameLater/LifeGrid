from datetime import datetime, UTC

from sqlmodel import select

from base_dao import BaseDAO
from database import init_session
from exceptions import *

from .models import IssuedTokens, RefreshTokenPayload
from .security import create_refresh_token


class IssuedTokensDAO(BaseDAO):
    model = IssuedTokens

    @classmethod
    async def add(cls, token: RefreshTokenPayload) -> None:
        async with init_session() as session:
            issued_token = IssuedTokens(
                sub=token.sub,
                device_id=token.device_id,
                exp=token.exp,
                token=create_refresh_token(token)
            )
            session.add(issued_token)
            await session.commit()

    @classmethod
    async def revoke_former_token(cls, token: RefreshTokenPayload) -> None:
        async with init_session() as session:
            statement = select(cls.model).where(
                cls.model.sub == token.sub,
                cls.model.device_id == token.device_id,
                cls.model.token == create_refresh_token(token)
            )
            former_token = (await session.exec(statement)).one()
            if former_token.is_revoked:
                raise TokenAlreadyRevoked
            else:
                former_token.is_revoked = True
                session.add(former_token)
                await session.commit()

    @classmethod
    async def revoke_user_tokens(cls, sub: int, device_id: str) -> None:
        async with init_session() as session:
            statement = select(
                cls.model
            ).where(cls.model.sub == sub, cls.model.device_id == device_id)
            user_tokens = await session.exec(statement)
            for token in user_tokens:
                token.is_revoked = True
                session.add(token)
            await session.commit()

    @classmethod
    async def clean_expired(cls) -> None:
        async with init_session() as session:
            current_time = int(datetime.now(UTC).timestamp())
            statement = select(cls.model).where(cls.model.exp < current_time)
            expired_tokens = await session.exec(statement)
            for token in expired_tokens:
                await session.delete(token)
            await session.commit()
