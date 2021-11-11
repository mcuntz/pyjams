#!/usr/bin/env python
"""
This is the unittest for division module.

python -m unittest -v tests/test_division.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_division.py

"""
from __future__ import division, absolute_import, print_function
import unittest


class TestDivision(unittest.TestCase):
    """
    Tests for division.py
    """

    def test_division(self):
        import numpy as np
        from pyjams import division

        a = (1., 2., 3.)
        b = 2.
        assert isinstance(division(a, b), tuple)
        self.assertEqual(list(division(a, b)),
                         [0.5, 1.0, 1.5])

        a = [1., 2., 3.]
        b = 2.
        assert isinstance(division(a, b), list)
        self.assertEqual(list(division(a, b)),
                         [0.5, 1.0, 1.5])

        a = [1., 1., 1.]
        b = [2., 1., 0.]
        dd = division(a, b)
        assert isinstance(dd, list)
        self.assertEqual(list(dd[0:2]), [0.5, 1.0])
        assert np.isnan(dd[2])
        self.assertEqual(list(division(a, b, 0.)),
                         [0.5, 1.0, 0.0])
        self.assertEqual(list(division(a, b, otherwise=0.)),
                         [0.5, 1.0, 0.0])
        dd = division(a, b, prec=1.)
        self.assertEqual(dd[0], 0.5)
        assert np.isnan(dd[1])
        assert np.isnan(dd[2])

        a = np.array([1., 1., 1.])
        b = [2., 1., 0.]
        dd = division(a, b)
        assert isinstance(dd, np.ndarray)
        self.assertEqual(list(dd[0:2]), [0.5, 1.0])
        assert np.isnan(dd[2])

        a = np.array([1., 1., 1.])
        b = np.array([2., 1., 0.])
        assert isinstance(dd, np.ndarray)
        self.assertEqual(list(dd[0:2]), [0.5, 1.0])
        assert np.isnan(dd[2])

        a = np.array([1., 1., 1.])
        mask = [0, 0, 1]
        b = np.ma.array([2., 1., 0.], mask=mask)
        dd = division(a, b)
        assert isinstance(dd, np.ma.masked_array)
        self.assertEqual(list(dd), [0.5, 1.0, np.ma.masked])

    def test_div(self):
        import numpy as np
        from pyjams import div

        a = (1., 2., 3.)
        b = 2.
        assert isinstance(div(a, b), tuple)
        self.assertEqual(list(div(a, b)),
                         [0.5, 1.0, 1.5])

        a = [1., 2., 3.]
        b = 2.
        assert isinstance(div(a, b), list)
        self.assertEqual(list(div(a, b)),
                         [0.5, 1.0, 1.5])

        a = [1., 1., 1.]
        b = [2., 1., 0.]
        dd = div(a, b)
        assert isinstance(dd, list)
        self.assertEqual(list(dd[0:2]), [0.5, 1.0])
        assert np.isnan(dd[2])
        self.assertEqual(list(div(a, b, 0.)),
                         [0.5, 1.0, 0.0])
        self.assertEqual(list(div(a, b, otherwise=0.)),
                         [0.5, 1.0, 0.0])
        dd = div(a, b, prec=1.)
        self.assertEqual(dd[0], 0.5)
        assert np.isnan(dd[1])
        assert np.isnan(dd[2])

        a = np.array([1., 1., 1.])
        b = [2., 1., 0.]
        dd = div(a, b)
        assert isinstance(dd, np.ndarray)
        self.assertEqual(list(dd[0:2]), [0.5, 1.0])
        assert np.isnan(dd[2])

        a = np.array([1., 1., 1.])
        b = np.array([2., 1., 0.])
        assert isinstance(dd, np.ndarray)
        self.assertEqual(list(dd[0:2]), [0.5, 1.0])
        assert np.isnan(dd[2])

        a = np.array([1., 1., 1.])
        mask = [0, 0, 1]
        b = np.ma.array([2., 1., 0.], mask=mask)
        dd = div(a, b)
        assert isinstance(dd, np.ma.masked_array)
        self.assertEqual(list(dd), [0.5, 1.0, np.ma.masked])


if __name__ == "__main__":
    unittest.main()
