from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List

from book_series._book_series import BookSeries
from book_series._book_status import BookStatus


def _is_idle(series: BookSeries) -> bool:
    return all(b.status in [BookStatus.UNREAD, BookStatus.READ] for b in series.books)


@dataclass
class BookSeriesCollection:
    series: List[BookSeries]

    def idle_series(self) -> List[BookSeries]:
        return [s for s in self.series if _is_idle(s)]

    @classmethod
    def from_list(cls, lst: list[dict[str, Any]]) -> BookSeriesCollection:
        return cls(series=[BookSeries.from_dict(s) for s in lst])
