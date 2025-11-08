import pytest

from app.sentiment import ANALYZER, Sentiment


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Я люблю этот продукт, он просто супер!", Sentiment.positive),
        ("Это ужас и отстой", Sentiment.negative),
        ("Нормальный, средний опыт", Sentiment.neutral),
        ("Люблю и ненавижу одновременно, но люблю больше", Sentiment.positive),
        ("Ненавижу и люблю одновременно, но ненавижу сильнее", Sentiment.negative),
    ],
)
def test_analyzer(text: str, expected: Sentiment) -> None:
    """Проверка корректности определения тональности."""
    assert ANALYZER.analyze(text) == expected
