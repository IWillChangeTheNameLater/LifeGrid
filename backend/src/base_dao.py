from abc import ABC
from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import select, SQLModel

from database import init_session


T = TypeVar('T', bound=SQLModel)


class BaseDAO(Generic[T], ABC):
    model: Type[T]

    @classmethod
    async def fetch_all(cls) -> Sequence[T]:
        async with init_session() as session:
            statement = select(cls.model)
            results = await session.exec(statement)
            return results.all()

    @classmethod
    async def fetch_by_primary_key(cls, primary_key: Any) -> T|None:
        async with init_session() as session:
            result: T|None = await session.get(cls.model, primary_key)
            return result

    @classmethod
    async def add(cls, row: T) -> None:
        async with init_session() as session:
            session.add(row)
            await session.commit()

    @classmethod
    async def delete(cls, row: T) -> None:
        async with init_session() as session:
            await session.delete(row)
            await session.commit()

    @classmethod
    async def delete_by_primary_key(cls, primary_key: Any) -> None:
        async with init_session() as session:
            result = await session.get(cls.model, primary_key)
            await session.delete(result)
            await session.commit()

    @classmethod
    async def delete_by_condition(cls, condition: BinaryExpression) -> None:
        async with init_session() as session:
            statement = select(cls.model).where(condition)
            results = await session.exec(statement)
            for row in results:
                await session.delete(row)
            await session.commit()
