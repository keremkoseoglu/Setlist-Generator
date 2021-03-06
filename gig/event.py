""" Event module """
from typing import List
from gig.set import Set


class Event:
    """ Event class """
    def __init__(self,
                 name: str = None,
                 sets: List[Set] = None,
                 genre_filter: List[str] = None,
                 language_filter: List[str] = None):
        if name is None:
            self.name = ""
        else:
            self.name = name

        if sets is None:
            self.sets = []
        else:
            self.sets = sets

        if genre_filter is None:
            self.genre_filter = []
        else:
            self.genre_filter = genre_filter

        if language_filter is None:
            self.language_filter = []
        else:
            self.language_filter = language_filter
