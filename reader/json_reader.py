from reader.abstract_reader import AbstractReader
import json
from gig import performance, set, set_flow_step, song
import datetime
from config.constants import *
from util import file_system


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

    def get_performance_list(self) -> list:
        output = []

        for file in file_system.get_files_in_dir(DATA_DIR_PATH):
            output.append(file)

        return output

    def read(self, param:str) -> performance.Performance:
        output_songs = []
        output_sets = []

        with open(param) as f:
            json_data = json.load(f)

        for json_song in json_data["songs"]:
            if json_song["active"]:
                song_obj = song.Song(json_song)
                output_songs.append(song_obj)

        for json_set in json_data["sets"]:
            set_flow = []

            for json_flow_step in json_set["flow"]:
                flow_step_obj = set_flow_step.SetFlowStep(json_flow_step)
                set_flow.append(flow_step_obj)

            set_input = {"number": json_set["number"],
                         "duration": json_set["duration"],
                         "start": _parse_json_date(json_set["start"]),
                         "flow": set_flow}

            set_obj = set.Set(set_input)
            output_sets.append(set_obj)

        return performance.Performance(output_sets, output_songs)


