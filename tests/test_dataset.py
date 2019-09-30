import unittest

import pymudata


class TestActivity(unittest.TestCase):

    base_dataset = './tests/test_ds'
    test_coordinates = './tests/test_ds/test_coordinates.csv'

    def test_dataset_created(self):
        ds = pymudata.Dataset(self.base_dataset)

        self.assertEqual(self.base_dataset, ds.data_location)
        self.assertListEqual(['emptyone', 'flexstand', 'hs'], ds.exercises)

    def test_synth_dataset(self):
        ds = pymudata.Dataset(self.base_dataset)
        ds.synth()

        self.assertEqual(4, len(ds.all_activities()))

        for act in ds.all_activities():
            self.assertIsInstance(act, pymudata.Activity)

        self.assertEqual('flexstand', ds.all_activities()[0].exercise_name)
        self.assertEqual('flexstand', ds.all_activities()[1].exercise_name)
        self.assertEqual('hs', ds.all_activities()[2].exercise_name)
        self.assertEqual('hs', ds.all_activities()[3].exercise_name)

    def test_mask_dataset(self):
        ds = pymudata.Dataset(self.base_dataset)
        ds.synth()

        ds.mask_for_exercise('hs')

        self.assertListEqual(['hs'], ds.exercises)

        self.assertIsInstance(ds.all_activities()[0], pymudata.Activity)
        self.assertIsInstance(ds.all_activities()[1], pymudata.Activity)

        self.assertEqual(ds.all_activities()[0].exercise_name, 'hs')
        self.assertEqual(ds.all_activities()[1].exercise_name, 'hs')

    def test_mask_dataset_multiple(self):
        ds = pymudata.Dataset(self.base_dataset)
        ds.synth()
        ds.mask_for_exercise(['hs', 'flexstand'])

        self.assertEqual(len(ds.all_activities()), 4)

        self.assertIsInstance(ds.all_activities()[0], pymudata.Activity)
        self.assertIsInstance(ds.all_activities()[1], pymudata.Activity)

        self.assertEqual(ds.all_activities()[0].exercise_name, 'flexstand')
        self.assertEqual(ds.all_activities()[1].exercise_name, 'flexstand')
        self.assertEqual(ds.all_activities()[2].exercise_name, 'hs')
        self.assertEqual(ds.all_activities()[3].exercise_name, 'hs')

    def test_mask_dataset_wrong_mask(self):
        ds = pymudata.Dataset(self.base_dataset)
        ds.synth()
        ds.mask_for_exercise(['hs', 'yolo'])

        self.assertListEqual(['hs'], ds.exercises)

        self.assertIsInstance(ds.all_activities()[0], pymudata.Activity)
        self.assertIsInstance(ds.all_activities()[1], pymudata.Activity)

        self.assertEqual(ds.all_activities()[0].exercise_name, 'hs')
        self.assertEqual(ds.all_activities()[1].exercise_name, 'hs')

    def test_unmask_dataset(self):
        ds = pymudata.Dataset(self.base_dataset)
        ds.synth()

        ds.mask_for_exercise('hs')
        ds.unmask()

        self.assertListEqual(['emptyone', 'flexstand', 'hs'], ds.exercises)

    def test_annotate_dataset(self):
        ds = pymudata.Dataset(self.base_dataset)
        ds.synth()

        ds.annotate(self.test_coordinates, None, None)

        self.assertListEqual(ds.all_activities()[1].ground_coordinates,
                             [379, 740, 821, 1218, 1289, 1604, 1699, 1989,
                              2069, 2402, 2463, 2758, 2850, 3160, 3254, 3541,
                              3644, 3924, 3993, 4272])
        
