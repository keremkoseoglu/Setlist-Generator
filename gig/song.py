""" Song module """
from enum import Enum
from typing import List
from os import path
from config import Config

class SongCriteria(Enum):
    """ Criteria to pick a song """
    undefined = 0
    key = 1
    mood = 2
    genre = 3
    chord = 4
    age = 5

def conv_str_to_song_criteria(str_val: str) -> SongCriteria:
    """ Convert literal to song criteria enum """
    for song_crit in SongCriteria:
        if song_crit.name == str_val:
            return song_crit
    return None


class Song:
    """ Song class """
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
        self.lyrics = song_input["lyrics"]
        self.pads = song_input["pads"]

        if "lineups" in song_input:
            self.lineups = song_input["lineups"]
        else:
            self.lineups = []

        self._calculate_rating()
        self._calculate_energy()

    @property
    def formatted_key(self) -> str:
        """ Returns the well formatted song key """
        output = self.key
        if self.chord == self._CHORD_MINOR:
            output += "m"
        return output

    @property
    def lyrics_as_list(self) -> List[str]:
        """ Returns the lyrics as list """
        output = []

        if self.lyrics == "":
            return output

        lyric_path = path.join(Config().lyric_dir, self.lyrics)
        if not path.exists(lyric_path):
            raise Exception(f"File not found: {lyric_path}")

        with open(lyric_path, "r", encoding="utf-8", errors="ignore") as lyric_file:
            output = lyric_file.readlines()

        output = [x.strip() for x in output]
        for line_index in range(0, len(output)):
            line = output[line_index]
            line = line.replace("\x00", "")
            output[line_index] = line
            if line.replace(" ", "") == "":
                line = "__________"
                output[line_index] = line
        return output

    @property
    def has_lineup_constraint(self) -> bool:
        """ Returns true if the song can only be played with a specific lineup """
        return len(self.lineups) > 0

    def can_be_played_with_lineup(self, lineup: str) -> bool:
        """ Can the song be played with the specified lineup """
        if not self.has_lineup_constraint:
            return True
        return lineup in self.lineups

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
