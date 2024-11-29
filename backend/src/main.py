from fastapi import FastAPI
import uvicorn

from auth.router import router as router_auth


app = FastAPI()
app.include_router(router_auth)

if __name__ == '__main__':
    uvicorn.run('main:app')
