import asyncio

from celery import shared_task

from email_service import send_email
from email_service.composers.confirmation import confirmation_email
from task_queue.celery_config import CeleryQueue


event_loop = asyncio.get_event_loop()


@shared_task(queue=CeleryQueue.HIGH_PRIORITY)
def request_confirmation_email(
    recipient_email: str, confirmation_link: str
) -> None:
    send_email(confirmation_email(confirmation_link), to_=recipient_email)
