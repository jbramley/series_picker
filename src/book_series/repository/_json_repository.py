from __future__ import annotations

import json
from typing import Iterable

from book_series import BookSeries
from book_series.repository._abstract_repository import AbstractBookSeriesRepository


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

    def _load(self) -> dict[str, BookSeries]:
        with open(self._filename, "r", encoding="utf8") as fp:
            raw_series = json.load(fp)
        return {s["title"]: BookSeries.from_dict(s) for s in raw_series}

    def _save(self):
        raw_series = [s.to_dict() for s in self.book_series.values()]
        with open(self._filename, "w", encoding="utf8") as fp:
            json.dump(raw_series, fp)
