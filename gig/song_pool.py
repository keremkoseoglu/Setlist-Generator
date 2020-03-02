from gig.event import Event
from gig.song import Song
from statistics import median
from typing import List


class ObsoleteSongs:
    def __init__(self):
        self.inactive = []
        self.filtered_by_genre = []

    @property
    def all(self) -> List[Song]:
        output = []
        for song in self.inactive:
            output.append(song)
        for song in self.filtered_by_genre:
            output.append(song)
        return output


class SongPool:
    _INFINITY = 9999999

    def __init__(self, input_event: Event, input_songs: List[Song]):
        self.unreserved_songs = []
        self.reserved_songs = []
        self.low_energy = []
        self.medium_energy = []
        self.high_energy = []
        self.event = input_event
        self.obsolete_songs = ObsoleteSongs()
        self._accept_songs_checking_reservation(input_songs)
        self.categorize_songs_by_energy()

    def categorize_songs_by_energy(self):
        self.low_energy = []
        self.medium_energy = []
        self.high_energy = []

        overall_median = SongPool._get_energy_median_of_songs(self.unreserved_songs)

        lower_songs = SongPool._filter_songs_by_energy(self.unreserved_songs, -self._INFINITY, overall_median)
        lower_median = SongPool._get_energy_median_of_songs(lower_songs)
        low_songs = SongPool._filter_songs_by_energy(lower_songs, -self._INFINITY, lower_median)
        low_medium_songs = SongPool._filter_songs_by_energy(lower_songs, lower_median, self._INFINITY)

        higher_songs = SongPool._filter_songs_by_energy(self.unreserved_songs, overall_median, self._INFINITY)
        higher_median = SongPool._get_energy_median_of_songs(higher_songs)
        high_medium_songs = SongPool._filter_songs_by_energy(higher_songs, overall_median, higher_median)
        high_songs = SongPool._filter_songs_by_energy(higher_songs, higher_median, self._INFINITY)

        self.low_energy = low_songs
        self.high_energy = high_songs

        for song in low_medium_songs:
            self.medium_energy.append(song)

        for song in high_medium_songs:
            self.medium_energy.append(song)

        self.low_energy.sort(key=lambda x: x.energy)
        self.medium_energy.sort(key=lambda x: x.energy)
        self.high_energy.sort(key=lambda x: x.energy)

    def get_leftover_songs(self) -> list:
        output = []

        for song in self.low_energy:
            output.append(song)

        for song in self.medium_energy:
            output.append(song)

        for song in self.high_energy:
            output.append(song)

        for song in self.reserved_songs:
            output.append(song)

        output.sort(key=lambda x: x.name)
        return output

    def get_reserved_songs(self, gig_opener=False, set_closer=False, gig_closer=False, set_opener=False) -> []:
        output = []
        for song in self.reserved_songs:
            if song.gig_opener == gig_opener and \
                    song.set_closer == set_closer and \
                    song.gig_closer == gig_closer and \
                    song.set_opener == set_opener:
                output.append(song)
        return output

    def remove_song(self, name: str):
        idx = SongPool._get_song_index(name, self.unreserved_songs)
        if idx >= 0:
            self.unreserved_songs.pop(idx)

        idx = SongPool._get_song_index(name, self.reserved_songs)
        if idx >= 0:
            self.reserved_songs.pop(idx)

        self.categorize_songs_by_energy()

    def _accept_songs_checking_reservation(self, input_songs: list):
        self.reserved_songs = []
        self.unreserved_songs = []
        self.obsolete_songs = ObsoleteSongs()

        for song in input_songs:
            if not song.active:
                self.obsolete_songs.inactive.append(song)
            elif len(self.event.genre_filter) > 0 and song.genre not in self.event.genre_filter:
                self.obsolete_songs.filtered_by_genre.append(song)
            elif song.gig_opener or song.set_opener or song.set_closer or song.gig_closer:
                self.reserved_songs.append(song)
            else:
                self.unreserved_songs.append(song)

    @staticmethod
    def _filter_songs_by_energy(input_songs: list, hpf: int, lpf: int):
        output = []
        for song in input_songs:
            if hpf <= song.energy < lpf:
                output.append(song)
        return output

    @staticmethod
    def _get_energy_median_of_songs(input_songs: list) -> int:
        energy_list_of_songs = SongPool._get_energy_list_of_songs(input_songs)
        if len(energy_list_of_songs) <= 0:
            return 0
        else:
            return median(SongPool._get_energy_list_of_songs(input_songs))

    @staticmethod
    def _get_energy_list_of_songs(input_songs: list) -> list:
        output = []
        for song in input_songs:
            output.append(song.energy)
        return output

    @staticmethod
    def _get_song_index(song_name: str, song_list: []) -> int:
        output = -1
        for song in song_list:
            output += 1
            if song_name == song.name:
                return output
        return -1

