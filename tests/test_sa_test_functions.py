#!/usr/bin/env python
"""
This is the unittest for the Sensitivity Analysis Test Functions module.

python -m unittest -v tests/test_sa_test_functions.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_sa_test_functions.py

"""
import unittest


class TestSATestFunctions(unittest.TestCase):
    """
    Tests for functions/sa_test_functions.py

    """
    def setUp(self):
        import numpy as np
        # seed for reproducible results
        seed = 1234
        np.random.seed(seed=seed)

    def test_sa_test_functions(self):
        import numpy as np
        import pandas as pd
        from pyjams.functions import B, g, G, Gstar, K, bratley
        from pyjams.functions import oakley_ohagan, ishigami_homma
        from pyjams.functions import linear, product, ratio
        from pyjams.functions import ishigami_homma_easy, fmorris, morris

        # scalar
        x = np.arange(10)
        self.assertEqual(B(x), 80)
        self.assertEqual(B(pd.Series(x)), 80)
        x = np.ones(5)
        self.assertEqual(g(x, np.zeros(5)), 32.0)
        self.assertEqual(g(pd.Series(x), np.zeros(5)), 32.0)
        self.assertEqual(G(x, np.zeros(5)), 32.0)
        self.assertEqual(G(pd.Series(x), np.zeros(5)), 32.0)
        self.assertEqual(Gstar(x, np.zeros(5), x, np.zeros(5)), 1.0)
        self.assertEqual(Gstar(pd.Series(x), np.zeros(5), x, np.zeros(5)), 1.0)
        self.assertEqual(Gstar(x, [0., 0., 0., 0., 0.], x, np.zeros(5)), 1.0)
        self.assertEqual(Gstar(pd.Series(x), [0., 0., 0., 0., 0.],
                               x, np.zeros(5)), 1.0)
        x = np.arange(5)
        self.assertEqual(K(x + 1.), -101.0)
        self.assertEqual(K(pd.Series(x) + 1.), -101.0)
        self.assertEqual(bratley(x + 1.), -101.0)
        self.assertEqual(bratley(pd.Series(x) + 1.), -101.0)
        x = np.zeros(15)
        self.assertEqual(oakley_ohagan(x), 15.75)
        self.assertEqual(oakley_ohagan(pd.Series(x)), 15.75)
        x = np.array([np.pi / 2., np.pi / 2., 1.])
        self.assertEqual(ishigami_homma(x, 1., 1.),
                         3.0)
        self.assertEqual(ishigami_homma(pd.Series(x), 1., 1.),
                         3.0)
        x = np.ones(1)
        self.assertEqual(linear(x, 1., 1.), 2.0)
        self.assertEqual(linear(pd.Series(x), 1., 1.), 2.0)
        x = np.arange(2)
        self.assertEqual(product(x + 1.), 2.0)
        self.assertEqual(product(pd.Series(x) + 1.), 2.0)
        self.assertEqual(ratio(x + 1.), 0.5)
        self.assertEqual(ratio(pd.Series(x) + 1.), 0.5)
        x = np.array([np.pi / 2., 1.])
        self.assertEqual(ishigami_homma_easy(x), 2.0)
        self.assertEqual(ishigami_homma_easy(pd.Series(x)), 2.0)

        # vector
        x = np.arange(12).reshape(6, 2)
        self.assertEqual(list(B(x)), [56, 89])
        self.assertEqual(list(B(pd.DataFrame(x))), [56, 89])
        x = np.ones((5, 2))
        self.assertEqual(list(g(x, np.zeros(5))), [32.0, 32.0])
        self.assertEqual(list(g(pd.DataFrame(x), np.zeros(5))), [32.0, 32.0])
        self.assertEqual(list(G(x, np.zeros(5))), [32.0, 32.0])
        self.assertEqual(list(G(pd.DataFrame(x), np.zeros(5))), [32.0, 32.0])
        self.assertEqual(list(Gstar(x, np.zeros(5), np.ones(5),
                                    np.zeros(5))), [1.0, 1.0])
        self.assertEqual(list(Gstar(pd.DataFrame(x), np.zeros(5), np.ones(5),
                                    np.zeros(5))), [1.0, 1.0])
        x = np.arange(8).reshape((4, 2))
        self.assertEqual(list(K(x + 1.)), [92., 342.])
        self.assertEqual(list(K(pd.DataFrame(x) + 1.)), [92., 342.])
        self.assertEqual(list(bratley(x + 1.)), [92., 342.])
        self.assertEqual(list(bratley(pd.DataFrame(x) + 1.)), [92., 342.])
        x = np.zeros((15, 2))
        self.assertEqual(list(oakley_ohagan(x)), [15.75, 15.75])
        self.assertEqual(list(oakley_ohagan(pd.DataFrame(x))), [15.75, 15.75])
        x = np.array([[np.pi / 2., np.pi / 2.],
                      [np.pi / 2., np.pi / 2.],
                      [1., 1.]])
        self.assertEqual(list(ishigami_homma(x, 1., 1.)), [3.0, 3.0])
        self.assertEqual(list(ishigami_homma(pd.DataFrame(x), 1., 1.)),
                         [3.0, 3.0])
        x = np.ones((1, 2))
        self.assertEqual(list(linear(x, 1., 1.)), [2.0, 2.0])
        self.assertEqual(list(linear(pd.DataFrame(x), 1., 1.)), [2.0, 2.0])
        x = np.arange(4).reshape((2, 2))
        self.assertEqual(list(product(x + 1.)), [3.0, 8.0])
        self.assertEqual(list(product(pd.DataFrame(x) + 1.)), [3.0, 8.0])
        x = np.arange(2).repeat(2).reshape((2, 2))
        self.assertEqual(list(ratio(x + 1.)), [0.5, 0.5])
        self.assertEqual(list(ratio(pd.DataFrame(x) + 1.)), [0.5, 0.5])
        x = np.array([[np.pi / 2., np.pi / 2.],
                      [1., 1.]])
        self.assertEqual(list(ishigami_homma_easy(x)), [2.0, 2.0])
        self.assertEqual(list(ishigami_homma_easy(pd.DataFrame(x))),
                         [2.0, 2.0])

        # Morris
        npars = 20
        # x0 = np.ones(npars) * 0.5
        # lb = np.zeros(npars)
        # ub = np.ones(npars)
        beta0                 = 0.
        beta1                 = np.random.standard_normal(npars)
        beta1[:10]            = 20.
        beta2                 = np.random.standard_normal((npars, npars))
        beta2[:6, :6]         = -15.
        beta3                 = np.zeros((npars, npars, npars))
        beta3[:5, :5, :5]     = -10.
        beta4                 = np.zeros((npars, npars, npars, npars))
        beta4[:4, :4, :4, :4] = 5.

        x = np.linspace(0, 2 * (npars - 1), npars) / float(2 * npars - 1)
        mm = fmorris(x, beta0, beta1, beta2, beta3, beta4)
        self.assertEqual(np.around(mm, 3), -82.711)
        mm = fmorris(pd.Series(x), beta0, beta1, beta2, beta3, beta4)
        self.assertEqual(np.around(mm, 3), -82.711)
        x = (np.arange(2 * npars, dtype=float).reshape((npars, 2)) /
             float(2 * npars - 1))
        mm = fmorris(x, beta0, beta1, beta2, beta3, beta4)
        self.assertEqual(list(np.around(mm, 3)), [-82.711, -60.589])
        mm = fmorris(pd.DataFrame(x), beta0, beta1, beta2, beta3, beta4)
        self.assertEqual(list(np.around(mm, 3)), [-82.711, -60.589])

        x = np.linspace(0, 2 * (npars - 1), npars) / float(2 * npars - 1)
        mm = morris(x, beta0, beta1, beta2, beta3, beta4)
        self.assertEqual(np.around(mm, 3), -82.711)
        mm = morris(pd.Series(x), beta0, beta1, beta2, beta3, beta4)
        self.assertEqual(np.around(mm, 3), -82.711)
        x = (np.arange(2 * npars, dtype=float).reshape((npars, 2)) /
             float(2 * npars - 1))
        mm = morris(x, beta0, beta1, beta2, beta3, beta4)
        self.assertEqual(list(np.around(mm, 3)), [-82.711, -60.589])
        mm = morris(pd.DataFrame(x), beta0, beta1, beta2, beta3, beta4)
        self.assertEqual(list(np.around(mm, 3)), [-82.711, -60.589])


if __name__ == "__main__":
    unittest.main()
