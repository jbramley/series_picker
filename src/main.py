import json

from book_series import BookSeriesCollection


def main():
    with open("../series_status.json", "r", encoding="utf-8") as fp:
        series = json.load(fp)
    series_collection = BookSeriesCollection.from_list(series)
    print([s.title for s in series_collection.series])
    print([s.title for s in series_collection.idle_series()])


if __name__ == "__main__":
    main()
