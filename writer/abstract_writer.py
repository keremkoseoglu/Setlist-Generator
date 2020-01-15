from abc import ABC, abstractmethod
from gig.performance import Performance

class AbstractWriter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def write(self, generated_performance: Performance):
        pass