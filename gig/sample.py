""" Module regarding pad sample sounds """
from os import path
import json
from config.constants import SAMPLE_DIR, SAMPLE_JSON


def get_samples_as_list() -> []:
    """ Returns sample file contents """
    sample_file_path = path.join(SAMPLE_DIR, SAMPLE_JSON)
    with open(sample_file_path, "r") as sample_file:
        sample_dict = json.load(sample_file)
    return sample_dict["samples"]
