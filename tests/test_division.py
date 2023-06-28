#!/usr/bin/env python
"""
This is the unittest for division module.

python -m unittest -v tests/test_division.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_division.py

"""
import unittest


class TestDivision(unittest.TestCase):
    """
    Tests for division.py
    """

    def test_division(self):
        import numpy as np
        import pandas as pd
        from pyjams import division, div

        for dfunc in [division, div]:
            a = (1., 2., 3.)
            b = 2.
            assert isinstance(dfunc(a, b), tuple)
            self.assertEqual(list(dfunc(a, b)),
                             [0.5, 1.0, 1.5])

            a = [1., 2., 3.]
            b = 2.
            assert isinstance(dfunc(a, b), list)
            self.assertEqual(list(dfunc(a, b)),
                             [0.5, 1.0, 1.5])

            a = np.array([1., 2., 3.])
            b = 2.
            assert isinstance(dfunc(a, b), np.ndarray)
            self.assertEqual(list(dfunc(a, b)),
                             [0.5, 1.0, 1.5])

            # pandas.Series
            a = np.array([1., 2., 3.])
            b = 2.
            d1 = [pd.to_datetime('2020-06-01 12:30'),
                  pd.to_datetime('2020-09-03 16:00'),
                  pd.to_datetime('2021-06-03 11:00')]
            df = pd.Series(a)
            df.index = d1
            dd = dfunc(df, b)
            assert isinstance(dd, pd.Series)
            self.assertEqual(list(dd.values), [0.5, 1.0, 1.5])

            # pandas.DataFrame
            a = np.array([1., 2., 3.])
            a1 = np.vstack([a, a])
            d1 = [pd.to_datetime('2020-06-01 12:30'),
                  pd.to_datetime('2020-09-03 16:00')]
            df = pd.DataFrame(a1)
            df.index = d1
            dd = dfunc(df, b)
            assert isinstance(dd, pd.DataFrame)
            self.assertEqual(list(dd.values.flatten()),
                             [0.5, 1.0, 1.5, 0.5, 1.0, 1.5])

            a = 1.
            b = (1., 2., 4.)
            assert isinstance(dfunc(a, b), tuple)
            self.assertEqual(list(dfunc(a, b)),
                             [1.0, 0.5, 0.25])

            a = 1.
            b = [1., 2., 4.]
            assert isinstance(dfunc(a, b), list)
            self.assertEqual(list(dfunc(a, b)),
                             [1.0, 0.5, 0.25])

            a = 1.
            b = np.array([1., 2., 4.])
            assert isinstance(dfunc(a, b), np.ndarray)
            self.assertEqual(list(dfunc(a, b)),
                             [1.0, 0.5, 0.25])

            a = 1.
            b = np.array([1., 2., 4.])
            d1 = [pd.to_datetime('2020-06-01 12:30'),
                  pd.to_datetime('2020-09-03 16:00'),
                  pd.to_datetime('2021-06-03 11:00')]
            df = pd.Series(b)
            df.index = d1
            dd = dfunc(a, df)
            assert isinstance(dd, pd.Series)
            self.assertEqual(list(dd.values), [1.0, 0.5, 0.25])

            a = 1.
            b = np.array([1., 2., 4.])
            b1 = np.vstack([b, b])
            d1 = [pd.to_datetime('2020-06-01 12:30'),
                  pd.to_datetime('2020-09-03 16:00')]
            df = pd.DataFrame(b1)
            df.index = d1
            dd = dfunc(a, df)
            assert isinstance(dd, pd.DataFrame)
            self.assertEqual(list(dd.values.flatten()),
                             [1.0, 0.5, 0.25, 1.0, 0.5, 0.25])

            a = [1., 1., 1.]
            b = [2., 1., 0.]
            dd = dfunc(a, b)
            assert isinstance(dd, list)
            self.assertEqual(list(dd[0:2]), [0.5, 1.0])
            assert np.isnan(dd[2])
            self.assertEqual(list(dfunc(a, b, 0.)),
                             [0.5, 1.0, 0.0])
            self.assertEqual(list(dfunc(a, b, otherwise=0.)),
                             [0.5, 1.0, 0.0])
            dd = dfunc(a, b, prec=1.)
            self.assertEqual(dd[0], 0.5)
            assert np.isnan(dd[1])
            assert np.isnan(dd[2])

            a = np.array([1., 1., 1.])
            b = [2., 1., 0.]
            dd = dfunc(a, b)
            assert isinstance(dd, np.ndarray)
            self.assertEqual(list(dd[0:2]), [0.5, 1.0])
            assert np.isnan(dd[2])

            a = [1., 1., 1.]
            b = [2., 1., 0.]
            d1 = [pd.to_datetime('2020-06-01 12:30'),
                  pd.to_datetime('2020-09-03 16:00'),
                  pd.to_datetime('2021-06-03 11:00')]
            df = pd.Series(a)
            df.index = d1
            dd = dfunc(df, b)
            assert isinstance(dd, pd.Series)
            self.assertEqual(list(dd.values[:2]), [0.5, 1.0])
            assert np.isnan(dd.iloc[2])

            a = [1., 1., 1.]
            b = [2., 1., 0.]
            d1 = [pd.to_datetime('2020-06-01 12:30'),
                  pd.to_datetime('2020-09-03 16:00'),
                  pd.to_datetime('2021-06-03 11:00')]
            df = pd.Series(b)
            df.index = d1
            dd = dfunc(a, df)
            assert isinstance(dd, list)
            self.assertEqual(dd[:2], [0.5, 1.0])
            assert np.isnan(dd[2])

            a = np.array([1., 1., 1.])
            b = np.array([2., 1., 0.])
            dd = dfunc(a, b)
            assert isinstance(dd, np.ndarray)
            self.assertEqual(list(dd[0:2]), [0.5, 1.0])
            assert np.isnan(dd[2])

            mask = [0, 0, 1]
            a = np.ma.array([1., 1., 1.], mask=mask)
            b = np.array([2., 1., 0.])
            dd = dfunc(a, b)
            assert isinstance(dd, np.ma.masked_array)
            self.assertEqual(list(dd), [0.5, 1.0, np.ma.masked])

            a = np.array([1., 1., 1.])
            mask = [0, 0, 1]
            b = np.ma.array([2., 1., 0.], mask=mask)
            dd = dfunc(a, b)
            assert isinstance(dd, np.ma.masked_array)
            self.assertEqual(list(dd), [0.5, 1.0, np.ma.masked])


if __name__ == "__main__":
    unittest.main()
