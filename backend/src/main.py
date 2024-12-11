from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import uvicorn

from common.config import RedisLogicalDB, settings
from domains.auth.router import router as router_auth

from common.task_queue import celery_app  # noqa


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(
        RedisBackend(
            aioredis.from_url(settings.get_redis_dsn(RedisLogicalDB.CACHE))
        )
    )

    yield

    pass


app = FastAPI(lifespan=lifespan)
app.include_router(router_auth)

if __name__ == '__main__':
    uvicorn.run('main:app')
