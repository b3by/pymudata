import unittest
import sys

from io import StringIO
from contextlib import contextmanager

import pandas as pd

import pymu


@contextmanager
def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out


class TestActivity(unittest.TestCase):

    base_activity = './tests/activity.csv'

    def test_activity_created(self):
        act = pymu.Activity(self.base_activity)

        self.assertEqual(self.base_activity, act.file_path)

        self.assertIsNone(act.dataframe)
        self.assertIsNone(act.ground_coordinates)
        self.assertIsNone(act.ground_pairs)
        self.assertIsNone(act.primitive_deviations)
        self.assertIsNone(act.exercise_name)
        self.assertIsNone(act.subject)
        self.assertIsNone(act.pointwise_labels)

        with self.assertRaises(AttributeError):
            act.file_path = 'new'

    def test_activity_not_created(self):
        with self.assertRaises(FileNotFoundError):
            pymu.Activity('./nonexisting_file.csv')

    def test_activity_with_name(self):
        act = pymu.Activity(self.base_activity, exercise_name='exercise')

        self.assertEqual('exercise', act.exercise_name)

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

    def test_double_acquire(self):
        act = pymu.Activity(self.base_activity)
        act.acquire()

        with capture(act.acquire) as output:
            msg = 'Data file already acquired for ./tests/activity.csv\n'
            self.assertEqual(msg, output)

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

        self.assertIn('Odd coordinates on ./tests/activity.csv',
                      str(ex.exception))

    def test_assign_coordinates(self):
        act = pymu.Activity(self.base_activity)
        self.assertIsNone(act.ground_coordinates)

        act.ground_coordinates = [1, 2, 3, 4]
        self.assertListEqual([1, 2, 3, 4], act.ground_coordinates)

        with self.assertRaises(Exception) as ex:
            act.ground_coordinates = [1, 2, 3]

        self.assertIn('Odd coordinates on ./tests/activity.csv',
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
                            primitive_deviations=[1, 2],
                            pointwise_labels=[1] * 7972)

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

    def test_pointwise_labels_mismatch(self):
        act = pymu.Activity(self.base_activity, lazy=False)
        labels = [1] * 555

        with self.assertRaises(Exception) as ex:
            act.pointwise_labels = labels

        self.assertIn('Count mismatch between points and labels',
                      str(ex.exception))

    def test_stream_unloaded_dataframe(self):
        act = pymu.Activity(self.base_activity)
        stream = act.stream(10, 1)

        with self.assertRaises(Exception) as ex:
            next(stream)

        self.assertIn('Dataframe not loaded.', str(ex.exception))

    def test_stream_loaded_dataframe(self):
        act = pymu.Activity(self.base_activity, lazy=False)

        stream = act.stream(10, 1)

        for win, lbs in stream:
            self.assertEqual(10, win.shape[0])
            self.assertEqual(7, win.shape[1])
            self.assertIsNone(lbs)

    def test_stream_dataframe_with_labels(self):
        act = pymu.Activity(self.base_activity,
                            pointwise_labels=[1] * 7972,
                            lazy=False)

        stream = act.stream(30, 5)

        for _, lbs in stream:
            self.assertListEqual([1] * 30, lbs)

    def test_stream_single_points(self):
        act = pymu.Activity(self.base_activity,
                            pointwise_labels=[1] * 7972,
                            lazy=False)

        stream = act.stream(1, 1)

        for p, l in stream:
            self.assertEqual(1, p.shape[0])
            self.assertListEqual([1], l)

        self.assertEqual(7972, len(list(act.stream(1, 1))))
