""" Pick option module """
import tkinter
from config.constants import GUI_CELL_WIDTH
from gui.labeled_checkbox import LabeledCheckbox


class SongPickOption:
    """ Pick option class """

    checkbox: LabeledCheckbox
    _priority: tkinter.Entry
    _priority_text: tkinter.StringVar

    def __init__(self,
                 parent: tkinter.Toplevel,
                 label_text: str,
                 priority: int,
                 x_pos: int,
                 y_pos: int):
        self.checkbox = LabeledCheckbox(parent, label_text, x_pos, y_pos)

        self._priority_text = tkinter.StringVar()
        self._priority_text.set(str(priority))
        self._priority = tkinter.Entry(parent, textvariable=self._priority_text, width=5)
        self._priority.place(x=x_pos + GUI_CELL_WIDTH + 100, y=y_pos)
        parent.update()

    @property
    def priority(self) -> int:
        """ Returns the priority of the option """
        return int(self._priority_text.get())

    @priority.setter
    def priority(self, new_priority: int):
        """ Sets the priority of the option """
        self._priority_text.set(new_priority)
