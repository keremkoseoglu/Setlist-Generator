""" Primary HTML GUI """
import json
from flask import Flask, jsonify, request # pylint: disable=E0401
import webview # pylint: disable=E0401
from gui.html.path_helper import PathHelper

_PATH = PathHelper()
_FLASK_APP = Flask(__name__, static_folder=_PATH.static_folder)
_MAIN_WINDOW = webview.create_window("Setlist Builder", _FLASK_APP, height=800)

@_FLASK_APP.route("/")
def index():
    """ Home page """
    return _FLASK_APP.send_static_file("index.html")

@_FLASK_APP.route("/api/band_list")
def api_band_list():
    """ Band list """
    return jsonify(_PATH.reader.band_list)

@_FLASK_APP.route("/api/edit_band")
def api_edit_band():
    """ Band edit """
    _PATH.edit_band_file(request.args.get("json_file"))
    return ""

@_FLASK_APP.route("/api/event_list")
def api_event_list():
    """ Event list """
    return jsonify(_PATH.reader.event_list)

@_FLASK_APP.route("/api/edit_event")
def api_edit_event():
    """ Event edit """
    _PATH.edit_event_file(request.args.get("json_file"))
    return ""

@_FLASK_APP.route("/api/get_selection_variant")
def api_get_selection_variant():
    """ Get selection variant """
    band_file = request.args.get("band_json_file")
    event_file = request.args.get("event_json_file")
    entries = _PATH.get_selection_variant_entries(band_file, event_file)
    return jsonify(entries)

@_FLASK_APP.route("/api/generate", methods=["POST"])
def api_generate():
    """ Generate """
    band_file = request.form["band_json_file"]
    event_file = request.form["event_json_file"]
    sel_var = json.loads(request.form["selection_variant"])
    _PATH.generate_setlist(band_file, event_file, sel_var)
    return ""

@_FLASK_APP.route("/api/get_performance_set_list")
def api_get_performance_set_list():
    """ Set list """
    return jsonify(_PATH.get_performance_set_list())

@_FLASK_APP.route("/api/save", methods=["POST"])
def api_save():
    """ Save """
    song_order = json.loads(request.form["song_order"])
    _PATH.save(song_order)
    return ""

@_FLASK_APP.route("/api/stats")
def api_stats():
    """ Event edit """
    _PATH.generate_stats(request.args.get("json_file"))
    return ""

@_FLASK_APP.route("/api/history_list")
def history_list():
    """ History entries """
    return jsonify(_PATH.history_reader.get_file_list())

@_FLASK_APP.route("/api/history_select")
def history_select():
    """ Returns selected file from history """
    _PATH.load_history_file(request.args["file"])
    return ""

@_FLASK_APP.route("/api/history_delete")
def history_delete():
    """ Deletes given file """
    _PATH.history_writer.delete(request.args["file"])
    return ""

def start_gui():
    """ Start GUI """
    webview.start()
    #_FLASK_APP.run(host="0.0.0.0", port=5001, debug=True)
