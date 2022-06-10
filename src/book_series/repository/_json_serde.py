from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Optional

from book_series.models import BookSeries, BookSeriesCollection

JSON_SERDE_LATEST_VERSION = "1.0"


class AbstractJsonSerde(ABC):
    @staticmethod
    @abstractmethod
    def serialize(book_series_collection: BookSeriesCollection) -> str:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(json_data) -> BookSeriesCollection:
        pass


class JsonV0Serde(AbstractJsonSerde):
    @staticmethod
    def serialize(book_series_collection: BookSeriesCollection) -> str:
        return json.dumps([s.to_dict() for s in book_series_collection.series])

    @staticmethod
    def deserialize(raw_series: list[dict[str, Any]]) -> BookSeriesCollection:
        return BookSeriesCollection(
            series=[BookSeries.from_dict(s) for s in raw_series]
        )


class JsonV1Serde(AbstractJsonSerde):
    @staticmethod
    def serialize(book_series_collection: BookSeriesCollection) -> str:
        return json.dumps(
            {"v": "1.0", "b": [s.to_dict() for s in book_series_collection.series]}
        )

    @staticmethod
    def deserialize(json_data: dict[str, Any]) -> BookSeriesCollection:
        return BookSeriesCollection(
            series=[BookSeries.from_dict(s) for s in json_data.get("b", [])]
        )


def json_serde_factory(version: Optional[str] = None) -> AbstractJsonSerde:
    if version is None:
        return JsonV0Serde()
    if version == "1.0":
        return JsonV1Serde()
    raise ValueError("Invalid json file version")
