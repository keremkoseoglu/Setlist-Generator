import tkinter
from gui.labeled_combobox import LabeledCombobox
from config.constants import *
from reader.json_reader import JsonReader
import os
from generator import primal_generator
from writer import console_writer, html_writer
from analysis.song_pool_analysis import SongPoolAnalysis, SongPoolAnalysisHtmlGenerator

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

        # Performance selection
        self._performances = JsonReader().get_performance_list()
        self._performance_combo_val = []
        self._build_performance_combo_values()
        self._performance_combo = LabeledCombobox(self._root, "Performance", self._performance_combo_val, 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        # Buttons
        gen_button = tkinter.Button(self._root, text="Edit", command=self._edit_file)
        gen_button.place(x=0, y=cell_y)

        gen_button = tkinter.Button(self._root, text="Generate", command=self._generate)
        gen_button.place(x=GUI_CELL_WIDTH, y=cell_y)

        gen_button = tkinter.Button(self._root, text="Stats", command=self._stats)
        gen_button.place(x=GUI_CELL_WIDTH*2, y=cell_y)

        cell_y += GUI_CELL_HEIGHT

        # Start GUI
        self._root.mainloop()

    def _build_performance_combo_values(self):
        for name in self._performances:
            self._performance_combo_val.append(name)

    def _edit_file(self):
        selected_file_path = self._get_selected_file_path()
        os.system("open " + selected_file_path)

    def _generate(self):
        selected_file_path = self._get_selected_file_path()

        performance = JsonReader().read(param=selected_file_path)
        primal_generator.PrimalGenerator().generate(performance)

        console_writer.ConsoleWriter().write(performance)
        html_writer.HtmlWriter().write(performance)

    def _get_selected_file_path(self) -> str:
        selected_file_name = self._performance_combo.get_selected_value()
        selected_file_path = os.path.join(DATA_DIR_PATH, selected_file_name)
        return selected_file_path

    def _stats(self):
        selected_file_path = self._get_selected_file_path()
        performance = JsonReader().read(param=selected_file_path)
        analysis = SongPoolAnalysis(performance.song_pool)
        generator = SongPoolAnalysisHtmlGenerator(analysis)
        generator.generate()

