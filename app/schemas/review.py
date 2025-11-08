from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.sentiment import Sentiment


class ReviewCreate(BaseModel):
    """Схема для создания отзыва."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=1024,
        description="Текст пользовательского отзыва",
        examples=["Очень понравился сервис — всё быстро и удобно!"],
    )


class ReviewRead(BaseModel):
    """Схема для чтения отзыва."""

    id: int = Field(description="Идентификатор отзыва", examples=[1])
    text: str = Field(description="Текст пользовательского отзыва")
    sentiment: Sentiment = Field(
        description="Распознанная тональность",
        examples=[Sentiment.positive],
    )
    created_at: datetime = Field(
        description="Дата и время создания отзыва",
        examples=["2024-01-01T12:00:00+00:00"],
    )

    model_config = ConfigDict(from_attributes=True)
