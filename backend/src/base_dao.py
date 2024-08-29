from abc import ABC
from typing import Generic, Type, TypeVar

from sqlmodel import SQLModel


T = TypeVar('T', bound=SQLModel)


class BaseDAO(Generic[T], ABC):
    model: Type[T]
