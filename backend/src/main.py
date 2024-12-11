from fastapi import FastAPI
import uvicorn

from common.task_queue import celery_app
from domains.auth.router import router as router_auth

# To ensure that the import will not be removed due to uselessness
celery_app = celery_app

app = FastAPI()
app.include_router(router_auth)

if __name__ == '__main__':
    uvicorn.run('main:app')
