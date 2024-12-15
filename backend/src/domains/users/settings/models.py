from enum import StrEnum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from common.models import ULIDField, ULIDStr

if TYPE_CHECKING:
    from domains.users.models import Users


class Theme(StrEnum):
    LIGHT = 'light'
    DARK = 'dark'


# class UserSettings(SQLModel):
#     accent_color: str|None = Field(min_length=3, max_length=6)
#     theme: Theme|None


class UsersSettings(SQLModel, table=True):
    __tablename__ = 'users_settings'

    id: ULIDStr = ULIDField(primary_key=True)

    user_id: ULIDStr = Field(
        foreign_key='users.id', ondelete='CASCADE', unique=True
    )
    user: 'Users' = Relationship(
        back_populates='user_settings',
        sa_relationship_kwargs={
            'lazy': 'selectin', 'uselist': False
        }
    )
