from collections.abc import Sequence
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review
from app.sentiment import Sentiment


class ReviewRepository:
    """Репозиторий для работы с отзывами на уровне БД."""

    async def add(self, session: AsyncSession, review: Review) -> Review:
        """Добавить отзыв в сессию и получить его с ID."""
        session.add(review)
        await session.flush()
        await session.refresh(review)
        return review

    async def commit(self, session: AsyncSession) -> None:
        """Зафиксировать изменения в БД."""
        await session.commit()

    async def get_by_text(self, session: AsyncSession, text: str) -> Optional[Review]:
        """Найти отзыв по тексту."""
        stmt = select(Review).where(Review.text == text)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self, session: AsyncSession, sentiment: Optional[Sentiment] = None
    ) -> Sequence[Review]:
        """Получить список отзывов с опциональной фильтрацией по тональности."""
        stmt = select(Review).order_by(Review.id.desc())
        if sentiment is not None:
            stmt = stmt.where(Review.sentiment == sentiment)
        result = await session.execute(stmt)
        return result.scalars().all()
