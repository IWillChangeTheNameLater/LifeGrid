from fastapi import FastAPI
import uvicorn

from auth.router import router as router_auth
from task_queue import celery_app

# To ensure that the import will not be removed due to uselessness
celery_app = celery_app

app = FastAPI()
app.include_router(router_auth)

if __name__ == '__main__':
    uvicorn.run('main:app')
