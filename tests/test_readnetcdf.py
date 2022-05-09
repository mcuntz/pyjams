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


class TestInfonetcdf(unittest.TestCase):
    """
    Tests for readnetcdf.py
    """

    def test_infonetcdf(self):
        import numpy as np
        import netCDF4 as nc
        from pyjams import infonetcdf

        ncfile = 'tests/test_readnetcdf.nc'

        # variables
        fout = infonetcdf(ncfile, variables=True)
        fsoll = ['x', 'y', 'is1', 'is2']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # variables, sort
        fout = infonetcdf(ncfile, variables=True, sort=True)
        fsoll = ['is1', 'is2', 'x', 'y']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # codes
        fout = infonetcdf(ncfile, codes=True)
        fsoll = [-1, -1, 128, 129]
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # codes, sort
        fout = infonetcdf(ncfile, codes=True, sort=True)
        fsoll = [128, 129, -1, -1]
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # units
        fout = infonetcdf(ncfile, units=True)
        fsoll = ['xx', 'yy', 'arbitrary', 'arbitrary']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # units, sort
        fout = infonetcdf(ncfile, units=True, sort=True)
        fsoll = ['arbitrary', 'arbitrary', 'xx', 'yy']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # long_names
        fout = infonetcdf(ncfile, long_names=True)
        fsoll = ['x-axis', 'y-axis', 'all ones', 'all twos']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # long_names, sort
        fout = infonetcdf(ncfile, long_names=True, sort=True)
        fsoll = ['all ones', 'all twos', 'x-axis', 'y-axis']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # dims, var
        fout = infonetcdf(ncfile, var='is1', dims=True)
        fsoll = ('y', 'x')
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # dims, code
        fout = infonetcdf(ncfile, code=128, dims=True)
        fsoll = ('y', 'x')
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # shape, var
        fout = infonetcdf(ncfile, var='is1', shape=True)
        fsoll = (2, 4)
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # shape, code
        fout = infonetcdf(ncfile, code=128, shape=True)
        fsoll = (2, 4)
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # variable attributes, var
        fout = infonetcdf(ncfile, var='is1', attributes=True)
        fsoll = ['code', 'long_name', 'units']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # variable attributes, var
        fout = infonetcdf(ncfile, 'is1', attributes=True)
        fsoll = ['code', 'long_name', 'units']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # variable attributes, code
        fout = infonetcdf(ncfile, code=128, attributes=True)
        fsoll = ['code', 'long_name', 'units']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # file attributes
        fout = infonetcdf(ncfile, attributes=True)
        fsoll = ['creator', 'history', 'NCO']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # no keyword
        fout = infonetcdf(ncfile)
        fsoll = None
        assert fout is fsoll

        # errors
        # dims, no var
        self.assertRaises(ValueError, infonetcdf, ncfile, dims=True)
        # dims, var does not exist
        self.assertRaises(ValueError, infonetcdf, ncfile, dims=True,
                          var='is3')
        # dims, code does not exist
        self.assertRaises(ValueError, infonetcdf, ncfile, dims=True,
                          code=130)
        # shape, no var
        self.assertRaises(ValueError, infonetcdf, ncfile, shape=True)
        # shape, var does not exist
        self.assertRaises(ValueError, infonetcdf, ncfile, shape=True,
                          var='is3')
        # shape, code does not exist
        self.assertRaises(ValueError, infonetcdf, ncfile, shape=True,
                          code=130)
        # attributes, var does not exist
        self.assertRaises(ValueError, infonetcdf, ncfile, attributes=True,
                          var='is3')
        # attributes, code does not exist
        self.assertRaises(ValueError, infonetcdf, ncfile, attributes=True,
                          code=130)

    def test_ncinfo(self):
        import numpy as np
        import netCDF4 as nc
        from pyjams import ncinfo

        ncfile = 'tests/test_readnetcdf.nc'

        # variables
        fout = ncinfo(ncfile, variables=True)
        fsoll = ['x', 'y', 'is1', 'is2']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # variables, sort
        fout = ncinfo(ncfile, variables=True, sort=True)
        fsoll = ['is1', 'is2', 'x', 'y']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # codes
        fout = ncinfo(ncfile, codes=True)
        fsoll = [-1, -1, 128, 129]
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # codes, sort
        fout = ncinfo(ncfile, codes=True, sort=True)
        fsoll = [128, 129, -1, -1]
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # units
        fout = ncinfo(ncfile, units=True)
        fsoll = ['xx', 'yy', 'arbitrary', 'arbitrary']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # units, sort
        fout = ncinfo(ncfile, units=True, sort=True)
        fsoll = ['arbitrary', 'arbitrary', 'xx', 'yy']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # long_names
        fout = ncinfo(ncfile, long_names=True)
        fsoll = ['x-axis', 'y-axis', 'all ones', 'all twos']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # long_names, sort
        fout = ncinfo(ncfile, long_names=True, sort=True)
        fsoll = ['all ones', 'all twos', 'x-axis', 'y-axis']
        assert isinstance(fout, list)
        self.assertEqual(fout, fsoll)

        # dims, var
        fout = ncinfo(ncfile, var='is1', dims=True)
        fsoll = ('y', 'x')
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # dims, code
        fout = ncinfo(ncfile, code=128, dims=True)
        fsoll = ('y', 'x')
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # shape, var
        fout = ncinfo(ncfile, var='is1', shape=True)
        fsoll = (2, 4)
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # shape, code
        fout = ncinfo(ncfile, code=128, shape=True)
        fsoll = (2, 4)
        assert isinstance(fout, tuple)
        self.assertEqual(fout, fsoll)

        # variable attributes, var
        fout = ncinfo(ncfile, var='is1', attributes=True)
        fsoll = ['code', 'long_name', 'units']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # variable attributes, var
        fout = ncinfo(ncfile, 'is1', attributes=True)
        fsoll = ['code', 'long_name', 'units']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # variable attributes, code
        fout = ncinfo(ncfile, code=128, attributes=True)
        fsoll = ['code', 'long_name', 'units']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # file attributes
        fout = ncinfo(ncfile, attributes=True)
        fsoll = ['creator', 'history', 'NCO']
        assert isinstance(fout, dict)
        fout = sorted(fout.keys())
        fsoll = sorted(fsoll)
        self.assertEqual(fout, fsoll)

        # no keyword
        fout = ncinfo(ncfile)
        fsoll = None
        assert fout is fsoll

        # errors
        # dims, no var
        self.assertRaises(ValueError, ncinfo, ncfile, dims=True)
        # dims, var does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, dims=True,
                          var='is3')
        # dims, code does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, dims=True,
                          code=130)
        # shape, no var
        self.assertRaises(ValueError, ncinfo, ncfile, shape=True)
        # shape, var does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, shape=True,
                          var='is3')
        # shape, code does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, shape=True,
                          code=130)
        # attributes, var does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, attributes=True,
                          var='is3')
        # attributes, code does not exist
        self.assertRaises(ValueError, ncinfo, ncfile, attributes=True,
                          code=130)


