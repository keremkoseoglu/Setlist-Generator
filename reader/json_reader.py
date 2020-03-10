from reader.abstract_reader import AbstractReader
import json
from gig import performance, set_flow_step
from gig.band import Band, EventSetting, SongReservation
from gig.event import Event
from gig.set import Set
from gig.song import Song
import datetime
from config.constants import *
from util import file_system


class JsonReader(AbstractReader):

    @staticmethod
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

    def __init__(self):
        pass

    def get_event_list(self) -> list:
        output = []
        for file in file_system.get_files_in_dir(EVENT_DIR):
            output.append(file)
        return output

    def get_event(self, event_param) -> Event:
        output = Event()

        with open(event_param) as f:
            event_json = json.load(f)

        output.name = event_json["name"]
        output.genre_filter = event_json["genre_filter"]
        output.language_filter = event_json["lang_filter"]

        for json_set in event_json["sets"]:
            set_flow = []

            for json_flow_step in json_set["flow"]:
                flow_step_obj = set_flow_step.SetFlowStep(json_flow_step)
                set_flow.append(flow_step_obj)

            set_input = {"number": json_set["number"],
                         "duration": json_set["duration"],
                         "start": JsonReader._parse_json_date(json_set["start"]),
                         "flow": set_flow}

            set_obj = Set(set_input)
            output.sets.append(set_obj)

        return output

    def get_band_list(self) -> list:
        output = []
        for file in file_system.get_files_in_dir(BAND_DIR):
            output.append(file)
        return output

    def get_band(self, band_param: str) -> Band:
        output = Band()

        with open(band_param) as f:
            band_json = json.load(f)

        for json_song in band_json["songs"]:
            song_obj = Song(json_song)
            output.songs.append(song_obj)

        for json_event_setting in band_json["event_settings"]:
            excluded_songs = json_event_setting["excluded_songs"]
            gig_openers = json_event_setting["gig_openers"]
            gig_closers = json_event_setting["gig_closers"]
            set_openers = json_event_setting["set_openers"]
            set_closers = json_event_setting["set_closers"]

            event_setting_obj = EventSetting(excluded_songs, gig_openers, gig_closers, set_openers, set_closers)
            output.event_settings.append(json_event_setting["name"], event_setting_obj)

        return output

    def read(self, band_param: str, event_param: str) -> performance.Performance:
        output_band = self.get_band(band_param)
        output_event = self.get_event(event_param)
        return performance.Performance(output_event, output_band)


