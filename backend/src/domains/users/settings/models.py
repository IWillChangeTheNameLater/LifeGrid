from enum import IntEnum, StrEnum, unique
from typing import Annotated, TYPE_CHECKING

from pydantic import AfterValidator
from sqlmodel import Field, Relationship, SQLModel

from common.models import ULIDField, ULIDStr

from .user_profile import UserProfile

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


def is_hex_color(color_code: str) -> str:
    color_code = color_code.lower()
    if len(color_code) == 3:
        color_code = ''.join(i + i for i in color_code)

    if len(color_code) != 6:
        raise ValueError(
            f'The color code {color_code} must be 3 or 6 characters long'
        )
    if set(color_code) - set('0123456789abcdef'):
        raise ValueError(f'The color code {color_code} must be a hex number')

    return color_code


HEXStr = Annotated[str, AfterValidator(is_hex_color)]


class UserSettingsScheme(SQLModel):
    accent_color_hex: HEXStr|None = Field(min_length=6, max_length=6)
    theme: Theme|None = None
    week_start_day: Weekdays|None = None

    profile: UserProfile|None = None


_user_default_settings = UserSettingsScheme(
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
