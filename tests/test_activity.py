import unittest

import pandas as pd

import pymu


class TestActivity(unittest.TestCase):

    def test_activity_created(self):
        act = pymu.Activity('./tests/activity.csv')

        self.assertEqual('./tests/activity.csv', act.file_path)
        self.assertIsNone(act.dataframe)

        # file path for the activity should not be changed
        with self.assertRaises(AttributeError):
            act.file_path = 'new'

    def test_activity_not_created(self):
        with self.assertRaises(FileNotFoundError):
            pymu.Activity('./nonexisting_file.csv')

    def test_activity_created_not_lazy(self):
        act = pymu.Activity('./tests/activity.csv', lazy=False)

        self.assertIsInstance(act.dataframe, pd.DataFrame)

    def test_activity_created_ground_coords(self):
        pass
