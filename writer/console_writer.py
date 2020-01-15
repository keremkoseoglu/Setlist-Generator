from writer.abstract_writer import AbstractWriter
from gig import performance


class ConsoleWriter(AbstractWriter):

    def __init__(self):
        pass

    def write(self, generated_performance: performance.Performance):

        for set in generated_performance.sets:
            print("Set " + str(set.number))

            for flow_step in set.flow:
                for song in flow_step.songs:
                    print(song.name + " - " + song.key + " " + song.chord)

            print("")
            print("Total set duration: " + str(set.get_actual_duration()))

