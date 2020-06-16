""" Labeled checkbox control module """
import tkinter
from config import Config


class LabeledCheckbox:
    """ Labeled checkbox control class """

    def __init__(self, parent: tkinter.Toplevel, label_text: str, x_pos: int, y_pos: int):
        self._label = tkinter.Label(parent, text=label_text)
        self._label.place(x=x_pos, y=y_pos)

        self._val = tkinter.BooleanVar()
        self._checkbox = tkinter.Checkbutton(parent, text="", variable=self._val)
        self._checkbox.place(x=x_pos + Config().gui_cell_width, y=y_pos)

    @property
    def is_checked(self) -> bool:
        """ Tells if the checkbox is checked """
        return self._val.get()

    def check(self):
        """ Checks the checkbox """
        self._val.set(True)

    def set_value(self, val: bool):
        """ Sets checked / not checked directly """
        if val:
            self.check()
        else:
            self.uncheck()

    def uncheck(self):
        """ Unchecks the checkbox """
        self._val.set(False)
