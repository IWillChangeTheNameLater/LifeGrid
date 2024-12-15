from typing import Any

from sqlmodel import select

from common.base_dao import BaseDAO
from common.database import init_session
from common.models import ULIDStr

from .models import user_default_settings, UserSettingsScheme, UsersSettings


def _extract_custom_settings(
    user_settings: UserSettingsScheme
) -> dict[str, Any]:
    user_default_settings_dict = user_default_settings.model_dump()
    user_settings_dict = user_settings.model_dump(
        exclude_none=True, exclude_unset=True, exclude_defaults=True
    )
    return {
        k: v
        for k,
        v in user_settings_dict.items()
        if user_settings_dict[k] != user_default_settings_dict[k]
    }


class UsersSettingsDAO(BaseDAO[UsersSettings]):
    model = UsersSettings

    @classmethod
    async def update_settings(
        cls, user_id: ULIDStr, settings_to_update: UserSettingsScheme
    ) -> UserSettingsScheme:
        async with init_session() as session:
            statement = select(cls.model).where(cls.model.user_id == user_id)
            current_settings = (await session.exec(statement)).first()
            if current_settings is None:
                current_settings = cls.model(user_id=user_id)

            custom_settings = _extract_custom_settings(settings_to_update)
            for attr, val in custom_settings.items():
                setattr(current_settings, attr, val)

            session.add(current_settings)
            await session.commit()
            await session.refresh(current_settings)

            return UserSettingsScheme(**current_settings.model_dump())

    @classmethod
    async def get_settings(cls, user_id: ULIDStr) -> UserSettingsScheme:
        async with init_session() as session:
            statement = select(cls.model).where(cls.model.user_id == user_id)
            user_settings = (await session.exec(statement)).first()
            settings = user_settings or user_default_settings

            complete_settings = UserSettingsScheme(**settings.model_dump())
            for attr, val in settings.model_dump().items():
                if val is None:
                    setattr(
                        complete_settings,
                        attr,
                        getattr(user_default_settings, attr)
                    )

            return complete_settings

    @classmethod
    async def reset_settings(cls, user_id: ULIDStr) -> UserSettingsScheme:
        async with init_session() as session:
            statement = select(cls.model).where(cls.model.user_id == user_id)
            settings = (await session.exec(statement)).first()
            await session.delete(settings)
            await session.commit()

        return user_default_settings
