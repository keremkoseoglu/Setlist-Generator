""" Performance preview module """
import tkinter.ttk
import tkinter
from gig.performance import Performance
from writer.html_writer import HtmlWriter
from writer.igigi_writer import IgigiWriter
from writer.flukebox_writer import FlukeBoxWriter


class PerformancePreviewWindow(tkinter.Toplevel):
    """ Performance preview window """

    _BUTTON_HEIGHT = 50
    _BUTTON_WIDTH = 50
    _LIST_HEIGHT = 450
    _WINDOW_WIDTH = 400
    _WINDOW_HEIGHT = 1000
    _X_SPACING = 5
    _Y_SPACING = 10

    def __init__(self, performance: Performance):
        tkinter.Toplevel.__init__(self)
        self.wm_geometry(self._geometry)
        self._performance = performance

        cell_y = 0

        self._song_list = tkinter.Listbox(self, exportselection=False)
        self._song_list.place(x=0,
                              y=cell_y,
                              width=PerformancePreviewWindow._WINDOW_WIDTH,
                              height=PerformancePreviewWindow._LIST_HEIGHT)

        cell_y += PerformancePreviewWindow._LIST_HEIGHT + PerformancePreviewWindow._Y_SPACING

        cell_x = 0
        save_button = tkinter.Button(self, text="<<", command=self._prev_set)
        save_button.place(x=cell_x, y=cell_y)
        cell_x += PerformancePreviewWindow._BUTTON_WIDTH + PerformancePreviewWindow._X_SPACING

        save_button = tkinter.Button(self, text="↓", command=self._kill)
        save_button.place(x=cell_x, y=cell_y)
        cell_x += PerformancePreviewWindow._BUTTON_WIDTH + PerformancePreviewWindow._X_SPACING

        save_button = tkinter.Button(self, text="↑", command=self._resurrect)
        save_button.place(x=cell_x, y=cell_y)
        cell_x += PerformancePreviewWindow._BUTTON_WIDTH + PerformancePreviewWindow._X_SPACING

        save_button = tkinter.Button(self, text=">>", command=self._next_set)
        save_button.place(x=cell_x, y=cell_y)
        cell_x += PerformancePreviewWindow._BUTTON_WIDTH + PerformancePreviewWindow._X_SPACING

        save_button = tkinter.Button(self, text="Save", command=self._save)
        save_button.place(x=cell_x, y=cell_y)
        cell_y += PerformancePreviewWindow._BUTTON_HEIGHT + PerformancePreviewWindow._X_SPACING

        self._dead_list = tkinter.Listbox(self, exportselection=False)
        self._dead_list.place(x=0,
                              y=cell_y,
                              width=PerformancePreviewWindow._WINDOW_WIDTH,
                              height=PerformancePreviewWindow._LIST_HEIGHT)

        self._set_index = 0
        self._fill_song_list()
        self.mainloop()

    @property
    def _geometry(self) -> str:
        return str(PerformancePreviewWindow._WINDOW_WIDTH) + \
                "x" + \
                str(PerformancePreviewWindow._WINDOW_HEIGHT)

    @property
    def _selected_dead_song(self) -> str:
        return self._dead_list.get(self._dead_list.curselection())

    @property
    def _selected_live_song(self) -> str:
        return self._song_list.get(self._song_list.curselection())

    def _fill_song_list(self):
        self._song_list.delete(0, tkinter.END)
        song_index = -1
        for flow_step in self._performance.event.sets[self._set_index].flow:
            for song in flow_step.songs:
                song_index += 1
                self._song_list.insert(song_index, song.name)

        self._dead_list.delete(0, tkinter.END)
        song_index = -1
        for song in self._performance.song_pool.leftover_songs:
            song_index += 1
            self._dead_list.insert(song_index, song.name)

        self.update()

    def _kill(self):
        self._performance.kill_song(self._selected_live_song)
        self._fill_song_list()

    def _next_set(self):
        if self._set_index >= len(self._performance.event.sets) - 1:
            return
        self._set_index += 1
        self._fill_song_list()

    def _prev_set(self):
        if self._set_index <= 0:
            return
        self._set_index -= 1
        self._fill_song_list()

    def _resurrect(self):
        self._performance.resurrect_song(
            self._selected_dead_song,
            self._set_index,
            self._dead_list.curselection()[0])

        self._fill_song_list()

    def _save(self):
        HtmlWriter().write(self._performance)
        IgigiWriter().write(self._performance)
        FlukeBoxWriter().write(self._performance)
