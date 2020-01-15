from abc import ABC, abstractmethod
from gig.performance import Performance


class AbstractGenerator(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def generate(self, perf: Performance):
        pass
