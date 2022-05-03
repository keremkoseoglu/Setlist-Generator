""" Console writer module """
from writer import Writer
from gig import performance


class ConsoleWriter(Writer):
    """ Console writer class """
    def write(self, generated_performance: performance.Performance):
        """ Prints everything to console """

        for event_set in generated_performance.event.sets:
            print(f"Set {str(event_set.number)}")

            for flow_step in event_set.flow:
                for song in flow_step.songs:
                    print(song.name + " - " + song.key + " " + song.chord)

            print("")
            print(f"Total set duration: {str(event_set.get_actual_duration())}")
