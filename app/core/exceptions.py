from http import HTTPStatus


class AppError(Exception):
    """Базовое исключение приложения с привязкой к HTTP статусу."""

    def __init__(
        self,
        detail: str,
        *,
        status_code: int = HTTPStatus.BAD_REQUEST,
        code: str | None = None,
    ) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = int(status_code)
        self.code = code


class ReviewAlreadyExistsError(AppError):
    """Отзыв с таким текстом уже существует."""

    def __init__(self, *, text: str) -> None:
        super().__init__(
            detail="Отзыв с таким текстом уже существует",
            status_code=HTTPStatus.CONFLICT,
            code="review_already_exists",
        )
        self.text = text


class EmptyReviewTextError(AppError):
    """Текст отзыва пустой или содержит только пробелы."""

    def __init__(self) -> None:
        super().__init__(
            detail="Отзыв не может быть пустым",
            code="empty_review",
            status_code=HTTPStatus.BAD_REQUEST,
        )
