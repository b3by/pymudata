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

    Attributes
    ----------
    file_path : str
        The file path of the CSV containing the activity. Does not change.
    dataframe : pandas.DataFrame
        The `pandas` representation of the activity. Does not change.

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

    def __init__(self, file_path: str,
                 exercise_name: str = None,
                 subject: int = None,
                 ground_coordinates: list = None,
                 primitive_deviations: list = None,
                 pointwise_labels: list = None,
                 lazy: bool = True):
        if not pathlib.Path(file_path).exists():
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), file_path)

        self._file_path = file_path
        self._dataframe = None
        self.exercise_name = exercise_name
        self.subject = subject

        if not lazy:
            self.acquire()

        self.ground_coordinates = ground_coordinates
        self.primitive_deviations = primitive_deviations
        self.pointwise_labels = pointwise_labels

    @property
    def file_path(self):
        return self._file_path

    @property
    def dataframe(self):
        return self._dataframe

    @property
    def ground_pairs(self):
        return self.__ground_pairs if self.__ground_coordinates else None

    @property
    def ground_coordinates(self):
        return self.__ground_coordinates

    @property
    def primitive_deviations(self):
        return self.__primitive_deviations

    @property
    def pointwise_labels(self):
        return self.__pointwise_labels

    @ground_coordinates.setter
    def ground_coordinates(self, ground_coordinates: list):
        if ground_coordinates:
            prs = list(zip(ground_coordinates[::2], ground_coordinates[1::2]))

            if len(ground_coordinates) % 2 != 0:
                raise Exception(f'Odd coordinates on {self.file_path}')

            if hasattr(self, '_Activity__primitive_deviations') and \
               self.primitive_deviations and \
               len(prs) != len(self.primitive_deviations):
                raise Exception(
                    'Count mismatch between primitives and deviations')

        self.__ground_coordinates = ground_coordinates

        if ground_coordinates:
            self.__ground_pairs = list(zip(self.__ground_coordinates[::2],
                                           self.__ground_coordinates[1::2]))

    @primitive_deviations.setter
    def primitive_deviations(self, primitive_deviations: list):
        if primitive_deviations and hasattr(
                self, '_Activity__ground_pairs') and self.ground_pairs and len(
                    primitive_deviations) != len(self.__ground_pairs):
            raise Exception('Count mismatch between primitives and deviations')

        self.__primitive_deviations = primitive_deviations

    @pointwise_labels.setter
    def pointwise_labels(self, pointwise_labels):
        if self._dataframe is None:
            self.__pointwise_labels = pointwise_labels
        elif pointwise_labels:
            if self._dataframe.shape[0] != len(pointwise_labels):
                msg = ('Count mismatch between points and labels '
                       '({} data points, {} labels passed)')
                raise Exception(msg.format(self._dataframe.shape[0],
                                           len(pointwise_labels)))
            else:
                self.__pointwise_labels = pointwise_labels
        else:
            self.__pointwise_labels = None

    def clear_annotations(self):
        """Clear coordinates, pairs, deviations and labels

        This method can be used to wipe out all the annotations related to the
        series in the activity. It will reset ground coordinates, coordinate
        pairs, primitive deviations and pointwise labels.
        """
        self.__ground_coordinates = None
        self.__ground_pairs = None
        self.__primitive_deviations = None
        self.__pointwise_labels = None

    def acquire(self):
        """Read in the data file

        This method will read in the data file corresponding to this activity.
        The user will be warned in case the data file is already acquired
        (either the Activity was created with laxy=False, or acquire was
        already called).

        """
        if self._dataframe is not None:
            print(f'Data file already acquired for {self.file_path}')
        else:
            self._dataframe = pd.read_csv(self.file_path)

    def stream(self, window: int, stride: int):
        """Get a generator of sliding windows over the activity

        This method returns a generator of sliding windows for the activity,
        given a window size and a stride value (whatever is left from the
        overlap).

        Parameters
        ----------
        window : int
            The size of the window to use during the slicing operation
        stride : int
            The value of stride betweeb consecutive windows

        """
        if self.dataframe is None:
            raise Exception('Dataframe not loaded. Please run acquire()')

        c_win = 0

        while c_win + window <= self.dataframe.shape[0]:
            if self.pointwise_labels is not None:
                lbs = self.__pointwise_labels[c_win:c_win + window]
            else:
                lbs = None

            yield self.dataframe.iloc[c_win:c_win + window], lbs
            c_win += stride
