from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from config import settings


engine = create_async_engine(settings.db_dsn)

init_session = async_sessionmaker(engine, class_=AsyncSession)
