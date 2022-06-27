"""Main."""

from fastapi import FastAPI
from mangum import Mangum

from .config import settings
from .routers import router

root_path = "/" if not settings.stage else f"/{settings.stage}"


app = FastAPI(title="PDF Generator", root_path=root_path)


app.include_router(router)


handler = Mangum(app)
