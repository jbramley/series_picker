from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from book_series._book_status import BookStatus


@dataclass
class Book:
    title: str
    status: BookStatus = BookStatus.UNREAD

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Book:
        title = d.get("title")
        if not title:
            raise KeyError("Required field `title' not found in dict")
        status = d.get("status", BookStatus.UNREAD)
        return cls(title=title, status=status)
