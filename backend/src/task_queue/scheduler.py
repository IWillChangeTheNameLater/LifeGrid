from datetime import timedelta
from typing import Any

from celery.app.base import Celery

from .tasks.scheduled import *
from .worker import celery_app


# noinspection PyUnusedLocal
@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs: dict[str, Any]) -> None:
    sender.add_periodic_task(
        name='Clear the database of expired tokens',
        sig=delete_expired_tokens.s(),
        schedule=timedelta(days=1)
    )

    sender.add_periodic_task(
        name='Clear the database of expired confirmation tokens',
        sig=delete_expired_confirmation_tokens.s(),
        schedule=timedelta(days=1)
    )
