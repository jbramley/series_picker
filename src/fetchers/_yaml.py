import yaml

from book_series import Book, BookSeries


def yaml_fetcher(filename: str) -> BookSeries:
    with open(filename, "r", encoding="utf8") as fp:
        data = yaml.load(fp, Loader=yaml.CLoader)
    return BookSeries(title=data["title"], books=[Book(title=b) for b in data["books"]])
