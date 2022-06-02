import argparse
from typing import Any

from book_series.repository import JsonBookSeriesRepository
from fetchers import goodreads_fetcher

DEFAULT_CONFIG_FILE = "series_picker.cfg"


def main(data_file: str):
    book_series_repository = JsonBookSeriesRepository(data_file)
    print([s.title for s in book_series_repository.get_all()])
    print([s.title for s in book_series_repository.get_all_idle()])

    new_series = goodreads_fetcher("https://www.goodreads.com/series/56399-the-expanse")
    print(new_series)
    # book_series_repository.add(new_series)
    print([s.title for s in book_series_repository.get_all()])


def parse_args() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datafile", dest="data_file")

    args = parser.parse_args()
    return {"data_file": args.data_file}


if __name__ == "__main__":
    args = parse_args()
    main(**parse_args())
