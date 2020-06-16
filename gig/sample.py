""" Module regarding pad sample sounds """
from os import path
import json
from config import Config


def get_samples_as_list() -> []:
    """ Returns sample file contents """
    config = Config()
    sample_file_path = path.join(config.sample_dir, config.sample_json)
    with open(sample_file_path, "r") as sample_file:
        sample_dict = json.load(sample_file)
    return sample_dict["samples"]
