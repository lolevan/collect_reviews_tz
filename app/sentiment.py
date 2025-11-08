from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Sentiment(str, Enum):
    """Тональность отзыва."""

    positive = "positive"
    negative = "negative"
    neutral = "neutral"


@dataclass(frozen=True)
class LexiconAnalyzer:
    """Лексический анализатор тональности на основе словаря."""

    positives: Tuple[str, ...] = (
        "хорош",
        "люблю",
        "отличн",
        "нрав",
        "супер",
        "класс",
    )
    negatives: Tuple[str, ...] = (
        "плохо",
        "ненавиж",
        "ужас",
        "отстой",
        "ненрав",
        "плох",
    )

    def analyze(self, text: str) -> Sentiment:
        """Определить тональность текста."""
        lowered = text.lower()
        has_positive = any(term in lowered for term in self.positives)
        has_negative = any(term in lowered for term in self.negatives)

        if has_positive and not has_negative:
            return Sentiment.positive
        if has_negative and not has_positive:
            return Sentiment.negative
        if has_positive and has_negative:
            positive_score = sum(lowered.count(term) for term in self.positives)
            negative_score = sum(lowered.count(term) for term in self.negatives)
            return (
                Sentiment.positive
                if positive_score >= negative_score
                else Sentiment.negative
            )
        return Sentiment.neutral


ANALYZER = LexiconAnalyzer()
