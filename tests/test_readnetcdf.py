#!/usr/bin/env python
"""
This is the unittest for readnetcdf module.

python -m unittest -v tests/test_readnetcdf.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_readnetcdf.py

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


class TestNcinfo(unittest.TestCase):
    """
    Tests for readnetcdf.py
    """

    def test_ncinfo(self):
        from pyjams import ncinfo, infonetcdf

        ncfile = 'tests/test_readnetcdf.nc'

        for fncinfo in [ncinfo, infonetcdf]:
            # variables
            fout = fncinfo(ncfile, variables=True)
            fsoll = ['x', 'y', 'is1', 'is2']
            assert isinstance(fout, list)
            self.assertEqual(fout, fsoll)

            # variables, sort
            fout = fncinfo(ncfile, variables=True, sort=True)
            fsoll = ['is1', 'is2', 'x', 'y']
            assert isinstance(fout, list)
            self.assertEqual(fout, fsoll)

            # codes
            fout = fncinfo(ncfile, codes=True)
            fsoll = [-1, -1, 128, 129]
            assert isinstance(fout, list)
            self.assertEqual(fout, fsoll)

            # codes, sort
            fout = fncinfo(ncfile, codes=True, sort=True)
            fsoll = [128, 129, -1, -1]
            assert isinstance(fout, list)
            self.assertEqual(fout, fsoll)

            # units
            fout = fncinfo(ncfile, units=True)
            fsoll = ['xx', 'yy', 'arbitrary', 'arbitrary']
            assert isinstance(fout, list)
            self.assertEqual(fout, fsoll)

            # units, sort
            fout = fncinfo(ncfile, units=True, sort=True)
            fsoll = ['arbitrary', 'arbitrary', 'xx', 'yy']
            assert isinstance(fout, list)
            self.assertEqual(fout, fsoll)

            # long_names
            fout = fncinfo(ncfile, long_names=True)
            fsoll = ['x-axis', 'y-axis', 'all ones', 'all twos']
            assert isinstance(fout, list)
            self.assertEqual(fout, fsoll)

            # long_names, sort
            fout = fncinfo(ncfile, long_names=True, sort=True)
            fsoll = ['all ones', 'all twos', 'x-axis', 'y-axis']
            assert isinstance(fout, list)
            self.assertEqual(fout, fsoll)

            # dims, var
            fout = fncinfo(ncfile, var='is1', dims=True)
            fsoll = ('y', 'x')
            assert isinstance(fout, tuple)
            self.assertEqual(fout, fsoll)

            # dims, code
            fout = fncinfo(ncfile, code=128, dims=True)
            fsoll = ('y', 'x')
            assert isinstance(fout, tuple)
            self.assertEqual(fout, fsoll)

            # shape, var
            fout = fncinfo(ncfile, var='is1', shape=True)
            fsoll = (2, 4)
            assert isinstance(fout, tuple)
            self.assertEqual(fout, fsoll)

            # shape, code
            fout = fncinfo(ncfile, code=128, shape=True)
            fsoll = (2, 4)
            assert isinstance(fout, tuple)
            self.assertEqual(fout, fsoll)

            # variable attributes, var
            fout = fncinfo(ncfile, var='is1', attributes=True)
            fsoll = ['_FillValue', 'code', 'long_name', 'missing_value',
                     'units']
            assert isinstance(fout, dict)
            fout = sorted(fout.keys())
            fsoll = sorted(fsoll)
            self.assertEqual(fout, fsoll)

            # variable attributes, var
            fout = fncinfo(ncfile, 'is1', attributes=True)
            fsoll = ['_FillValue', 'code', 'long_name', 'missing_value',
                     'units']
            assert isinstance(fout, dict)
            fout = sorted(fout.keys())
            fsoll = sorted(fsoll)
            self.assertEqual(fout, fsoll)

            # variable attributes, code
            fout = fncinfo(ncfile, code=128, attributes=True)
            fsoll = ['_FillValue', 'code', 'long_name', 'missing_value',
                     'units']
            assert isinstance(fout, dict)
            fout = sorted(fout.keys())
            fsoll = sorted(fsoll)
            self.assertEqual(fout, fsoll)

            # file attributes
            fout = fncinfo(ncfile, attributes=True)
            fsoll = ['creator', 'history', 'NCO']
            assert isinstance(fout, dict)
            fout = sorted(fout.keys())
            fsoll = sorted(fsoll)
            self.assertEqual(fout, fsoll)

            # no keyword
            fout = fncinfo(ncfile)
            fsoll = None
            assert fout is fsoll

            # errors
            # dims, no var
            self.assertRaises(ValueError, fncinfo, ncfile, dims=True)
            # dims, var does not exist
            self.assertRaises(ValueError, fncinfo, ncfile, dims=True,
                              var='is3')
            # dims, code does not exist
            self.assertRaises(ValueError, fncinfo, ncfile, dims=True,
                              code=130)
            # shape, no var
            self.assertRaises(ValueError, fncinfo, ncfile, shape=True)
            # shape, var does not exist
            self.assertRaises(ValueError, fncinfo, ncfile, shape=True,
                              var='is3')
            # shape, code does not exist
            self.assertRaises(ValueError, fncinfo, ncfile, shape=True,
                              code=130)
            # attributes, var does not exist
            self.assertRaises(ValueError, fncinfo, ncfile, attributes=True,
                              var='is3')
            # attributes, code does not exist
            self.assertRaises(ValueError, fncinfo, ncfile, attributes=True,
                              code=130)


class TestNcread(unittest.TestCase):
    """
    Tests for readnetcdf.py
    """

    def test_ncread(self):
        import numpy as np
        import netCDF4 as nc
        from pyjams import ncread, readnetcdf

        ncfile = 'tests/test_readnetcdf.nc'
        ncfile1 = 'tests/test_readnetcdf1.nc'

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
