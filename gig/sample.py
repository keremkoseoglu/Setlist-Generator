""" Module regarding pad sample sounds """
from os import path
from typing import List
import json
from config import Config


def get_samples_as_list() -> List:
    """ Returns sample file contents """
    config = Config()
    sample_file_path = path.join(config.sample_dir, config.sample_json)
    with open(sample_file_path, "r", encoding="utf-8") as sample_file:
        sample_dict = json.load(sample_file)
    return sample_dict["samples"]
