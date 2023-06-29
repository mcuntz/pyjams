#!/usr/bin/env python
"""
This is the unittest for closest module.

python -m unittest -v tests/test_closest.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_closest.py

"""
import unittest


class TestClosest(unittest.TestCase):
    """
    Tests for closest.py
    """

    def test_closest(self):
        import numpy as np
        import pandas as pd
        from pyjams import closest

        nn = 51

        # 1D
        arr = np.arange(nn) / float(nn - 1) * 5.
        assert closest(arr, 3.125) == 31
        assert closest(arr, 3.125, value=True) == 3.1

        df = pd.Series(arr)
        df.index = pd.date_range('2022-01-01', periods=nn)
        assert closest(df, 3.125) == 31
        assert closest(df, 3.125, value=True) == 3.1

        # 2D
        arr2 = np.arange(nn).reshape((17, 3)) / float(nn - 1) * 5.
        assert closest(arr2, 3.125, value=True) == 3.1
        ii = np.unravel_index(closest(arr2, 3.125), arr2.shape)
        self.assertEqual(ii, (10, 1))
        assert arr2[ii] == 3.1

        df2 = pd.DataFrame(arr2)
        df2.index = pd.date_range('2022-01-01', periods=17)
        assert closest(df2, 3.125, value=True) == 3.1
        ii = np.unravel_index(closest(df2, 3.125), df2.shape)
        self.assertEqual(ii, (10, 1))
        assert df2.iloc[ii] == 3.1


if __name__ == "__main__":
    unittest.main()
