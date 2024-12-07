from pathlib import Path

from celery import Celery


celery_app = Celery(main=Path(__file__).parent.name)
celery_app.config_from_object('task_queue.celery_config')

if __name__ == '__main__':
    celery_app.start()
