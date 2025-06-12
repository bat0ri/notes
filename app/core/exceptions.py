from typing import Any, Dict, Optional
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

class AppException(HTTPException):
    """Базовый класс для всех исключений приложения"""
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(AppException):
    """Исключение для случаев, когда ресурс не найден"""
    def __init__(self, detail: str = "Ресурс не найден") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ValidationException(AppException):
    """Исключение для ошибок валидации"""
    def __init__(self, detail: str = "Ошибка валидации данных") -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class DatabaseException(AppException):
    """Исключение для ошибок базы данных"""
    def __init__(self, detail: str = "Ошибка базы данных") -> None:
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class StorageException(AppException):
    """Исключение для ошибок хранилища"""
    def __init__(self, detail: str = "Ошибка хранилища") -> None:
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Обработчик для HTTP исключений"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": str(exc.detail),
                "type": exc.__class__.__name__
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Обработчик для ошибок валидации"""
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Ошибка валидации данных",
                "type": "ValidationError",
                "details": errors
            }
        }
    )

async def pydantic_validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Обработчик для ошибок валидации Pydantic"""
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Ошибка валидации данных",
                "type": "ValidationError",
                "details": errors
            }
        }
    ) 