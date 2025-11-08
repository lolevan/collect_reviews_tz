from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.reviews import router as reviews_router
from app.core.config import settings
from app.core.error_handlers import register_error_handlers


async def run_migrations() -> None:
    """Apply database migrations on startup if enabled."""
    import asyncio
    from alembic import command
    from alembic.config import Config

    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", settings.database_url)
    await asyncio.to_thread(command.upgrade, cfg, "head")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Run startup/shutdown logic."""
    if settings.run_migrations_on_startup:
        await run_migrations()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    register_error_handlers(app)
    app.include_router(reviews_router, prefix="/api/v1")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
