#!/bin/bash


cd src

# Workers
celery --app=main:celery_app worker --loglevel=info --queues=high_priority --concurrency=3
celery --app=main:celery_app worker --loglevel=info --queues=medium_priority,high_priority --concurrency=2
celery --app=main:celery_app worker --loglevel=info --queues=low_priority,medium_priority,high_priority --concurrency=1

# Scheduler
celery --app=main:celery_app beat --loglevel=info

# Client
celery --app=main:celery_app flower
