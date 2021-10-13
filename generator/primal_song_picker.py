""" Song picker module, used by primal generator """
import copy
from typing import List
from gig.performance import Performance
from gig.song_pool import SongPool
from gig.song import Song, SongCriteria
from gig.set_flow_step import SetFlowStep
from gig.set import Set


class PrimalSongPickerInput:
    """ Picks the next best song """
    def __init__(self,
                 p_song_pool: SongPool,
                 p_flow_step: SetFlowStep,
                 p_prev_song: Song,
                 p_prev_flow_step: SetFlowStep,
                 p_next_flow_step: SetFlowStep,
                 p_is_last_flow_step_of_gig: bool,
                 p_set: Set,
                 p_is_last_set: bool,
                 p_is_first_set: bool,
                 p_song_criteria: List[SongCriteria],
                 p_performance: Performance):
        self.song_pool = p_song_pool
        self.flow_step = p_flow_step
        self.prev_song = p_prev_song
        self.prev_flow_step = p_prev_flow_step
        self.next_flow_step = p_next_flow_step
        self.is_last_flow_step_of_gig = p_is_last_flow_step_of_gig
        self.is_last_set = p_is_last_set
        self.is_first_set = p_is_first_set
        self.set = p_set
        self.song_criteria = p_song_criteria
        self.performance = p_performance


class PrimalCandidateSet:
    """ Defines a set of candidates """
    candidates: List

    def __init__(self, p_candidates: List):
        self.candidates = p_candidates


