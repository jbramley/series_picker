from __future__ import annotations

import json
from typing import Any, Iterable

from book_series.models import BookSeries, BookStatus
from book_series.repository._abstract_repository import AbstractBookSeriesRepository
from book_series.repository._json_serde import json_serde_factory


def _deserialize(raw_series: list[dict[str, Any]]) -> dict[str, BookSeries]:
    return {s["title"]: BookSeries.from_dict(s) for s in raw_series}


def _serialize(book_series: Iterable[BookSeries]) -> list[dict[str, Any]]:
    return [s.to_dict() for s in book_series]


class JsonBookSeriesRepository(AbstractBookSeriesRepository):
    def __init__(self, filename: str):
        self._filename = filename
        self.book_series = self._load()

    def get_by_title(self, title: str) -> BookSeries:
        return self.book_series[title]

    def get_all_idle(self) -> Iterable[BookSeries]:
        return [s for s in self.book_series.values() if self._is_idle(s)]

    def get_all(self) -> Iterable[BookSeries]:
        return list(self.book_series.values())

    def add(self, series: BookSeries):
        if series.title in self.book_series:
            raise KeyError(f"{series.title} already exists in repository")
        self.book_series[series.title] = series
        self._save()

    def update_book_status(
        self, series: BookSeries, book_title: str, book_status: BookStatus
    ):
        for book in self.book_series[series.title].books:
            if book.title == book_title:
                book.status = book_status
                break
        self._save()

    def _load(self) -> dict[str, BookSeries]:
        with open(self._filename, "r", encoding="utf8") as fp:
            json_data = json.load(fp)
            if isinstance(json_data, list):
                self._serde = json_serde_factory()
                series_json = json_data
            else:
                self._serde = json_serde_factory(json_data.get("v", "1"))
                series_json = json_data.get("b", [])
            series = self._serde.deserialize(series_json)
            return {s.title: s for s in series}

    def _save(self):
        with open(self._filename, "w", encoding="utf8") as fp:
            json.dump(self._serde.serialize(self.book_series.values()), fp)
