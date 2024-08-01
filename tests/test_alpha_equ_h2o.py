#!/usr/bin/env python
"""
This is the unittest for alpha_equ_h2o module.

python -m unittest -v tests/test_alpha_equ_h2o.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_alpha_equ_h2o.py

"""
import unittest
import numpy as np
from numpy.ma import masked
import pandas as pd


def _flatten(itr, decimals=0):
    # if isinstance(itr, np.ma.MaskedArray):
    #     fitr = np.ma.around(np.ma.array(itr).flatten(), decimals)
    # else:
    #     fitr = np.around(np.array(itr).flatten(), decimals)
    fitr = np.around(np.ma.array(itr).flatten(), decimals)
    if len(fitr) == 0:
        return list(fitr)
    else:
        if isinstance(fitr[0], str):
            return [ i for i in fitr ]
        else:
            return list(fitr)


class TestAlphaEquH2O(unittest.TestCase):
    """
    Tests for alpha_equ_h2o.py
    """

    def test_alpha_equ_h2o(self):
        from pyjams import alpha_equ_h2o

        T0 = 273.15
        T = [0., 10., 15., 25.]

        # scalar
        alpha = alpha_equ_h2o(T0, isotope=1)
        assert isinstance(alpha, float)
        assert np.around(alpha, 4) == 1.1123

        # list
        T1 = [ tt + T0 for tt in T ]
        alpha = alpha_equ_h2o(T1, isotope=0)
        assert isinstance(alpha, list)
        self.assertEqual(list(alpha), [1.0, 1.0, 1.0, 1.0])

        # tuple
        T1 = tuple(T1)
        alpha = alpha_equ_h2o(T1, isotope=1)
        assert isinstance(alpha, tuple)
        self.assertEqual(_flatten(alpha, 4), [1.1123, 1.0977, 1.0911, 1.0793])

        # ndarray
        T1  = np.array(T) + T0
        alpha = alpha_equ_h2o(T1, isotope=0)
        assert isinstance(alpha_equ_h2o(T1), np.ndarray)
        self.assertEqual(list(alpha), [1.0, 1.0, 1.0, 1.0])
        alpha = alpha_equ_h2o(T1, isotope=2)
        self.assertEqual(_flatten(alpha, 4), [1.0117, 1.0107, 1.0102, 1.0094])

        # pandas.Series
        T1 = [ tt + T0 for tt in T ]
        d1 = [pd.to_datetime('2020-06-01 12:30'),
              pd.to_datetime('2020-09-03 16:00'),
              pd.to_datetime('2021-06-03 11:00'),
              pd.to_datetime('2020-09-03 16:00')]
        df = pd.Series(T1)
        df.index = d1
        alpha = alpha_equ_h2o(df)
        assert isinstance(alpha, pd.Series)
        self.assertEqual(list(alpha.values), [1.0, 1.0, 1.0, 1.0])
        alpha = alpha_equ_h2o(df, isotope=2)
        self.assertEqual(_flatten(alpha.values, 4),
                         [1.0117, 1.0107, 1.0102, 1.0094])

        # pandas.DataFrame
        T1 = np.vstack([T, T]) + T0
        d1 = [pd.to_datetime('2020-06-01 12:30'),
              pd.to_datetime('2020-09-03 16:00')]
        df = pd.DataFrame(T1)
        df.index = d1
        alpha = alpha_equ_h2o(df)
        assert isinstance(alpha, pd.DataFrame)
        self.assertEqual(_flatten(alpha.values, 1),
                         [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        alpha = alpha_equ_h2o(df, isotope=2)
        self.assertEqual(_flatten(alpha.values, 4),
                         [1.0117, 1.0107, 1.0102, 1.0094,
                          1.0117, 1.0107, 1.0102, 1.0094])

        # masked_array and greater1=False
        T1  = np.array(T) + T0
        alpha = alpha_equ_h2o(np.ma.array(T1, mask=(T1 == T0)),
                              isotope=2, greater1=False)
        assert isinstance(alpha, np.ndarray)
        assert isinstance(alpha, np.ma.MaskedArray)
        self.assertEqual(_flatten(alpha, 4),
                         [masked, 0.9894, 0.9899, 0.9907])

        # epsilon, HO18O, scalar
        epsilon = alpha_equ_h2o(0. + T0, isotope=2, eps=True) * 1000.
        assert np.around(epsilon, 4) == 11.7187

        # epsilon, HDO
        T1  = np.array(T) + T0
        epsilon = alpha_equ_h2o(T1, isotope=1, eps=True) * 1000.
        self.assertEqual(_flatten(epsilon, 4),
                         [112.3194, 97.6829, 91.1296, 79.3443])

        # undef, scalar
        epsilon = alpha_equ_h2o(-9998., undef=-9998., isotope=2, eps=True)
        self.assertEqual(epsilon, -9998.)
        epsilon = alpha_equ_h2o(-9999., isotope=2, eps=True)
        self.assertEqual(epsilon, -9999.)

        # undef is NaN, scalar
        epsilon = alpha_equ_h2o(np.nan, undef=np.nan, isotope=2, eps=True)
        assert np.isnan(epsilon)
        epsilon = alpha_equ_h2o(np.nan, isotope=2, eps=True)
        assert np.isnan(epsilon)

        # undef is Inf, scalar
        epsilon = alpha_equ_h2o(np.inf, undef=np.inf, isotope=2, eps=True)
        assert np.isinf(epsilon)

        # undef, list
        T1 = [ tt + T0 for tt in T ]
        T1[0] = -1.
        epsilon = alpha_equ_h2o(T1, undef=-1., isotope=1, eps=True)
        epsilon = [ a * 1000. for a in epsilon ]
        self.assertEqual(_flatten(epsilon, 4),
                         [-1000.0000, 97.6829, 91.1296, 79.3443])

        # undef, tuple
        T1 = [ tt + T0 for tt in T ]
        T1[0] = -1.
        T1 = tuple(T1)
        epsilon = alpha_equ_h2o(T1, undef=-1., isotope=1, eps=True)
        epsilon = [ a * 1000. for a in epsilon ]
        self.assertEqual(_flatten(epsilon, 4),
                         [-1000.0000, 97.6829, 91.1296, 79.3443])

        # undef, np.array
        T1 = np.array(T) + T0
        T1[0] = -1.
        epsilon = alpha_equ_h2o(T1, undef=-1., isotope=1, eps=True) * 1000.
        self.assertEqual(_flatten(epsilon, 4),
                         [-1000.0000, 97.6829, 91.1296, 79.3443])

        # undef, masked_array
        T1 = np.array(T) + T0
        T1[0] = -1.
        T1 = np.ma.array(T1, mask=(T1 == (T0 + 10.)))
        epsilon = alpha_equ_h2o(T1, undef=-1., isotope=1, eps=True) * 1000.
        self.assertEqual(_flatten(epsilon, 4),
                         [masked, masked, 91.1296, 79.3443])

        # undef and NaN, pandas.Series
        T1 = np.array(T) + T0
        T1[0] = np.nan
        T1[1] = -1.
        d1 = [pd.to_datetime('2020-06-01 12:30'),
              pd.to_datetime('2020-09-03 16:00'),
              pd.to_datetime('2021-06-03 11:00'),
              pd.to_datetime('2020-09-03 16:00')]
        df = pd.Series(T1)
        df.index = d1
        epsilon = alpha_equ_h2o(df, undef=-1., isotope=1, eps=True) * 1000.
        assert isinstance(epsilon, pd.Series)
        self.assertEqual(_flatten(epsilon.values[1:], 4),
                         [-1000.0, 91.1296, 79.3443])
        assert np.isnan(epsilon.iloc[0])


if __name__ == "__main__":
    unittest.main()
