from enum import Enum


class BookStatus(str, Enum):
    READ = "Read"
    READING = "Reading"
    ON_HOLD = "On Hold"
    UNREAD = "Unread"
