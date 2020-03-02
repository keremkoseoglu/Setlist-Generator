from gig.song import Song
from typing import List


class EventSetting:
    def __init__(self, excluded_songs: List[str] = None):
        if excluded_songs is None:
            self.excluded_songs = []
        else:
            self.excluded_songs = excluded_songs


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

    def get_excluded_songs(self, event_name: str) -> List[Song]:
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
