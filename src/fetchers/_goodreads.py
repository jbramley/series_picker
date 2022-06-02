import re

import bs4
import requests

from book_series.models import Book, BookSeries


def goodreads_fetcher(url: str) -> BookSeries:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    series_title = (
        soup.find("div", class_="responsiveSeriesHeader__title")
        .find_next("h1")
        .contents[0]
        .text.rsplit(" ", 1)[0]
    )
    series_books = []
    for list_item in soup.find_all("div", class_="listWithDividers__item"):
        item_h3 = list_item.find_next("h3")
        series_descriptor = item_h3.contents[0].text
        if not re.match("^Book [0-9]+$", series_descriptor):
            continue
        book_name_span = list_item.find_next("span", itemprop="name")
        series_books.append(Book(title=book_name_span.contents[0].text))
    return BookSeries(title=series_title, books=series_books)
