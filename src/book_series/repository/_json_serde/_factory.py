from typing import Optional

from book_series.repository._json_serde._abstract_serde import AbstractJsonSerde
from book_series.repository._json_serde.json_v1_serde import JsonV1Serde


def json_serde_factory(version: Optional[str] = None) -> AbstractJsonSerde:
    if version is None:
        return JsonV1Serde()
    raise ValueError("Invalid json file version")
