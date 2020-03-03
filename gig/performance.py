from gig.band import Band, EventSetting
from gig.event import Event
from gig.song_pool import SongPool


class Performance:
    def __init__(self, event: Event, band: Band):
        self.event = event
        self.band = band
        self.song_pool = SongPool(self.band, self.event)

    @property
    def event_setting(self) -> EventSetting:
        return self.band.event_settings.get(self.event.name)

