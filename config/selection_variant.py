from config.constants import *
from gig.band import Band
from gig.event import Event
from gig.song import SongCriteria
import json
from os import path
from typing import List


class SelectionVariantEntry:
    def __init__(self, song_criteria: SongCriteria, priority: int, selected: bool):
        self.song_criteria = song_criteria
        self.priority = priority
        self.selected = selected


class SelectionVariant:
    _SEPARATOR = "__"

    def __init__(self, band: Band, event: Event):
        self.band = band
        self.event = event

    @property
    def file_name(self) -> str:
        output = self.band.name + SelectionVariant._SEPARATOR + self.event.name + "." + DATA_FILE_EXTENSION
        output = output.replace(" ", SelectionVariant._SEPARATOR)
        return output

    @property
    def file_path(self) -> str:
        return path.join(SELECTION_VARIANT_DIR, self.file_name)

    def load(self) -> List[SelectionVariantEntry]:
        output = []
        try:
            with open(self.file_path) as fp:
                data = json.load(fp)
                for entry in data:
                    criteria = entry["criteria"]
                    song_criteria = SongCriteria[criteria]
                    sve = SelectionVariantEntry(song_criteria,
                                                entry["priority"],
                                                entry["selected"])
                    output.append(sve)
        except:
            pass
        return output

    def save(self, entries: List[SelectionVariantEntry]):
        output = []

        for entry in entries:
            entry_dict = {"criteria": entry.song_criteria.name,
                          "priority": entry.priority,
                          "selected": entry.selected}
            output.append(entry_dict)

        with open(self.file_path, "w") as fp:
            json.dump(output, fp)
