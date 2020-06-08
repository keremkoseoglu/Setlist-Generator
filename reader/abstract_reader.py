""" Abstract reader module """
from abc import ABC, abstractmethod
from gig.band import Band
from gig.event import Event
from gig.performance import Performance


class AbstractReader(ABC):
    """ Abstract reader class
    If you need to supply a new data source in the future,
    you can derive a new class from AbstractReader and
    replace json_reader throughout the code
    """
    def __init__(self):
        pass

    @property
    @abstractmethod
    def event_list(self) -> list:
        """ Returns a list of events """

    @property
    @abstractmethod
    def band_list(self) -> list:
        """ Returns a list of bands """

    @abstractmethod
    def get_event(self, event_param) -> Event:
        """ Returns the requested event """

    @abstractmethod
    def get_band(self, band_param: str) -> Band:
        """ Returns the requested band """

    @abstractmethod
    def read(self, band_param: str, event_param: str) -> Performance:
        """ Reads the files and returns a performance """
