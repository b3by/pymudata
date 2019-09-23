import ast

from pathlib import Path
from typing import Union

import pandas as pd

from .activity import Activity


Mask = Union[str, list]


class Dataset:
    """Dataset: smart collector of activities, grouped by exercise

    This class can be used to store a collection of exercises. A dataset should
    be created starting from the root folder of a data collection, under the
    assumption that exercises are stored into separate folders, and that all
    other files within the root folder of the dataset will be ignored. So, if
    the folder has this content:

    root /
        exercise1/
            act1.csv
            act2.csv
        exercise2/
            act1.csv
            act2.csv
        othercontent.csv

    the dataset will be created with 2 exercises only (exercise1 and exercise1)
    and the file othercontent.csv will be ignored.

    """

    def __init__(self, data_location: str):
        self.__data_location = data_location
        self.__exercises = [x for x in Path(self.__data_location).glob('*/')
                            if x.is_dir()]
        self.__masked = None

    @property
    def data_location(self):
        return self.__data_location

    @property
    def exercises(self):
        if self.__masked is None:
            return sorted([x.name for x in self.__exercises])
        else:
            return sorted([x.name for x in self.__exercises
                           if x.name in self.__masked])
    
    def synth(self):
        """Acquire activities and store them

        This method reads all the csv files in the dataset location, and then
        creates the cooresponding activities. It returns a list of activity
        objects.

        Parameters
        ----------
        """
        self.__activities = {}

        for exercise in self.__exercises:
            ff = Path(exercise).glob('*.csv')
            ex = exercise.name
            self.__activities[ex] = []

            for f in ff:
                self.__activities[ex].append(Activity(f, exercise_name=ex))

    def all_activities(self):
        """Get all activities in dataset

        This method returns a flat list of all the activities in the dataset.
        The state of the activities will not be modified.

        """
        if self.__masked is not None:
            return sum(list(l for e, l in self.__activities.items()
                            if e in self.__masked), [])
        else:
            return sum(list(l for e, l in self.__activities.items()), [])

    def mask_for_exercise(self, mask: Mask):
        """Apply a mask to the dataset to only retrieve one exercise

        When an entire dataset is loaded, a mask can be applied to is to that
        only the activities for a particular exercise will be aggregated.

        Parameters
        ----------
        mask : Mask
            The name of the exercise, or list of exercises, to filter in during
            masking

        """
        self.__masked = mask

    def unmask(self, mask: Mask = None):
        """Unmask a previouslty masked dataset

        This method will void a mask previously applied to the dataset. If no
        mask is passed to the unmask method, any mask currently in place will
        be wiped out. If a string mask is passed, it will be subtracted from
        the existing mask if present.

        Parameters
        ----------
        mask : Mask
            The name of the exercise, or list of exercises, to remove from the
            existing mask
        """
        if mask is None:
            self.__masked = None
        elif isinstance(mask, str) and self.__masked == mask:
            self.__masked = None
        elif isinstance(mask, list):
            self.__masked = list(set(self.__masked) - set(mask))

    def annotate(self, coordinate_file, deviation_file, label_file):
        coordinates = pd.read_csv(coordinate_file)

        for row in coordinates.iterrows():
            r = row[1]
            filename = r['filename']
            crds = ast.literal_eval(r['coordinates'])
            match = [x for x in self.all_activities()
                     if x.file_path.name == filename]

            for m in match:
                m.ground_coordinates = crds
