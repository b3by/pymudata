import pathlib
import errno
import os

import pandas as pd


class Activity:
    """Activity class: high-level model of an activity CSV file

    This class provides a container for an activity file, that is, an
    individual file that is a record of an exercise execution. An activity
    object points to a file that is supposed to exist on the file system until
    its very acquisition.

    """

    def __init__(self, file_path: str,
                 exercise: str = None,
                 ground_deviations: list = None,
                 ground_coordinates: list = None,
                 lazy: bool = True):
        """Create a new activity, based on a csv file

        The activity object stores different pieces of information about the
        stored exercise, such as its deviation, the ground coordinates of the
        primitives, and the deviations of each one of them.

        Parameters
        ----------
        file_path : str
            The path of the file that contains the activity
        exercise : str
            The name of the exercise performed in the activity
        ground_deviations : list
            The list of deviations for each primitives
        ground_coordinates : list
            The list of cutting indices for the primitives

        """
        if not pathlib.Path(file_path).exists():
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), file_path)

        self._file_path = file_path
        self._dataframe = None

        if not lazy:
            self.acquire()

        if ground_coordinates is not None:
            self.ground_coordinates = ground_coordinates

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
