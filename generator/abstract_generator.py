""" Abstract generator module """
from abc import ABC, abstractmethod
from typing import List
from gig.performance import Performance
from gig.song import SongCriteria


class AbstractGenerator(ABC):
    """ Abstract generator class
    This is the base file for any setlist generator.
    If, for whatever reason, you need a different generator
    (instead of primal_generator), you can derive a new
    class from AbstractGenerator and replace the Where Used List
    of the primal_generator with your new generator.
    """

    def __init__(self):
        pass

    @abstractmethod
    def generate(self, perf: Performance, criteria: List[SongCriteria]):
        """ Generates a new setlist """
