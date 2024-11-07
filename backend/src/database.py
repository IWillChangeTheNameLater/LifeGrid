from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from config import settings


_engine = create_async_engine(settings.db_dsn)

init_session = async_sessionmaker(_engine, class_=AsyncSession)


async def _generate_session() -> AsyncGenerator[AsyncSession, None]:
    async with init_session() as session:
        yield session


session_dependency = Annotated[AsyncSession, Depends(_generate_session)]
