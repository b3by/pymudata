import pathlib
import errno
import os

import pandas as pd


class Activity:

    def __init__(self, file_path, lazy=True):
        if not pathlib.Path(file_path).exists():
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), file_path)

        self._file_path = file_path
        self._dataframe = None

        if not lazy:
            self.acquire()

    @property
    def file_path(self):
        return self._file_path

    @property
    def dataframe(self):
        return self._dataframe

    def acquire(self):
        if self._dataframe is not None:
            print(f'Data file already acquired for {self.file_path}')
        else:
            self._dataframe = pd.read_csv(self.file_path)
