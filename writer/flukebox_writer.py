""" Module for FlukeBox integration

About FlukeBox: https://github.com/keremkoseoglu/igigi

FlukeBox is a cross-streaming-service audio player. Purpose of this file is;
after generating a setlist, a corresponding practice content will be
generated and opened in Flukebox.
"""
from os import path, system
import json
from writer.abstract_writer import AbstractWriter
from gig import performance
from config import Config


class FlukeBoxWriter(AbstractWriter):
    """ Writes output JSON for FlukeBox and submits the program """
    _FILE = "flukebox_seek.json"

    def __init__(self):
        super().__init__()
        self._output = {}
        self._config = Config()
        self._seek_path = ""

    def write(self, generated_performance: performance.Performance):
        """ Write files to disk """
        self._build_output(generated_performance)
        self._write_file()
        self._submit_flukebox()

    def _build_output(self, generated_performance: performance.Performance):
        self._output = {"seek_songs": [],
                        "seek_in_playlists": []}
        self._seek_path = ""
        if self._config.flukebox_dir == "":
            return
        if len(generated_performance.band.flukebox_playlists) <= 0:
            return
        for event_set in generated_performance.event.sets:
            for flow_step in event_set.flow:
                for song in flow_step.songs:
                    self._output["seek_songs"].append(song.name)
        self._output["seek_in_playlists"] = generated_performance.band.flukebox_playlists

    def _write_file(self):
        self._seek_path = path.join(self._config.download_dir, FlukeBoxWriter._FILE)
        with open(self._seek_path, "w", encoding="utf-8") as output_file:
            json.dump(self._output, output_file)

    def _submit_flukebox(self):
        command = f"cd {self._config.flukebox_dir};"
        command += " venv/bin/python3 main.py seek="
        command += self._seek_path
        system(command)
