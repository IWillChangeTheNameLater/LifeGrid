from celery import Celery

from config import settings


celery = Celery(
    'tasks',
    broker=f'redis://{settings.redis_host}:{settings.redis_port}',
    include=['src.tasks_queue.tasks']
)
