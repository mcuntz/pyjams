#!/usr/bin/env python
"""
This is the unittest for gridcellarea module.

python -m unittest -v tests/test_gridcellarea.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_gridcellarea.py

"""
import unittest


def _flatten(itr):
    import numpy as np
    fitr = np.array(itr).flatten()
    if len(fitr) == 0:
        return list(fitr)
    else:
        if isinstance(fitr[0], str):
            return [ i for i in fitr ]
        else:
            return [ i if np.isfinite(i) else np.finfo(float).max
                     for i in fitr ]


class TestGridcellarea(unittest.TestCase):
    """
    Tests for gridcellarea.py
    """

    def test_gridcellarea(self):
        import numpy as np
        from pyjams import gridcellarea

        lat = [0., 2.5, 5.0]
        lon = [0., 3.75, 7.5]

        rearth = 6371009.
        fsoll = [[1.15906555e+11, 1.15906555e+11, 1.15906555e+11],
                 [1.15796237e+11, 1.15796237e+11, 1.15796237e+11],
                 [1.15465495e+11, 1.15465495e+11, 1.15465495e+11]]

        rearth1 = 6371000.
        fsoll1 = [[1.15906227e+11, 1.15906227e+11, 1.15906227e+11],
                  [1.15795910e+11, 1.15795910e+11, 1.15795910e+11],
                  [1.15465169e+11, 1.15465169e+11, 1.15465169e+11]]

        # descending latitudes
        dlat = [0., -2.5, -5.0]

        # meridian within longitudes
        lon360 = [360., 3.75, 7.5]
        # dateline within longitudes
        lon180 = [180., -180.+3.75, -180.+7.5]

        # list
        fout  = gridcellarea(lat, lon)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -3)), _flatten(fsoll))

        # tuple, list
        fout  = gridcellarea(tuple(lat), lon)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -3)), _flatten(fsoll))

        # 2 tuple
        fout  = gridcellarea(tuple(lat), tuple(lon))
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -3)), _flatten(fsoll))

        # array, list
        fout  = gridcellarea(np.array(lat), lon)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -3)), _flatten(fsoll))

        # 2 array
        fout  = gridcellarea(np.array(lat), np.array(lon))
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -3)), _flatten(fsoll))

        # rearth
        fout  = gridcellarea(lat, lon, rearth=rearth)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -3)), _flatten(fsoll))

        # rearth classic
        fout  = gridcellarea(lat, lon, rearth=rearth1)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -3)), _flatten(fsoll1))

        # globe
        fout  = gridcellarea(lat, lon, globe=True)
        fsoll2 = [[3.79774834e+12, 3.79774834e+12, 3.79774834e+12],
                  [1.15796240e+11, 1.15796240e+11, 1.15796240e+11],
                  [3.61823239e+12, 3.61823239e+12, 3.61823239e+12]]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -4)), _flatten(fsoll2))

        # descending lats
        fout  = gridcellarea(dlat, lon, globe=True)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -4)), _flatten(fsoll2))

        # meridian in lon
        fout  = gridcellarea(lat, lon360)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -3)), _flatten(fsoll))

        # date line in lon
        fout  = gridcellarea(lat, lon180)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(np.around(fout, -3)), _flatten(fsoll))

        # errors
        # lat > 90
        lat1 = [0., 2.5, 95.0]
        self.assertRaises(AssertionError, gridcellarea, lat1, lon)


if __name__ == "__main__":
    unittest.main()
