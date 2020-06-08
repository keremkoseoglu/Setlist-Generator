""" File system module """
import os
from config.constants import DATA_FILE_EXTENSION


def get_desktop_path():
    """ Returns desktop path """
    return os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


def get_desktop_file_name(file_name: str, extension: str) -> str:
    """ Builds desktop file name """
    output = os.path.join(get_desktop_path(), file_name + "." + extension)
    return output


def get_files_in_dir(dir_name: str) -> []:
    """ Returns all files in the given dir """
    output = []

    for current_item in os.listdir(dir_name):
        current_path = os.path.join(dir_name, current_item)
        try:
            if os.path.isfile(current_path) and DATA_FILE_EXTENSION in current_item:
                output.append(current_item)
        except Exception as path_error:
            print(path_error)

    output.sort()
    return output
