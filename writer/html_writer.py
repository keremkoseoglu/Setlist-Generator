from writer.abstract_writer import AbstractWriter
from gig import performance
from gig.song import Song
from datetime import datetime, timedelta
import os
from config.constants import *
from typing import List


def _get_formatted_time(d: datetime) -> str:
    hour_txt = str(d.hour)
    while len(hour_txt) < 2:
        hour_txt = "0" + hour_txt

    minute_txt = str(d.minute)
    while len(minute_txt) < 2:
        minute_txt = "0" + minute_txt

    return hour_txt + ":" + minute_txt


class HtmlWriter(AbstractWriter):

    def __init__(self):
        self._html_file = os.path.join(DOWNLOAD_DIR, 'setlist.html')
        self.html = ""

    def write(self, generated_performance: performance.Performance):
        self.html = "<html><head>"
        self.html += "<style>"
        self.html += "td { font-family: Arial; font-size: 30px; padding: 5px; }"
        self.html += "tr:nth-child(even) { background: #CCC }"
        self.html += "tr:nth-child(odd) {background: #FFF }"
        self.html += "</style>"
        self.html += "</head><body>"

        for set in generated_performance.event.sets:
            time_bookmark = set.start

            if len(generated_performance.event.sets) > 1:
                self.html += "<h1>Set " + str(set.number) + "</h1>"

            self.html += "<table>"

            for flow_step in set.flow:
                for song in flow_step.songs:
                    self.html += "<tr>"
                    self.html += "<td>" + _get_formatted_time(time_bookmark) + "</td>"
                    self.html += "<td><strong>" + song.name + "</strong></td>"
                    self.html += "<td>" + song.get_formatted_key()
                    self.html += "</tr>"
                    time_bookmark = time_bookmark + timedelta(seconds=song.duration * 60)

            self.html += "<tr>"
            self.html += "<td>" + _get_formatted_time(time_bookmark) + "</td>"
            self.html += "<td>(END)</td>"
            self.html += "<td></td>"
            self.html += "</tr>"

            self.html += "</table>"

        self._append_excluded_songs("Backup",
                                    generated_performance.song_pool.get_leftover_songs())
        self._append_excluded_songs("Inactive",
                                    generated_performance.song_pool.obsolete_songs.inactive)
        self._append_excluded_songs("Filtered by genre",
                                    generated_performance.song_pool.obsolete_songs.filtered_by_genre)
        self._append_excluded_songs("Filtered by language",
                                    generated_performance.song_pool.obsolete_songs.filtered_by_language)
        self._append_excluded_songs("Filtered for event",
                                    generated_performance.song_pool.obsolete_songs.filtered_for_event)

        self.html += "</body></html>"

        file2 = open(self._html_file, "w+")
        file2.write(self.html)
        file2.close()
        os.system("open " + self._html_file)

    def _append_excluded_songs(self, title: str, songs: List[Song]):
        if len(songs) <= 0:
            return
        self.html += "<br><br><strong>" + title + ": </strong><br>"
        leftover_html = ""
        leftover_count = 0
        for leftover_song in songs:
            leftover_count += 1
            if len(leftover_html) > 0:
                leftover_html += ", "
            if leftover_count % 4 == 0:
                leftover_html += "<br>"
            leftover_html += leftover_song.name
        self.html += leftover_html

