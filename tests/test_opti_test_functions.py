#!/usr/bin/env python
"""
This is the unittest for the Optimisation Test Functions module.

python -m unittest -v tests/test_opti_test_functions.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_opti_test_functions.py

"""
from __future__ import division, absolute_import, print_function
import unittest


class TestOptiTestFunctions(unittest.TestCase):
    """
    Tests for functions/opti_test_functions.py

    """
    def setUp(self):
        import numpy as np
        # seed for reproducible results
        seed = 1234
        np.random.seed(seed=seed)

    def test_sa_test_functions(self):
        import numpy as np
        from pyjams.functions import ackley, griewank, goldstein_price
        from pyjams.functions import rastrigin, rosenbrock
        from pyjams.functions import six_hump_camelback

        # optima
        self.assertTrue(np.isclose(ackley(np.zeros(15)), 0.0))
        self.assertEqual(griewank(np.zeros(2)), 0.0)
        self.assertEqual(griewank(np.zeros(10)), 0.0)
        self.assertEqual(goldstein_price([0.0, -1.0]), 3.0)
        self.assertEqual(rastrigin(np.zeros(2)), -2.0)
        self.assertEqual(rosenbrock(np.ones(2)), 0.0)
        self.assertEqual(np.around(six_hump_camelback([-0.08983, 0.7126]), 4),
                         -1.0316)
        self.assertEqual(np.around(six_hump_camelback([0.08983, -0.7126]), 4),
                         -1.0316)


if __name__ == "__main__":
    unittest.main()
