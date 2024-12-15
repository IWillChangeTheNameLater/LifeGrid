from enum import IntEnum, StrEnum, unique
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from common.models import ULIDField, ULIDStr

if TYPE_CHECKING:
    from domains.users.models import Users


@unique
class Theme(StrEnum):
    LIGHT = 'light'
    DARK = 'dark'
    SYSTEM = 'system'


@unique
class Weekdays(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class UserSettingsScheme(SQLModel):
    accent_color_hex: str|None = Field(min_length=6, max_length=6)
    theme: Theme|None = None
    week_start_day: Weekdays|None = None


user_default_settings = UserSettingsScheme(
    accent_color_hex='42adff',
    theme=Theme.SYSTEM,
    week_start_day=Weekdays.MONDAY
)


class UsersSettings(UserSettingsScheme, table=True):
    __tablename__ = 'users_settings'

    id: ULIDStr = ULIDField(primary_key=True)

    user_id: ULIDStr = Field(
        foreign_key='users.id',
        ondelete='CASCADE',
        unique=True,
        nullable=False,
        index=True
    )

    user: 'Users' = Relationship(
        back_populates='user_settings',
        sa_relationship_kwargs={
            'lazy': 'selectin', 'uselist': False
        }
    )
