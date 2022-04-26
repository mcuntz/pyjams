#!/usr/bin/env python
"""
This is the unittest for kernel_regression module.

python -m unittest -v tests/test_kernel_regression.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_kernel_regression.py

"""
import unittest


def _flatten(itr):
    import numpy as np
    fitr = np.array(itr).flatten()
    if len(fitr) == 0:
        return list(fitr)
    else:
        if isinstance(fitr[0], str):
            return [ i for i in fitr ]
        else:
            return [ i if np.isfinite(i) else np.finfo(float).max
                     for i in fitr ]


class TestKernelRegression(unittest.TestCase):
    """
    Tests for kernel_regression.py
    """

    def setUp(self):
        import numpy as np
        # seed for reproducible results
        self.seed = 1234
        np.random.seed(seed=self.seed)

    def test_kernel_regression_h(self):
        import numpy as np
        from pyjams import kernel_regression_h

        # 1971 Canadian Census Public Use Tapes
        # as in Wikipedia article about kernel regression,
        # taken from R package crs:
        # https://github.com/JeffreyRacine/R-Package-crs
        infile = 'tests/cps71.csv'
        dat = np.loadtxt('tests/cps71.csv', skiprows=1, delimiter=',')
        y = dat[:, 1]
        x = dat[:, 2]

        # bootstrap h
        hout  = kernel_regression_h(x, y)
        hsoll = 4.46598
        assert isinstance(hout, np.float64)
        self.assertEqual(np.around(hout, 5), hsoll)

        # silverman
        hout  = kernel_regression_h(x, y, silverman=True)
        hsoll = 4.46598
        assert isinstance(hout, np.float64)
        self.assertEqual(np.around(hout, 5), hsoll)

        #

        # made up multidimensional data
        n = 10
        x = np.zeros((n, 2))
        x[:, 0] = np.arange(n, dtype=float) / float(n-1)
        x[:, 1] = 1. / (np.arange(n, dtype=float) / float(n-1) + 0.1)
        y = 1. + x[:, 0]**2 - np.sin(x[:, 1])**2

        # cross-validation
        hout  = kernel_regression_h(x, y)
        hsoll = [0.17268, 9.51691]
        assert isinstance(hout, np.ndarray)
        self.assertEqual(list(np.around(hout, 5)), hsoll)

        # silverman
        hout = kernel_regression_h(x, y, silverman=True)
        hsoll = [0.22919, 1.90338]
        assert isinstance(hout, np.ndarray)
        self.assertEqual(list(np.around(hout, 5)), hsoll)

        # errors
        # shapes
        self.assertRaises(AssertionError, kernel_regression_h,
                          x, y[1:])

    def test_kernel_regression(self):
        import numpy as np
        from pyjams import kernel_regression_h, kernel_regression

        # 1971 Canadian Census Public Use Tapes
        # as in Wikipedia article about kernel regression,
        # taken from R package crs:
        # https://github.com/JeffreyRacine/R-Package-crs
        infile = 'tests/cps71.csv'
        dat = np.loadtxt('tests/cps71.csv', skiprows=1, delimiter=',')
        y = dat[:, 1]
        x = dat[:, 2]

        nout = 5
        xout = (x.min() + (x.max() - x.min()) *
                np.arange(nout, dtype=float) / float(nout-1))

        # using kernel_regression_h
        h = kernel_regression_h(x, y)
        fout = kernel_regression(x, y, h)
        fsoll = [13.0172, 13.3331, 13.693, 13.6816, 13.3306]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout[::50], 4)), fsoll)

        # w/o kernel_regression_h
        fout = kernel_regression(x, y)
        fsoll = [13.0172, 13.3331, 13.693, 13.6816, 13.3306]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout[::50], 4)), fsoll)

        # silverman
        fout = kernel_regression(x, y, silverman=True)
        fsoll = [13.0172, 13.3331, 13.693, 13.6816, 13.3306]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout[::50], 4)), fsoll)

        # xout
        fout = kernel_regression(x, y, silverman=True, xout=xout)
        fsoll = [13.0172, 13.6, 13.66, 13.6791, 13.2663]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        # different input/output types
        fout = kernel_regression(x, list(y), silverman=True, xout=xout)
        fsoll = [13.0172, 13.6, 13.66, 13.6791, 13.2663]
        assert isinstance(fout, list)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        fout = kernel_regression(x, tuple(y), silverman=True, xout=xout)
        fsoll = [13.0172, 13.6, 13.66, 13.6791, 13.2663]
        assert isinstance(fout, tuple)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        fout = kernel_regression(x, np.ma.array(y), silverman=True, xout=xout)
        fsoll = [13.0172, 13.6, 13.66, 13.6791, 13.2663]
        assert isinstance(fout, np.ma.masked_array)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        fout = kernel_regression(list(x), y)
        fsoll = [13.0172, 13.3331, 13.693, 13.6816, 13.3306]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout[::50], 4)), fsoll)

        fout = kernel_regression(tuple(x), y)
        fsoll = [13.0172, 13.3331, 13.693, 13.6816, 13.3306]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout[::50], 4)), fsoll)

        fout = kernel_regression(np.ma.array(x), y)
        fsoll = [13.0172, 13.3331, 13.693, 13.6816, 13.3306]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout[::50], 4)), fsoll)

        #

        # made up multidimensional data
        n = 10
        x = np.zeros((n, 2))
        x[:, 0] = np.arange(n, dtype=float) / float(n-1)
        x[:, 1] = 1. / (np.arange(n, dtype=float) / float(n-1) + 0.1)
        y = 1. + x[:, 0]**2 - np.sin(x[:, 1])**2

        nout = 5
        xout = np.empty((nout, 2))
        xout[:, 0] = (np.amin(x[:, 0]) +
                      (np.amax(x[:, 0]) - np.amin(x[:, 0])) *
                      np.arange(nout, dtype=float) / float(nout-1))
        xout[:, 1] = (np.amin(x[:, 1]) +
                      (np.amax(x[:, 1]) - np.amin(x[:, 1])) *
                      np.arange(nout, dtype=float) / float(nout-1))

        # using kernel_regression_h
        h = kernel_regression_h(x, y)
        fout = kernel_regression(x, y, h)
        fsoll = [0.5224, 0.5257, 0.5418, 0.5178,
                 0.4764, 0.4923, 0.6034, 0.7775,
                 0.9545, 1.0960]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        # using given kernel
        fout = kernel_regression(x, y, 0.2)
        fsoll = [0.704, 0.0129, 1.0478, 0.5477,
                 0.2902, 0.3825, 0.5992, 0.843,
                 1.0402, 1.1707]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        # w/o kernel_regression_h
        fout = kernel_regression(x, y)
        fsoll = [0.5224, 0.5257, 0.5418, 0.5178,
                 0.4764, 0.4923, 0.6034, 0.7775,
                 0.9545, 1.0960]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        # silverman
        fout = kernel_regression(x, y, silverman=True)
        fsoll = [0.6912, 0.4228, 0.5458, 0.5343,
                 0.5215, 0.5554, 0.6421, 0.7619,
                 0.8878, 1.0001]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        # xout
        fout = kernel_regression(x, y, silverman=True, xout=xout)
        fsoll = [0.6055, 0.5428, 0.4945, 0.5267, 0.6951]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        # different input/output types
        fout = kernel_regression(x, list(y))
        fsoll = [0.5224, 0.5257, 0.5418, 0.5178,
                 0.4764, 0.4923, 0.6034, 0.7775,
                 0.9545, 1.0960]
        assert isinstance(fout, list)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        fout = kernel_regression(x, tuple(y))
        fsoll = [0.5224, 0.5257, 0.5418, 0.5178,
                 0.4764, 0.4923, 0.6034, 0.7775,
                 0.9545, 1.0960]
        assert isinstance(fout, tuple)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        fout = kernel_regression(x, np.ma.array(y))
        fsoll = [0.5224, 0.5257, 0.5418, 0.5178,
                 0.4764, 0.4923, 0.6034, 0.7775,
                 0.9545, 1.0960]
        assert isinstance(fout, np.ma.masked_array)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        fout = kernel_regression(np.ma.array(x), y)
        fsoll = [0.5224, 0.5257, 0.5418, 0.5178,
                 0.4764, 0.4923, 0.6034, 0.7775,
                 0.9545, 1.0960]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

        # errors
        # shapes do not match
        self.assertRaises(AssertionError, kernel_regression, x, y[1:])
        # h has wrong size
        self.assertRaises(AssertionError, kernel_regression, x, y,
                          [0.1, 0.2, 0.3])
        # xout dimension does not match
        xxout = np.empty((nout, 3))
        xxout[:, 0:2] = xout
        xxout[:, 2] = xout[:, 1]
        self.assertRaises(AssertionError, kernel_regression, x, y,
                          [0.1, 0.2, 0.3], xout=xxout)


if __name__ == "__main__":
    unittest.main()
