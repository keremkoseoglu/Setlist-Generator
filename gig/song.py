from enum import Enum


class SongCriteria(Enum):
    undefined = 0
    key = 1
    mood = 2
    genre = 3
    chord = 4
    age = 5


class Song:
    _CHORD_MINOR = "minor"

    _MOOD_BRIGHT = "bright"
    _MOOD_DARK = "dark"

    _MULTIPLIER_LOW = 0.90
    _MULTIPLIER_HIGH = 1.10

    def __init__(self, song_input: dict):
        self.name = song_input["name"]
        self.key = song_input["key"]
        self.chord = song_input["chord"]
        self.duration = song_input["duration"]
        self.bpm = song_input["bpm"]
        self.genre = song_input["genre"]
        self.mood = song_input["mood"]
        self.age = song_input["age"]
        self.popular = song_input["popular"]
        self.we_like = song_input["we_like"]
        self.we_play = song_input["we_play"]
        self.volume = song_input["volume"]
        self.groove = song_input["groove"]
        self.rating = 0
        self.energy = 0
        self.active = song_input["active"]
        self.language = song_input["lang"]

        self._calculate_rating()
        self._calculate_energy()

    def get_formatted_key(self) -> str:
        output = self.key
        if self.chord == self._CHORD_MINOR:
            output += "m"
        return output

    def _calculate_energy(self):
        self.energy = self.bpm * self.volume * self.popular * self.groove

        if self.mood == self._MOOD_BRIGHT:
            self.energy *= self._MULTIPLIER_HIGH
        elif self.mood == self._MOOD_DARK:
            self.energy *= self._MULTIPLIER_LOW
        else:
            assert False

    def _calculate_rating(self):
        self.rating = self.popular * self.we_like * self.we_play
