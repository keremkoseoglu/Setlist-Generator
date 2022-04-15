""" History writer module
Purpose: When we manually modify & save a playlist,
we might want to re-call the same playlist once again.
Therefore; this module is saving a snapshot of the
given playlist, which can be called later again.

Written files can be read by reader.history_reader.
"""
from datetime import datetime
from os import path, remove
import pickle
from config import Config
from gig.performance import Performance
from writer.abstract_writer import AbstractWriter

class HistoryWriter(AbstractWriter):
    """ History Writer """
    FILE_FORMAT = "pickle"
    EXTENSION = f".{FILE_FORMAT}"

    def __init__(self):
        super().__init__()
        self._config = Config()

    def write(self, generated_performance: Performance):
        """ Writes the history file """
        file_path = self._build_file_path(generated_performance)
        with open(file_path, "wb") as pickle_file:
            pickle.dump(generated_performance, pickle_file)

    def delete(self, pickle_file: str):
        """ Deletes history file """
        file_name = pickle_file if HistoryWriter.EXTENSION in pickle_file \
                    else pickle_file + HistoryWriter.EXTENSION
        file_path = path.join(self._config.history_dir, file_name)
        remove(file_path)

    @staticmethod
    def _build_file_name(generated_performance: Performance) -> str:
        now = datetime.now()

        return f"{now.strftime('%Y-%m-%d %H-%M-%S')} - " \
               f"{generated_performance.band.name} - " \
               f"{generated_performance.event.name }" \
               f"{HistoryWriter.EXTENSION}"

    def _build_file_path(self, generated_performance: Performance) -> str:
        file_name = HistoryWriter._build_file_name(generated_performance)
        file_path = path.join(self._config.history_dir, file_name)
        return file_path
