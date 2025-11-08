from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from .exceptions import AppError


def register_error_handlers(app: FastAPI) -> None:
    """Register global exception handlers for the application."""

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        payload = {"detail": exc.detail}
        if exc.code:
            payload["code"] = exc.code
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(IntegrityError)
    async def sqlalchemy_integrity_error_handler(
        _: Request, exc: IntegrityError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={
                "detail": "Нарушение ограничения целостности базы данных",
                "code": "integrity_error",
                "message": str(exc.orig) if exc.orig else str(exc),
            },
        )
