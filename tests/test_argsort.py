#!/usr/bin/env python
"""
This is the unittest for argsort module.

python -m unittest -v tests/test_argsort.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_argsort.py

"""
from __future__ import division, absolute_import, print_function
import unittest


class TestArgsort(unittest.TestCase):
    """
    Tests for argsort.py
    """

    def test_argmax(self):
        import numpy as np
        from pyjams import argmax

        # one-dimensional array
        a = np.array([0, 4, 6, 2, 1, 5, 3, 5])
        self.assertEqual(argmax(a), 2)
        self.assertEqual(a[argmax(a)], 6)

        # one-dimensional masked array
        a = np.ma.array([0, 4, 6, 2, 1, 5, 3, 5],
                        mask=[0, 0, 1, 1, 0, 0, 0, 0])
        self.assertEqual(argmax(a), 5)
        self.assertEqual(a[argmax(a)], 5)
        self.assertEqual(argmax(a, fill_value=6), 2)

        # list
        a = [0, 4, 6, 2, 1, 5, 3, 5]
        self.assertEqual(argmax(a), 2)
        self.assertEqual(a[argmax(a)], 6)

        # from numpy.argmax docstring
        a = np.arange(6).reshape(2, 3) + 10
        self.assertEqual(argmax(a), 5)
        self.assertEqual(list(argmax(a, axis=0)), [1, 1, 1])
        self.assertEqual(list(argmax(a, axis=1)), [2, 2])

        # indexes of the maximal elements of a n-dimensional array
        ind = np.unravel_index(argmax(a, axis=None), a.shape)
        self.assertEqual(list(ind), [1, 2])
        self.assertEqual(a[ind], 15)

        # Only the first occurrence is returned.
        b = np.arange(6)
        b[1] = 5
        self.assertEqual(argmax(b), 1)

    def test_argmin(self):
        import numpy as np
        from pyjams import argmin

        # one-dimensional array
        a = np.array([0, 4, 6, 2, 1, 5, 3, 5])
        self.assertEqual(argmin(a), 0)
        self.assertEqual(a[argmin(a)], 0)

        # one-dimensional masked array
        a = np.ma.array([0, 4, 6, 2, 1, 5, 3, 5],
                        mask=[1, 0, 1, 1, 0, 0, 0, 0])
        self.assertEqual(argmin(a), 4)
        self.assertEqual(a[argmin(a)], 1)
        self.assertEqual(argmin(a, fill_value=1), 0)

        # list
        a = [0, 4, 6, 2, 1, 5, 3, 5]
        self.assertEqual(argmin(a), 0)
        self.assertEqual(a[argmin(a)], 0)

        # from numpy.argmin docstring
        a = np.arange(6).reshape(2, 3) + 10
        self.assertEqual(argmin(a), 0)
        self.assertEqual(list(argmin(a, axis=0)), [0, 0, 0])
        self.assertEqual(list(argmin(a, axis=1)), [0, 0])

        # indexes of the maximal elements of a n-dimensional array
        ind = np.unravel_index(argmin(a, axis=None), a.shape)
        self.assertEqual(list(ind), [0, 0])
        self.assertEqual(a[ind], 10)

        # Only the first occurrence is returned.
        b = np.arange(6) + 10
        b[4] = 10
        self.assertEqual(argmin(b), 0)

    def test_argsort(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import argsort

        # 1D array
        a = np.array([0, 4, 6, 2, 1, 5, 3, 5])
        self.assertEqual(list(a[argsort(a)]), [0, 1, 2, 3, 4, 5, 5, 6])

        # sort algorithm
        self.assertEqual(list(a[argsort(a, kind='quicksort')]),
                         [0, 1, 2, 3, 4, 5, 5, 6])

        # 1D masked array
        a = np.ma.array([0, 4, 6, 2, 1, 5, 3, 5],
                        mask=[0, 0, 1, 1, 0, 0, 0, 0])
        self.assertEqual(list(a[argsort(a)]),
                         [0, 1, 3, 4, 5, 5, masked, masked])
        self.assertEqual(list(a[argsort(a, fill_value=1)]),
                         [0, masked, masked, 1, 3, 4, 5, 5])

        # list
        a = [0, 4, 6, 2, 1, 5, 3, 5]
        ii = argsort(a)
        b = [ a[i] for i in ii ]
        self.assertEqual(b, [0, 1, 2, 3, 4, 5, 5, 6])
        self.assertRaises(KeyError, argsort, a, key=a)

        a = [0,4,6,2,1,5,3,5]
        ii = argsort(a, reverse=True)
        b = [ a[i] for i in ii ]
        self.assertEqual(b, [6, 5, 5, 4, 3, 2, 1, 0])

        # from numpy.argsort docstring
        # one-dimensional array
        x = np.array([3, 1, 2])
        self.assertEqual(list(argsort(x)), [1, 2, 0])

        # two-dimensional array
        x = np.array([[0, 3], [2, 2]])
        # sorts along first axis (down)
        ind = argsort(x, axis=0)
        # self.assertEqual(list(ind), [[0, 1], [1, 0]])
        self.assertEqual(list(ind.flatten()), [0, 1, 1, 0])
        # same as np.sort(x, axis=0)
        ind = np.take_along_axis(x, ind, axis=0)
        self.assertEqual(list(ind.flatten()), [0, 2, 2, 3])
        # sorts along last axis (across)
        ind = argsort(x, axis=1)
        self.assertEqual(list(ind.flatten()), [0, 1, 0, 1])
        # same as np.sort(x, axis=1)
        ind = np.take_along_axis(x, ind, axis=1)
        self.assertEqual(list(ind.flatten()), [0, 3, 2, 2])

        # indices of the sorted elements of a N-dimensional array
        ind = np.unravel_index(argsort(x, axis=None), x.shape)
        ind1 = np.array([ list(i) for i in ind ])
        self.assertEqual(list(ind1.flatten()), [0, 1, 1, 0, 0, 0, 1, 1])
        # same as np.sort(x, axis=None)
        self.assertEqual(list(x[ind]), [0, 2, 2, 3])

        # sorting with keys
        x = np.array([(1, 0), (0, 1)], dtype=[('x', '<i4'), ('y', '<i4')])
        self.assertEqual(list(argsort(x, order=('x', 'y'))), [1, 0])
        self.assertEqual(list(argsort(x, order=('y', 'x'))), [0, 1])


if __name__ == "__main__":
    unittest.main()
