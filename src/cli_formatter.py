from __future__ import annotations

import urllib.parse
from typing import Iterable

from slugify import slugify

from book_series.models import Book, BookSeries


def _mk_libby_series_search_url(title: str) -> str:
    url_title = urllib.parse.quote(title)
    return f"https://ncdigital.overdrive.com/ncdigital-greensboro/content/search/series?query={url_title}"


def mk_libby_book_search_url(title: str) -> str:
    url_title = urllib.parse.quote(title)
    return f"https://ncdigital.overdrive.com/ncdigital-greensboro/content/search/title?query={url_title}"


def mk_kobo_direct_url(title: str) -> str:
    slug_title = slugify(title)
    return f"https://www.kobo.com/us/en/ebook/{slug_title}"


def mk_kobo_search_url(title: str) -> str:
    url_title = urllib.parse.quote(title)
    return f"https://www.kobo.com/us/en/search?query={url_title}&nd=true&ac=1&ac.title={url_title}&fcmedia=Book"


def list_formatter(series: Iterable[BookSeries]) -> list[tuple[str, BookSeries | Book]]:
    return [(f" * {s.title}", s) for s in series]


def detail_formatter(
    series_list: list[tuple[str, BookSeries | Book]]
) -> list[tuple[str, BookSeries | Book]]:
    detail_list: list[tuple[str, BookSeries | Book]] = []
    for title, series in series_list:
        detail_list.append((title, series))
        if isinstance(series, BookSeries):
            detail_list.extend(
                [(f"   * {b.title} [{b.status}]", b) for b in series.books]
            )
    return detail_list
