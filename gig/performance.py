from gig.band import Band
from gig.event import Event
from gig.song_pool import SongPool


class Performance:
    def __init__(self, event: Event, band: Band):
        self.event = event
        self.band = band
        self.song_pool = SongPool(self.band.songs,
                                  self.event,
                                  self.band.event_settings.get_excluded_songs(self.event.name))

