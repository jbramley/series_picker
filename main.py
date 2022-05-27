import json

from book_series import BookSeries


def main():
    with open("series_status.json", "r", encoding="utf-8") as fp:
        series = json.load(fp)
    book_series = [BookSeries.from_dict(s) for s in series]
    print(book_series)


if __name__ == "__main__":
    main()
