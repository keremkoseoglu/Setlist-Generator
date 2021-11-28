""" Primal setlist generator module """
from typing import List
from generator.abstract_generator import AbstractGenerator
from generator.primal_song_picker import PrimalSongPicker, PrimalSongPickerInput
from gig.performance import Performance
from gig.set import Set
from gig.song import SongCriteria


def _get_next_energy(current_set: Set, current_index: int):
    if current_index == len(current_set.flow)-1:
        return 0
    return current_set.flow[current_index+1].energy


def _get_previous_energy(current_set: Set, current_index: int):
    if current_index == 0:
        return 0
    return current_set.flow[current_index - 1].energy


def _plan_set_duration_surpassed(event_set: Set):
    return event_set.actual_duration >= event_set.plan_duration


class PrimalGenerator(AbstractGenerator):
    """ Primal setlist generator class """

    def __init__(self):
        super().__init__()
        self._performance = None

    def generate(self, perf: Performance, criteria: List[SongCriteria]):
        """ Generates a new setlist """
        self._performance = perf
        self._performance.song_pool.categorize_songs_by_energy()
        set_count = len(self._performance.event.sets)

        for set_index in range(0, set_count):
            self._generate_set(set_index, set_count, perf, criteria)


    def _generate_set(self,
                      set_index: int,
                      set_count: int,
                      perf: Performance,
                      criteria: List[SongCriteria]):

        # Prepare
        event_set = self._performance.event.sets[set_index]

        # Case: Set is defined in band JSON
        for manual_set in self._performance.event_setting.manual_sets:
            if manual_set.number == set_index + 1:
                flow_step = event_set.flow[0]
                for manual_song in manual_set.songs:
                    manual_song_obj = self._performance.song_pool.pop_leftover_song(manual_song)
                    flow_step.songs.append(manual_song_obj)
                return

        # Case: Set is not defined in band JSON
        flow_step_count = len(event_set.flow)

        while not _plan_set_duration_surpassed(event_set):
            flow_set_ran_out_of_songs = False

            if len(self._performance.song_pool.unreserved_songs) <= 0:
                return

            for flow_step_index in range(0, flow_step_count):
                flow_step = event_set.flow[flow_step_index]

                planned_flow_step_duration = event_set.get_plan_flow_step_duration(flow_step)
                actual_flow_step_duration = flow_step.duration
                flow_set_ran_out_of_songs = False

                while planned_flow_step_duration >= actual_flow_step_duration:

                    if flow_step_index == 0:
                        previous_flow_step = None
                    else:
                        previous_flow_step = event_set.flow[flow_step_index-1]

                    if flow_step_index == flow_step_count - 1:
                        next_flow_step = None
                    else:
                        next_flow_step = event_set.flow[flow_step_index+1]

                    if len(flow_step.songs) <= 0:
                        if previous_flow_step is not None:
                            prev_song_pos = len(previous_flow_step.songs) - 1
                            previous_song = previous_flow_step.songs[prev_song_pos]
                        else:
                            previous_song = None
                    else:
                        previous_song = flow_step.songs[len(flow_step.songs)-1]

                    if set_index == set_count - 1:
                        is_last_set = True
                        if flow_step_index == flow_step_count - 1:
                            is_last_flow_step_of_gig = True
                        else:
                            is_last_flow_step_of_gig = False
                    else:
                        is_last_set = False
                        is_last_flow_step_of_gig = False

                    psi_input = PrimalSongPickerInput(
                        p_song_pool=self._performance.song_pool,
                        p_flow_step=flow_step,
                        p_prev_song=previous_song,
                        p_prev_flow_step=previous_flow_step,
                        p_next_flow_step=next_flow_step,
                        p_is_last_flow_step_of_gig=is_last_flow_step_of_gig,
                        p_set=event_set,
                        p_is_last_set=is_last_set,
                        p_is_first_set=set_index == 0,
                        p_song_criteria=criteria,
                        p_performance=perf)

                    song_found = PrimalSongPicker().pop_best_song(psi_input)
                    if not song_found:
                        flow_set_ran_out_of_songs = True
                        break

                    if _plan_set_duration_surpassed(event_set):
                        break

                    planned_flow_step_duration = event_set.get_plan_flow_step_duration(flow_step) # pylint: disable=C0301
                    actual_flow_step_duration = flow_step.duration

                if flow_set_ran_out_of_songs:
                    break

            if flow_set_ran_out_of_songs:
                break
