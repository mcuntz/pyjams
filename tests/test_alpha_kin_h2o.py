#!/usr/bin/env python
"""
This is the unittest for alpha_kin_h2o module.

python -m unittest -v tests/test_alpha_kin_h2o.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_alpha_kin_h2o.py

"""
import unittest


class TestAlphaKinH2O(unittest.TestCase):
    """
    Tests for alpha_kin_h2o.py
    """

    def test_alpha_kin_h2o(self):
        import numpy as np
        from pyjams import alpha_kin_h2o

        alpha = alpha_kin_h2o(isotope=0)
        self.assertEqual(np.around(alpha, 4), 1.0)

        epsilon = alpha_kin_h2o(isotope=1, eps=True) * 1000.
        self.assertEqual(np.around(epsilon, 4), 25.1153)

        epsilon = alpha_kin_h2o(isotope=2, eps=True, greater1=False) * 1000.
        self.assertEqual(np.around(epsilon, 4), -27.3)

        epsilon = alpha_kin_h2o(isotope=2, eps=True, boundary=True) * 1000.
        self.assertEqual(np.around(epsilon, 4), 18.6244)

        epsilon = alpha_kin_h2o(isotope=1, eps=True, cappa=True) * 1000.
        self.assertEqual(np.around(epsilon, 4), 16.3635)

        epsilon = alpha_kin_h2o(isotope=2, eps=True, greater1=False,
                                boundary=True, cappa=True) * 1000.
        self.assertEqual(np.around(epsilon, 4), -20.7076)


if __name__ == "__main__":
    unittest.main()
