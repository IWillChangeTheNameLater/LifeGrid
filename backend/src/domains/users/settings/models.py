from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, Relationship

from common.models import ULIDField, ULIDStr

if TYPE_CHECKING:
    from ..models import Users


class Theme(StrEnum):
    LIGHT = 'light'
    DARK = 'dark'


class UserSettings(BaseModel):
    accent_color: str|None = Field(min_length=3, max_length=6)
    theme: Theme|None


class UsersSettings(UserSettings, table=True):
    __tablename__ = 'users_settings'

    id: ULIDStr = ULIDField(primary_key=True)

    user: Users = Relationship(
        back_populates='user_settings',
        sa_relationship_kwargs={
            'lazy': 'selectin', 'uselist': False
        }
    )
