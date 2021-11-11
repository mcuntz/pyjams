#!/usr/bin/env python
"""
This is the unittest for the General Functions module.

python -m unittest -v tests/test_general_functions.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_general_functions.py

"""
from __future__ import division, absolute_import, print_function
import unittest


class TestGeneralFunctions(unittest.TestCase):
    """
    Tests for functions/general_functions.py

    """

    def test_general_functions(self):
        import numpy as np
        from pyjams.functions import curvature
        from pyjams.functions import dlogistic_offset, d2logistic_offset
        from pyjams.functions import dlogistic_offset_p, d2logistic_offset_p

        self.assertEqual(np.around(curvature(1., dlogistic_offset,
                                             d2logistic_offset,
                                             1., 2., 2., 1.), 4), 0.2998)
        self.assertEqual(np.around(curvature(1., dlogistic_offset_p,
                                             d2logistic_offset_p,
                                             [1., 2., 2., 1.]), 4), 0.2998)


if __name__ == "__main__":
    unittest.main()
