from fastapi import FastAPI
import uvicorn

from domains.auth.router import router as router_auth

from common.task_queue import celery_app  # noqa


app = FastAPI()
app.include_router(router_auth)

if __name__ == '__main__':
    uvicorn.run('main:app')
