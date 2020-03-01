from gig.song import Song
from gig.song_pool import SongPool
import os


class NumericSongStatistic:
    def __init__(self):
        self.avg_value = 0
        self.max_song = None
        self.max_value = -999999
        self.min_song = None
        self.min_value = 999999
        self.total_value = 0
        self.song_count = 0

    def get_average_value(self) -> int:
        return int(self.total_value / self.song_count)


class NumericSongStatisticGenerator:
    def __init__(self):
        self.result = NumericSongStatistic()

    def analyse(self, p_song: Song, p_value: int):
        self.result.song_count += 1
        self.result.total_value += p_value

        if p_value > self.result.max_value:
            self.result.max_value = p_value
            self.result.max_song = p_song

        if p_value < self.result.min_value:
            self.result.min_value = p_value
            self.result.min_song = p_song


class SongPropertyCount:
    def __init__(self):
        self.counts = {}

    def add(self, key: str, value: int = 1):
        if key in self.counts:
            self.counts[key] = self.counts[key] + value
        else:
            self.counts[key] = value


class SongPoolAnalysisResult:
    def __init__(self,
                 key_count: SongPropertyCount,
                 duration_stats: NumericSongStatistic,
                 genre_count: SongPropertyCount,
                 energy_stats: NumericSongStatistic,
                 rating_stats: NumericSongStatistic,
                 genre_duration: SongPropertyCount
                 ):
        self.key_count = key_count
        self.duration_stats = duration_stats
        self.genre_count = genre_count
        self.energy_stats = energy_stats
        self.rating_stats = rating_stats
        self.genre_duration = genre_duration


class SongPoolAnalysis:
    def __init__(self, pool: SongPool):
        self.pool = pool
        self.result = None

        key_count = SongPropertyCount()
        genre_count = SongPropertyCount()
        genre_duration = SongPropertyCount()

        duration_generator = NumericSongStatisticGenerator()
        energy_generator = NumericSongStatisticGenerator()
        rating_generator = NumericSongStatisticGenerator()

        for song in pool.get_leftover_songs():
            duration_generator.analyse(p_song=song, p_value=song.duration)
            energy_generator.analyse(p_song=song, p_value=song.energy)
            rating_generator.analyse(p_song=song, p_value=song.rating)
            key_count.add(song.key)
            genre_count.add(song.genre)
            genre_duration.add(song.genre, value=song.duration)

        self.result = SongPoolAnalysisResult(key_count=key_count,
                                             duration_stats=duration_generator.result,
                                             genre_count=genre_count,
                                             energy_stats=energy_generator.result,
                                             rating_stats=rating_generator.result,
                                             genre_duration=genre_duration)


class SongPoolAnalysisHtmlGenerator:
    _HTML_FILE = "/Users/kerem/Downloads/stats.html"
    analysis: SongPoolAnalysis
    _html: str

    def __init__(self, analysis: SongPoolAnalysis):
        self.analysis = analysis
        self._html = ""

    def generate(self):
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

    def _download_file(self):
        file2 = open(self._HTML_FILE, "w+")
        file2.write(self._html)
        file2.close()
        os.system("open " + self._HTML_FILE)

    def _put_numeric_song_statistic(self, stat: NumericSongStatistic, title: str):
        self._html += "<h1>" + title + "</h1><ul>"
        self._html += "<li>Max: " + stat.max_song.name + " (" + str(stat.max_value) + ")</li>"
        self._html += "<li>Min: " + stat.min_song.name + " (" + str(stat.min_value) + ")</li>"
        self._html += "<li>Avg: " + str(stat.get_average_value()) + "</li>"
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
                            energy="Energy")

        for song in self.analysis.pool.get_leftover_songs():
            self._put_song_line(name=song.name,
                                formatted_key=song.get_formatted_key(),
                                duration=str(song.duration),
                                bpm=str(song.bpm),
                                genre=song.genre,
                                rating=str(int(song.rating)),
                                energy=str(int(song.energy)))

        self._html += "</table><hr>"

    def _put_song_line(self,
                       name:str,
                       formatted_key:str,
                       duration:str,
                       bpm:str,
                       genre:str,
                       rating:str,
                       energy:str):
        song_html = "<tr>"
        song_html += "<td align=left valign=top>" + name + "</td>"
        song_html += "<td align=left valign=top>" + formatted_key + "</td>"
        song_html += "<td align=right valign=top>" + duration + "</td>"
        song_html += "<td align=right valign=top>" + bpm + "</td>"
        song_html += "<td align=left valign=top>" + genre + "</td>"
        song_html += "<td align=right valign=top>" + rating + "</td>"
        song_html += "<td align=right valign=top>" + energy + "</td>"
        song_html += "</tr>"

        self._html += song_html
