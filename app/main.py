from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from app.core.config import settings

from app.api.routes.auth import router as auth_router
from app.api.routes.video_generation import router as video_generation_router
from app.api.routes.history import router as history_router
from app.api.routes.export import router as export_router

from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.include_router(
    auth_router,
    prefix="/api"
)

app.include_router(
    video_generation_router,
    prefix="/api"
)

app.include_router(
    history_router,
    prefix="/api"
)

app.include_router(
    export_router,
    prefix="/api"
)

@app.get("/")
async def root():
    return {
        "message": "AI Video Generator Backend Running",
        "environment": settings.APP_ENV
    }