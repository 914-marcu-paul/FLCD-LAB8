from enum import Enum


class ParsingState(Enum):
    NORMAL = "q"
    BACK = "b"
    FINAL = "f"
    ERROR = "e"

    def __str__(self):
        return self.value
