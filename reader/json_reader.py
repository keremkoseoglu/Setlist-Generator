from reader.abstract_reader import AbstractReader
import json
from gig import performance, set_flow_step
from gig.set import Set
from gig.song import Song
import datetime
from config.constants import *
from util import file_system
from typing import List


def _parse_json_date(json_date: str) -> datetime:
    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%dT%H:%M:%S.%f')
    except:
        pass

    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        pass

    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%d %H:%M:%S.%f')
    except:
        pass

    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%dT%H:%M:%S')
    except:
        pass

    try:
        return datetime.datetime.strptime(json_date, '%Y-%m-%d %H:%M:%S')
    except:
        pass

    return datetime.datetime.strptime(json_date, '%Y-%m-%d')


class JsonReader(AbstractReader):

    def __init__(self):
        pass

    def get_event_list(self) -> list:
        output = []
        for file in file_system.get_files_in_dir(EVENT_DIR):
            output.append(file)
        return output

    def get_event_sets(self, event_param) -> List[Set]:
        output_sets = []

        with open(event_param) as f:
            event_json = json.load(f)

        for json_set in event_json["sets"]:
            set_flow = []

            for json_flow_step in json_set["flow"]:
                flow_step_obj = set_flow_step.SetFlowStep(json_flow_step)
                set_flow.append(flow_step_obj)

            set_input = {"number": json_set["number"],
                         "duration": json_set["duration"],
                         "start": _parse_json_date(json_set["start"]),
                         "flow": set_flow}

            set_obj = Set(set_input)
            output_sets.append(set_obj)

        return output_sets

    def get_band_list(self) -> list:
        output = []
        for file in file_system.get_files_in_dir(BAND_DIR):
            output.append(file)
        return output

    def get_band_songs(self, band_param: str) -> List[Song]:
        output_songs = []

        with open(band_param) as f:
            band_json = json.load(f)

        for json_song in band_json["songs"]:
            if json_song["active"]:
                song_obj = Song(json_song)
                output_songs.append(song_obj)

        return output_songs

    def read(self, band_param: str, event_param: str) -> performance.Performance:
        output_songs = self.get_band_songs(band_param)
        output_sets = self.get_event_sets(event_param)
        return performance.Performance(output_sets, output_songs)


