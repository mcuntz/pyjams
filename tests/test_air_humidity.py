#!/usr/bin/env python
"""
This is the unittest for esat module.

python -m unittest -v tests/test_air_humidity.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_air_humidity.py

"""
import unittest


class TestEsat(unittest.TestCase):
    """
    Tests for test_air_humidity.py
    """

    def test_esat(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import esat
        import warnings

        T0 = 273.15

        # scalar
        T1 = T0 + 20.
        assert isinstance(esat(T1), float)
        assert np.around(esat(T1), 3) == 2335.847
        T1 = T0 - 20.
        assert isinstance(esat(T1), float)
        assert np.around(esat(T1), 3) == 103.074

        # list - different formulas with different word cases
        T = [20., -20.]
        T1 = [ tt + T0 for tt in T ]
        assert isinstance(esat(T1), list)
        self.assertEqual(
            list(np.around(esat(T1), 3)),
            [2335.847, 103.074])
        self.assertEqual(
            list(np.around(esat(T1, formula='GoffGratch'), 3)),
            [2335.847, 103.074])
        self.assertEqual(
            list(np.around(esat(T1, formula='MartiMauersberger'), 3)),
            [2335.847, 103.650])
        self.assertEqual(
            list(np.around(esat(T1, formula='MagnusTeten'), 3)),
            [2335.201, 102.771])
        self.assertEqual(
            list(np.around(esat(T1, formula='buck'), 3)),
            [2338.340, 103.286])
        self.assertEqual(
            list(np.around(esat(T1, formula='Buck_original'), 3)),
            [2337.282, 103.267])
        self.assertEqual(
            list(np.around(esat(T1, formula='wmo'), 3)),
            [2337.080, 103.153])
        self.assertEqual(
            list(np.around(esat(T1, formula='WEXLER'), 3)),
            [2323.254, 103.074])
        self.assertEqual(
            list(np.around(esat(T1, formula='Sonntag'), 3)),
            [2339.249, 103.249])
        self.assertEqual(
            list(np.around(esat(T1, formula='Bolton'), 3)),
            [2336.947, 103.074])
        self.assertEqual(
            list(np.around(esat(T1, formula='Fukuta'), 3)),
            [2335.847, 103.074])
        self.assertEqual(
            list(np.around(esat(T1, formula='HylandWexler'), 3)),
            [2338.804, 103.260])
        self.assertEqual(
            list(np.around(esat(T1, formula='IAPWS'), 3)),
            [2339.194, 103.074])
        self.assertEqual(
            list(np.around(esat(T1, formula='MurphyKoop'), 3)),
            [2339.399, 103.252])

        # tuple
        T1 = tuple(T1)
        assert isinstance(esat(T1), tuple)
        # ndarray
        T  = np.array(T)
        T1 = T + T0
        assert isinstance(esat(T1), np.ndarray)
        # masked_array
        T1 = np.ma.array(T + T0, mask=(T == 20.))
        es = esat(T1)
        assert isinstance(es, np.ndarray)
        assert isinstance(es, np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(esat(T1), 3)),
            [masked, 103.074])

        # liquid
        T1 = [ tt + T0 for tt in T ]
        self.assertEqual(
            list(np.around(esat(T1, liquid=True), 3)),
            [2335.847, 125.292])
        self.assertEqual(
            list(np.around(esat(T1, formula='Fukuta', liquid=True), 3)),
            [2335.847, 125.079])

        # undef, scalar
        T1 = -9998.
        es = esat(T1, undef=-9998.)
        assert isinstance(es, float)
        self.assertEqual(es, -9998.)
        T1 = -9999.
        es = esat(T1)
        assert isinstance(es, float)
        self.assertEqual(es, -9999.)

        # undef, list
        T1 = [20. + T0, -9998.]
        es = esat(T1, undef=-9998.)
        assert isinstance(es, list)
        self.assertEqual(
            list(np.around(es, 3)),
            [2335.847, -9998.])
        T1 = [20. + T0, -9999.]
        es = esat(T1)
        assert isinstance(es, list)
        self.assertEqual(
            list(np.around(es, 3)),
            [2335.847, -9999.])

        # undef, tuple
        T1 = (20. + T0, -9998.)
        es = esat(T1, undef=-9998.)
        assert isinstance(es, tuple)
        self.assertEqual(
            list(np.around(es, 3)),
            [2335.847, -9998.])
        T1 = (20. + T0, -9999.)
        es = esat(T1)
        assert isinstance(es, tuple)
        self.assertEqual(
            list(np.around(es, 3)),
            [2335.847, -9999.])

        # undef, ndarray
        T1 = np.array([20. + T0, -9998.])
        es = esat(T1, undef=-9998.)
        assert isinstance(es, np.ndarray)
        self.assertEqual(
            list(np.around(es, 3)),
            [2335.847, -9998.])
        T1 = np.array([20. + T0, -9999.])
        es = esat(T1)
        assert isinstance(es, np.ndarray)
        self.assertEqual(
            list(np.around(es, 3)),
            [2335.847, -9999.])

        # undef, masked array
        T = np.array([20. + T0, -9998., -9999.])
        T1 = np.ma.array(T, mask=(T == -9999.))
        es = esat(T1, undef=-9998.)
        assert isinstance(es, np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(es, 3)),
            [2335.847, masked, masked])
        T = np.array([20. + T0, -9998., -9999.])
        T1 = np.ma.array(T, mask=(T == -9998.))
        es = esat(T1)
        assert isinstance(es, np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(es, 3)),
            [2335.847, masked, masked])

        # errors
        # T < 0
        T1 = T0 - T0
        self.assertRaises(AssertionError, esat, T1)
        # T > 373.15
        T1 = T0 + 101.
        self.assertRaises(AssertionError, esat, T1)
        # wrong formula
        T1 = T0 + 20.
        self.assertRaises(ValueError, esat, T1, formula='dummy')
        T1 = T0 - 20.
        self.assertRaises(ValueError, esat, T1, formula='dummy')

        # warning T < 100
        T1 = T0 - 200.
        with warnings.catch_warnings(record=True) as w:
            es = esat(T1)
            assert len(w) > 0

    def test_eair2rhair(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import eair2rhair

        eair = 1000.
        Ta = 293.15
        res2 = 42.81

        # scalar
        e1 = eair
        T1 = Ta
        assert isinstance(eair2rhair(e1, T1), float)
        assert np.around(eair2rhair(e1, T1) * 100., 2) == res2

        # list
        e1 = [eair, eair]
        T1 = Ta
        assert isinstance(eair2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in eair2rhair(e1, T1)], 2)),
            [res2, res2])
        e1 = eair
        T1 = [Ta, Ta]
        assert isinstance(eair2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in eair2rhair(e1, T1)], 2)),
            [res2, res2])
        e1 = [eair, eair]
        T1 = [Ta, Ta]
        assert isinstance(eair2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in eair2rhair(e1, T1)], 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        T1 = tuple(T1)
        assert isinstance(eair2rhair(e1, T1), tuple)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in eair2rhair(e1, T1)], 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        T1 = np.array(T1)
        assert isinstance(eair2rhair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(eair2rhair(e1, T1) * 100., 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        T1 = np.ma.array(T1)
        assert isinstance(eair2rhair(e1, T1), np.ndarray)
        assert isinstance(eair2rhair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2rhair(e1, T1) * 100., 2)),
            [res2, res2])

        # mixed types
        e1 = [eair, eair]
        T1 = tuple([Ta, Ta])
        assert isinstance(eair2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in eair2rhair(e1, T1)], 2)),
            [res2, res2])
        e1 = tuple([eair, eair])
        T1 = [Ta, Ta]
        assert isinstance(eair2rhair(e1, T1), tuple)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in eair2rhair(e1, T1)], 2)),
            [res2, res2])
        e1 = np.array(e1)
        T1 = [Ta, Ta]
        assert isinstance(eair2rhair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(eair2rhair(e1, T1) * 100., 2)),
            [res2, res2])
        e1 = [eair, eair]
        T1 = np.array(T1)
        assert isinstance(eair2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in eair2rhair(e1, T1)], 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        T1 = Ta
        assert isinstance(eair2rhair(e1, T1, undef=-9998.), float)
        assert np.around(eair2rhair(e1, T1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        T1 = Ta
        assert isinstance(eair2rhair(e1, T1), float)
        assert np.around(eair2rhair(e1, T1), 2) == -9999.
        e1 = eair
        T1 = -9999.
        assert isinstance(eair2rhair(e1, T1), float)
        assert np.around(eair2rhair(e1, T1), 2) == -9999.

        # undef, list
        e1 = [eair, -9999.]
        T1 = [Ta, Ta]
        assert isinstance(eair2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in eair2rhair(e1, T1)], 2)),
            [res2, -9999. * 100.])
        e1 = [eair, eair]
        T1 = [Ta, -9999.]
        assert isinstance(eair2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in eair2rhair(e1, T1)], 2)),
            [res2, -9999. * 100.])

        # undef, masked array
        e1 = np.ma.array([eair, -9998., -9999.])
        T1 = [Ta, Ta, Ta]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(eair2rhair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2rhair(e1, T1) * 100., 2)),
            [res2, masked, masked])
        e1 = [eair, eair, eair]
        T1 = np.ma.array([Ta, -9998., -9999.])
        T1 = np.ma.array(T1, mask=(T1 == -9998.))
        assert isinstance(eair2rhair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2rhair(e1, T1) * 100., 2)),
            [res2, masked, masked])

    def test_rhair2eair(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import rhair2eair

        rhair = 0.5
        Ta = 293.15
        res2 = 1167.92

        # scalar
        e1 = rhair
        T1 = Ta
        assert isinstance(rhair2eair(e1, T1), float)
        assert np.around(rhair2eair(e1, T1), 2) == res2

        # list
        e1 = [rhair, rhair]
        T1 = Ta
        assert isinstance(rhair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = rhair
        T1 = [Ta, Ta]
        assert isinstance(rhair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = [rhair, rhair]
        T1 = [Ta, Ta]
        assert isinstance(rhair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        T1 = tuple(T1)
        assert isinstance(rhair2eair(e1, T1), tuple)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        T1 = np.array(T1)
        assert isinstance(rhair2eair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        T1 = np.ma.array(T1)
        assert isinstance(rhair2eair(e1, T1), np.ndarray)
        assert isinstance(rhair2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])

        # mixed types
        e1 = [rhair, rhair]
        T1 = tuple([Ta, Ta])
        assert isinstance(rhair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = tuple([rhair, rhair])
        T1 = [Ta, Ta]
        assert isinstance(rhair2eair(e1, T1), tuple)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = np.array(e1)
        T1 = [Ta, Ta]
        assert isinstance(rhair2eair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = [rhair, rhair]
        T1 = np.array(T1)
        assert isinstance(rhair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        T1 = Ta
        assert isinstance(rhair2eair(e1, T1, undef=-9998.), float)
        assert np.around(rhair2eair(e1, T1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        T1 = Ta
        assert isinstance(rhair2eair(e1, T1), float)
        assert np.around(rhair2eair(e1, T1), 2) == -9999.
        e1 = rhair
        T1 = -9999.
        assert isinstance(rhair2eair(e1, T1), float)
        assert np.around(rhair2eair(e1, T1), 2) == -9999.

        # undef, list
        e1 = [rhair, -9999.]
        T1 = [Ta, Ta]
        assert isinstance(rhair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, -9999.])
        e1 = [rhair, rhair]
        T1 = [Ta, -9999.]
        assert isinstance(rhair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, -9999.])

        # undef, masked array
        e1 = np.ma.array([rhair, -9998., -9999.])
        T1 = [Ta, Ta, Ta]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(rhair2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, masked, masked])
        e1 = [rhair, rhair, rhair]
        T1 = np.ma.array([Ta, -9998., -9999.])
        T1 = np.ma.array(T1, mask=(T1 == -9998.))
        assert isinstance(rhair2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(rhair2eair(e1, T1), 2)),
            [res2, masked, masked])

    def test_eair2vpd(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import eair2vpd

        eair = 1000.
        Ta = 293.15
        res2 = 1335.85

        # scalar
        e1 = eair
        T1 = Ta
        assert isinstance(eair2vpd(e1, T1), float)
        assert np.around(eair2vpd(e1, T1), 2) == res2

        # list
        e1 = [eair, eair]
        T1 = Ta
        assert isinstance(eair2vpd(e1, T1), list)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])
        e1 = eair
        T1 = [Ta, Ta]
        assert isinstance(eair2vpd(e1, T1), list)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])
        e1 = [eair, eair]
        T1 = [Ta, Ta]
        assert isinstance(eair2vpd(e1, T1), list)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        T1 = tuple(T1)
        assert isinstance(eair2vpd(e1, T1), tuple)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        T1 = np.array(T1)
        assert isinstance(eair2vpd(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        T1 = np.ma.array(T1)
        assert isinstance(eair2vpd(e1, T1), np.ndarray)
        assert isinstance(eair2vpd(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])

        # mixed types
        e1 = [eair, eair]
        T1 = tuple([Ta, Ta])
        assert isinstance(eair2vpd(e1, T1), list)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])
        e1 = tuple([eair, eair])
        T1 = [Ta, Ta]
        assert isinstance(eair2vpd(e1, T1), tuple)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])
        e1 = np.array(e1)
        T1 = [Ta, Ta]
        assert isinstance(eair2vpd(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])
        e1 = [eair, eair]
        T1 = np.array(T1)
        assert isinstance(eair2vpd(e1, T1), list)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        T1 = Ta
        assert isinstance(eair2vpd(e1, T1, undef=-9998.), float)
        assert np.around(eair2vpd(e1, T1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        T1 = Ta
        assert isinstance(eair2vpd(e1, T1), float)
        assert np.around(eair2vpd(e1, T1), 2) == -9999.
        e1 = eair
        T1 = -9999.
        assert isinstance(eair2vpd(e1, T1), float)
        assert np.around(eair2vpd(e1, T1), 2) == -9999.

        # undef, list
        e1 = [eair, -9999.]
        T1 = [Ta, Ta]
        assert isinstance(eair2vpd(e1, T1), list)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, -9999.])
        e1 = [eair, eair]
        T1 = [Ta, -9999.]
        assert isinstance(eair2vpd(e1, T1), list)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, -9999.])

        # undef, masked array
        e1 = np.ma.array([eair, -9998., -9999.])
        T1 = [Ta, Ta, Ta]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(eair2vpd(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, masked, masked])
        e1 = [eair, eair, eair]
        T1 = np.ma.array([Ta, -9998., -9999.])
        T1 = np.ma.array(T1, mask=(T1 == -9998.))
        assert isinstance(eair2vpd(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2vpd(e1, T1), 2)),
            [res2, masked, masked])

    def test_vpd2eair(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import vpd2eair

        vpd = 1000.
        Ta = 293.15
        res2 = 1335.85

        # scalar
        e1 = vpd
        T1 = Ta
        assert isinstance(vpd2eair(e1, T1), float)
        assert np.around(vpd2eair(e1, T1), 2) == res2

        # list
        e1 = [vpd, vpd]
        T1 = Ta
        assert isinstance(vpd2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])
        e1 = vpd
        T1 = [Ta, Ta]
        assert isinstance(vpd2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])
        e1 = [vpd, vpd]
        T1 = [Ta, Ta]
        assert isinstance(vpd2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        T1 = tuple(T1)
        assert isinstance(vpd2eair(e1, T1), tuple)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        T1 = np.array(T1)
        assert isinstance(vpd2eair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        T1 = np.ma.array(T1)
        assert isinstance(vpd2eair(e1, T1), np.ndarray)
        assert isinstance(vpd2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])

        # mixed types
        e1 = [vpd, vpd]
        T1 = tuple([Ta, Ta])
        assert isinstance(vpd2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])
        e1 = tuple([vpd, vpd])
        T1 = [Ta, Ta]
        assert isinstance(vpd2eair(e1, T1), tuple)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])
        e1 = np.array(e1)
        T1 = [Ta, Ta]
        assert isinstance(vpd2eair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])
        e1 = [vpd, vpd]
        T1 = np.array(T1)
        assert isinstance(vpd2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        T1 = Ta
        assert isinstance(vpd2eair(e1, T1, undef=-9998.), float)
        assert np.around(vpd2eair(e1, T1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        T1 = Ta
        assert isinstance(vpd2eair(e1, T1), float)
        assert np.around(vpd2eair(e1, T1), 2) == -9999.
        e1 = vpd
        T1 = -9999.
        assert isinstance(vpd2eair(e1, T1), float)
        assert np.around(vpd2eair(e1, T1), 2) == -9999.

        # undef, list
        e1 = [vpd, -9999.]
        T1 = [Ta, Ta]
        assert isinstance(vpd2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, -9999.])
        e1 = [vpd, vpd]
        T1 = [Ta, -9999.]
        assert isinstance(vpd2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, -9999.])

        # undef, masked array
        e1 = np.ma.array([vpd, -9998., -9999.])
        T1 = [Ta, Ta, Ta]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(vpd2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, masked, masked])
        e1 = [vpd, vpd, vpd]
        T1 = np.ma.array([Ta, -9998., -9999.])
        T1 = np.ma.array(T1, mask=(T1 == -9998.))
        assert isinstance(vpd2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(vpd2eair(e1, T1), 2)),
            [res2, masked, masked])

    def test_rhair2vpd(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import rhair2vpd

        rhair = 0.5
        Ta = 293.15
        res2 = 1167.92

        # scalar
        rhair1 = rhair
        T1 = Ta
        assert isinstance(rhair2vpd(rhair1, T1), float)
        assert np.around(rhair2vpd(rhair1, T1), 2) == res2

        # list
        rhair1 = [rhair, rhair]
        T1 = Ta
        assert isinstance(rhair2vpd(rhair1, T1), list)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])
        rhair1 = rhair
        T1 = [Ta, Ta]
        assert isinstance(rhair2vpd(rhair1, T1), list)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])
        rhair1 = [rhair, rhair]
        T1 = [Ta, Ta]
        assert isinstance(rhair2vpd(rhair1, T1), list)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])

        # tuple
        rhair1 = tuple(rhair1)
        T1 = tuple(T1)
        assert isinstance(rhair2vpd(rhair1, T1), tuple)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])

        # ndarray
        rhair1 = np.array(rhair1)
        T1 = np.array(T1)
        assert isinstance(rhair2vpd(rhair1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])

        # masked_array
        rhair1 = np.ma.array(rhair1)
        T1 = np.ma.array(T1)
        assert isinstance(rhair2vpd(rhair1, T1), np.ndarray)
        assert isinstance(rhair2vpd(rhair1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])

        # mixed types
        rhair1 = [rhair, rhair]
        T1 = tuple([Ta, Ta])
        assert isinstance(rhair2vpd(rhair1, T1), list)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])
        rhair1 = tuple([rhair, rhair])
        T1 = [Ta, Ta]
        assert isinstance(rhair2vpd(rhair1, T1), tuple)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])
        rhair1 = np.array(rhair1)
        T1 = [Ta, Ta]
        assert isinstance(rhair2vpd(rhair1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])
        rhair1 = [rhair, rhair]
        T1 = np.array(T1)
        assert isinstance(rhair2vpd(rhair1, T1), list)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, res2])

        # undef, scalar
        rhair1 = -9998.
        T1 = Ta
        assert isinstance(rhair2vpd(rhair1, T1, undef=-9998.), float)
        assert np.around(rhair2vpd(rhair1, T1, undef=-9998.), 2) == -9998.
        rhair1 = -9999.
        T1 = Ta
        assert isinstance(rhair2vpd(rhair1, T1), float)
        assert np.around(rhair2vpd(rhair1, T1), 2) == -9999.
        rhair1 = rhair
        T1 = -9999.
        assert isinstance(rhair2vpd(rhair1, T1), float)
        assert np.around(rhair2vpd(rhair1, T1), 2) == -9999.

        # undef, list
        rhair1 = [rhair, -9999.]
        T1 = [Ta, Ta]
        assert isinstance(rhair2vpd(rhair1, T1), list)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, -9999.])
        rhair1 = [rhair, rhair]
        T1 = [Ta, -9999.]
        assert isinstance(rhair2vpd(rhair1, T1), list)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, -9999.])

        # undef, masked array
        rhair1 = np.ma.array([rhair, -9998., -9999.])
        T1 = [Ta, Ta, Ta]
        rhair1 = np.ma.array(rhair1, mask=(rhair1 == -9998.))
        assert isinstance(rhair2vpd(rhair1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, masked, masked])
        rhair1 = [rhair, rhair, rhair]
        T1 = np.ma.array([Ta, -9998., -9999.])
        T1 = np.ma.array(T1, mask=(T1 == -9998.))
        assert isinstance(rhair2vpd(rhair1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(rhair2vpd(rhair1, T1), 2)),
            [res2, masked, masked])

    def test_vpd2rhair(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import vpd2rhair

        vpd = 1000.
        Ta = 293.15
        res2 = 57.19

        # scalar
        e1 = vpd
        T1 = Ta
        assert isinstance(vpd2rhair(e1, T1), float)
        assert np.around(vpd2rhair(e1, T1) * 100., 2) == res2

        # list
        e1 = [vpd, vpd]
        T1 = Ta
        assert isinstance(vpd2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in vpd2rhair(e1, T1)], 2)),
            [res2, res2])
        e1 = vpd
        T1 = [Ta, Ta]
        assert isinstance(vpd2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in vpd2rhair(e1, T1)], 2)),
            [res2, res2])
        e1 = [vpd, vpd]
        T1 = [Ta, Ta]
        assert isinstance(vpd2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in vpd2rhair(e1, T1)], 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        T1 = tuple(T1)
        assert isinstance(vpd2rhair(e1, T1), tuple)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in vpd2rhair(e1, T1)], 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        T1 = np.array(T1)
        assert isinstance(vpd2rhair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(vpd2rhair(e1, T1) * 100., 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        T1 = np.ma.array(T1)
        assert isinstance(vpd2rhair(e1, T1), np.ndarray)
        assert isinstance(vpd2rhair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(vpd2rhair(e1, T1) * 100., 2)),
            [res2, res2])

        # mixed types
        e1 = [vpd, vpd]
        T1 = tuple([Ta, Ta])
        assert isinstance(vpd2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in vpd2rhair(e1, T1)], 2)),
            [res2, res2])
        e1 = tuple([vpd, vpd])
        T1 = [Ta, Ta]
        assert isinstance(vpd2rhair(e1, T1), tuple)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in vpd2rhair(e1, T1)], 2)),
            [res2, res2])
        e1 = np.array(e1)
        T1 = [Ta, Ta]
        assert isinstance(vpd2rhair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(vpd2rhair(e1, T1) * 100., 2)),
            [res2, res2])
        e1 = [vpd, vpd]
        T1 = np.array(T1)
        assert isinstance(vpd2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in vpd2rhair(e1, T1)], 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        T1 = Ta
        assert isinstance(vpd2rhair(e1, T1, undef=-9998.), float)
        assert np.around(vpd2rhair(e1, T1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        T1 = Ta
        assert isinstance(vpd2rhair(e1, T1), float)
        assert np.around(vpd2rhair(e1, T1), 2) == -9999.
        e1 = vpd
        T1 = -9999.
        assert isinstance(vpd2rhair(e1, T1), float)
        assert np.around(vpd2rhair(e1, T1), 2) == -9999.

        # undef, list
        e1 = [vpd, -9999.]
        T1 = [Ta, Ta]
        assert isinstance(vpd2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in vpd2rhair(e1, T1)], 2)),
            [res2, -9999. * 100.])
        e1 = [vpd, vpd]
        T1 = [Ta, -9999.]
        assert isinstance(vpd2rhair(e1, T1), list)
        self.assertEqual(
            list(np.around([ ee * 100. for ee in vpd2rhair(e1, T1)], 2)),
            [res2, -9999. * 100.])

        # undef, masked array
        e1 = np.ma.array([vpd, -9998., -9999.])
        T1 = [Ta, Ta, Ta]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(vpd2rhair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(vpd2rhair(e1, T1) * 100., 2)),
            [res2, masked, masked])
        e1 = [vpd, vpd, vpd]
        T1 = np.ma.array([Ta, -9998., -9999.])
        T1 = np.ma.array(T1, mask=(T1 == -9998.))
        assert isinstance(vpd2rhair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(vpd2rhair(e1, T1) * 100., 2)),
            [res2, masked, masked])

    def test_eair2shair(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import eair2shair

        eair = 1000.
        Pa = 101325.
        res2 = 6.16

        # scalar
        e1 = eair
        P1 = Pa
        assert isinstance(eair2shair(e1, P1), float)
        assert np.around(eair2shair(e1, P1) * 1000., 2) == res2

        # list
        e1 = [eair, eair]
        P1 = Pa
        assert isinstance(eair2shair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2shair(e1, P1)], 2)),
            [res2, res2])
        e1 = eair
        P1 = [Pa, Pa]
        assert isinstance(eair2shair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2shair(e1, P1)], 2)),
            [res2, res2])
        e1 = [eair, eair]
        P1 = [Pa, Pa]
        assert isinstance(eair2shair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2shair(e1, P1)], 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        P1 = tuple(P1)
        assert isinstance(eair2shair(e1, P1), tuple)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2shair(e1, P1)], 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        P1 = np.array(P1)
        assert isinstance(eair2shair(e1, P1), np.ndarray)
        self.assertEqual(
            list(np.around(eair2shair(e1, P1) * 1000., 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        P1 = np.ma.array(P1)
        assert isinstance(eair2shair(e1, P1), np.ndarray)
        assert isinstance(eair2shair(e1, P1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2shair(e1, P1) * 1000., 2)),
            [res2, res2])

        # mixed types
        e1 = [eair, eair]
        P1 = tuple([Pa, Pa])
        assert isinstance(eair2shair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2shair(e1, P1)], 2)),
            [res2, res2])
        e1 = tuple([eair, eair])
        P1 = [Pa, Pa]
        assert isinstance(eair2shair(e1, P1), tuple)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2shair(e1, P1)], 2)),
            [res2, res2])
        e1 = np.array(e1)
        P1 = [Pa, Pa]
        assert isinstance(eair2shair(e1, P1), np.ndarray)
        self.assertEqual(
            list(np.around(eair2shair(e1, P1) * 1000., 2)),
            [res2, res2])
        e1 = [eair, eair]
        P1 = np.array(P1)
        assert isinstance(eair2shair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2shair(e1, P1)], 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        P1 = Pa
        assert isinstance(eair2shair(e1, P1, undef=-9998.), float)
        assert np.around(eair2shair(e1, P1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        P1 = Pa
        assert isinstance(eair2shair(e1, P1), float)
        assert np.around(eair2shair(e1, P1), 2) == -9999.
        e1 = eair
        P1 = -9999.
        assert isinstance(eair2shair(e1, P1), float)
        assert np.around(eair2shair(e1, P1), 2) == -9999.

        # undef, list
        e1 = [eair, -9999.]
        P1 = [Pa, Pa]
        assert isinstance(eair2shair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2shair(e1, P1)], 2)),
            [res2, -9999. * 1000.])
        e1 = [eair, eair]
        P1 = [Pa, -9999.]
        assert isinstance(eair2shair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2shair(e1, P1)], 2)),
            [res2, -9999. * 1000.])

        # undef, masked array
        e1 = np.ma.array([eair, -9998., -9999.])
        P1 = [Pa, Pa, Pa]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(eair2shair(e1, P1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2shair(e1, P1) * 1000., 2)),
            [res2, masked, masked])
        e1 = [eair, eair, eair]
        P1 = np.ma.array([Pa, -9998., -9999.])
        P1 = np.ma.array(P1, mask=(P1 == -9998.))
        assert isinstance(eair2shair(e1, P1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2shair(e1, P1) * 1000., 2)),
            [res2, masked, masked])

    def test_shair2eair(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import shair2eair

        shair = 0.006
        Pa = 101325.
        res2 = 973.89

        # scalar
        e1 = shair
        T1 = Pa
        assert isinstance(shair2eair(e1, T1), float)
        assert np.around(shair2eair(e1, T1), 2) == res2

        # list
        e1 = [shair, shair]
        T1 = Pa
        assert isinstance(shair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = shair
        T1 = [Pa, Pa]
        assert isinstance(shair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = [shair, shair]
        T1 = [Pa, Pa]
        assert isinstance(shair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        T1 = tuple(T1)
        assert isinstance(shair2eair(e1, T1), tuple)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        T1 = np.array(T1)
        assert isinstance(shair2eair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        T1 = np.ma.array(T1)
        assert isinstance(shair2eair(e1, T1), np.ndarray)
        assert isinstance(shair2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])

        # mixed types
        e1 = [shair, shair]
        T1 = tuple([Pa, Pa])
        assert isinstance(shair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = tuple([shair, shair])
        T1 = [Pa, Pa]
        assert isinstance(shair2eair(e1, T1), tuple)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = np.array(e1)
        T1 = [Pa, Pa]
        assert isinstance(shair2eair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = [shair, shair]
        T1 = np.array(T1)
        assert isinstance(shair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        T1 = Pa
        assert isinstance(shair2eair(e1, T1, undef=-9998.), float)
        assert np.around(shair2eair(e1, T1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        T1 = Pa
        assert isinstance(shair2eair(e1, T1), float)
        assert np.around(shair2eair(e1, T1), 2) == -9999.
        e1 = shair
        T1 = -9999.
        assert isinstance(shair2eair(e1, T1), float)
        assert np.around(shair2eair(e1, T1), 2) == -9999.

        # undef, list
        e1 = [shair, -9999.]
        T1 = [Pa, Pa]
        assert isinstance(shair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, -9999.])
        e1 = [shair, shair]
        T1 = [Pa, -9999.]
        assert isinstance(shair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, -9999.])

        # undef, masked array
        e1 = np.ma.array([shair, -9998., -9999.])
        T1 = [Pa, Pa, Pa]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(shair2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, masked, masked])
        e1 = [shair, shair, shair]
        T1 = np.ma.array([Pa, -9998., -9999.])
        T1 = np.ma.array(T1, mask=(T1 == -9998.))
        assert isinstance(shair2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(shair2eair(e1, T1), 2)),
            [res2, masked, masked])

    def test_eair2mrair(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import eair2mrair

        eair = 1000.
        Pa = 101325.
        res2 = 6.2

        # scalar
        e1 = eair
        P1 = Pa
        assert isinstance(eair2mrair(e1, P1), float)
        assert np.around(eair2mrair(e1, P1) * 1000., 2) == res2

        # list
        e1 = [eair, eair]
        P1 = Pa
        assert isinstance(eair2mrair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2mrair(e1, P1)], 2)),
            [res2, res2])
        e1 = eair
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2mrair(e1, P1)], 2)),
            [res2, res2])
        e1 = [eair, eair]
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2mrair(e1, P1)], 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        P1 = tuple(P1)
        assert isinstance(eair2mrair(e1, P1), tuple)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2mrair(e1, P1)], 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        P1 = np.array(P1)
        assert isinstance(eair2mrair(e1, P1), np.ndarray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1) * 1000., 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        P1 = np.ma.array(P1)
        assert isinstance(eair2mrair(e1, P1), np.ndarray)
        assert isinstance(eair2mrair(e1, P1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1) * 1000., 2)),
            [res2, res2])

        # mixed types
        e1 = [eair, eair]
        P1 = tuple([Pa, Pa])
        assert isinstance(eair2mrair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2mrair(e1, P1)], 2)),
            [res2, res2])
        e1 = tuple([eair, eair])
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1), tuple)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2mrair(e1, P1)], 2)),
            [res2, res2])
        e1 = np.array(e1)
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1), np.ndarray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1) * 1000., 2)),
            [res2, res2])
        e1 = [eair, eair]
        P1 = np.array(P1)
        assert isinstance(eair2mrair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2mrair(e1, P1)], 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        P1 = Pa
        assert isinstance(eair2mrair(e1, P1, undef=-9998.), float)
        assert np.around(eair2mrair(e1, P1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        P1 = Pa
        assert isinstance(eair2mrair(e1, P1), float)
        assert np.around(eair2mrair(e1, P1), 2) == -9999.
        e1 = eair
        P1 = -9999.
        assert isinstance(eair2mrair(e1, P1), float)
        assert np.around(eair2mrair(e1, P1), 2) == -9999.

        # undef, list
        e1 = [eair, -9999.]
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2mrair(e1, P1)], 2)),
            [res2, -9999. * 1000.])
        e1 = [eair, eair]
        P1 = [Pa, -9999.]
        assert isinstance(eair2mrair(e1, P1), list)
        self.assertEqual(
            list(np.around([ ee * 1000. for ee in eair2mrair(e1, P1)], 2)),
            [res2, -9999. * 1000.])

        # undef, masked array
        e1 = np.ma.array([eair, -9998., -9999.])
        P1 = [Pa, Pa, Pa]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(eair2mrair(e1, P1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1) * 1000., 2)),
            [res2, masked, masked])
        e1 = [eair, eair, eair]
        P1 = np.ma.array([Pa, -9998., -9999.])
        P1 = np.ma.array(P1, mask=(P1 == -9998.))
        assert isinstance(eair2mrair(e1, P1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1) * 1000., 2)),
            [res2, masked, masked])

        # mol = True

        eair = 1000.
        Pa = 101325.
        res2 = 9.97

        # scalar
        e1 = eair
        P1 = Pa
        assert isinstance(eair2mrair(e1, P1, mol=True), float)
        assert np.around(eair2mrair(e1, P1, mol=True) * 1000., 2) == res2

        # list
        e1 = [eair, eair]
        P1 = Pa
        assert isinstance(eair2mrair(e1, P1, mol=True), list)
        self.assertEqual(
            list(np.around([ ee * 1000.
                             for ee in eair2mrair(e1, P1, mol=True)], 2)),
            [res2, res2])
        e1 = eair
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1, mol=True), list)
        self.assertEqual(
            list(np.around([ ee * 1000.
                             for ee in eair2mrair(e1, P1, mol=True)], 2)),
            [res2, res2])
        e1 = [eair, eair]
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1, mol=True), list)
        self.assertEqual(
            list(np.around([ ee * 1000.
                             for ee in eair2mrair(e1, P1, mol=True)], 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        P1 = tuple(P1)
        assert isinstance(eair2mrair(e1, P1, mol=True), tuple)
        self.assertEqual(
            list(np.around([ ee * 1000.
                             for ee in eair2mrair(e1, P1, mol=True)], 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        P1 = np.array(P1)
        assert isinstance(eair2mrair(e1, P1, mol=True), np.ndarray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1, mol=True) * 1000., 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        P1 = np.ma.array(P1)
        assert isinstance(eair2mrair(e1, P1, mol=True), np.ndarray)
        assert isinstance(eair2mrair(e1, P1, mol=True), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1, mol=True) * 1000., 2)),
            [res2, res2])

        # mixed types
        e1 = [eair, eair]
        P1 = tuple([Pa, Pa])
        assert isinstance(eair2mrair(e1, P1, mol=True), list)
        self.assertEqual(
            list(np.around([ ee * 1000.
                             for ee in eair2mrair(e1, P1, mol=True)], 2)),
            [res2, res2])
        e1 = tuple([eair, eair])
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1, mol=True), tuple)
        self.assertEqual(
            list(np.around([ ee * 1000.
                             for ee in eair2mrair(e1, P1, mol=True)], 2)),
            [res2, res2])
        e1 = np.array(e1)
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1, mol=True), np.ndarray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1, mol=True) * 1000., 2)),
            [res2, res2])
        e1 = [eair, eair]
        P1 = np.array(P1)
        assert isinstance(eair2mrair(e1, P1, mol=True), list)
        self.assertEqual(
            list(np.around([ ee * 1000.
                             for ee in eair2mrair(e1, P1, mol=True)], 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        P1 = Pa
        assert isinstance(eair2mrair(e1, P1, undef=-9998.), float)
        assert np.around(eair2mrair(e1, P1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        P1 = Pa
        assert isinstance(eair2mrair(e1, P1, mol=True), float)
        assert np.around(eair2mrair(e1, P1, mol=True), 2) == -9999.
        e1 = eair
        P1 = -9999.
        assert isinstance(eair2mrair(e1, P1, mol=True), float)
        assert np.around(eair2mrair(e1, P1, mol=True), 2) == -9999.

        # undef, list
        e1 = [eair, -9999.]
        P1 = [Pa, Pa]
        assert isinstance(eair2mrair(e1, P1, mol=True), list)
        self.assertEqual(
            list(np.around([ ee * 1000.
                             for ee in eair2mrair(e1, P1, mol=True)], 2)),
            [res2, -9999. * 1000.])
        e1 = [eair, eair]
        P1 = [Pa, -9999.]
        assert isinstance(eair2mrair(e1, P1, mol=True), list)
        self.assertEqual(
            list(np.around([ ee * 1000.
                             for ee in eair2mrair(e1, P1, mol=True)], 2)),
            [res2, -9999. * 1000.])

        # undef, masked array
        e1 = np.ma.array([eair, -9998., -9999.])
        P1 = [Pa, Pa, Pa]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(eair2mrair(e1, P1, mol=True), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1, mol=True) * 1000., 2)),
            [res2, masked, masked])
        e1 = [eair, eair, eair]
        P1 = np.ma.array([Pa, -9998., -9999.])
        P1 = np.ma.array(P1, mask=(P1 == -9998.))
        assert isinstance(eair2mrair(e1, P1, mol=True), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(eair2mrair(e1, P1, mol=True) * 1000., 2)),
            [res2, masked, masked])

    def test_mrair2eair(self):
        import numpy as np
        from numpy.ma import masked
        from pyjams import mrair2eair

        mrair = 0.006
        Pa = 101325.
        res2 = 968.10

        # scalar
        e1 = mrair
        T1 = Pa
        assert isinstance(mrair2eair(e1, T1), float)
        assert np.around(mrair2eair(e1, T1), 2) == res2

        # list
        e1 = [mrair, mrair]
        T1 = Pa
        assert isinstance(mrair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = mrair
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = [mrair, mrair]
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        T1 = tuple(T1)
        assert isinstance(mrair2eair(e1, T1), tuple)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        T1 = np.array(T1)
        assert isinstance(mrair2eair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        T1 = np.ma.array(T1)
        assert isinstance(mrair2eair(e1, T1), np.ndarray)
        assert isinstance(mrair2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])

        # mixed types
        e1 = [mrair, mrair]
        T1 = tuple([Pa, Pa])
        assert isinstance(mrair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = tuple([mrair, mrair])
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1), tuple)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = np.array(e1)
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1), np.ndarray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])
        e1 = [mrair, mrair]
        T1 = np.array(T1)
        assert isinstance(mrair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        T1 = Pa
        assert isinstance(mrair2eair(e1, T1, undef=-9998.), float)
        assert np.around(mrair2eair(e1, T1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        T1 = Pa
        assert isinstance(mrair2eair(e1, T1), float)
        assert np.around(mrair2eair(e1, T1), 2) == -9999.
        e1 = mrair
        T1 = -9999.
        assert isinstance(mrair2eair(e1, T1), float)
        assert np.around(mrair2eair(e1, T1), 2) == -9999.

        # undef, list
        e1 = [mrair, -9999.]
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, -9999.])
        e1 = [mrair, mrair]
        T1 = [Pa, -9999.]
        assert isinstance(mrair2eair(e1, T1), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, -9999.])

        # undef, masked array
        e1 = np.ma.array([mrair, -9998., -9999.])
        T1 = [Pa, Pa, Pa]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(mrair2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, masked, masked])
        e1 = [mrair, mrair, mrair]
        T1 = np.ma.array([Pa, -9998., -9999.])
        T1 = np.ma.array(T1, mask=(T1 == -9998.))
        assert isinstance(mrair2eair(e1, T1), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1), 2)),
            [res2, masked, masked])

        # mol = True

        mrair = 0.006
        Pa = 101325.
        res2 = 604.32

        # scalar
        e1 = mrair
        T1 = Pa
        assert isinstance(mrair2eair(e1, T1, mol=True), float)
        assert np.around(mrair2eair(e1, T1, mol=True), 2) == res2

        # list
        e1 = [mrair, mrair]
        T1 = Pa
        assert isinstance(mrair2eair(e1, T1, mol=True), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])
        e1 = mrair
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1, mol=True), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])
        e1 = [mrair, mrair]
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1, mol=True), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])

        # tuple
        e1 = tuple(e1)
        T1 = tuple(T1)
        assert isinstance(mrair2eair(e1, T1, mol=True), tuple)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])

        # ndarray
        e1 = np.array(e1)
        T1 = np.array(T1)
        assert isinstance(mrair2eair(e1, T1, mol=True), np.ndarray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])

        # masked_array
        e1 = np.ma.array(e1)
        T1 = np.ma.array(T1)
        assert isinstance(mrair2eair(e1, T1, mol=True), np.ndarray)
        assert isinstance(mrair2eair(e1, T1, mol=True), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])

        # mixed types
        e1 = [mrair, mrair]
        T1 = tuple([Pa, Pa])
        assert isinstance(mrair2eair(e1, T1, mol=True), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])
        e1 = tuple([mrair, mrair])
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1, mol=True), tuple)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])
        e1 = np.array(e1)
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1, mol=True), np.ndarray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])
        e1 = [mrair, mrair]
        T1 = np.array(T1)
        assert isinstance(mrair2eair(e1, T1, mol=True), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, res2])

        # undef, scalar
        e1 = -9998.
        T1 = Pa
        assert isinstance(mrair2eair(e1, T1, undef=-9998.), float)
        assert np.around(mrair2eair(e1, T1, undef=-9998.), 2) == -9998.
        e1 = -9999.
        T1 = Pa
        assert isinstance(mrair2eair(e1, T1, mol=True), float)
        assert np.around(mrair2eair(e1, T1, mol=True), 2) == -9999.
        e1 = mrair
        T1 = -9999.
        assert isinstance(mrair2eair(e1, T1, mol=True), float)
        assert np.around(mrair2eair(e1, T1, mol=True), 2) == -9999.

        # undef, list
        e1 = [mrair, -9999.]
        T1 = [Pa, Pa]
        assert isinstance(mrair2eair(e1, T1, mol=True), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, -9999.])
        e1 = [mrair, mrair]
        T1 = [Pa, -9999.]
        assert isinstance(mrair2eair(e1, T1, mol=True), list)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, -9999.])

        # undef, masked array
        e1 = np.ma.array([mrair, -9998., -9999.])
        T1 = [Pa, Pa, Pa]
        e1 = np.ma.array(e1, mask=(e1 == -9998.))
        assert isinstance(mrair2eair(e1, T1, mol=True), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, masked, masked])
        e1 = [mrair, mrair, mrair]
        T1 = np.ma.array([Pa, -9998., -9999.])
        T1 = np.ma.array(T1, mask=(T1 == -9998.))
        assert isinstance(mrair2eair(e1, T1, mol=True), np.ma.MaskedArray)
        self.assertEqual(
            list(np.around(mrair2eair(e1, T1, mol=True), 2)),
            [res2, masked, masked])


if __name__ == "__main__":
    unittest.main()
