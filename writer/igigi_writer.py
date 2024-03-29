""" Module for Igigi integration

About Igigi: https://github.com/keremkoseoglu/igigi

Igigi is a mobile React Native app, which can display setlist & lyrics
during the gig. You can also assign sounds to pads
and play them during the gig.

This writer will generate files in Igigi format so you can import
them to your iPad over Dropbox.
"""
import json
from os import path
from copy import deepcopy
from datetime import datetime
from gig import performance
from gig.song import Song
from gig.sample import get_samples_as_list
from writer import Writer
from config import Config


class IgigiWriter(Writer):
    """ Generates files in Igigi format """
    def __init__(self):
        super().__init__()
        self._json = {}
        self._json_before = {}
        config = Config()
        self._json_path = path.join(config.igigi_dir, config.igigi_json)
        self._performance = performance.Performance(None, None)

    def write(self, generated_performance: performance.Performance):
        """ Write files to disk """
        self._performance = generated_performance
        self._read_json()

        self._merge_performance_into_json()

        if self._json != self._json_before:
            self._write_json()

    def _read_json(self):
        if path.exists(self._json_path):
            with open(self._json_path, encoding="utf-8") as igigi_json_file:
                self._json = json.load(igigi_json_file)
        else:
            self._json = {
                "samples": [],
                "gigs": []
            }
        self._json_before = deepcopy(self._json)

    def _write_json(self):
        try:
            with open(self._json_path, "w", encoding="utf-8") as igigi_json_file:
                json.dump(self._json, igigi_json_file, indent=4)
        except Exception as error:
            with open(self._json_path, "w", encoding="utf-8") as igigi_json_file:
                json.dump(self._json_before, igigi_json_file, indent=4)
            raise error

    def _merge_performance_into_json(self):
        igigi_gig = self._append_or_get_performance()
        self._write_sets(igigi_gig)
        self._write_inactive_songs(igigi_gig)
        self._write_filtered_songs(igigi_gig)
        self._write_samples()

    def _write_samples(self):
        self._json["samples"] = get_samples_as_list()

    def _write_sets(self, igigi_gig: dict):
        for event_set in self._performance.event.sets:
            igigi_set = {
                "start": IgigiWriter._datetime_to_json(event_set.start),
                "songs": []
            }

            for flow_step in event_set.flow:
                for song in flow_step.songs:
                    igigi_song = self._song_to_igigi_dict(song)
                    igigi_set["songs"].append(igigi_song)

            igigi_gig["sets"].append(igigi_set)

    @staticmethod
    def _datetime_to_json(date_time: datetime) -> str:
        """ 2012-04-23T21:30:00 """
        output = ""
        output += str(date_time.year) + "-"
        output += IgigiWriter._get_time_val(date_time.month) + "-"
        output += IgigiWriter._get_time_val(date_time.day) + "T"
        output += IgigiWriter._get_time_val(date_time.hour) + ":"
        output += IgigiWriter._get_time_val(date_time.minute) + ":00"
        return output

    @staticmethod
    def _get_time_val(raw: int) -> str:
        output = str(raw)
        while len(output) < 2:
            output = "0" + output
        return output

    def _song_to_igigi_dict(self, song: Song):
        is_skippable = self._performance != None and \
                       self._performance.event_setting != None and \
                       self._performance.event_setting.skippables != None and \
                       song.name in self._performance.event_setting.skippables

        output = {
            "name": song.name,
            "duration": song.duration,
            "key": song.formatted_key,
            "pads": song.pads,
            "lyrics": song.lyrics_as_list,
            "skippable": is_skippable
        }
        return output

    def _write_inactive_songs(self, igigi_gig: dict):
        for inactive_song in self._performance.song_pool.leftover_songs:
            igigi_song = self._song_to_igigi_dict(inactive_song)
            igigi_gig["inactive_songs"].append(igigi_song)

    def _write_filtered_songs(self, igigi_gig: dict):
        for filtered_song in self._performance.song_pool.obsolete_songs.all:
            igigi_song = self._song_to_igigi_dict(filtered_song)
            igigi_gig["filtered_songs"].append(igigi_song)

    def _append_or_get_performance(self) -> dict:
        output = None
        gig_exists = False

        for gig in self._json["gigs"]:
            if gig["band"] == self._performance.band.name and \
                gig["event"] == self._performance.event.name:
                output = gig
                gig_exists = True
                break

        if output is None:
            output = {
                "band": self._performance.band.name,
                "event": self._performance.event.name,
            }

        output["sets"] = []
        output["inactive_songs"] = []
        output["filtered_songs"] = []

        if not gig_exists:
            self._json["gigs"].append(output)
        return output
