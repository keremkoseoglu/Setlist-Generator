from abc import ABC, abstractmethod
from gig.performance import Performance
from gig.song import SongCriteria
from typing import List


class AbstractGenerator(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def generate(self, perf: Performance, criteria: List[SongCriteria]):
        pass
