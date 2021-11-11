#!/usr/bin/env python
"""
This is the unittest for the Fit Functions module.

python -m unittest -v tests/test_fit_functions.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_fit_functions.py

"""
from __future__ import division, absolute_import, print_function
import unittest


class TestFitFunctions(unittest.TestCase):
    """
    Tests for functions/logistic_function.py
    Missing coverage:
        ca. 200ff: exception for import at different levels

    """

    def test_cost_abs_square(self):
        import numpy as np
        from pyjams.functions import logistic_p, cost_logistic, cost2_logistic
        from pyjams.functions import cost_abs, cost_square

        p = [1., 1., 0.]
        x = np.arange(2)
        y = np.zeros(2)
        self.assertEqual(cost_logistic(p, x, y),
                         cost_abs(p, logistic_p, x, y))
        self.assertEqual(cost2_logistic(p, x, y),
                         cost_square(p, logistic_p, x, y))

    def test_arrhenius(self):
        import numpy as np
        from pyjams.functions import arrhenius, arrhenius_p, cost_arrhenius
        from pyjams.functions import cost2_arrhenius

        T25 = 298.15
        R   = 8.3144621
        p = [1.]
        x = np.arange(2) + 25.
        y = np.zeros(2)
        out = np.exp(np.arange(2) / (T25 * R * (np.arange(2)+T25)))
        self.assertEqual(list(arrhenius(x, *p)), list(out))
        self.assertEqual(list(arrhenius_p(x, p)), list(out))
        self.assertEqual(cost_arrhenius(p, x, y), np.sum(out))
        self.assertEqual(cost2_arrhenius(p, x, y), np.sum(out**2))

    def test_f1x(self):
        import numpy as np
        from pyjams.functions import f1x, f1x_p, cost_f1x, cost2_f1x

        p = [0., 2.]
        x = np.arange(2) + 1.
        y = np.zeros(2)
        out = 2. / x
        self.assertEqual(list(f1x(x, *p)), list(out))
        self.assertEqual(list(f1x_p(x, p)), list(out))
        self.assertEqual(cost_f1x(p, x, y), np.sum(out))
        self.assertEqual(cost2_f1x(p, x, y), np.sum(out**2))

    def test_fexp(self):
        import numpy as np
        from pyjams.functions import fexp, fexp_p, cost_fexp, cost2_fexp

        p = [0., 1., 1.]
        x = np.arange(2)
        y = np.zeros(2)
        out = np.exp(x)
        self.assertEqual(list(fexp(x, *p)), list(out))
        self.assertEqual(list(fexp_p(x, p)), list(out))
        self.assertEqual(cost_fexp(p, x, y), np.sum(out))
        self.assertEqual(cost2_fexp(p, x, y), np.sum(out**2))

    def test_fgauss(self):
        import numpy as np
        from pyjams.functions import gauss, gauss_p, cost_gauss, cost2_gauss

        p = [1., 1.]
        x = np.arange(2)
        y = np.zeros(2)
        out = 1. / np.sqrt(2.*np.pi) * np.exp(-np.abs(x-1.)/2.)
        self.assertEqual(list(gauss(x, *p)), list(out))
        self.assertEqual(list(gauss_p(x, p)), list(out))
        self.assertEqual(cost_gauss(p, x, y), np.sum(out))
        self.assertEqual(cost2_gauss(p, x, y), np.sum(out**2))

    def test_lasslop(self):
        import numpy as np
        from pyjams.functions import lasslop, lasslop_p, cost_lasslop
        from pyjams.functions import cost2_lasslop

        p = [1., 1., 1., 1.]
        Rg = np.arange(2) * 1000.
        et = np.arange(2)
        VPD = np.arange(2) * 10. + 1000.
        y = np.zeros(2)
        beta = np.array([1., np.exp(-10.)])
        out = et - beta*Rg/(Rg+beta)
        self.assertEqual(list(lasslop(Rg, et, VPD, *p)), list(out))
        self.assertEqual(list(lasslop_p(Rg, et, VPD, p)), list(out))
        self.assertEqual(cost_lasslop(p, Rg, et, VPD, y), np.sum(out))
        self.assertEqual(cost2_lasslop(p, Rg, et, VPD, y), np.sum(out**2))

    def test_line(self):
        import numpy as np
        from pyjams.functions import line, line_p, cost_line, cost2_line

        p = [0., 1.]
        x = np.arange(2)
        y = np.zeros(2)
        out = np.arange(2)
        self.assertEqual(list(line(x, *p)), list(out))
        self.assertEqual(list(line_p(x, p)), list(out))
        self.assertEqual(cost_line(p, x, y), np.sum(out))
        self.assertEqual(cost2_line(p, x, y), np.sum(out**2))

    def test_line0(self):
        import numpy as np
        from pyjams.functions import line0, line0_p, cost_line0, cost2_line0

        p = [1.]
        x = np.arange(2)
        y = np.zeros(2)
        out = np.arange(2)
        self.assertEqual(list(line0(x, *p)), list(out))
        self.assertEqual(list(line0_p(x, p)), list(out))
        self.assertEqual(cost_line0(p, x, y), np.sum(out))
        self.assertEqual(cost2_line0(p, x, y), np.sum(out**2))

    def test_lloyd_fix(self):
        import numpy as np
        from pyjams.functions import lloyd_fix, lloyd_fix_p, cost_lloyd_fix
        from pyjams.functions import cost2_lloyd_fix

        p = [1., 1.]
        x = np.arange(2) + 273.15
        y = np.zeros(2)
        out = np.exp(1./56.02 - 1./(x-227.13))
        self.assertEqual(list(lloyd_fix(x, *p)), list(out))
        self.assertEqual(list(lloyd_fix_p(x, p)), list(out))
        self.assertEqual(cost_lloyd_fix(p, x, y), np.sum(out))
        self.assertEqual(cost2_lloyd_fix(p, x, y), np.sum(out**2))

    def test_lloyd_only_rref(self):
        import numpy as np
        from pyjams.functions import lloyd_only_rref, lloyd_only_rref_p
        from pyjams.functions import cost_lloyd_only_rref
        from pyjams.functions import cost2_lloyd_only_rref

        p = [2.]
        x = np.arange(2)
        y = np.zeros(2)
        out = 2. * np.arange(2)
        self.assertEqual(list(lloyd_only_rref(x, *p)), list(out))
        self.assertEqual(list(lloyd_only_rref_p(x, p)), list(out))
        self.assertEqual(cost_lloyd_only_rref(p, x, y), np.sum(out))
        self.assertEqual(cost2_lloyd_only_rref(p, x, y), np.sum(out**2))

    def test_logistic(self):
        import numpy as np
        from pyjams.functions import logistic, logistic_p, cost_logistic
        from pyjams.functions import cost2_logistic

        p = [1., 1., 0.]
        x = np.arange(2)
        y = np.zeros(2)
        out = 1. / (1. + np.exp(-x))
        self.assertEqual(list(logistic(x, *p)), list(out))
        self.assertEqual(list(logistic_p(x, p)), list(out))
        self.assertEqual(cost_logistic(p, x, y), np.sum(out))
        self.assertEqual(cost2_logistic(p, x, y), np.sum(out**2))

    def test_logistic_offset(self):
        import numpy as np
        from pyjams.functions import logistic_offset, logistic_offset_p
        from pyjams.functions import cost_logistic_offset
        from pyjams.functions import cost2_logistic_offset

        p = [1., 1., 0., 1.]
        x = np.arange(2)
        y = np.zeros(2)
        out = 1. / (1. + np.exp(-x)) + 1.
        self.assertEqual(list(logistic_offset(x, *p)), list(out))
        self.assertEqual(list(logistic_offset_p(x, p)), list(out))
        self.assertEqual(cost_logistic_offset(p, x, y), np.sum(out))
        self.assertEqual(cost2_logistic_offset(p, x, y), np.sum(out**2))

    def test_logistic2_offset(self):
        import numpy as np
        from pyjams.functions import logistic2_offset, logistic2_offset_p
        from pyjams.functions import cost_logistic2_offset
        from pyjams.functions import cost2_logistic2_offset

        p = [1., 1., 0., 1., 2., 0., 1.]
        x = np.arange(2)
        y = np.zeros(2)
        out = 1. / (1. + np.exp(-x)) - 1. / (1. + np.exp(-2.*x)) + 1.
        self.assertEqual(list(logistic2_offset(x, *p)), list(out))
        self.assertEqual(list(logistic2_offset_p(x, p)), list(out))
        self.assertEqual(cost_logistic2_offset(p, x, y), np.sum(out))
        self.assertEqual(cost2_logistic2_offset(p, x, y), np.sum(out**2))

    def test_poly(self):
        import numpy as np
        from pyjams.functions import poly, poly_p, cost_poly, cost2_poly

        p = [0., 1., 2., 3]
        x = np.arange(2)
        y = np.zeros(2)
        out = 0. + 1. * x + 2. * x**2 + 3. * x**3
        self.assertEqual(list(poly(x, *p)), list(out))
        self.assertEqual(list(poly_p(x, p)), list(out))
        self.assertEqual(cost_poly(p, x, y), np.sum(out))
        self.assertEqual(cost2_poly(p, x, y), np.sum(out**2))

    def test_sabx(self):
        import numpy as np
        from pyjams.functions import sabx, sabx_p, cost_sabx, cost2_sabx

        p = [0., 2.]
        x = np.arange(2) + 1.
        y = np.zeros(2)
        out = np.sqrt(2. / x)
        self.assertEqual(list(sabx(x, *p)), list(out))
        self.assertEqual(list(sabx_p(x, p)), list(out))
        self.assertEqual(cost_sabx(p, x, y), np.sum(out))
        self.assertEqual(cost2_sabx(p, x, y), np.sum(out**2))

    def test_see(self):
        import numpy as np
        from pyjams.functions import see, see_p, cost_see, cost2_see

        p = [1., 1., 2.]
        x = np.arange(2) + 0.5
        y = np.zeros(2)
        out = np.array([0., 0.25])
        self.assertEqual(list(see(x, *p)), list(out))
        self.assertEqual(list(see_p(x, p)), list(out))
        self.assertEqual(cost_see(p, x, y), np.sum(out))
        self.assertEqual(cost2_see(p, x, y), np.sum(out**2))


if __name__ == "__main__":
    unittest.main()
