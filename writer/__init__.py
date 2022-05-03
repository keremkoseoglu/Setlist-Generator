""" Writer module """
from typing import Protocol
from gig.performance import Performance

class Writer(Protocol):
    """ Writer protocol """
    def write(self, generated_performance: Performance):
        """ Writes a new file """
