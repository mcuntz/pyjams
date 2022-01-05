#!/usr/bin/env python
"""
This is the unittest for esat module.

python -m unittest -v tests/test_esat.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_esat.py

"""
import unittest


class TestEsat(unittest.TestCase):
    """
    Tests for esat.py
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


if __name__ == "__main__":
    unittest.main()
