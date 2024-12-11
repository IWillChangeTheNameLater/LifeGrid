import asyncio

from celery import shared_task
from pydantic import EmailStr

from common.emails import confirmation_email, send_email
from common.task_queue.celery_config import CeleryQueue


event_loop = asyncio.get_event_loop()


@shared_task(queue=CeleryQueue.HIGH_PRIORITY)
def request_confirmation_email(
    recipient_email: EmailStr, confirmation_link: str
) -> None:
    send_email(confirmation_email(confirmation_link), to_=recipient_email)
