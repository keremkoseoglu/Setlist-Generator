from writer.abstract_writer import AbstractWriter
from gig import performance


class ConsoleWriter(AbstractWriter):

    def __init__(self):
        super().__init__()

    def write(self, generated_performance: performance.Performance):

        for event_set in generated_performance.event.sets:
            print("Set " + str(event_set.number))

            for flow_step in event_set.flow:
                for song in flow_step.songs:
                    print(song.name + " - " + song.key + " " + song.chord)

            print("")
            print("Total set duration: " + str(event_set.get_actual_duration()))

