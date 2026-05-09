from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.core.config import settings

from app.api.routes.auth import router as auth_router

from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.include_router(auth_router)

@app.get("/")
async def root():
    return {
        "message": "AI Video Generator Backend Running",
        "environment": settings.APP_ENV
    }