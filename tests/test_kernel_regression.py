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
        hsoll = [4.46598]
        assert isinstance(hout, np.ndarray)
        self.assertEqual(list(np.around(hout, 5)), hsoll)

        # silverman
        hout  = kernel_regression_h(x, y, silverman=True)
        hsoll = [4.46598]
        assert isinstance(hout, np.ndarray)
        self.assertEqual(list(np.around(hout, 5)), hsoll)

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
        fsoll = [13.01725, 13.33307, 13.69295, 13.68156, 13.33056]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout[::50], 5)), fsoll)

        # w/o kernel_regression_h
        fout = kernel_regression(x, y)
        fsoll = [13.01725, 13.33307, 13.69295, 13.68156, 13.33056]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout[::50], 5)), fsoll)

        # silverman
        fout = kernel_regression(x, y, silverman=True)
        fsoll = [13.01725, 13.33307, 13.69295, 13.68156, 13.33056]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout[::50], 5)), fsoll)

        # xout
        fout = kernel_regression(x, y, silverman=True, xout=xout)
        fsoll = [13.0172, 13.6, 13.66, 13.6791, 13.2663]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 4)), fsoll)

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
        fsoll = [0.52240941, 0.52569869, 0.54179589, 0.51780751,
                 0.47644245, 0.49230196, 0.60344806, 0.77747177,
                 0.95450468, 1.0960389]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 8)), fsoll)

        # using given kernel
        fout = kernel_regression(x, y, 0.2)
        fsoll = [0.70404103, 0.01294352, 1.04777665, 0.54772199,
                 0.29020837, 0.38250561, 0.59918264, 0.84297652,
                 1.04019479, 1.17067274]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 8)), fsoll)

        # w/o kernel_regression_h
        fout = kernel_regression(x, y)
        fsoll = [0.52240941, 0.52569869, 0.54179589, 0.51780751,
                 0.47644245, 0.49230196, 0.60344806, 0.77747177,
                 0.95450468, 1.0960389]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 8)), fsoll)

        # silverman
        fout = kernel_regression(x, y, silverman=True)
        fsoll = [0.69115273, 0.42280858, 0.54584447, 0.53431539,
                 0.52149406, 0.55542563, 0.64206536, 0.76189995,
                 0.88777986, 1.00014619]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 8)), fsoll)

        # xout
        fout = kernel_regression(x, y, silverman=True, xout=xout)
        fsoll = [0.60548523, 0.54284698, 0.49447115, 0.52671401,
                 0.69506313]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(list(np.around(fout, 8)), fsoll)

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
