""" Constants used throughout the program """
import os
import json

class Config:
    """ Class to handle constants """

    _CONFIG_FILE = "config.json"
    _DATA_DIR = "data"

    def __init__(self):
        self._config = {}
        config_path = Config._get_path_in_cwd(Config._CONFIG_FILE)
        with open(config_path) as config_file:
            self._config = json.load(config_file)

    @property
    def band_dir(self) -> str:
        """ Band directory """
        return Config._get_data_path_in_cwd(self._config["BAND_DIR"])

    @property
    def data_file_extension(self) -> str:
        """ Data file extension """
        return self._config["DATA_FILE_EXTENSION"]

    @property
    def download_dir(self) -> str:
        """ Download directory """
        return self._config["DOWNLOAD_DIR"]

    @property
    def event_dir(self) -> str:
        """ Event directory """
        return Config._get_data_path_in_cwd(self._config["EVENT_DIR"])

    @property
    def selection_variant_dir(self) -> str:
        """ Selection variant directory """
        return Config._get_data_path_in_cwd(self._config["SELECTION_VARIANT_DIR"])

    @property
    def igigi_dir(self) -> str:
        """ Igigi directory """
        return self._config["IGIGI_DIR"]

    @property
    def igigi_json(self) -> str:
        """ Igigi json file name """
        return self._config["IGIGI_JSON"]

    @property
    def lyric_dir(self) -> str:
        """ Lyric directory """
        return Config._get_data_path_in_cwd(self._config["LYRIC_DIR"])

    @property
    def sample_dir(self) -> str:
        """ Sample directory """
        return Config._get_data_path_in_cwd(self._config["SAMPLE_DIR"])

    @property
    def sample_json(self) -> str:
        """ Sample json file name """
        return self._config["SAMPLE_JSON"]

    @property
    def gui_cell_height(self) -> int:
        """ GUI cell height """
        return self._config["GUI_CELL_HEIGHT"]

    @property
    def gui_cell_width(self) -> int:
        """ GUI cell width """
        return self._config["GUI_CELL_WIDTH"]

    @staticmethod
    def _get_path_in_cwd(file: str) -> str:
        return os.path.join(os.getcwd(), file)

    @staticmethod
    def _get_data_path_in_cwd(file: str) -> str:
        data_dir = Config._get_path_in_cwd(Config._DATA_DIR)
        return os.path.join(data_dir, file)
        


# File system
BAND_DIR = "/Users/kerem/OneDrive/Software/Kerem/Development/setlist/data/band/"
DATA_FILE_EXTENSION = "json"
DOWNLOAD_DIR = "/Users/kerem/Downloads/"
EVENT_DIR = "/Users/kerem/OneDrive/Software/Kerem/Development/setlist/data/event/"
SELECTION_VARIANT_DIR = "/Users/kerem/OneDrive/Software/Kerem/Development/setlist/data/selvar/"
IGIGI_DIR = "/Users/kerem/OneDrive/Apps/igigi/"
IGIGI_JSON = "igigi.json"
LYRIC_DIR = "/Users/kerem/OneDrive/Software/Kerem/Development/setlist/data/lyric/"
SAMPLE_DIR = "/Users/kerem/OneDrive/Software/Kerem/Development/setlist/data/sample/"
SAMPLE_JSON = "sample.json"

# GUI
GUI_CELL_HEIGHT = 30
GUI_CELL_WIDTH = 150
