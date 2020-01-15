from gig.song_pool import SongPool


class Performance:
    sets: list
    song_pool: SongPool

    def __init__(self, input_sets: list, input_song_pool: list):
        self.sets = input_sets
        self.song_pool = SongPool(input_song_pool)
