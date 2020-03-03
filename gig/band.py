from gig.song import Song
from typing import List


class SongReservation:
    def __init__(self,
                 song_name: str,
                 gig_opener: bool = False,
                 gig_closer: bool = False,
                 gig_closer_order: int = 0,
                 set_opener: bool = False,
                 set_closer: bool = False):
        self.song_name = song_name
        self.gig_opener = gig_opener
        self.gig_closer = gig_closer
        self.gig_closer_order = gig_closer_order
        self.set_opener = set_opener
        self.set_closer = set_closer


class EventSetting:
    def __init__(self, excluded_songs: List[str] = None, song_reservations: List[SongReservation] = None):
        if excluded_songs is None:
            self.excluded_songs = []
        else:
            self.excluded_songs = excluded_songs

        if song_reservations is None:
            self.song_reservations = []
        else:
            self.song_reservations = song_reservations

    def get_song_reservation(self, song_name: str) -> SongReservation:
        for sr in self.song_reservations:
            if sr.song_name == song_name:
                return sr
        return None

    def is_song_reserved(self, song_name: str):
        return self.get_song_reservation(song_name) is not None


class EventSettings:
    def __init__(self):
        self._event_settings = {}

    def append(self, event_name: str, event_setting: EventSetting):
        self._event_settings[event_name] = event_setting

    def get(self, event_name: str) -> EventSetting:
        if event_name in self._event_settings:
            return self._event_settings[event_name]
        else:
            return None

    def get_excluded_songs(self, event_name: str) -> List[str]:
        event_settings = self.get(event_name)
        if event_settings is None:
            return []
        else:
            return event_settings.excluded_songs


class Band:
    def __init__(self, name: str = None, songs: List[Song] = None, event_settings: EventSettings = None):
        if name is None:
            self.name = ""
        else:
            self.name = name

        if songs is None:
            self.songs = []
        else:
            self.songs = songs

        if event_settings is None:
            self.event_settings = EventSettings()
        else:
            self.event_settings = event_settings
