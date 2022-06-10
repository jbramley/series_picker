from abc import ABC, abstractmethod
from typing import Any, Iterable

from book_series.models import BookSeries


class AbstractJsonSerde(ABC):
    @staticmethod
    @abstractmethod
    def serialize(book_series: Iterable[BookSeries]) -> str:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(raw_series: list[dict[str, Any]]) -> list[BookSeries]:
        pass
