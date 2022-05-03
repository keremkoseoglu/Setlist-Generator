""" Abstract generator module """
from typing import List, Protocol
from gig.performance import Performance
from gig.song import SongCriteria

class Generator(Protocol):
    """ Generator protocol
    This is the base file for any setlist generator.
    If, for whatever reason, you need a different generator
    (instead of primal_generator), you can derive a new
    class from Generator and replace the Where Used List
    of the primal_generator with your new generator.
    """
    def generate(self, perf: Performance, criteria: List[SongCriteria]):
        """ Generates a new setlist """
