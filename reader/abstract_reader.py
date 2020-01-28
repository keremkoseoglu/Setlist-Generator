from abc import ABC, abstractmethod
from gig.performance import Performance


class AbstractReader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_event_list(self) -> list:
        pass

    @abstractmethod
    def get_band_list(self) -> list:
        pass

    @abstractmethod
    def read(self, band_param: str, event_param: str) -> Performance:
        pass
