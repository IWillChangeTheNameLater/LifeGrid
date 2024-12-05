from enum import Enum, unique

from kombu import Queue

from config import RedisDB, settings


@unique
class CeleryQueue(Enum):
    LOW_PRIORITY = 'low_priority'
    HIGH_PRIORITY = 'high_priority'

    DEFAULT = 'default'


# The Celery app config
imports = ('task_queue.scheduler', 'task_queue.tasks')
broker_url = f'redis://{settings.redis_host}:{settings.redis_port}/{RedisDB.MESSAGE_BROKER.value}'
result_backend = f'redis://{settings.redis_host}:{settings.redis_port}/{RedisDB.RESULT_BACKEND.value}'

# Misc config
task_create_missing_queues = False
task_default_queue = CeleryQueue.DEFAULT.value
task_queues = (Queue(q.value) for q in CeleryQueue)
worker_max_memory_per_child = 10*1024  # 10 megabytes
task_acks_late = True
task_time_limit = 3600  # 1 hour
broker_transport_options = {
    'visibility_timeout': 86400  # 1 day
}
