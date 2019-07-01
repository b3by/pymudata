from pathlib import Path

from .activity import Activity


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

    def __init__(self, data_location: str,
                 coordinate_file: str = None,
                 deviation_file: str = None):
        self.__data_location = data_location
        self.__exercises = (x for x in Path(self.__data_location).glob('*/')
                            if x.is_dir())

    @property
    def data_location(self):
        return self.__data_location

    @property
    def exercises(self):
        return sorted([x.name for x in self.__exercises])

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
        return sum(list(l for l in self.__activities.values()), [])
