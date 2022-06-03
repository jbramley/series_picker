from fetchers._goodreads import goodreads_fetcher
from fetchers._yaml import yaml_fetcher

FETCHERS = ["goodreads", "yaml"]


def get_fetcher(fetcher_type: str):
    fetcher_type = fetcher_type.lower()
    if fetcher_type == "goodreads":
        return goodreads_fetcher
    if fetcher_type == "yaml":
        return yaml_fetcher
    raise ValueError(f"Invalid fetcher type: {fetcher_type}")
