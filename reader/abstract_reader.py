from abc import ABC, abstractmethod
from gig.performance import Performance


class AbstractReader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_performance_list(self) -> list:
        pass

    @abstractmethod
    def read(self, param: str) -> Performance:
        pass
