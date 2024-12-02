from typing import Any

from celery.app.base import Celery

from task_queue.worker import celery_app


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs: dict[str, Any]) -> None:
    ...
