import unittest

import pandas as pd

import pymudata


class TestUtils(unittest.TestCase):
    pass

    def test_activity_created_from_file(self):
        act = pymudata.from_file('./tests/activity.csv')
        self.assertEqual('./tests/activity.csv', act.file_path)
        self.assertIsNone(act.dataframe)

    def test_activity_created_from_file_not_lazy(self):
        act = pymudata.from_file('./tests/activity.csv', lazy=False)
        self.assertIsInstance(act.dataframe, pd.DataFrame)
