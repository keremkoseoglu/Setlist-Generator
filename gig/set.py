""" Gig set module """
from typing import List
from gig.set_flow_step import SetFlowStep
from gig.song import Song


class Set:
    """ Gig set class """
    def __init__(self, set_input: dict):
        self.number = set_input["number"]
        self.plan_duration = set_input["duration"]
        self.flow = set_input["flow"]
        self.start = set_input["start"]

    @property
    def actual_duration(self) -> int:
        """ Actual duration of the set """
        output = 0
        for flow_step in self.flow:
            for song in flow_step.songs:
                output += song.duration
        return output

    def get_plan_flow_index_duration(self, flow_number: int) -> int:
        """ Returns the planned flow set duration """
        for flow_step in self.flow:
            if flow_step.number == flow_number:
                return self.get_plan_flow_step_duration(flow_step)
        return 0

    def get_plan_flow_step_duration(self, flow_step: SetFlowStep) -> int:
        """ Returns the planned flow set duration """
        return self.plan_duration * flow_step.percentage / 100

    def insert_song(self, song: Song, index: int):
        """ Adds a new song to the set """
        cursor = -1
        for flow_step in self.flow:
            flow_cursor = -1
            found = False
            for flow_song in flow_step.songs: # pylint: disable=W0612
                cursor += 1
                flow_cursor += 1
                if cursor == index:
                    found = True
                    break
            if found:
                flow_step.songs.insert(flow_cursor, song)
                return

    def enforce_song_list(self, new_song_list: List[str], song_pool: List[Song]):
        """ Enforces given song list """
        first_step = True
        for flow_step in self.flow:
            flow_step.songs = []
            if not first_step:
                continue
            first_step = False

            for new_song in new_song_list:
                for pool_entry in song_pool:
                    if pool_entry.name == new_song:
                        flow_step.songs.append(pool_entry)
