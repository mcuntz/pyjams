#!/usr/bin/env python
"""
This is the unittest for esat module.

python -m unittest -v tests/test_air_humidity.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_air_humidity.py

"""
import unittest
import numpy as np
from numpy.ma import masked
import pandas as pd


def _flatten(itr, decimals=0):
    if isinstance(itr, np.ma.MaskedArray):
        fitr = np.ma.around(np.ma.array(itr).flatten(), decimals)
    else:
        fitr = np.around(np.array(itr).flatten(), decimals)
    if len(fitr) == 0:
        return list(fitr)
    else:
        if isinstance(fitr[0], str):
            return [ i for i in fitr ]
        else:
            return list(fitr)


class TestEsat(unittest.TestCase):
    """
    Tests for test_air_humidity.py
    """

    def test_esat(self):
        from pyjams import esat
        import warnings

        T0 = 273.15
        T = np.array([20., -20.])
        res = [2335.847, 103.074]

        # scalar
        T1 = T0 + 20.
        assert isinstance(esat(T1), float)
        assert np.around(esat(T1), 3) == 2335.847
        T1 = T0 - 20.
        assert isinstance(esat(T1), float)
        assert np.around(esat(T1), 3) == 103.074

        # list - different formulas with different word cases
        T1 = [ tt + T0 for tt in T ]
        assert isinstance(esat(T1), list)
        es = esat(T1)
        self.assertEqual(_flatten(es, 3), res)
        formulas = {'GoffGratch': res,
                    'MartiMauersberger': [2335.847, 103.650],
                    'MagnusTeten': [2335.201, 102.771],
                    'buck': [2338.340, 103.286],
                    'Buck_original': [2337.282, 103.267],
                    'wmo': [2337.080, 103.153],
                    'WEXLER': [2323.254, 103.074],
                    'Sonntag': [2339.249, 103.249],
                    'Bolton': [2336.947, 103.074],
                    'Fukuta': [2335.847, 103.074],
                    'HylandWexler': [2338.804, 103.260],
                    'IAPWS': [2339.194, 103.074],
                    'MurphyKoop': [2339.399, 103.252]}
        for ff in formulas:
            es = esat(T1, formula=ff)
            self.assertEqual(_flatten(es, 3), formulas[ff])

        # tuple
        T1 = tuple([ tt + T0 for tt in T ])
        es = esat(T1)
        assert isinstance(es, tuple)
        self.assertEqual(_flatten(es, 3), res)
        # ndarray
        T1 = np.vstack([T, T]) + T0
        res2 = res[:]
        res2.extend(res)
        es = esat(T1)
        assert isinstance(esat(T1), np.ndarray)
        self.assertEqual(_flatten(es, 3), res2)
        # masked_array
        T1 = np.ma.array(T + T0, mask=(T == 20.))
        es = esat(T1)
        assert isinstance(es, np.ndarray)
        assert isinstance(es, np.ma.MaskedArray)
        self.assertEqual(_flatten(es, 3), [masked, 103.074])
        # pandas.Series
        T1 = [ tt + T0 for tt in T ]
        d1 = [pd.to_datetime('2020-06-01 12:30'),
              pd.to_datetime('2020-09-03 16:00')]
        df = pd.Series(T1)
        df.index = d1
        es = esat(df)
        assert isinstance(es, pd.Series)
        self.assertEqual(_flatten(es.values, 3), res)
        # pandas.DataFrame
        T1 = np.vstack([T, T]) + T0
        res2 = res[:]
        res2.extend(res)
        d1 = [pd.to_datetime('2020-06-01 12:30'),
              pd.to_datetime('2020-09-03 16:00')]
        df = pd.DataFrame(T1)
        df.index = d1
        es = esat(df)
        assert isinstance(es, pd.DataFrame)
        self.assertEqual(_flatten(es.values.flatten(), 3), res2)

        # liquid
        T1 = [ tt + T0 for tt in T ]
        es = esat(T1, liquid=True)
        self.assertEqual(_flatten(es, 3), [2335.847, 125.292])
        es = esat(T1, formula='Fukuta', liquid=True)
        self.assertEqual(_flatten(es, 3), [2335.847, 125.079])

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
        self.assertEqual(_flatten(es, 3), [2335.847, -9998.])
        T1 = [20. + T0, -9999.]
        es = esat(T1)
        assert isinstance(es, list)
        self.assertEqual(_flatten(es, 3), [2335.847, -9999.])

        # undef, tuple
        T1 = (20. + T0, -9998.)
        es = esat(T1, undef=-9998.)
        assert isinstance(es, tuple)
        self.assertEqual(_flatten(es, 3), [2335.847, -9998.])
        T1 = (20. + T0, -9999.)
        es = esat(T1)
        assert isinstance(es, tuple)
        self.assertEqual(_flatten(es, 3), [2335.847, -9999.])

        # undef, ndarray
        T1 = np.array([20. + T0, -9998.])
        es = esat(T1, undef=-9998.)
        assert isinstance(es, np.ndarray)
        self.assertEqual(_flatten(es, 3), [2335.847, -9998.])
        T1 = np.array([20. + T0, -9999.])
        es = esat(T1)
        assert isinstance(es, np.ndarray)
        self.assertEqual(_flatten(es, 3), [2335.847, -9999.])

        # undef, masked array
        T = np.array([20. + T0, -9998., -9999.])
        T1 = np.ma.array(T, mask=(T == -9999.))
        es = esat(T1, undef=-9998.)
        assert isinstance(es, np.ma.MaskedArray)
        self.assertEqual(_flatten(es, 3), [2335.847, masked, masked])
        T = np.array([20. + T0, -9998., -9999.])
        T1 = np.ma.array(T, mask=(T == -9998.))
        es = esat(T1)
        assert isinstance(es, np.ma.MaskedArray)
        self.assertEqual(_flatten(es, 3), [2335.847, masked, masked])

        # undef and nan, pandas.Series
        T = [20., -20., -9999. - T0, np.nan]
        T1 = [ tt + T0 for tt in T ]
        d1 = [pd.to_datetime('2020-06-01 12:30'),
              pd.to_datetime('2020-09-03 16:00'),
              pd.to_datetime('2021-06-01 12:30'),
              pd.to_datetime('2021-09-03 16:00')]
        df = pd.Series(T1)
        df.index = d1
        es = esat(df, undef=-9999.)
        assert isinstance(es, pd.Series)
        assert np.isnan(es.iloc[-1])
        self.assertEqual(_flatten(es.values[:-1], 3),
                         [2335.847, 103.074, -9999.])

        # undef and nan, pandas.DataFrame
        T = [20., -20., -9999. - T0, np.nan]
        T1 = np.array([T, T]) + T0
        d1 = [pd.to_datetime('2020-06-01 12:30'),
              pd.to_datetime('2020-09-03 16:00')]
        df = pd.DataFrame(T1)
        df.index = d1
        es = esat(df, undef=-9999.)
        assert isinstance(es, pd.DataFrame)
        assert np.isnan(es.iloc[-1, -1])
        self.assertEqual(_flatten(es.values[:, :-1], 3),
                         [2335.847, 103.074, -9999.,
                          2335.847, 103.074, -9999.])

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

    def test_air2air(self):
        from pyjams import eair2rhair
        from pyjams import rhair2eair
        from pyjams import eair2vpd
        from pyjams import vpd2eair
        from pyjams import rhair2vpd
        from pyjams import vpd2rhair
        from pyjams import eair2shair
        from pyjams import shair2eair
        from pyjams import eair2mrair
        from pyjams import mrair2eair

        tests = ['eair2rhair', 'rhair2eair',
                 'eair2vpd', 'vpd2eair',
                 'rhair2vpd', 'vpd2rhair',
                 'eair2shair', 'shair2eair',
                 'eair2mrair', 'eair2mrair_mol',
                 'mrair2eair', 'mrair2eair_mol']
        for test in tests:
            if test == 'eair2rhair':
                func = eair2rhair
                xair = 1000.
                Ta = 293.15
                res2 = 42.81
                fac = 100.
                kwargs = {}
            elif test == 'rhair2eair':
                func = rhair2eair
                xair = 0.5
                Ta = 293.15
                res2 = 1167.92
                fac = 1.
                kwargs = {}
            elif test == 'eair2vpd':
                func = eair2vpd
                xair = 1000.
                Ta = 293.15
                res2 = 1335.85
                fac = 1.
                kwargs = {}
            elif test == 'vpd2eair':
                func = vpd2eair
                xair = 1000.
                Ta = 293.15
                res2 = 1335.85
                fac = 1.
                kwargs = {}
            elif test == 'rhair2vpd':
                func = rhair2vpd
                xair = 0.5
                Ta = 293.15
                res2 = 1167.92
                fac = 1.
                kwargs = {}
            elif test == 'vpd2rhair':
                func = vpd2rhair
                xair = 1000.
                Ta = 293.15
                res2 = 57.19
                fac = 100.
                kwargs = {}
            elif test == 'eair2shair':
                func = eair2shair
                xair = 1000.
                Ta = 101325.
                res2 = 6.16
                fac = 1000.
                kwargs = {}
            elif test == 'shair2eair':
                func = shair2eair
                xair = 0.006
                Ta = 101325.
                res2 = 973.89
                fac = 1.
                kwargs = {}
            elif test == 'eair2mrair':
                func = eair2mrair
                xair = 1000.
                Ta = 101325.
                res2 = 6.2
                fac = 1000.
                kwargs = {}
            elif test == 'eair2mrair_mol':
                func = eair2mrair
                xair = 1000.
                Ta = 101325.
                res2 = 9.97
                fac = 1000.
                kwargs = {'mol': True}
            elif test == 'mrair2eair':
                func = mrair2eair
                xair = 0.006
                Ta = 101325.
                res2 = 968.10
                fac = 1.
                kwargs = {}
            elif test == 'mrair2eair_mol':
                func = mrair2eair
                xair = 0.006
                Ta = 101325.
                res2 = 604.32
                fac = 1.
                kwargs = {'mol': True}

            # scalar
            e1 = xair
            T1 = Ta
            yair = func(e1, T1, **kwargs) * fac
            assert isinstance(yair, float)
            assert np.around(yair, 2) == res2

            # list
            e1 = [xair, xair]
            T1 = Ta
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, list)
            yair = [ ee * fac for ee in yair ]
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            e1 = xair
            T1 = [Ta, Ta]
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, list)
            yair = [ ee * fac for ee in yair ]
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            e1 = [xair, xair]
            T1 = [Ta, Ta]
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, list)
            yair = [ ee * fac for ee in yair ]
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            # tuple
            e1 = tuple([xair, xair])
            T1 = tuple([Ta, Ta])
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, tuple)
            yair = [ ee * fac for ee in yair ]
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            # ndarray
            e1 = np.array([xair, xair])
            T1 = np.array([Ta, Ta])
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, np.ndarray)
            yair *= fac
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            e1 = np.array([[xair, xair], [xair, xair]])
            T1 = np.array([[Ta, Ta], [Ta, Ta]])
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, np.ndarray)
            yair *= fac
            self.assertEqual(_flatten(yair, 2), [res2, res2, res2, res2])

            # masked_array
            e1 = [xair, xair]
            T1 = [Ta, Ta]
            e1 = np.ma.array(e1)
            T1 = np.ma.array(T1)
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, np.ndarray)
            assert isinstance(yair, np.ma.MaskedArray)
            yair *= fac
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            # mixed types
            e1 = [xair, xair]
            T1 = tuple([Ta, Ta])
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, list)
            yair = [ ee * fac for ee in yair ]
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            e1 = tuple([xair, xair])
            T1 = [Ta, Ta]
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, tuple)
            yair = [ ee * fac for ee in yair ]
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            e1 = np.array(e1)
            T1 = [Ta, Ta]
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, np.ndarray)
            yair *= fac
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            e1 = [xair, xair]
            T1 = np.array(T1)
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, list)
            yair = [ ee * fac for ee in yair ]
            self.assertEqual(_flatten(yair, 2), [res2, res2])

            # pandas.Series
            e1 = np.array([xair, xair])
            T1 = np.array([Ta, Ta])
            d1 = [pd.to_datetime('2020-06-01 12:30'),
                  pd.to_datetime('2020-09-03 16:00')]
            d2 = [pd.to_datetime('2021-06-01 12:30'),
                  pd.to_datetime('2021-09-03 16:00')]
            df1 = pd.Series(e1)
            df1.index = d1
            df2 = pd.Series(T1)
            df2.index = d2
            yair = func(df1, df2, **kwargs)
            assert isinstance(yair, pd.Series)
            yair *= fac
            self.assertEqual(_flatten(yair.values, 2), [res2, res2])

            # pandas.DataFrame
            e1 = np.array([xair, xair])
            T1 = np.array([Ta, Ta])
            d1 = [pd.to_datetime('2020-06-01 12:30'),
                  pd.to_datetime('2020-09-03 16:00')]
            df = pd.DataFrame({'xair': e1, 'Ta': T1})
            df.index = d1
            yair = func(df['xair'], df['Ta'], **kwargs)
            assert isinstance(yair, pd.Series)
            yair *= fac
            self.assertEqual(_flatten(yair.values, 2), [res2, res2])

            # undef, scalar
            e1 = -9998.
            T1 = Ta
            es = func(e1, T1, undef=-9998., **kwargs)
            assert isinstance(es, float)
            assert np.around(es, 2) == -9998.
            e1 = -9999.
            T1 = Ta
            es = func(e1, T1, **kwargs)
            assert isinstance(es, float)
            assert np.around(es, 2) == -9999.
            e1 = xair
            T1 = -9999.
            es = func(e1, T1, **kwargs)
            assert isinstance(es, float)
            assert np.around(es, 2) == -9999.

            # undef, list
            e1 = [xair, -9999.]
            T1 = [Ta, Ta]
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, list)
            yair = [ ee * fac for ee in yair ]
            self.assertEqual(_flatten(yair, 2), [res2, -9999. * fac])

            e1 = [xair, xair]
            T1 = [Ta, -9999.]
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, list)
            yair = [ ee * fac for ee in yair ]
            self.assertEqual(_flatten(yair, 2), [res2, -9999. * fac])

            # undef, masked array
            e1 = np.ma.array([xair, -9998., -9999.])
            T1 = [Ta, Ta, Ta]
            e1 = np.ma.array(e1, mask=(e1 == -9998.))
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, np.ma.MaskedArray)
            yair *= fac
            self.assertEqual(_flatten(yair, 2), [res2, masked, masked])

            e1 = [xair, xair, xair]
            T1 = np.ma.array([Ta, -9998., -9999.])
            T1 = np.ma.array(T1, mask=(T1 == -9998.))
            yair = func(e1, T1, **kwargs)
            assert isinstance(yair, np.ma.MaskedArray)
            yair *= fac
            self.assertEqual(_flatten(yair, 2), [res2, masked, masked])


if __name__ == "__main__":
    unittest.main()
