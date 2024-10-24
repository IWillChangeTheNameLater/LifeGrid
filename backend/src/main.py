from fastapi import FastAPI

from auth.router import router as router_auth


app = FastAPI()
app.include_router(router_auth)
