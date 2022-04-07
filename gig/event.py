""" Event module """
from dataclasses import dataclass
from typing import List
from gig.set import Set


@dataclass
class Event:
    """ Event class """
    name: str = "",
    sets: List[Set] = None,
    genre_filter: List[str] = None,
    language_filter: List[str] = None

    def __post_init__(self):
        if self.sets is None:
            self.sets = []

        if self.genre_filter is None:
            self.genre_filter = []

        if self.language_filter is None:
            self.language_filter = []
