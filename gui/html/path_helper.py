""" Path helper """
from os import path, system
from typing import List
from config import Config
from config.selection_variant import SelectionVariant, SelectionVariantEntry
from gig.song_pool import SongPool
from gig.performance import Performance
from gig.song import conv_str_to_song_criteria
from reader import history_reader, json_reader
from analysis.song_pool_analysis import SongPoolAnalysis, SongPoolAnalysisHtmlGenerator
from generator import primal_generator
from writer import html_writer, igigi_writer, flukebox_writer, history_writer

class PathHelper():
    """ Main helper for GUI """
    def __init__(self) -> None:
        self._config = Config()
        self.performance = Performance()
        self.reader = json_reader.JsonReader()
        self.history_reader = history_reader.HistoryReader()
        self.history_writer = history_writer.HistoryWriter()

    @property
    def static_folder(self) -> str:
        """ Returns the static folder """
        return path.join("web", "static")

    def get_selected_band_path(self, json_file: str) -> str:
        """ Returns band path """
        return path.join(self._config.band_dir, json_file)

    def edit_band_file(self, json_file: str):
        """ Edit band file """
        self._edit_file(self.get_selected_band_path(json_file))

    def get_selected_event_path(self, json_file: str) -> str:
        """ Event path """
        return path.join(self._config.event_dir, json_file)

    def edit_event_file(self, json_file: str):
        """ Edit event file """
        self._edit_file(self.get_selected_event_path(json_file))

    def get_selection_variant_entries(self,
                                      band_file: str,
                                      event_file:str
                                     ) -> List[SelectionVariantEntry]:
        """ Selection variant entries """
        try:
            band_path = self.get_selected_band_path(band_file)
            event_path = self.get_selected_event_path(event_file)
            band = self.reader.get_band(band_path)
            event = self.reader.get_event(event_path)
        except Exception:
            return None

        entries = SelectionVariant(band, event).load_serialized()
        return entries

    def generate_stats(self, band_file: str):
        """ Stats """
        selected_band_path = self.get_selected_band_path(band_file)
        band = self.reader.get_band(selected_band_path)
        band_song_pool = SongPool(band, None)
        analysis = SongPoolAnalysis(band_song_pool, with_obsolete=True)
        generator = SongPoolAnalysisHtmlGenerator(analysis)
        generator.generate()

    def generate_setlist(self, band_file: str, event_file:str, selection_variant: List):
        """ Setlist """
        selected_band_path = self.get_selected_band_path(band_file)
        selected_event_path = self.get_selected_event_path(event_file)

        self.performance = self.reader.read(band_param=selected_band_path,
                                            event_param=selected_event_path)

        criteria = []
        sel_var_list = self.build_selection_variant_from_list(selection_variant)
        sel_var_list.sort(key=lambda x: x.priority)
        for sve in sel_var_list:
            if sve.selected:
                criteria.append(sve.song_criteria)

        primal_generator.PrimalGenerator().generate(self.performance, criteria)
        SelectionVariant(self.performance.band, self.performance.event).save(sel_var_list)

    def get_performance_set_list(self) -> List:
        """ Performance set list """
        output = []

        for event_set in self.performance.event.sets:
            set_dict = {"set": event_set.number, "songs": []}

            for flow_step in event_set.flow:
                for song in flow_step.songs:
                    set_dict["songs"].append(song.name)

            output.append(set_dict)

        dead_set_dict = {"set": 0, "songs": []}
        for dead_song in self.performance.song_pool.dead_songs:
            dead_set_dict["songs"].append(dead_song.name)
        output.append(dead_set_dict)

        return output

    def build_selection_variant_from_list(self, sv_list: List): # pylint: disable=R0201
        """ Build variant """
        output = []
        for entry in sv_list:
            sve = SelectionVariantEntry(conv_str_to_song_criteria(entry["song_criteria"]),
                                        entry["priority"],
                                        entry["selected"])
            output.append(sve)
        return output

    def save(self, song_order: List[str]):
        """ Save """
        self.performance.reorder_songs(song_order)
        html_writer.HtmlWriter().write(self.performance)
        igigi_writer.IgigiWriter().write(self.performance)
        self.history_writer.write(self.performance)
        flukebox_writer.FlukeBoxWriter().write(self.performance)

    def load_history_file(self, file_name: str):
        """ Set history file as performance """
        self.performance = self.history_reader.get_performance(file_name)

    def _edit_file(self, file_path: str): # pylint: disable=R0201
        system(f"open {file_path}")
