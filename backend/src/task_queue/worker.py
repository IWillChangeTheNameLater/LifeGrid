from pathlib import Path

from celery import Celery

from config import settings


celery_app = Celery(
    main=Path(__file__).parent.name,
    broker=settings.redis_broker_dsn,
    backend=settings.redis_backend_dsn,
)

celery_app.autodiscover_tasks(['task_queue.scheduler', 'task_queue.tasks'])

if __name__ == '__main__':
    celery_app.start()
