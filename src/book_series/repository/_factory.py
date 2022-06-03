from book_series.repository._abstract_repository import AbstractBookSeriesRepository
from book_series.repository._json_repository import JsonBookSeriesRepository


def get_repository(datastore: str) -> AbstractBookSeriesRepository:
    repo_type, *repo_parameters = datastore.split(":")
    repo_type = repo_type.lower()

    if repo_type == "json":
        return JsonBookSeriesRepository(*repo_parameters)

    raise ValueError(f"Invalid BookSeriesRepository type: {repo_type}")
