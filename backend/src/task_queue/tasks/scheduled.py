from auth.dao import IssuedTokensDAO
from task_queue.worker import celery_app


@celery_app.task
async def delete_expired_tokens() -> None:
    await IssuedTokensDAO.delete_expired()
