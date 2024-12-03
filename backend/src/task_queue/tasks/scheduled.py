import asyncio

from auth.dao import IssuedTokensDAO
from task_queue.worker import celery_app


event_loop = asyncio.get_event_loop()


@celery_app.task
def delete_expired_tokens() -> None:
    event_loop.run_until_complete(IssuedTokensDAO.delete_expired())
