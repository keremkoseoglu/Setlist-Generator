from gig.set import Set
from typing import List


class Event:
    def __init__(self, sets: List[Set] = None, genre_filter: List[str] = None):
        if sets is None:
            self.sets = []
        else:
            self.sets = sets

        if genre_filter is None:
            self.genre_filter = []
        else:
            self.genre_filter = genre_filter
