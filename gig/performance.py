""" Performance module """
from typing import List
from gig.band import Band, EventSetting
from gig.event import Event
from gig.song_pool import SongPool, Song

class Performance:
    """ Performance class """
    def __init__(self, event: Event = None, band: Band = None):
        self.event = event
        self.band = band

        if self.event is not None and self.band is not None:
            self.song_pool = SongPool(self.band, self.event)

    @property
    def event_setting(self) -> EventSetting:
        """ Returns settings of the event """
        return self.band.event_settings.get(self.event.name)

    def reorder_songs(self, new_sets: List):
        """ Re-orders songs according to given data
        [
            {"set": 1, "songs": ["Cafe/Muito", "Rim Shot"]},
            {"set": 2, "songs": ["Amour Tes La", "Smooth Operator"]}
        ]
        """
        self.song_pool.dead_songs = []
        killable_songs = []

        for new_set in new_sets:
            set_no = new_set["set"]
            if set_no == 0:
                killable_songs = new_set["songs"]
            else:
                set_index = set_no - 1
                if set_index < len(self.event.sets):
                    self.event.sets[set_index].enforce_song_list(new_set["songs"], self.band.songs)

        self.kill_songs(killable_songs, seek_in_sets = False)

    def kill_songs(self, names: List[str], seek_in_sets: bool = True):
        """ Kills the given songs """
        if seek_in_sets:
            for name in names:
                self.kill_song(name)
        else:
            for song in self.song_pool.band.songs:
                if song.name in names:
                    self._collect_dead_song(song)

    def kill_song(self, name: str):
        """ Kills the given song """
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

        self._collect_dead_song(song_to_backup)

    def resurrect_song(self, name: str, set_index: int, song_index: int):
        """ Resurrects the given song """
        lazarus = self.song_pool.pop_leftover_song(name)
        if lazarus is None:
            return
        self.event.sets[set_index].insert_song(lazarus, song_index)

    def move_song_up(self, name: str):
        """ Move song one step up"""
        self._move_song(name, -1)

    def move_song_down(self, name: str):
        """ Move song one step down """
        self._move_song(name, 1)

    def _move_song(self, name: str, places: int):
        """ Move song by X places """
        # Determine existing indexes
        set_index = -1
        song_to_move = None
        for event_set in self.event.sets:
            set_index += 1
            flow_step_index = -1
            for flow_step in event_set.flow:
                flow_step_index += 1
                song_index = -1
                for song in flow_step.songs:
                    song_index += 1
                    if song.name == name:
                        song_to_move = song
                        break
                if song_to_move is not None:
                    break
            if song_to_move is not None:
                break

        if song_to_move is None:
            return

        # Determine new indexes
        new_flow_step_index = flow_step_index
        new_song_index = song_index + places
        if new_song_index < 0:
            new_flow_step_index -= 1

            if new_flow_step_index < 0:
                return

            new_song_index = len(self.event.sets[set_index].flow[new_flow_step_index].songs) - 1

        elif new_song_index >= len(self.event.sets[set_index].flow[flow_step_index].songs):
            new_song_index = 1
            new_flow_step_index += 1

            if new_flow_step_index >= len(self.event.sets[set_index].flow):
                return

        # Move song
        event_set = self.event.sets[set_index]
        flow_set = event_set.flow[flow_step_index]
        song = flow_set.songs.pop(song_index)

        flow_set = event_set.flow[new_flow_step_index]
        flow_set.songs.insert(new_song_index, song)

    def _collect_dead_song(self, song: Song):
        if song is None:
            return

        for already_dead in self.song_pool.dead_songs:
            if already_dead.name == song.name:
                return

        self.song_pool.dead_songs.append(song)
