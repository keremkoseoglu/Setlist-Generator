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
    def __init__(self,
                 excluded_songs: List[str] = None,
                 gig_openers: List[str] = None,
                 gig_closers: List[str] = None,
                 set_openers: List[str] = None,
                 set_closers: List[str] = None):
        if excluded_songs is None:
            self.excluded_songs = []
        else:
            self.excluded_songs = excluded_songs

        self.song_reservations = []

        if gig_openers is not None:
            for gig_opener in gig_openers:
                sr = self.get_song_reservation(gig_opener)
                if sr is None:
                    self.song_reservations.append(SongReservation(gig_opener, gig_opener=True))
                else:
                    sr.gig_opener = True

        if gig_closers is not None:
            gig_closer_index = -1
            for gig_closer in gig_closers:
                gig_closer_index += 1
                sr = self.get_song_reservation(gig_closer)
                if sr is None:
                    self.song_reservations.append(SongReservation(gig_closer,
                                                                  gig_closer=True,
                                                                  gig_closer_order=gig_closer_index))
                else:
                    sr.gig_closer = True
                    sr.gig_closer_order = gig_closer_index

        if set_openers is not None:
            for set_opener in set_openers:
                sr = self.get_song_reservation(set_opener)
                if sr is None:
                    self.song_reservations.append(SongReservation(set_opener, set_opener=True))
                else:
                    sr.set_opener = True

        if set_closers is not None:
            for set_closer in set_closers:
                sr = self.get_song_reservation(set_closer)
                if sr is None:
                    self.song_reservations.append(SongReservation(set_closer, set_closer=True))
                else:
                    sr.set_closer = True

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
