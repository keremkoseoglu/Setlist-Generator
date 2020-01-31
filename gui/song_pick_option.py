from config.constants import *
import tkinter
from gui.labeled_checkbox import LabeledCheckbox


class SongPickOption:

    checkbox: LabeledCheckbox
    _priority: tkinter.Entry
    _priority_text: tkinter.StringVar

    def __init__(self, parent: tkinter.Toplevel, label_text: str, priority: int, x_pos: int, y_pos: int):
        self.checkbox = LabeledCheckbox(parent, label_text, x_pos, y_pos)

        self._priority_text = tkinter.StringVar()
        self._priority_text.set(str(priority))
        self._priority = tkinter.Entry(parent, textvariable=self._priority_text, width=5)
        self._priority.place(x=x_pos + GUI_CELL_WIDTH + 100, y=y_pos)
        parent.update()

    def get_priority(self) -> int:
        return int(self._priority_text.get())

