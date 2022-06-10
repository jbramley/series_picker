from __future__ import annotations

import json
from typing import Iterable, Optional

from book_series.models import BookSeries, BookSeriesCollection, BookStatus
from book_series.repository._abstract_repository import AbstractBookSeriesRepository
from book_series.repository._json_serde import (
    JSON_SERDE_LATEST_VERSION,
    AbstractJsonSerde,
    json_serde_factory,
)


class JsonBookSeriesRepository(AbstractBookSeriesRepository):
    def __init__(self, filename: str):
        self._filename = filename
        self._book_series_collection = self._load()
        self._book_series = {s.title: s for s in self._book_series_collection.series}
        self._serde: Optional[AbstractJsonSerde] = None

    def get_by_title(self, title: str) -> BookSeries:
        return self._book_series[title]

    def get_all_idle(self) -> Iterable[BookSeries]:
        return [s for s in self._book_series.values() if self._is_idle(s)]

    def get_all(self) -> Iterable[BookSeries]:
        return list(self._book_series.values())

    def add(self, series: BookSeries):
        if series.title in self._book_series:
            raise KeyError(f"{series.title} already exists in repository")
        self._book_series[series.title] = series
        self._save()

    def upgrade(self):
        self._serde = json_serde_factory(JSON_SERDE_LATEST_VERSION)
        self._save()

    def update_book_status(
        self, series: BookSeries, book_title: str, book_status: BookStatus
    ):
        for book in self._book_series[series.title].books:
            if book.title == book_title:
                book.status = book_status
                break
        self._save()

    def _load(self) -> BookSeriesCollection:
        with open(self._filename, "r", encoding="utf8") as fp:
            json_data = json.load(fp)
            if isinstance(json_data, list):
                self._serde = json_serde_factory()
            else:
                self._serde = json_serde_factory(json_data.get("v", "1"))
            return self._serde.deserialize(json_data)

    def _save(self):
        with open(self._filename, "w", encoding="utf8") as fp:
            fp.write(self._serde.serialize(self._book_series_collection))
