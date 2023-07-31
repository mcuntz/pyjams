#!/usr/bin/env python
"""
This is the unittest for the Optimisation Test Functions module.

python -m unittest -v tests/test_opti_test_functions.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_opti_test_functions.py

"""
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
        import pandas as pd
        from pyjams.functions import ackley, griewank, goldstein_price
        from pyjams.functions import rastrigin, rosenbrock
        from pyjams.functions import six_hump_camelback

        # optima
        x = np.zeros(15)
        self.assertTrue(np.isclose(ackley(x), 0.0))
        self.assertTrue(np.isclose(ackley(pd.Series(x)), 0.0))
        x = np.zeros(2)
        self.assertEqual(griewank(x), 0.0)
        self.assertEqual(griewank(pd.Series(x)), 0.0)
        x = np.zeros(10)
        self.assertEqual(griewank(x), 0.0)
        self.assertEqual(griewank(pd.Series(x)), 0.0)
        x = [0.0, -1.0]
        self.assertEqual(goldstein_price(x), 3.0)
        self.assertEqual(goldstein_price(pd.Series(x)), 3.0)
        x = np.zeros(2)
        self.assertEqual(rastrigin(x), -2.0)
        self.assertEqual(rastrigin(pd.Series(x)), -2.0)
        x = np.ones(2)
        self.assertEqual(rosenbrock(x), 0.0)
        self.assertEqual(rosenbrock(pd.Series(x)), 0.0)
        x = np.array([-0.08983, 0.7126])
        self.assertEqual(np.around(six_hump_camelback(x), 4), -1.0316)
        self.assertEqual(np.around(six_hump_camelback(-x), 4), -1.0316)
        self.assertEqual(np.around(six_hump_camelback(pd.Series(x)), 4),
                         -1.0316)
        self.assertEqual(np.around(six_hump_camelback(-pd.Series(x)), 4),
                         -1.0316)


if __name__ == "__main__":
    unittest.main()
