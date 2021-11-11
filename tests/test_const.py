#!/usr/bin/env python
"""
This is the unittest for the const module.

python -m unittest -v test_const.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_const.py

"""
from __future__ import division, absolute_import, print_function
import unittest


class TestConst(unittest.TestCase):
    """
    Tests for const/const.py

    """

    def test_const(self):
        import numpy as np
        from pyjams.const import Pi, pi, Pi2, pi2, Pi3, pi3
        from pyjams.const import TwoPi, Twopi, Sqrt2, Gravity, T0, P0, T25
        from pyjams.const import sigma, R, R_air, R_H2O, Na, REarth
        from pyjams.const import mmol_co2, mmol_h2o, mmol_air
        from pyjams.const import density_quartz, cheat_quartz, cheat_water
        from pyjams.const import cheat_air, latentheat_vaporization
        from pyjams.const import R13VPDB, R18VSMOW, R2VSMOW
        from pyjams.const import eps, huge, tiny

        self.assertEqual(np.around(Pi, 4), 3.1416)
        self.assertEqual(np.around(pi, 4), 3.1416)
        self.assertEqual(np.around(Pi2, 4), 1.5708)
        self.assertEqual(np.around(pi2, 4), 1.5708)
        self.assertEqual(np.around(Pi3, 4), 1.0472)
        self.assertEqual(np.around(pi3, 4), 1.0472)
        self.assertEqual(np.around(TwoPi, 4), 6.2832)
        self.assertEqual(np.around(Twopi, 4), 6.2832)
        self.assertEqual(np.around(Sqrt2, 4), 1.4142)
        self.assertEqual(Gravity, 9.81)
        self.assertEqual(T0, 273.15)
        self.assertEqual(P0, 101325.)
        self.assertEqual(T25, 298.15)
        self.assertEqual(sigma, 5.67e-08)
        self.assertEqual(np.around(R, 4), 8.3145)
        self.assertEqual(R_air, 287.06)
        self.assertEqual(R_H2O, 461.4)
        self.assertEqual(Na, 6.02214129e23)
        self.assertEqual(REarth, 6371009.)
        self.assertEqual(mmol_co2, 44.01)
        self.assertEqual(mmol_h2o, 18.01528)
        self.assertEqual(mmol_air, 28.9644)
        self.assertEqual(density_quartz, 2.65)
        self.assertEqual(cheat_quartz, 800.)
        self.assertEqual(cheat_water, 4180.)
        self.assertEqual(cheat_air, 1010.)
        self.assertEqual(latentheat_vaporization, 2.45e6)
        self.assertEqual(R13VPDB, 0.0112372)
        self.assertEqual(R18VSMOW, 2005.2e-6)
        self.assertEqual(R2VSMOW, 155.76e-6)
        self.assertEqual(eps, np.finfo(float).eps)
        self.assertEqual(huge, np.finfo(float).max)
        self.assertEqual(tiny, np.finfo(float).tiny)


if __name__ == "__main__":
    unittest.main()
