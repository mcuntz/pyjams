#!/usr/bin/env python
"""
This is the unittest for the Logistic Functions module.

python -m unittest -v tests/test_logistic_function.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_logistic_function.py

"""
import unittest


class TestLogisticFunction(unittest.TestCase):
    """
    Tests for functions/logistic_function.py

    """

    def test_logistic_function(self):
        import numpy as np
        import pandas as pd
        from pyjams.functions import logistic, logistic_offset
        from pyjams.functions import logistic2_offset
        from pyjams.functions import dlogistic, dlogistic_offset
        from pyjams.functions import dlogistic2_offset
        from pyjams.functions import d2logistic, d2logistic_offset
        from pyjams.functions import d2logistic2_offset
        from pyjams.functions import logistic_p, logistic_offset_p
        from pyjams.functions import logistic2_offset_p
        from pyjams.functions import dlogistic_p, dlogistic_offset_p
        from pyjams.functions import dlogistic2_offset_p
        from pyjams.functions import d2logistic_p, d2logistic_offset_p
        from pyjams.functions import d2logistic2_offset_p

        assert logistic(1., 1., 0., 2.) == 0.5
        assert logistic(1., 1., 2., 1.) == 0.5
        assert logistic(2., 1., 1., 1.) == 1. / (1. + np.exp(-1.))
        assert logistic_offset(1., 1., 0., 2., 1.) == 1.5
        assert logistic_offset(1., 1., 2., 1., 1.) == 1.5
        assert (logistic_offset(2., 1., 1., 1., 1.) ==
                1. / (1. + np.exp(-1.)) + 1.)
        assert logistic2_offset(1., 1., 2., 1., 2., 2., 1., 1.) == 0.5
        assert dlogistic(1., 1., 2., 1.) == 0.5
        assert dlogistic_offset(1., 1., 2., 1., 1.) == 0.5
        assert dlogistic2_offset(1., 1., 2., 1., 2., 2., 1., 1.) == -0.5
        assert np.around(d2logistic(1., 1., 2., 2.), 4) == 0.3199
        assert np.around(d2logistic_offset(1., 1., 2., 2., 1.), 4) == 0.3199
        assert (np.around(d2logistic2_offset(1., 1., 2., 2., 2., 2., 2., 1.),
                          4) == -0.3199)

        assert logistic_p(1., [1., 0., 2.]) == 0.5
        assert logistic_p(1., [1., 2., 1.]) == 0.5
        assert logistic_p(2., [1., 1., 1.]) == 1. / (1. + np.exp(-1.))
        assert logistic_offset_p(1., [1., 0., 2., 1.]) == 1.5
        assert logistic_offset_p(1., [1., 2., 1., 1.]) == 1.5
        assert (logistic_offset_p(2., [1., 1., 1., 1.]) ==
                1. / (1. + np.exp(-1.)) + 1.)
        assert logistic2_offset_p(1., [1., 2., 1., 2., 2., 1., 1.]) == 0.5
        assert dlogistic_p(1., [1., 2., 1.]) == 0.5
        assert dlogistic_offset_p(1., [1., 2., 1., 1.]) == 0.5
        assert dlogistic2_offset_p(1., [1., 2., 1., 2., 2., 1., 1.]) == -0.5
        assert np.around(d2logistic_p(1., [1., 2., 2.]), 4) == 0.3199
        assert (np.around(d2logistic_offset_p(1., [1., 2., 2., 1.]), 4)
                == 0.3199)
        assert (np.around(
            d2logistic2_offset_p(1., [1., 2., 2., 2., 2., 2., 1.]),
            4) == -0.3199)

        self.assertEqual(list(logistic(np.array([1., 1.]), 1., 0., 2.)),
                         [0.5, 0.5])

        ll = logistic(pd.Series([1., 1.]), 1., 0., 2.)
        self.assertEqual(list(ll), [0.5, 0.5])
        ll = logistic(pd.DataFrame([[1., 1.], [1., 1.]]), 1., 0., 2.)
        self.assertEqual(list(ll.to_numpy().flatten()), [0.5, 0.5, 0.5, 0.5])


if __name__ == "__main__":
    unittest.main()
