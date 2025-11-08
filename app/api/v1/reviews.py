from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_review_service
from app.core.db import get_db_session
from app.schemas.review import ReviewCreate, ReviewRead
from app.sentiment import Sentiment
from app.services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(
    payload: ReviewCreate,
    service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_db_session),
) -> ReviewRead:
    """Создать новый отзыв с автоматическим определением тональности."""
    return await service.create_review(session, payload)


@router.get("", response_model=list[ReviewRead])
async def list_reviews(
    sentiment: Annotated[
        Sentiment | None,
        Query(
            description="Фильтрация по тональности",
            examples={
                "positive": {"summary": "Только позитивные", "value": "positive"},
                "negative": {"summary": "Только негативные", "value": "negative"},
            },
        ),
    ] = None,
    service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_db_session),
) -> list[ReviewRead]:
    """Получить список отзывов с опциональной фильтрацией по тональности."""
    return await service.list_reviews(session, sentiment=sentiment)
