from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.sentiment import Sentiment


class Review(Base):
    """Модель отзыва пользователя."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
        unique=True,
        doc="Текст отзыва",
    )
    sentiment: Mapped[Sentiment] = mapped_column(
        Enum(Sentiment, name="sentiment_enum", native_enum=False),
        nullable=False,
        index=True,
        doc="Распознанная тональность",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Дата создания",
    )

    def __repr__(self) -> str:
        return (
            f"Review(id={self.id!r}, text={self.text!r}, sentiment={self.sentiment!r}, "
            f"created_at={self.created_at!r})"
        )
