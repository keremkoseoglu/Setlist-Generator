""" Song pool analysis module """
from dataclasses import dataclass
import os
from gig.song import Song
from gig.song_pool import SongPool

@dataclass
class NumericSongStatistic:
    """ Numeric song statistic, containing average, min, max, etc values """
    max_song = None
    max_value = -999999
    min_song = None
    min_value = 999999
    total_value = 0
    song_count = 0

    @property
    def avg_value(self) -> int:
        """ Returns the average value """
        return int(self.total_value / self.song_count)


class NumericSongStatisticGenerator:
    """ Class to determine min / max values for the given stat """
    def __init__(self):
        self.result = NumericSongStatistic()

    def analyse(self, p_song: Song, p_value: int):
        """ Determines min/max values """
        self.result.song_count += 1
        self.result.total_value += p_value

        if p_value > self.result.max_value:
            self.result.max_value = p_value
            self.result.max_song = p_song

        if p_value < self.result.min_value:
            self.result.min_value = p_value
            self.result.min_song = p_song


class SongPropertyCount:
    """ Counter for any song property """

    def __init__(self):
        self.counts = {}

    def add(self, key: str, value: int = 1):
        """ Count++ """
        if key in self.counts:
            self.counts[key] = self.counts[key] + value
        else:
            self.counts[key] = value

@dataclass
class SongPoolAnalysisResult:
    """ Result of a song pool analysis """
    key_count: SongPropertyCount
    duration_stats: NumericSongStatistic
    genre_count: SongPropertyCount
    energy_stats: NumericSongStatistic
    rating_stats: NumericSongStatistic
    genre_duration: SongPropertyCount
    language_count: SongPropertyCount


class SongPoolAnalysis:
    """ Analyses the song pool and generates statistics
    Note that this class executes upon object creation,
    immediately.
    """

    def __init__(self, pool: SongPool, with_obsolete: bool = False):
        self.pool = pool
        self.result = None

        key_count = SongPropertyCount()
        genre_count = SongPropertyCount()
        genre_duration = SongPropertyCount()
        language_count = SongPropertyCount()

        duration_generator = NumericSongStatisticGenerator()
        energy_generator = NumericSongStatisticGenerator()
        rating_generator = NumericSongStatisticGenerator()

        self.analysis_songs = []
        self.analysis_songs.extend(pool.leftover_songs)
        if with_obsolete:
            self.analysis_songs.extend(pool.obsolete_songs.all)
            self.analysis_songs.extend(pool.dead_songs)

        self.analysis_songs.sort(key = lambda x : x.name)

        for song in self.analysis_songs:
            duration_generator.analyse(p_song=song, p_value=song.duration)
            energy_generator.analyse(p_song=song, p_value=song.energy)
            rating_generator.analyse(p_song=song, p_value=song.rating)
            key_count.add(song.key)
            genre_count.add(song.genre)
            genre_duration.add(song.genre, value=song.duration)
            language_count.add(song.language)

        self.result = SongPoolAnalysisResult(key_count=key_count,
                                             duration_stats=duration_generator.result,
                                             genre_count=genre_count,
                                             energy_stats=energy_generator.result,
                                             rating_stats=rating_generator.result,
                                             genre_duration=genre_duration,
                                             language_count=language_count)


class SongPoolAnalysisHtmlGenerator:
    """ Generates an HTML Report which analyses the song pool """

    _HTML_FILE = "/Users/kerem/Downloads/stats.html"
    analysis: SongPoolAnalysis
    _html: str

    def __init__(self, analysis: SongPoolAnalysis):
        self.analysis = analysis
        self._html = ""

    def generate(self):
        """ Entry method to generate analysis HTML """
        self._generate_html()
        self._download_file()

    def _generate_html(self):
        self._html = ""

        self._put_songs()

        self._put_numeric_song_statistic(stat=self.analysis.result.rating_stats, title="Rating")
        self._put_numeric_song_statistic(stat=self.analysis.result.energy_stats, title="Energy")
        self._put_numeric_song_statistic(stat=self.analysis.result.duration_stats, title="Duration")

        self._put_property_count(stat=self.analysis.result.genre_count, title="Genre")
        self._put_property_count(stat=self.analysis.result.key_count, title="Key")
        self._put_property_count(stat=self.analysis.result.genre_duration, title="Genre Duration")
        self._put_property_count(stat=self.analysis.result.language_count, title="Language")

    def _download_file(self):
        with open(self._HTML_FILE, "w+") as file2:
            file2.write(self._html)
        os.system(f"open {self._HTML_FILE}")

    def _put_numeric_song_statistic(self, stat: NumericSongStatistic, title: str):
        self._html += "<h1>" + title + "</h1><ul>"
        self._html += "<li>Max: " + stat.max_song.name + " (" + str(stat.max_value) + ")</li>"
        self._html += "<li>Min: " + stat.min_song.name + " (" + str(stat.min_value) + ")</li>"
        self._html += "<li>Avg: " + str(stat.avg_value) + "</li>"
        self._html += "<li>Sum: " + str(stat.total_value) + "</li>"
        self._html += "</ul><hr>"

    def _put_property_count(self, stat: SongPropertyCount, title: str):
        self._html += "<h1>" + title + "</h1><ul>"
        for key in stat.counts:
            self._html += "<li>" + key + " - " + str(stat.counts[key]) + "</li>"
        self._html += "</ul><hr>"

    def _put_songs(self):
        self._html += "<h1>Songs</h1><table cellspacing=3 cellpadding=3 border=0>"
        self._put_song_line(name="Name",
                            formatted_key="Key",
                            duration="Duration",
                            bpm="BPM",
                            genre="Genre",
                            rating="Rating",
                            energy="Energy",
                            language="Language")

        for song in self.analysis.analysis_songs:
            self._put_song_line(name=song.name,
                                formatted_key=song.formatted_key,
                                duration=str(song.duration),
                                bpm=str(song.bpm),
                                genre=song.genre,
                                rating=str(int(song.rating)),
                                energy=str(int(song.energy)),
                                language=song.language)

        self._html += "</table><hr>"

    def _put_song_line(self,
                       name: str,
                       formatted_key: str,
                       duration: str,
                       bpm: str,
                       genre: str,
                       rating: str,
                       energy: str,
                       language: str):
        song_html = "<tr>"
        song_html += "<td align=left valign=top>" + name + "</td>"
        song_html += "<td align=left valign=top>" + formatted_key + "</td>"
        song_html += "<td align=right valign=top>" + duration + "</td>"
        song_html += "<td align=right valign=top>" + bpm + "</td>"
        song_html += "<td align=left valign=top>" + genre + "</td>"
        song_html += "<td align=right valign=top>" + rating + "</td>"
        song_html += "<td align=right valign=top>" + energy + "</td>"
        song_html += "<td align=left valign=top>" + language + "</td>"
        song_html += "</tr>"

        self._html += song_html
