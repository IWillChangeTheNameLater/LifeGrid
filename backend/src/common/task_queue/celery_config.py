from enum import StrEnum, unique

from kombu import Queue

from common.config import RedisLogicalDB, settings


@unique
class CeleryQueue(StrEnum):
    LOW_PRIORITY = 'low_priority'
    MIDDLE_PRIORITY = 'middle_priority'
    HIGH_PRIORITY = 'high_priority'

    DEFAULT = 'default'


# The Celery app config
imports = ('common.task_queue.scheduler', 'common.task_queue.tasks')
broker_url = settings.get_redis_dsn(RedisLogicalDB.MESSAGE_BROKER)
result_backend = settings.get_redis_dsn(RedisLogicalDB.RESULT_BACKEND)

# Misc config
task_create_missing_queues = False
task_default_queue = CeleryQueue.DEFAULT
task_queues = (Queue(q) for q in CeleryQueue)
worker_max_memory_per_child = 10*1024  # 10 megabytes
task_acks_late = True
task_time_limit = 3600  # 1 hour
broker_transport_options = {
    'visibility_timeout': 86400  # 1 day
}
