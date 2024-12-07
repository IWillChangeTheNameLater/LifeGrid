import asyncio

from celery import shared_task

from auth.dao import IssuedConfirmationTokensDAO, IssuedTokensDAO
from task_queue.celery_config import CeleryQueue


event_loop = asyncio.get_event_loop()


@shared_task(
    time_limit=30*60, soft_time_limit=20*60, queue=CeleryQueue.LOW_PRIORITY
)
def delete_expired_tokens() -> None:
    event_loop.run_until_complete(IssuedTokensDAO.delete_expired())


@shared_task(
    time_limit=30*60, soft_time_limit=20*60, queue=CeleryQueue.LOW_PRIORITY
)
def delete_expired_confirmation_tokens() -> None:
    event_loop.run_until_complete(IssuedConfirmationTokensDAO.delete_expired())
