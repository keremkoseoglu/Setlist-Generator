from writer.abstract_writer import AbstractWriter
from gig import performance
from datetime import datetime, timedelta
import os
from config.constants import *


def _get_formatted_time(d: datetime) -> str:
    hour_txt = str(d.hour)
    while len(hour_txt) < 2:
        hour_txt = "0" + hour_txt

    minute_txt = str(d.minute)
    while len(minute_txt) < 2:
        minute_txt = "0" + minute_txt

    return hour_txt + ":" + minute_txt


class HtmlWriter(AbstractWriter):

    _html_file: str

    def __init__(self):
        self._html_file = os.path.join(DOWNLOAD_DIR, 'setlist.html')

    def write(self, generated_performance: performance.Performance):
        html = "<html><head>"
        html += "<style>"
        html += "td { font-family: Arial; font-size: 30px; padding: 5px; }"
        html += "tr:nth-child(even) { background: #CCC }"
        html += "tr:nth-child(odd) {background: #FFF }"
        html += "</style>"
        html += "</head><body>"

        for set in generated_performance.sets:
            time_bookmark = set.start

            if len(generated_performance.sets) > 1:
                html += "<h1>Set " + str(set.number) + "</h1>"

            html += "<table>"

            for flow_step in set.flow:
                for song in flow_step.songs:
                    html += "<tr>"
                    html += "<td>" + _get_formatted_time(time_bookmark) + "</td>"
                    html += "<td><strong>" + song.name + "</strong></td>"
                    html += "<td>" + song.get_formatted_key()
                    html += "</tr>"
                    time_bookmark = time_bookmark + timedelta(seconds=song.duration * 60)

            html += "<tr>"
            html += "<td>" + _get_formatted_time(time_bookmark) + "</td>"
            html += "<td>(END)</td>"
            html += "<td></td>"
            html += "</tr>"

            html += "</table>"

        leftover_songs = generated_performance.song_pool.get_leftover_songs()
        if len(leftover_songs) > 0:
            html += "<strong>Backup: </strong>"
            leftover_html = ""
            for leftover_song in leftover_songs:
                if len(leftover_html) > 0:
                    leftover_html += ", "
                leftover_html += leftover_song.name
            html += leftover_html
        if len(generated_performance.song_pool.inactive_songs) > 0:
            html += "<strong>Inactive: </strong>"
            inactive_html = ""
            for inactive_song in generated_performance.song_pool.inactive_songs:
                if len(inactive_html) > 0:
                    inactive_html += ", "
                inactive_html += inactive_song.name
            html += inactive_html

        html += "</body></html>"

        file2 = open(self._html_file, "w+")
        file2.write(html)
        file2.close()
        os.system("open " + self._html_file)

