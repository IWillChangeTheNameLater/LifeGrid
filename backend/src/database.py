from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from config import settings


_engine = create_async_engine(settings.db_dsn)

init_session = async_sessionmaker(_engine, class_=AsyncSession)


async def session_dependency() -> AsyncGenerator[AsyncSession, None]:
    async with init_session() as session:
        yield session
