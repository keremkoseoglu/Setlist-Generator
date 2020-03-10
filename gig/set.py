from gig.set_flow_step import SetFlowStep
from gig.song import Song


class Set:
    def __init__(self, set_input: dict):
        self.number = set_input["number"]
        self.plan_duration = set_input["duration"]
        self.flow = set_input["flow"]
        self.start = set_input["start"]

    def get_actual_duration(self) -> int:
        output = 0
        for flow_step in self.flow:
            for song in flow_step.songs:
                output += song.duration
        return output

    def get_plan_flow_step_duration(self, flow_number: int) -> int:
        for flow_step in self.flow:
            if flow_step.number == flow_number:
                return self.get_plan_flow_step_duration(flow_step)
        return 0

    def get_plan_flow_step_duration(self, flow_step: SetFlowStep) -> int:
        return self.plan_duration * flow_step.percentage / 100

    def insert_song(self, song: Song, index: int):
        cursor = -1
        for flow_step in self.flow:
            flow_cursor = -1
            found = False
            for flow_song in flow_step.songs:
                cursor += 1
                flow_cursor += 1
                if cursor == index:
                    found = True
                    break
            if found:
                flow_step.songs.insert(flow_cursor, song)
                return
