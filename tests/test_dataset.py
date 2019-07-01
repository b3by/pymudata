import unittest

import pymu


class TestActivity(unittest.TestCase):

    base_dataset = './tests/test_ds'

    def test_dataset_created(self):
        ds = pymu.Dataset(self.base_dataset)

        self.assertEqual(self.base_dataset, ds.data_location)
        self.assertListEqual(['emptyone', 'flexstand', 'hs'], ds.exercises)

    def test_synth_dataset(self):
        ds = pymu.Dataset(self.base_dataset)
        ds.synth()

        self.assertEqual(4, len(ds.all_activities()))

        for act in ds.all_activities():
            self.assertIsInstance(act, pymu.Activity)

        self.assertEqual('flexstand', ds.all_activities()[0].exercise_name)
        self.assertEqual('flexstand', ds.all_activities()[1].exercise_name)
        self.assertEqual('hs', ds.all_activities()[2].exercise_name)
        self.assertEqual('hs', ds.all_activities()[3].exercise_name)
