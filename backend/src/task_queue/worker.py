from enum import Enum, unique
from pathlib import Path

from celery import Celery

from config import settings


@unique
class CeleryQueue(Enum):
    LOW_PRIORITY = 'low_priority'
    HIGH_PRIORITY = 'high_priority'

    DEFAULT = 'default'


celery_app = Celery(
    main=Path(__file__).parent.name,
    broker=settings.redis_broker_dsn,
    backend=settings.redis_backend_dsn,
    include=['task_queue.scheduler', 'task_queue.tasks']
)

# Configuration
celery_app.conf.task_default_queue = CeleryQueue.DEFAULT.value

if __name__ == '__main__':
    celery_app.start()
