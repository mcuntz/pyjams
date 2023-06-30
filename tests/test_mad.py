#!/usr/bin/env python
"""
This is the unittest for mad module.

python -m unittest -v tests/test_mad.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_mad.py

"""
import unittest
from numpy.ma import masked
from pytest import raises as assert_raises


def _same(ist, soll):
    # xor
    thesame = all([ ist[i] != (not soll[i]) for i in range(len(soll)) ])
    return thesame


def _same_masked(ist, soll):
    istlist = list(ist)
    bout = True
    for i in range(len(soll)):
        if (istlist[i] is masked) or (soll[i] is masked):
            bout &= (istlist[i] is masked) and (soll[i] is masked)
        else:
            bout &= istlist[i] == soll[i]
    return bout


class TestMad(unittest.TestCase):
    """
    Tests for mad.py
    """

    def test_mad(self):
        import numpy as np
        import pandas as pd
        from pyjams import mad

        y = np.array([-0.25, 0.68, 0.94, 1.15, 2.26, 2.35, 2.37, 2.40, 2.47,
                      2.54, 2.62, 2.64, 2.90, 2.92, 2.92, 2.93, 3.21, 3.26,
                      3.30, 3.59, 3.68, 4.30, 4.64, 5.34, 5.42, 8.01])
        df = pd.Series(y)

        # raw data
        ist = mad(y)
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]
        assert _same(ist, soll)

        ist = mad(y, z=4)
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, True]
        assert _same(ist, soll)

        ist = mad(y, z=4, prepend=y[0])
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, True]
        assert _same(ist, soll)

        ist = mad(y, z=4, append=y[-1])
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, True]
        assert _same(ist, soll)

        ist = mad(y, z=3)
        soll = [True, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, True, True]
        assert _same(ist, soll)

        ist = mad(df, z=3)
        soll = [True, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, True, True]
        assert _same(ist, soll)

        # 1st derivatives
        ist = mad(y, z=4, deriv=1)
        soll = [True, False, False, True, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, True, False, True, False, True]
        assert _same(ist, soll)

        ist = mad(y, z=4, deriv=1, prepend=y[0])
        soll = [False, True, False, False, True, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, True, False, True, False, True]
        assert _same(ist, soll)

        ist = mad(y, z=4, deriv=1, append=y[-1])
        soll = [True, False, False, True, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, True, False, True, False, True, False]
        assert _same(ist, soll)

        # 2nd derivatives
        ist = mad(y, z=4, deriv=2)
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, True]
        assert _same(ist, soll)

        # 2nd derivatives, prepend and append
        ist = mad(y, z=4, deriv=2, prepend=y[0])
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, True]
        assert _same(ist, soll)

        ist = mad(y, z=4, deriv=2, append=y[-1])
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, True, True]
        assert _same(ist, soll)

        ist = mad(y, z=4, deriv=2, prepend=y[0], append=y[-1])
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, True, True]
        assert _same(ist, soll)

        ist = mad(df, z=4, deriv=2, prepend=y[0], append=y[-1])
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, True, True]
        assert _same(ist, soll)

        # direct use
        ist = np.ma.array(y, mask=mad(y, z=4))
        soll = [-0.25, 0.68, 0.94, 1.15, 2.26, 2.35, 2.37, 2.4, 2.47, 2.54,
                2.62, 2.64, 2.9, 2.92, 2.92, 2.93, 3.21, 3.26, 3.3, 3.59, 3.68,
                4.3, 4.64, 5.34, 5.42, masked]
        self.assertEqual(list(np.round(ist, 2)), soll)

        ist = np.ma.array(y, mask=mad(y, z=4, deriv=2,
                                      prepend=y[0], append=y[-1]))
        soll = [-0.25, 0.68, 0.94, 1.15, 2.26, 2.35, 2.37, 2.4, 2.47,
                2.54, 2.62, 2.64, 2.9, 2.92, 2.92, 2.93, 3.21, 3.26, 3.3, 3.59,
                3.68, 4.3, 4.64, 5.34, masked, masked]
        self.assertEqual(list(np.round(ist, 2)), soll)

        # several dimensions
        yy = np.transpose(np.array([y, y]))
        ist = np.transpose(mad(yy, z=4))
        soll = [[False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, True]]
        ist = list(np.array(ist).flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        df2 = pd.DataFrame(np.array([y, y]).T)
        ist = mad(df2, z=4)
        soll = [[False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, True]]
        ist = list(ist.to_numpy().T.flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        yyy = np.transpose(np.array([y, y, y]))
        ist = np.transpose(mad(yyy, z=3))
        soll = [[True, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, True, True],
                [True, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, True, True],
                [True, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, True, True]]
        ist = list(np.array(ist).flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        # several dimensions, deriv
        ist = np.transpose(mad(yy, z=4, deriv=2))
        soll = [[False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, True]]
        ist = list(np.array(ist).flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        # several dimensions, deriv, prepend and append
        ist = np.transpose(mad(yy, z=4, deriv=2, prepend=y[0], append=y[-1]))
        soll = [[False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True]]
        ist = list(np.array(ist).flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        ist = np.transpose(mad(yy, z=4, deriv=2,
                               prepend=yy[0, :], append=yy[-1, :]))
        soll = [[False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True]]
        ist = list(np.array(ist).flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        ist = np.transpose(mad(yy, z=4, deriv=2,
                               prepend=yy[0:1, :], append=yy[-1:, :]))
        soll = [[False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True]]
        ist = list(np.array(ist).flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        ist = np.transpose(mad(yyy, z=4, deriv=2,
                               prepend=y[0], append=y[-1]))
        soll = [[False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True]]
        ist = list(np.array(ist).flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        ist = np.transpose(mad(yyy, z=4, deriv=2,
                               prepend=yyy[0, ...], append=yyy[-1, ...]))
        soll = [[False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True]]
        ist = list(np.array(ist).flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        ist = np.transpose(mad(yyy, z=4, deriv=2,
                               prepend=yyy[0:1, ...], append=yyy[-1:, ...]))
        soll = [[False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True],
                [False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, False, False, False,
                 False, False, False, False, False, False, True, True]]
        ist = list(np.array(ist).flatten())
        soll = list(np.array(soll).flatten())
        assert _same(ist, soll)

        # masked arrays
        my = np.ma.array(y, mask=np.zeros(y.shape))
        my.mask[-1] = True
        ist = mad(my, z=4)
        soll = [True, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, masked]
        assert _same_masked(ist, soll)

        ist = mad(my, z=3)
        soll = [True, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, True, True, masked]
        assert _same_masked(ist, soll)

        my = np.ma.array(y, mask=np.ones(y.shape))
        ist = mad(my, z=4)
        soll = [True, True, True, True, True, True, True, True, True,
                True, True, True, True, True, True, True, True, True,
                True, True, True, True, True, True, True, True]
        assert _same(ist, soll)

        # arrays with NaNs
        ny = y.copy()
        ny[-1] = np.nan
        ist = mad(ny, z=4)
        soll = [True, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]
        assert _same(ist, soll)

        ist = mad(ny, z=3)
        soll = [True, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, True, True, False]
        assert _same(ist, soll)

        # all Nans
        ny = y.copy()
        ny[:] = np.nan
        ist = mad(ny, z=4)
        soll = [False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]
        assert _same(ist, soll)

        # exclude zeros
        zy = y.copy()
        zy[1] = 0.
        ist = mad(zy, z=3)
        soll = [True, True, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, True, True]
        assert _same(ist, soll)

        ist = mad(zy, z=3, nozero=True)
        soll = [True, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, True, True]
        assert _same(ist, soll)

        # errors
        # deriv > 2
        assert_raises(AssertionError, mad, y, deriv=3)
        # ndim > 2
        y3 = np.transpose(np.array([y, y]).reshape(len(y) // 2, 2, 2))
        assert_raises(ValueError, mad, y3)
        # prepend and append with deriv=1
        assert_raises(ValueError, mad, y, z=4, deriv=1,
                      prepend=y[0], append=y[-1])
        # append shape error
        assert_raises(ValueError, mad, y, z=4, deriv=2,
                      prepend=yy[0, :], append=yy[:, -1:])


if __name__ == "__main__":
    unittest.main()
