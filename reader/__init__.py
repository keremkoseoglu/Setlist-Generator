""" Reader module """
from typing import Protocol
from gig.band import Band
from gig.event import Event
from gig.performance import Performance

class Reader(Protocol):
    """ Reader protocol
    If you need to supply a new data source in the future,
    you can derive a new class from AbstractReader and
    replace json_reader throughout the code
    """
    @property
    def event_list(self) -> list:
        """ Returns a list of events """

    @property
    def band_list(self) -> list:
        """ Returns a list of bands """

    def get_event(self, event_param) -> Event:
        """ Returns the requested event """

    def get_band(self, band_param: str) -> Band:
        """ Returns the requested band """

    def read(self, band_param: str, event_param: str) -> Performance:
        """ Reads the files and returns a performance """
