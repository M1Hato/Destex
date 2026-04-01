from fastapi import FastAPI

from app.api.routers.auth import auth_router
from app.api.routers.tasks import task_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)