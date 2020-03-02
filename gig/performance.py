from gig.event import Event
from gig.song import Song
from gig.song_pool import SongPool
from typing import List


class Performance:
    def __init__(self, input_event: Event, input_song_pool: List[Song]):
        self.event = input_event
        self.song_pool = SongPool(self.event, input_song_pool)
