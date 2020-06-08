""" Set flow step module """

class SetFlowStep:
    """ Set flow step class """
    part: int
    energy: int
    songs: list
    percentage: int

    def __init__(self, step_input: dict):
        self.part = step_input["part"]
        self.energy = step_input["energy"]
        self.percentage = step_input["percentage"]
        self.songs = []

    @property
    def duration(self) -> int:
        """ Returns duration of the set flow step """
        output = 0
        for song in self.songs:
            output += song.duration
        return output
