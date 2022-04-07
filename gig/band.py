""" Band module """
from dataclasses import dataclass
from typing import List
from gig.song import Song

@dataclass
class SongReservation:
    """ Song reservation class """
    song_name: str
    gig_opener: bool = False
    gig_closer: bool = False
    gig_closer_order: int = 0
    set_opener: bool = False
    set_closer: bool = False


@dataclass
class ManualSet:
    """ Manual set class """
    number: int
    songs: List[str]


@dataclass
class EventSetting:
    """ Event settings class """
    excluded_songs: List[str] = None
    gig_openers: List[str] = None
    gig_closers: List[str] = None
    set_openers: List[str] = None
    set_closers: List[str] = None
    lineup: str = ""
    sets: List = None

    def __post_init__(self):
        if self.excluded_songs is None:
            self.excluded_songs = []

        self.song_reservations = []

        if self.gig_openers is not None:
            for gig_opener in self.gig_openers:
                song_reservation = self.get_song_reservation(gig_opener)
                if song_reservation is None:
                    self.song_reservations.append(SongReservation(gig_opener, gig_opener=True))
                else:
                    song_reservation.gig_opener = True

        if self.gig_closers is not None:
            gig_closer_index = -1
            for gig_closer in self.gig_closers:
                gig_closer_index += 1
                song_reservation = self.get_song_reservation(gig_closer)
                if song_reservation is None:
                    self.song_reservations.append(
                        SongReservation(
                            gig_closer,
                            gig_closer=True,
                            gig_closer_order=gig_closer_index))
                else:
                    song_reservation.gig_closer = True
                    song_reservation.gig_closer_order = gig_closer_index

        if self.set_openers is not None:
            for set_opener in self.set_openers:
                song_reservation = self.get_song_reservation(set_opener)
                if song_reservation is None:
                    self.song_reservations.append(SongReservation(set_opener, set_opener=True))
                else:
                    song_reservation.set_opener = True

        if self.set_closers is not None:
            for set_closer in self.set_closers:
                song_reservation = self.get_song_reservation(set_closer)
                if song_reservation is None:
                    self.song_reservations.append(SongReservation(set_closer, set_closer=True))
                else:
                    song_reservation.set_closer = True

        self.manual_sets = []

        if self.sets is not None:
            for set in self.sets:
                self.manual_sets.append(ManualSet(set["number"], set["songs"]))

    @property
    def has_lineup_constraint(self) -> bool:
        """ Returns true if event is played with a specific lineup """
        return self.lineup != ""

    def get_song_reservation(self, song_name: str) -> SongReservation:
        """ Returns the reserved song """
        for song_reservation in self.song_reservations:
            if song_reservation.song_name == song_name:
                return song_reservation
        return None

    def is_song_reserved(self, song_name: str):
        """ Tells if the song is reserved or not """
        return self.get_song_reservation(song_name) is not None


class EventSettings:
    """ Event settings class """
    def __init__(self):
        self._event_settings = {}

    def append(self, event_name: str, event_setting: EventSetting):
        """ Add a new event setting """
        self._event_settings[event_name] = event_setting

    def get(self, event_name: str) -> EventSetting:
        """ Returns settings for the given event """
        if event_name in self._event_settings:
            return self._event_settings[event_name]
        return None

    def get_excluded_songs(self, event_name: str) -> List[str]:
        """ Returns excluded songs of the given event """
        event_settings = self.get(event_name)
        if event_settings is None:
            return []
        return event_settings.excluded_songs


@dataclass
class Band:
    """ Band class """
    name: str = "",
    songs: List[Song] = None,
    event_settings: EventSettings = None,
    flukebox_playlists: List[str] = None,
    lineups: List[str] = None

    def __post_init__(self):
        if self.songs is None:
            self.songs = []

        if self.event_settings is None:
            self.event_settings = EventSettings()

        if self.flukebox_playlists is None:
            self.flukebox_playlists = []

        if self.lineups is None:
            self.lineups = []
