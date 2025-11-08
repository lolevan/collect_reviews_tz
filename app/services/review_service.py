from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import EmptyReviewTextError, ReviewAlreadyExistsError
from app.models.review import Review
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreate, ReviewRead
from app.sentiment import LexiconAnalyzer, Sentiment


class ReviewService:
    """Сервис для бизнес-логики работы с отзывами."""

    def __init__(
        self, *, repository: ReviewRepository, analyzer: LexiconAnalyzer
    ) -> None:
        self._repository = repository
        self._analyzer = analyzer

    async def create_review(
        self, session: AsyncSession, payload: ReviewCreate
    ) -> ReviewRead:
        """Создать новый отзыв с определением тональности."""
        normalized_text = payload.text.strip()
        if not normalized_text:
            raise EmptyReviewTextError()

        existing = await self._repository.get_by_text(session, normalized_text)
        if existing is not None:
            raise ReviewAlreadyExistsError(text=normalized_text)

        sentiment = self._analyzer.analyze(normalized_text)
        review = Review(
            text=normalized_text,
            sentiment=sentiment,
            created_at=datetime.now(timezone.utc),
        )

        created = await self._repository.add(session, review)
        await self._repository.commit(session)
        return ReviewRead.model_validate(created)

    async def list_reviews(
        self, session: AsyncSession, *, sentiment: Sentiment | None = None
    ) -> list[ReviewRead]:
        """Получить список отзывов с опциональной фильтрацией."""
        items = await self._repository.list(session, sentiment)
        return [ReviewRead.model_validate(item) for item in items]
