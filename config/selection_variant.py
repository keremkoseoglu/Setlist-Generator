""" Selection variant module """
from dataclasses import dataclass
import json
from os import path
from typing import List
from config import Config
from gig.band import Band
from gig.event import Event
from gig.song import SongCriteria


@dataclass
class SelectionVariantEntry:
    """ Selection variant entry """
    song_criteria: SongCriteria
    priority: int
    selected: bool

    @property
    def as_dict(self) -> dict:
        """ Returns entry as dict """
        return {
         "song_criteria": self.song_criteria.name,
         "priority": self.priority,
         "selected": self.selected
        }


class SelectionVariant:
    """ Selection variant """
    _SEPARATOR = "__"

    def __init__(self, band: Band, event: Event):
        self.band = band
        self.event = event
        self._config = Config()

    @property
    def file_name(self) -> str:
        """ Builds and returns a file name """
        output = self.band.name + SelectionVariant._SEPARATOR + self.event.name
        output += "." + self._config.data_file_extension
        output = output.replace(" ", SelectionVariant._SEPARATOR)
        return output

    @property
    def file_path(self) -> str:
        """ Builds and returns the file path """
        return path.join(self._config.selection_variant_dir, self.file_name)

    def load(self) -> List[SelectionVariantEntry]:
        """ Loads the selection variant from the file """
        output = []
        try:
            with open(self.file_path, encoding="utf-8") as variant_file:
                data = json.load(variant_file)
                for entry in data:
                    criteria = entry["criteria"]
                    song_criteria = SongCriteria[criteria]
                    sve = SelectionVariantEntry(song_criteria,
                                                entry["priority"],
                                                entry["selected"])
                    output.append(sve)
        except Exception:
            pass
        return output

    def load_serialized(self) -> List:
        """ Loads selection variant as JSON """
        output = []
        load_result = self.load()
        if load_result is None:
            return output
        for sve in load_result:
            output.append(sve.as_dict)
        return output

    def save(self, entries: List[SelectionVariantEntry]):
        """ Writes the variant to disk """
        output = []

        for entry in entries:
            entry_dict = {"criteria": entry.song_criteria.name,
                          "priority": entry.priority,
                          "selected": entry.selected}
            output.append(entry_dict)

        with open(self.file_path, "w", encoding="utf-8") as variant_file:
            json.dump(output, variant_file)