class TestReadnetcdf(unittest.TestCase):
    """
    Tests for readnetcdf.py
    """

    def test_readnetcdf(self):
        import numpy as np
        import netCDF4 as nc
        from pyjams import readnetcdf

        ncfile = 'tests/test_readnetcdf.nc'
        ncfile1 = 'tests/test_readnetcdf1.nc'

        # var
        fout = readnetcdf(ncfile, var='is1')
        fsoll = np.full((2, 4), 1.)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # code
        fout = readnetcdf(ncfile, code=129)
        fsoll = np.full((2, 4), 2.)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # squeeze
        fout = readnetcdf(ncfile, var='is1', squeeze=True)
        fsoll = np.full((2, 4), 1.)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # pointer
        fh, var = readnetcdf(ncfile1, var='is1', pointer=True)
        fsoll = np.full((2, 4), 1.)
        assert isinstance(fh, nc.Dataset)
        assert isinstance(var, nc.Variable)
        self.assertEqual(var.shape, (2, 4))
        fout = var[:]
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        fh.close()

        # overwrite
        fh, var = readnetcdf(ncfile1, var='is1', overwrite=True)
        fsoll = np.full((2, 4), 2.)
        assert isinstance(fh, nc.Dataset)
        assert isinstance(var, nc.Variable)
        self.assertEqual(var.shape, (2, 4))
        var[:] *= 2.
        fh.close()
        fout = readnetcdf(ncfile1, var='is1')
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        fh, var = readnetcdf(ncfile1, var='is1', overwrite=True)
        var[:] *= 0.5
        fh.close()

        # errors
        # no var or code
        self.assertRaises(ValueError, readnetcdf, ncfile)
        # var does not exist
        self.assertRaises(ValueError, readnetcdf, ncfile, 'is3')
        # code does not exist
        self.assertRaises(ValueError, readnetcdf, ncfile, code=130)
        # #vars > 1 with overwrite
        self.assertRaises(ValueError, readnetcdf, ncfile, 'is1', overwrite=True)

    def test_ncread(self):
        import os
        import numpy as np
        import netCDF4 as nc
        from pyjams import ncread

        ncfile = 'tests/test_readnetcdf.nc'
        ncfile1 = 'tests/test_readnetcdf1.nc'

        # var
        fout = ncread(ncfile, var='is1')
        fsoll = np.full((2, 4), 1.)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # code
        fout = ncread(ncfile, code=129)
        fsoll = np.full((2, 4), 2.)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # squeeze
        fout = ncread(ncfile, var='is1', squeeze=True)
        fsoll = np.full((2, 4), 1.)
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # pointer
        fh, var = ncread(ncfile1, var='is1', pointer=True)
        fsoll = np.full((2, 4), 1.)
        assert isinstance(fh, nc.Dataset)
        assert isinstance(var, nc.Variable)
        self.assertEqual(var.shape, (2, 4))
        fout = var[:]
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        fh.close()

        # overwrite
        fh, var = ncread(ncfile1, var='is1', overwrite=True)
        fsoll = np.full((2, 4), 2.)
        assert isinstance(fh, nc.Dataset)
        assert isinstance(var, nc.Variable)
        self.assertEqual(var.shape, (2, 4))
        var[:] *= 2.
        fh.close()
        fout = ncread(ncfile1, var='is1')
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        fh, var = ncread(ncfile1, var='is1', overwrite=True)
        var[:] *= 0.5
        fh.close()

        # errors
        # no var or code
        self.assertRaises(ValueError, ncread, ncfile)
        # var does not exist
        self.assertRaises(ValueError, ncread, ncfile, 'is3')
        # code does not exist
        self.assertRaises(ValueError, ncread, ncfile, code=130)
        # #vars > 1 with overwrite
        self.assertRaises(ValueError, ncread, ncfile, 'is1', overwrite=True)


if __name__ == "__main__":
    unittest.main()
