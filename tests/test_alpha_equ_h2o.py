#!/usr/bin/env python
"""
This is the unittest for alpha_equ_h2o module.

python -m unittest -v tests/test_alpha_equ_h2o.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_alpha_equ_h2o.py

"""
import unittest


class TestAlphaEquH2O(unittest.TestCase):
    """
    Tests for alpha_equ_h2o.py
    """

    def test_alpha_equ_h2o(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import alpha_equ_h2o

        T0 = 273.15

        # scalar
        assert isinstance(alpha_equ_h2o(T0), float)
        assert np.around(alpha_equ_h2o(T0, isotope=1), 4) == 1.1123

        # list
        T = [0., 10., 15., 25.]
        T1 = [ tt + T0 for tt in T ]
        assert isinstance(alpha_equ_h2o(T1), list)
        self.assertEqual(list(alpha_equ_h2o(T1, isotope=0)),
                         [1.0, 1.0, 1.0, 1.0])

        # tuple
        T1 = tuple(T1)
        assert isinstance(alpha_equ_h2o(T1), tuple)
        self.assertEqual(list(np.around(alpha_equ_h2o(T1, isotope=1), 4)),
                         [1.1123, 1.0977, 1.0911, 1.0793])

        # ndarray
        T  = np.array(T)
        assert isinstance(alpha_equ_h2o(T+T0), np.ndarray)
        self.assertEqual(list(alpha_equ_h2o(T+T0, isotope=0)),
                         [1.0, 1.0, 1.0, 1.0])
        self.assertEqual(list(np.around(alpha_equ_h2o(T+T0, isotope=2), 4)),
                         [1.0117, 1.0107, 1.0102, 1.0094])

        # masked_array and greater1=False
        alpha = alpha_equ_h2o(np.ma.array(T+T0, mask=(T == 0.)),
                              isotope=2, greater1=False)
        assert isinstance(alpha, np.ndarray)
        assert isinstance(alpha, np.ma.MaskedArray)
        self.assertEqual(list(np.around(alpha, 4)),
                         [masked, 0.9894, 0.9899, 0.9907])

        # epsilon, HO18O, scalar
        epsilon = alpha_equ_h2o(0.+T0, isotope=2, eps=True) * 1000.
        self.assertEqual(np.around(epsilon, 4), 11.7187)

        # epsilon, HDO
        epsilon = alpha_equ_h2o(T+T0, isotope=1, eps=True) * 1000.
        self.assertEqual(list(np.around(epsilon, 4)),
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
        T1 = list(T1)
        T1[0] = -1.
        alpha = alpha_equ_h2o(T1, undef=-1., isotope=1, eps=True)
        alpha = [ a * 1000. for a in alpha ]
        self.assertEqual(list(np.around(alpha, 4)),
                         [-1000.0000, 97.6829, 91.1296, 79.3443])

        # undef, tuple
        T1 = tuple(T1)
        alpha = alpha_equ_h2o(T1, undef=-1., isotope=1, eps=True)
        alpha = [ a * 1000. for a in alpha ]
        self.assertEqual(list(np.around(alpha, 4)),
                         [-1000.0000, 97.6829, 91.1296, 79.3443])

        # undef, np.array
        T1 = np.array(T1)
        alpha = alpha_equ_h2o(T1, undef=-1., isotope=1, eps=True) * 1000.
        self.assertEqual(list(np.around(alpha, 4)),
                         [-1000.0000, 97.6829, 91.1296, 79.3443])

        # undef, masked_array
        T1 = np.ma.array(T1, mask=(T == 10.))
        alpha = alpha_equ_h2o(T1, undef=-1., isotope=1, eps=True) * 1000.
        self.assertEqual(list(np.around(alpha, 4)),
                         [masked, masked, 91.1296, 79.3443])


if __name__ == "__main__":
    unittest.main()
