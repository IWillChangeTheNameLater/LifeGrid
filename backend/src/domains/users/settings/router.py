from fastapi import APIRouter

from domains.auth.dependencies import access_payload_dependency

from .dao import UsersSettingsDAO
from .models import UserSettingsScheme


router = APIRouter(prefix='/settings')


@router.patch('/')
async def update_settings(
    settings_to_update: UserSettingsScheme,
    access_token_payload: access_payload_dependency,
) -> UserSettingsScheme:
    return await UsersSettingsDAO.update_settings(
        user_id=access_token_payload.sub,
        settings_to_update=settings_to_update
    )


@router.get('/')
async def get_settings(
    access_token_payload: access_payload_dependency
) -> UserSettingsScheme:
    return await UsersSettingsDAO.get_settings(access_token_payload.sub)


@router.delete('/')
async def reset_settings(
    access_token_payload: access_payload_dependency
) -> UserSettingsScheme:
    return await UsersSettingsDAO.reset_settings(access_token_payload.sub)
