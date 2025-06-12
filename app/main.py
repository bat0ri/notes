from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.core.config import get_settings
from app.api.v1.router import api_router
from app.db.base import Base
from app.db.session import engine
from app.storage.minio import storage
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    pydantic_validation_exception_handler,
    AppException
)

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
app.add_exception_handler(AppException, http_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """
    Корневой эндпоинт для проверки работоспособности API.
    """
    return {
        "message": "Welcome to Notes API",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "openapi_url": f"{settings.API_V1_STR}/openapi.json"
    }


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения"""
    await storage.initialize()