from reader import json_reader
from generator import primal_generator
from writer import console_writer, html_writer
from gui.prime import Prime


_JOZI_JSON_FILE = "/Users/kerem/Dropbox/Software/Kerem/Development/setlist/data/jozi.json"
_TUSHE_JSON_FILE = "/Users/kerem/Dropbox/Software/Kerem/Development/setlist/data/tushe.json"
_PINYATA_JSON_FILE = "/Users/kerem/Dropbox/Software/Kerem/Development/setlist/data/pinyata.json"


def generate():
    performance = json_reader.JsonReader().read(param=_JOZI_JSON_FILE)
    primal_generator.PrimalGenerator().generate(performance)

    console_writer.ConsoleWriter().write(performance)
    html_writer.HtmlWriter().write(performance)


#generate()
Prime()

