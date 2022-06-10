import json
from typing import Any, Iterable

from book_series.models import BookSeries
from book_series.repository._json_serde._abstract_serde import AbstractJsonSerde


class JsonV1Serde(AbstractJsonSerde):
    @staticmethod
    def serialize(book_series: Iterable[BookSeries]) -> str:
        return json.dumps([s.to_dict() for s in book_series])

    @staticmethod
    def deserialize(raw_series: list[dict[str, Any]]) -> list[BookSeries]:
        return [BookSeries.from_dict(s) for s in raw_series]
