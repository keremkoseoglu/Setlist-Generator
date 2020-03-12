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

    def kill_song(self, name: str):
        song_to_backup = None
        for event_set in self.event.sets:
            for flow_step in event_set.flow:
                song_index = -1
                for song in flow_step.songs:
                    song_index += 1
                    if song.name == name:
                        song_to_backup = song
                        break
                if song_to_backup is not None:
                    flow_step.songs.pop(song_index)
                    break
            if song_to_backup is not None:
                break

        if song_to_backup is None:
            return

        self.song_pool.dead_songs.append(song_to_backup)

    def resurrect_song(self, name: str, set_index: int, song_index: int):
        lazarus = self.song_pool.pop_leftover_song(name)
        if lazarus is None:
            return
        self.event.sets[set_index].insert_song(lazarus, song_index)

