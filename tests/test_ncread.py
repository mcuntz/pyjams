#!/usr/bin/env python
"""
This is the unittest for ncread module.

python -m unittest -v tests/test_ncread.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_ncread.py

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


class TestNcread(unittest.TestCase):
    """
    Tests for ncread.py
    """

    def test_ncread(self):
        import numpy as np
        import netCDF4 as nc
        from pyjams import ncread, readnetcdf

        ncfile = 'tests/test_ncread.nc'
        ncfile1 = 'tests/test_ncread1.nc'

        for fncread in [ncread, readnetcdf]:
            # var
            fout = fncread(ncfile, var='is1')
            fsoll = np.full((2, 4), 1.)
            assert isinstance(fout, np.ndarray)
            self.assertEqual(_flatten(fout), _flatten(fsoll))

            # code
            fout = fncread(ncfile, code=129)
            fsoll = np.full((2, 4), 2.)
            assert isinstance(fout, np.ndarray)
            self.assertEqual(_flatten(fout), _flatten(fsoll))

            # squeeze
            fout = fncread(ncfile, var='is1', squeeze=True)
            fsoll = np.full((2, 4), 1.)
            assert isinstance(fout, np.ndarray)
            self.assertEqual(_flatten(fout), _flatten(fsoll))

            # pointer
            fh, var = fncread(ncfile1, var='is1', pointer=True)
            fsoll = np.full((2, 4), 1.)
            assert isinstance(fh, nc.Dataset)
            assert isinstance(var, nc.Variable)
            self.assertEqual(var.shape, (2, 4))
            fout = var[:]
            self.assertEqual(_flatten(fout), _flatten(fsoll))
            fh.close()

            # overwrite
            fh, var = fncread(ncfile1, var='is1', overwrite=True)
            fsoll = np.full((2, 4), 2.)
            assert isinstance(fh, nc.Dataset)
            assert isinstance(var, nc.Variable)
            self.assertEqual(var.shape, (2, 4))
            var[:] *= 2.
            fh.close()
            fout = fncread(ncfile1, var='is1')
            self.assertEqual(_flatten(fout), _flatten(fsoll))
            fh, var = fncread(ncfile1, var='is1', overwrite=True)
            var[:] *= 0.5
            fh.close()

            # errors
            # no var or code
            self.assertRaises(ValueError, fncread, ncfile)
            # var does not exist
            self.assertRaises(ValueError, fncread, ncfile, 'is3')
            # code does not exist
            self.assertRaises(ValueError, fncread, ncfile, code=130)
            # #vars > 1 with overwrite
            self.assertRaises(ValueError, fncread, ncfile, 'is1',
                              overwrite=True)


if __name__ == "__main__":
    unittest.main()
