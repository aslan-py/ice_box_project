from fastapi import FastAPI

from app.api.routers import main_router
from app.api.tags_metadata import tags_metadata
from app.core.config import settings
from app.core.loguru_config import logger  # noqa: F401

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    version='1.0.0',
    openapi_tags=tags_metadata,
)

app.include_router(main_router)
