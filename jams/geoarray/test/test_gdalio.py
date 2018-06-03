#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import tempfile
import geoarray as ga
import numpy as np
from test_utils import testArray, dtypeInfo

class Test(unittest.TestCase):

    def test_io(self):
        test_array = testArray((340, 270))
        endings = ga._DRIVER_DICT.keys()
        for ending in endings:
            with tempfile.NamedTemporaryFile(suffix=ending) as tf:
                # write and read again
                test_array.tofile(tf.name)
                check_array = ga.fromfile(tf.name)
                # gdal truncates values smaller/larger than the datatype, numpy wraps around.
                # clip array to make things comparable.
                dinfo = dtypeInfo(check_array.dtype)
                grid = test_array.clip(dinfo["min"], dinfo["max"])

                np.testing.assert_almost_equal(check_array, grid)
                self.assertDictEqual(check_array.bbox, test_array.bbox)
                self.assertEqual(check_array.cellsize, test_array.cellsize)
                self.assertEqual(check_array.proj, test_array.proj)
                self.assertEqual(check_array.fill_value, test_array.fill_value)
                self.assertEqual(check_array.mode, test_array.mode)
