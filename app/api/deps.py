from app.repositories.review_repository import ReviewRepository
from app.sentiment import ANALYZER
from app.services.review_service import ReviewService


def get_review_service() -> ReviewService:
    """Dependency для получения сервиса отзывов."""
    return ReviewService(repository=ReviewRepository(), analyzer=ANALYZER)
