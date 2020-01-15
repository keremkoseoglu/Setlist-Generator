class Song:
    _CHORD_MINOR = "minor"

    _MOOD_BRIGHT = "bright"
    _MOOD_DARK = "dark"

    _MULTIPLIER_LOW = 0.90
    _MULTIPLIER_HIGH = 1.10

    name: str
    key: str
    chord: str
    duration: int
    bpm: int
    genre: str
    gig_opener: bool
    gig_closer: bool
    mood: str
    age: int
    popular: int
    set_closer: bool
    we_like: int
    we_play: int
    rating: int
    energy: int
    volume: int
    groove: int

    def __init__(self, song_input: dict):
        self.name = song_input["name"]
        self.key = song_input["key"]
        self.chord = song_input["chord"]
        self.duration = song_input["duration"]
        self.bpm = song_input["bpm"]
        self.genre = song_input["genre"]
        self.mood = song_input["mood"]
        self.age = song_input["age"]
        self.popular = song_input["popular"]
        self.we_like = song_input["we_like"]
        self.we_play = song_input["we_play"]
        self.volume = song_input["volume"]
        self.groove = song_input["groove"]
        self.rating = 0
        self.energy = 0

        try:
            self.gig_opener = song_input["gig_opener"]
        except:
            self.gig_opener = False

        try:
            self.gig_closer = song_input["gig_closer"]
        except:
            self.gig_closer = False

        try:
            self.set_closer = song_input["set_closer"]
        except:
            self.set_closer = False

        self._calculate_rating()
        self._calculate_energy()

    def get_formatted_key(self) -> str:
        output = self.key
        if self.chord == self._CHORD_MINOR:
            output += "m"
        return output

    def _calculate_energy(self):
        self.energy = self.bpm * self.volume * self.popular * self.groove

        if self.mood == self._MOOD_BRIGHT:
            self.energy *= self._MULTIPLIER_HIGH
        elif self.mood == self._MOOD_DARK:
            self.energy *= self._MULTIPLIER_LOW
        else:
            assert False

    def _calculate_rating(self):
        self.rating = self.popular * self.we_like * self.we_play