class PrimalSongPicker:
    """ Class to pick the best next song """

    def __init__(self):
        self._input = None
        self._pop_recursion = False

    def pop_best_song(self, p_input: PrimalSongPickerInput) -> bool:
        """ Chooses the next best next song and removes from the song pool """
        self._input = p_input
        candidate_sets = self._get_candidate_sets()
        best_song = None

        for candidate_set in candidate_sets:
            if len(candidate_set.candidates) >= 1:
                best_song = candidate_set.candidates[0]
                break

        if best_song is None:
            best_song = self._append_closer()
        else:
            set_length_after_best_song = self._input.set.actual_duration + best_song.duration
            set_length_after_best_song_and_closers = set_length_after_best_song + self._get_closer_length() # pylint: disable=C0301

            if set_length_after_best_song_and_closers > self._input.set.plan_duration:
                best_song = self._append_closer()
            else:
                self._input.flow_step.songs.append(best_song)

        if best_song is None:
            return False
        self._input.song_pool.remove_song(best_song.name)
        return True

    def _append_closer(self) -> Song:
        out_song = None
        if self._input.is_last_set:
            out_song = self._pop_gig_closer()
        else:
            out_song = self._pop_set_closer()
        if out_song is not None:
            self._input.flow_step.songs.append(out_song)
        return out_song

    def _get_best_song_position(self, best_song: Song) -> tuple:
        step_index = 0
        song_index = 0
        best_energy_difference = 999999999

        flow_step_index = -1
        for flow_step in self._input.set.flow:
            flow_step_index += 1
            flow_song_index = -1
            for flow_song in flow_step.songs:
                flow_song_index += 1
                energy_difference = flow_song.energy - best_song.energy
                if energy_difference < best_energy_difference:
                    step_index = flow_step_index
                    song_index = flow_song_index
                    best_energy_difference = energy_difference

        return step_index, song_index

    def _get_candidate_sets(self) -> List[PrimalCandidateSet]:
        candidate_sets = []

        if self._input.prev_song is None:
            if self._input.is_first_set:
                candidate_sets.append(PrimalCandidateSet(self._input.song_pool.get_reserved_songs(
                    gig_opener=True,
                    set_opener=False,
                    set_closer=False)))
            else:
                candidate_sets.append(PrimalCandidateSet(self._input.song_pool.get_reserved_songs(
                    gig_opener=False,
                    set_opener=True,
                    set_closer=False)))
        else:
            event_setting = self._input.performance.event_setting
            if event_setting is not None:
                song_reservation = event_setting.get_song_reservation(self._input.prev_song.name)
                if song_reservation is not None:
                    if song_reservation.gig_opener:
                        candidate_sets.append(
                            PrimalCandidateSet(
                                self._input.song_pool.get_reserved_songs(
                                    gig_opener=True,
                                    set_opener=False,
                                    set_closer=False)))
                    if song_reservation.set_opener:
                        candidate_sets.append(
                            PrimalCandidateSet(
                                self._input.song_pool.get_reserved_songs(
                                    gig_opener=False,
                                    set_opener=True,
                                    set_closer=False)))

        remaining_criteria = copy.deepcopy(self._input.song_criteria)

        while len(remaining_criteria) > 0:
            candidate_sets.append(
                PrimalCandidateSet(
                    self._get_desired_songs(p_criteria=remaining_criteria)))
            remaining_criteria.pop()
        candidate_sets.append(
            PrimalCandidateSet(
                self._get_desired_songs()))

        return candidate_sets

    def _get_closer_length(self) -> int:
        out_length = 0
        closers = self._input.song_pool.get_reserved_songs(
            gig_closer=self._input.is_last_set,
            set_closer=not self._input.is_last_set)
        for closer in closers:
            out_length += closer.duration
        return out_length

    def _get_desired_songs(self, p_criteria: List[SongCriteria] = None):
        output = self._get_songs_of_desired_energy()
        if len(output) <= 0:
            return output

        if self._input.prev_song is not None:
            if p_criteria is None:
                criteria = []
            else:
                criteria = p_criteria

            if SongCriteria.key in criteria:
                for output_item in output:
                    if output_item.key == self._input.prev_song.key:
                        output.remove(output_item)

            if SongCriteria.mood in criteria:
                for output_item in output:
                    if output_item.mood != self._input.prev_song.mood:
                        output.remove(output_item)

            if SongCriteria.genre in criteria:
                for output_item in output:
                    if output_item.genre != self._input.prev_song.genre:
                        output.remove(output_item)

            if SongCriteria.chord in criteria:
                for output_item in output:
                    if output_item.chord != self._input.prev_song.chord:
                        output.remove(output_item)

            if SongCriteria.age in criteria:
                for output_item in output:
                    if output_item.age != self._input.prev_song.age:
                        output.remove(output_item)

        return output

    def _get_gig_closer_order(self, song_name: str) -> int:
        song_reservation = self._input.performance.event_setting.get_song_reservation(song_name)
        return song_reservation.gig_closer_order

    def _get_songs_of_desired_energy(self) -> []:
        output = []

        if self._input.flow_step.energy == 1:
            output = copy.deepcopy(self._input.song_pool.low_energy)
        elif self._input.flow_step.energy == 2:
            output = copy.deepcopy(self._input.song_pool.medium_energy)
        elif self._input.flow_step.energy == 3:
            output = copy.deepcopy(self._input.song_pool.high_energy)

        if self._input.prev_flow_step is not None and self._input.next_flow_step is not None:
            if self._input.prev_flow_step.energy < self._input.flow_step.energy < self._input.next_flow_step.energy: # pylint: disable=C0301
                output.sort(key=lambda x: x.energy)
            elif self._input.prev_flow_step.energy < self._input.flow_step.energy > self._input.next_flow_step.energy: # pylint: disable=C0301
                pass
            elif self._input.prev_flow_step.energy > self._input.flow_step.energy < self._input.next_flow_step.energy: # pylint: disable=C0301
                pass
            elif self._input.prev_flow_step.energy > self._input.flow_step.energy > self._input.next_flow_step.energy: # pylint: disable=C0301
                output.sort(key=lambda x: x.energy, reverse=True)
        elif self._input.prev_flow_step is not None:
            if self._input.prev_flow_step.energy < self._input.flow_step.energy:
                output.sort(key=lambda x: x.energy * x.rating)
            else:
                output.sort(key=lambda x: x.energy * x.rating, reverse=True)
        elif self._input.next_flow_step is not None:
            if self._input.next_flow_step.energy < self._input.flow_step.energy:
                output.sort(key=lambda x: x.energy, reverse=True)
            else:
                output.sort(key=lambda x: x.energy)

        return output

    def _pop_gig_closer(self) -> Song:
        gig_closer_songs = self._input.song_pool.get_reserved_songs(
            gig_opener=False,
            set_closer=False,
            gig_closer=True)

        if len(gig_closer_songs) <= 0:
            return self._pop_set_closer()

        gig_closer_songs.sort(key=lambda x: self._get_gig_closer_order(x.name))

        gig_closer_song = gig_closer_songs[0]
        self._input.song_pool.remove_song(gig_closer_song.name)
        return gig_closer_song

    def _pop_set_closer(self) -> Song:
        set_closer_songs = self._input.song_pool.get_reserved_songs(
            gig_opener=False,
            set_closer=True,
            gig_closer=False)

        if len(set_closer_songs) <= 0:
            return None

        set_closer_song = set_closer_songs[0]
        self._input.song_pool.remove_song(set_closer_song.name)
        return set_closer_song
