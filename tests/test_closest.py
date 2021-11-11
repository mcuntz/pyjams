#!/usr/bin/env python
"""
This is the unittest for closest module.

python -m unittest -v tests/test_closest.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_closest.py

"""
from __future__ import division, absolute_import, print_function
import unittest


class TestClosest(unittest.TestCase):
    """
    Tests for closest.py
    """

    def test_closest(self):
        import numpy as np
        from pyjams import closest

        nn = 51

        # 1D
        arr = np.arange(nn)/float(nn-1) * 5.
        self.assertEqual(closest(arr, 3.125), 31)
        self.assertEqual(closest(arr, 3.125, value=True), 3.1)

        # 2D
        arr = np.arange(nn).reshape((17, 3))/float(nn-1) * 5.
        self.assertEqual(closest(arr, 3.125), 31)
        ii = np.unravel_index(closest(arr, 3.125), arr.shape)
        self.assertEqual(ii, (10, 1))
        self.assertEqual(arr[ii], 3.1)


if __name__ == "__main__":
    unittest.main()
