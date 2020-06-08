""" Abstract writer module """
from abc import ABC, abstractmethod
from gig.performance import Performance


class AbstractWriter(ABC):
    """ Abstract writer class """

    def __init__(self):
        pass

    @abstractmethod
    def write(self, generated_performance: Performance):
        """ Writes a new file """
