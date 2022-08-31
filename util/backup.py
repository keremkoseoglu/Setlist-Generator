""" Backup module """
from config import Config
from datetime import datetime
from os import path, mkdir, scandir
from shutil import copytree, rmtree

class Backup:
    """ Backup class """
    _MAX_BACKUP_COUNT = 30

    def __init__(self) -> None:
        self._config = Config()

    def execute(self):
        """ Execute backup """
        self._clean_old_backups()
        self._create_new_backup()

    def _create_new_backup(self):
        """ Create new backup """
        bak_dir = self._config.backup_dir
        bak_folder = f"{datetime.now()}"
        bak_path = path.join(bak_dir, bak_folder)
        mkdir(bak_path)

        data_dirs = [ f.path for f in scandir(self._config.data_dir) if f.is_dir() ]

        for data_dir in data_dirs:
            if data_dir == bak_dir:
                continue
            dir_name = path.basename(data_dir)
            target_path = path.join(bak_path, dir_name)
            mkdir(target_path)
            copytree(data_dir, target_path, dirs_exist_ok=True)

    def _clean_old_backups(self):
        """ Clean old backups """
        base_bak_dir = self._config.backup_dir
        bak_dirs = [ f.path for f in scandir(base_bak_dir) if f.is_dir() ]
        bak_dirs.sort()

        while len(bak_dirs) > Backup._MAX_BACKUP_COUNT:
            bak_dir = bak_dirs.pop(0)
            rmtree(bak_dir)
