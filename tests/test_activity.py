import unittest

import pandas as pd

import pymu


class TestActivity(unittest.TestCase):

    base_activity = './tests/activity.csv'

    def test_activity_created(self):
        act = pymu.Activity(self.base_activity)

        self.assertEqual(self.base_activity, act.file_path)

        self.assertIsNone(act.dataframe)
        self.assertIsNone(act.ground_coordinates)
        self.assertIsNone(act.ground_pairs)
        self.assertIsNone(act.primitive_deviations)
        self.assertIsNone(act.name)
        self.assertIsNone(act.subject)
        self.assertIsNone(act.pointwise_labels)

        with self.assertRaises(AttributeError):
            act.file_path = 'new'

    def test_activity_not_created(self):
        with self.assertRaises(FileNotFoundError):
            pymu.Activity('./nonexisting_file.csv')

    def test_activity_with_name(self):
        act = pymu.Activity(self.base_activity, name='exercise')

        self.assertEqual('exercise', act.name)

    def test_activity_with_subject(self):
        act = pymu.Activity(self.base_activity, subject=10)

        self.assertEqual(10, act.subject)

    def test_activity_created_not_lazy(self):
        act = pymu.Activity(self.base_activity, lazy=False)

        self.assertIsInstance(act.dataframe, pd.DataFrame)

    def test_acquire_dataset(self):
        act = pymu.Activity(self.base_activity)
        self.assertIsNone(act.dataframe)

        act.acquire()
        self.assertIsInstance(act.dataframe, pd.DataFrame)

    def test_activity_created_ground_coords(self):
        act = pymu.Activity(self.base_activity,
                            ground_coordinates=[10, 20, 40, 50])

        self.assertListEqual([10, 20, 40, 50], act.ground_coordinates)

    def test_activity_created_primitive_deviations(self):
        act = pymu.Activity(self.base_activity,
                            ground_coordinates=[1, 2, 1, 2])

        self.assertListEqual([1, 2, 1, 2], act.ground_coordinates)

    def test_activity_created_wrong_ground_coords(self):
        with self.assertRaises(Exception) as ex:
            pymu.Activity(self.base_activity, ground_coordinates=[10])

        self.assertIn('Coordinates are passed in odd number.',
                      str(ex.exception))

    def test_assign_coordinates(self):
        act = pymu.Activity(self.base_activity)
        self.assertIsNone(act.ground_coordinates)

        act.ground_coordinates = [1, 2, 3, 4]
        self.assertListEqual([1, 2, 3, 4], act.ground_coordinates)

        with self.assertRaises(Exception) as ex:
            act.ground_coordinates = [1, 2, 3]

        self.assertIn('Coordinates are passed in odd number.',
                      str(ex.exception))

    def test_ground_pairs(self):
        act = pymu.Activity(self.base_activity)

        self.assertIsNone(act.ground_coordinates)
        self.assertIsNone(act.ground_pairs)

        act.ground_coordinates = [10, 20, 40, 50]

        self.assertListEqual([(10, 20), (40, 50)], act.ground_pairs)

    def test_ground_pairs_from_constructor(self):
        act = pymu.Activity(self.base_activity,
                            ground_coordinates=[10, 20])

        self.assertListEqual([(10, 20)], act.ground_pairs)

    def test_primitive_deviations(self):
        act = pymu.Activity(self.base_activity)

        act.primitive_deviations = [1, 2, 1]

        self.assertListEqual([1, 2, 1], act.primitive_deviations)

        with self.assertRaises(Exception) as ex:
            act.ground_coordinates = [10, 20]

        self.assertIn('Count mismatch between primitives and deviations',
                      str(ex.exception))

    def test_coords_deviation(self):
        act = pymu.Activity(self.base_activity,
                            ground_coordinates=[10, 20, 40, 50],
                            primitive_deviations=[1, 2])

        self.assertListEqual([10, 20, 40, 50], act.ground_coordinates)
        self.assertListEqual([1, 2], act.primitive_deviations)
        self.assertListEqual([(10, 20), (40, 50)], act.ground_pairs)

    def test_coords_deviation_constructor_mismatches(self):
        with self.assertRaises(Exception) as ex:
            pymu.Activity(self.base_activity,
                          ground_coordinates=[10, 20, 40, 50],
                          primitive_deviations=[1, 2, 1])

        self.assertIn('Count mismatch between primitives and deviations',
                      str(ex.exception))

    def test_clear_annotations(self):
        act = pymu.Activity(self.base_activity,
                            ground_coordinates=[10, 20, 40, 50],
                            primitive_deviations=[1, 2])
        act.clear_annotations()

        self.assertIsNone(act.ground_coordinates)
        self.assertIsNone(act.ground_pairs)
        self.assertIsNone(act.primitive_deviations)

    def test_reassign_fields(self):
        act = pymu.Activity(self.base_activity,
                            ground_coordinates=[10, 20, 40, 50],
                            primitive_deviations=[1, 2])

        act.ground_coordinates = None

        self.assertIsNone(act.ground_coordinates)
        self.assertIsNone(act.ground_pairs)
        self.assertListEqual([1, 2], act.primitive_deviations)

        act.primitive_deviations = None

        self.assertIsNone(act.primitive_deviations)

    def test_pointwise_labels(self):
        act = pymu.Activity(self.base_activity, lazy=False)

        labels = [1] * 7972
        act.pointwise_labels = labels

        self.assertListEqual([1] * 7972, act.pointwise_labels)
