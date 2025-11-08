import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import EmptyReviewTextError, ReviewAlreadyExistsError
from app.models.review import Review
from app.schemas.review import ReviewCreate
from app.sentiment import ANALYZER, Sentiment
from app.services.review_service import ReviewService


def test_create_review_success():
    """Успешное создание отзыва."""
    repository = AsyncMock()
    repository.get_by_text = AsyncMock(return_value=None)
    created_review = Review(
        id=1,
        text="Отличный сервис",
        sentiment=Sentiment.positive,
        created_at=datetime.now(timezone.utc),
    )
    repository.add = AsyncMock(return_value=created_review)
    repository.commit = AsyncMock(return_value=None)

    service = ReviewService(repository=repository, analyzer=ANALYZER)
    session = AsyncMock(spec=AsyncSession)

    payload = ReviewCreate(text="  Отличный сервис  ")
    result = asyncio.run(service.create_review(session, payload))

    assert result.text == "Отличный сервис"
    assert result.sentiment == Sentiment.positive
    repository.get_by_text.assert_awaited_once()
    repository.add.assert_awaited_once()
    repository.commit.assert_awaited_once_with(session)


def test_create_review_rejects_empty_text():
    """Отклонение пустого текста отзыва."""
    repository = AsyncMock()
    repository.get_by_text = AsyncMock(return_value=None)
    repository.add = AsyncMock()
    repository.commit = AsyncMock()

    service = ReviewService(repository=repository, analyzer=ANALYZER)
    session = AsyncMock(spec=AsyncSession)

    with pytest.raises(EmptyReviewTextError):
        asyncio.run(service.create_review(session, ReviewCreate(text="   ")))

    repository.get_by_text.assert_not_called()
    repository.add.assert_not_called()
