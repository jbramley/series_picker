from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Any, Dict, List

from book_series.models._book import Book


@dataclass
class BookSeries:
    title: str
    books: List[Book]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> BookSeries:
        title = d.get("title")
        if not title:
            raise KeyError("Required field `title' not found in dict")
        books = d.get("books")
        if not books:
            raise KeyError("Required field `books' not found in dict")

        return cls(title=title, books=[Book.from_dict(b) for b in books])

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
