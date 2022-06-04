from abc import ABC, abstractmethod
from typing import Iterable

from book_series.models import BookSeries, BookStatus


class AbstractBookSeriesRepository(ABC):
    @staticmethod
    def _is_idle(series: BookSeries) -> bool:
        return all(
            b.status in [BookStatus.UNREAD, BookStatus.READ] for b in series.books
        )

    @abstractmethod
    def get_all(self) -> Iterable[BookSeries]:
        pass

    @abstractmethod
    def get_by_title(self, title: str) -> BookSeries:
        pass

    @abstractmethod
    def get_all_idle(self) -> Iterable[BookSeries]:
        pass

    @abstractmethod
    def add(self, series: BookSeries):
        pass

    @abstractmethod
    def update_book_status(
        self, series: BookSeries, book_title: str, book_status: BookStatus
    ):
        pass
