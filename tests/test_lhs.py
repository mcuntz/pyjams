#!/usr/bin/env python
"""
This is the unittest for lhs module.

python -m unittest -v tests/test_lhs.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_lhs.py

"""
import unittest
from pytest import raises as assert_raises


class TestLHS(unittest.TestCase):
    """
    Tests for lhs.py

    """
    def setUp(self):
        import numpy as np
        # seed for reproducible results
        seed = 1234
        np.random.seed(seed=seed)
        self.normparam = (50, 2)
        self.uniparam = (1, 5)  # for uniform (min, max-min)

    def test_lhs(self):
        import numpy as np
        import scipy.stats as stats
        from pyjams import lhs

        dist = [stats.norm, stats.uniform]
        pars = [self.normparam, self.uniparam]
        rnums = lhs(dist, pars, 2)

        self.assertEqual(rnums.shape, (2, 2))
        self.assertEqual(list(np.around(rnums[0, :], 3)),
                         [47.388, 51.764])
        self.assertEqual(list(np.around(rnums[1, :], 3)),
                         [2.094, 5.463])

        dist = stats.norm
        pars = self.normparam
        rnums = lhs(dist, pars, 2)

        self.assertEqual(rnums.shape, (2,))
        self.assertEqual(list(np.around(rnums, 3)),
                         [47.806, 50.707])

        # errors
        # no scipy distribution given
        assert_raises(TypeError, lhs, 'norm', self.normparam, 2)


if __name__ == "__main__":
    unittest.main()
