from dataclasses import dataclass

from book_series.models._book_series import BookSeries


@dataclass
class BookSeriesCollection:
    series: list[BookSeries]
