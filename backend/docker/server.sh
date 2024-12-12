#!/bin/bash

alembic revision --autogenerate
alembic upgrade head

cd src
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker
