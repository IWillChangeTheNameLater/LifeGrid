import asyncio

from auth.dao import IssuedTokensDAO
from task_queue.worker import celery_app


@celery_app.task
def delete_expired_tokens() -> None:
    asyncio.run(IssuedTokensDAO.delete_expired())
