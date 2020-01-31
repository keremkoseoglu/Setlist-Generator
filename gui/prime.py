import tkinter
from gui.labeled_combobox import LabeledCombobox
from gui.song_pick_option import SongPickOption
from config.constants import *
from reader.json_reader import JsonReader
import os
from generator import primal_generator
from writer import console_writer, html_writer
from analysis.song_pool_analysis import SongPoolAnalysis, SongPoolAnalysisHtmlGenerator
from gig.song import SongCriteria


class Prime:

    _WINDOW_WIDTH = 800
    _WINDOW_HEIGHT = 350

    def __init__(self):
        # Initialization
        cell_y = 0

        # Main container
        self._root = tkinter.Tk()
        self._root.title("Setlist Builder")
        self._root.geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        # Band selection
        self._bands = JsonReader().get_band_list()
        self._band_combo_val = []
        self._build_band_combo_values()
        self._band_combo = LabeledCombobox(self._root, "Band", self._band_combo_val, 0, cell_y)

        gen_button = tkinter.Button(self._root, text="Edit", command=self._edit_band)
        gen_button.place(x=(GUI_CELL_WIDTH * 2)+75, y=cell_y)

        cell_y += GUI_CELL_HEIGHT

        # Event selection
        self._events = JsonReader().get_event_list()
        self._event_combo_val = []
        self._build_event_combo_values()
        self._event_combo = LabeledCombobox(self._root, "Event", self._event_combo_val, 0, cell_y)

        gen_button = tkinter.Button(self._root, text="Edit", command=self._edit_event)
        gen_button.place(x=(GUI_CELL_WIDTH * 2)+75, y=cell_y)

        cell_y += GUI_CELL_HEIGHT * 2

        # Options
        self._by_key = SongPickOption(self._root, "Separate keys", 1, 0, cell_y)
        self._by_key.checkbox.check()
        cell_y += GUI_CELL_HEIGHT
        self._by_genre = SongPickOption(self._root, "Group by genre", 2, 0, cell_y)
        cell_y += GUI_CELL_HEIGHT
        self._by_mood = SongPickOption(self._root, "Group by mood", 3, 0, cell_y)
        cell_y += GUI_CELL_HEIGHT
        self._by_age = SongPickOption(self._root, "Group by age", 4, 0, cell_y)
        cell_y += GUI_CELL_HEIGHT
        self._by_chord = SongPickOption(self._root, "Group by chord", 5, 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        self._song_pick_options = [{"option": self._by_key, "criteria": SongCriteria.key},
                                   {"option": self._by_genre, "criteria": SongCriteria.genre},
                                   {"option": self._by_mood, "criteria": SongCriteria.mood},
                                   {"option": self._by_age, "criteria": SongCriteria.age},
                                   {"option": self._by_chord, "criteria": SongCriteria.chord}]

        cell_y += GUI_CELL_HEIGHT

        # Buttons

        gen_button = tkinter.Button(self._root, text="Generate", command=self._generate)
        gen_button.place(x=0, y=cell_y)

        gen_button = tkinter.Button(self._root, text="Stats", command=self._stats)
        gen_button.place(x=GUI_CELL_WIDTH*2, y=cell_y)

        cell_y += GUI_CELL_HEIGHT

        # Start GUI
        self._root.mainloop()

    def _build_band_combo_values(self):
        for name in self._bands:
            self._band_combo_val.append(name)

    def _build_event_combo_values(self):
        for name in self._events:
            self._event_combo_val.append(name)

    def _edit_band(self):
        selected_file_path = self._get_selected_band_path()
        os.system("open " + selected_file_path)

    def _edit_event(self):
        selected_file_path = self._get_selected_event_path()
        os.system("open " + selected_file_path)

    def _generate(self):
        selected_band_path = self._get_selected_band_path()
        selected_event_path = self._get_selected_event_path()

        performance = JsonReader().read(band_param=selected_band_path, event_param=selected_event_path)

        self._song_pick_options.sort(key=lambda x: x["option"].get_priority())

        song_criteria = []
        for pick_option in self._song_pick_options:
            if pick_option["option"].checkbox.is_checked():
                song_criteria.append(pick_option["criteria"])

        primal_generator.PrimalGenerator().generate(perf=performance, criteria=song_criteria)

        console_writer.ConsoleWriter().write(performance)
        html_writer.HtmlWriter().write(performance)

    def _get_selected_band_path(self) -> str:
        selected_file_name = self._band_combo.get_selected_value()
        selected_file_path = os.path.join(BAND_DIR, selected_file_name)
        return selected_file_path

    def _get_selected_event_path(self) -> str:
        selected_file_name = self._event_combo.get_selected_value()
        selected_file_path = os.path.join(EVENT_DIR, selected_file_name)
        return selected_file_path

    def _stats(self):
        selected_band_path = self._get_selected_band_path()
        selected_event_path = self._get_selected_event_path()
        performance = JsonReader().read(band_param=selected_band_path, event_param=selected_event_path)
        analysis = SongPoolAnalysis(performance.song_pool)
        generator = SongPoolAnalysisHtmlGenerator(analysis)
        generator.generate()

