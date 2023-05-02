#!/usr/bin/env python
"""
This is the unittest for ncio module.

python -m unittest -v tests/test_ncio.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_ncio.py

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


class TestNcio(unittest.TestCase):
    """
    Tests for module ncio
    """

    def test_copy_file(self):
        import os
        import numpy as np
        import pyjams.ncio as ncio
        from pyjams import ncinfo, ncread

        ncfile = 'tests/test_readnetcdf.nc'
        ofile = 'test_ncio_copy_file.nc'

        # full copy
        ncio.copy_file(ncfile, ofile)
        fout = ncinfo(ofile, variables=True)
        fsoll = ncinfo(ncfile, variables=True)
        self.assertEqual(fout, fsoll)

        fout = ncinfo(ofile, long_names=True)
        fsoll = ncinfo(ncfile, long_names=True)
        self.assertEqual(fout, fsoll)

        fout = ncinfo(ofile, units=True)
        fsoll = ncinfo(ncfile, units=True)
        self.assertEqual(fout, fsoll)

        fout = ncread(ofile, var='is1')
        fsoll = ncread(ncfile, var='is1')
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # removevar
        ncio.copy_file(ncfile, ofile, removevar=('is1',))
        fout = ncinfo(ofile, variables=True)
        fsoll = ncinfo(ncfile, variables=True)
        fsoll.remove('is1')
        self.assertEqual(fout, fsoll)

        ncio.copy_file(ncfile, ofile, removevar=['is1', 'is2'])
        fout = ncinfo(ofile, variables=True)
        fsoll = ncinfo(ncfile, variables=True)
        fsoll.remove('is1')
        fsoll.remove('is2')
        self.assertEqual(fout, fsoll)

        # renamevar
        ncio.copy_file(ncfile, ofile, renamevar={'is1': 'is3'})
        fout = ncinfo(ofile, variables=True)
        fsoll = ncinfo(ncfile, variables=True)
        fsoll[fsoll.index('is1')] = 'is3'
        self.assertEqual(fout, fsoll)

        # replacevar
        isout = np.full((2, 4), 3.)
        ncio.copy_file(ncfile, ofile,
                       replacevar={'is1': {'is3': isout}})
        fout = ncinfo(ofile, variables=True)
        fsoll = ncinfo(ncfile, variables=True)
        fsoll[fsoll.index('is1')] = 'is3'
        self.assertEqual(fout, fsoll)

        fout = ncread(ofile, var='is3')
        fsoll = isout
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # replacevar, replaceatt
        isout = np.full((2, 4), 3.)
        ncio.copy_file(ncfile, ofile,
                       replacevar={'is1': {'is3': isout}},
                       replaceatt={'is2': {'long_name': 'twos'},
                                   'is3': {'long_name': 'threes',
                                           'units': 'arbitrary'}})
        fout = ncinfo(ofile, variables=True)
        fsoll = ncinfo(ncfile, variables=True)
        fsoll[fsoll.index('is1')] = 'is3'
        self.assertEqual(fout, fsoll)

        fout = ncread(ofile, var='is3')
        fsoll = isout
        self.assertEqual(fout.shape, fsoll.shape)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        att = ncinfo(ofile, var='is2', attributes=True)
        fout = att['long_name']
        fsoll = 'twos'
        self.assertEqual(fout, fsoll)

        att = ncinfo(ofile, var='is3', attributes=True)
        fout = att['long_name']
        fsoll = 'threes'
        self.assertEqual(fout, fsoll)
        fout = att['units']
        fsoll = 'arbitrary'
        self.assertEqual(fout, fsoll)

        # renamevar, noclose
        isout = np.full((2, 4), 3.)
        fo = ncio.copy_file(ncfile, ofile, renamevar={'is1': 'is3'},
                            noclose=True)
        fo.close()
        fout = ncread(ofile, var='is3')
        fsoll = ncread(ncfile, var='is1')
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fo = ncio.copy_file(ncfile, ofile, renamevar={'is1': 'is3'},
                            noclose=True)
        ovar = fo.variables['is3']
        ovar[:] = isout
        fo.close()
        fout = ncread(ofile, var='is3')
        fsoll = isout
        self.assertEqual(fout.shape, fsoll.shape)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # clean up
        if os.path.exists(ofile):
            os.remove(ofile)

    def test_get_fill_value_for_dtype(self):
        import numpy as np
        import netCDF4 as nc
        import pyjams.ncio as ncio

        itypes = [np.int8, np.int16, np.int32, np.int64,
                  np.uint8, np.uint16, np.uint32, np.uint64,
                  np.float32, np.float64]
        otypes = ['i1', 'i2', 'i4', 'i8',
                  'u1', 'u2', 'u4', 'u8',
                  'f4', 'f8']

        for ii, nn in enumerate(itypes):
            out = np.array([1, 2, 3], dtype=nn)
            fout = ncio.get_fill_value_for_dtype(out.dtype)
            fsoll = nc.default_fillvals[otypes[ii]]
            assert fout == fsoll

    def test_get_fill_value_for_float128(self):
        import sys
        import warnings
        import pytest
        import numpy as np
        import pyjams.ncio as ncio

        if sys.platform.startswith("win"):
            pytest.skip("skipping tests that require float128 on windows")
        # warning unknown type
        with warnings.catch_warnings(record=True) as w:
            nn = np.float128
            out = np.array([1, 2, 3], dtype=nn)
            fout = ncio.get_fill_value_for_dtype(out.dtype)
            assert len(w) > 0

    def test_set_output_filename(self):
        import pyjams.ncio as ncio

        # full copy
        fout = ncio.set_output_filename('in.nc', '-no_patch')
        assert fout == 'in-no_patch.nc'

        fout = ncio.set_output_filename('in.nc', '.nop')
        assert fout == 'in.nop.nc'

        fout = ncio.set_output_filename('in.nc', '')
        assert fout == 'in.nc'

    def test_dimensions(self):
        import os
        import numpy as np
        import netCDF4 as nc
        import pyjams.ncio as ncio
        from pyjams import ncinfo, ncread

        ifile = 'tests/test_ncio.nc'
        ofile = 'test_ncio_dimensions.nc'

        # remove and rename dimension, land is the last dimension
        vtime = 'time'
        vland = 'land'
        vpatch = 'patch'
        opatch = 'opatch'
        fi = nc.Dataset(ifile, 'r')
        if 'file_format' in dir(fi):
            fo = nc.Dataset(ofile, 'w', format=fi.file_format)
        else:
            fo = nc.Dataset(ofile, 'w', format='NETCDF4')
        ntime = fi.dimensions[vtime].size
        ncio.copy_global_attributes(fi, fo,
                                    add={'history': 'removedim/renamedim'},
                                    remove=['CABLE_input_file'])
        ncio.copy_dimensions(fi, fo, removedim=[vland],
                             renamedim={vpatch: opatch})
        ncio.create_variables(fi, fo, time=False, timedim=vtime, fill=True,
                              removedim=vland, renamedim={vpatch: opatch})
        ncio.create_variables(fi, fo, time=True, timedim=vtime, fill=True,
                              removedim=[vland], renamedim={vpatch: opatch})
        for ivar in fi.variables.values():
            if vtime not in ivar.dimensions:
                ovar = fo.variables[ivar.name]
                if vland in ivar.dimensions:
                    ovar[:] = ivar[:].mean(axis=-1)
                else:
                    ovar[:] = ivar[:]
        for tt in range(ntime):
            for ivar in fi.variables.values():
                if vtime in ivar.dimensions:
                    ovar = fo.variables[ivar.name]
                    if vland in ivar.dimensions:
                        ovar[tt, ...] = ivar[tt, ...].mean(axis=-1)
                    else:
                        if ivar.ndim == 1:
                            ovar[tt] = ivar[tt]
                        else:
                            ovar[tt, ...] = ivar[tt, ...]
        fi.close()
        fo.close()

        fout = ncinfo(ofile, variables=True)
        fsoll = ncinfo(ifile, variables=True)
        self.assertEqual(fout, fsoll)

        for vv in ['patchfrac', 'albsoil', 'ratecp', 'SoilMoist']:
            fout = list(ncinfo(ofile, vv, dims=True))
            fsoll = list(ncinfo(ifile, vv, dims=True))
            fsoll = fsoll[:-1]
            if vpatch in fsoll:
                fsoll[fsoll.index(vpatch)] = opatch
            self.assertEqual(fout, fsoll)
            assert opatch in fout
            assert vpatch not in fout

        fout = ncread(ofile, var='SoilTemp')
        fsoll = ncread(ifile, var='SoilTemp')
        self.assertEqual(_flatten(fout), _flatten(fsoll.mean(axis=-1)))

        # changedim, land is the last dimension
        vtime = 'time'
        vland = 'land'
        fi = nc.Dataset(ifile, 'r')
        if 'file_format' in dir(fi):
            fo = nc.Dataset(ofile, 'w', format=fi.file_format)
        else:
            fo = nc.Dataset(ofile, 'w', format='NETCDF4')
        ntime = fi.dimensions[vtime].size
        nland = fi.dimensions[vland].size
        ncio.copy_global_attributes(fi, fo,
                                    add={'history': 'changedim'})
        ncio.copy_dimensions(fi, fo, removedim=None,
                             changedim={vland: 2 * nland})
        ncio.create_variables(fi, fo, time=False, timedim=vtime, fill=None,
                              chunksizes=False)
        ncio.create_variables(fi, fo, time=True, timedim=vtime, fill=None,
                              chunksizes=False)
        for ivar in fi.variables.values():
            if vtime not in ivar.dimensions:
                ovar = fo.variables[ivar.name]
                if vland in ivar.dimensions:
                    ovar[:] = np.append(ivar[:], ivar[:], axis=-1)
                else:
                    ovar[:] = ivar[:]
        for tt in range(ntime):
            for ivar in fi.variables.values():
                if vtime in ivar.dimensions:
                    ovar = fo.variables[ivar.name]
                    if vland in ivar.dimensions:
                        ovar[tt, ...] = np.append(ivar[tt, ...], ivar[tt, ...],
                                                  axis=-1)
                    else:
                        if ivar.ndim == 1:
                            ovar[tt] = ivar[tt]
                        else:
                            ovar[tt, ...] = ivar[tt, ...]
        fi.close()
        fo.close()

        fout = ncinfo(ofile, variables=True)
        fsoll = ncinfo(ifile, variables=True)
        self.assertEqual(fout, fsoll)

        for vv in ['patchfrac', 'albsoil', 'ratecp', 'SoilMoist']:
            fout = ncinfo(ofile, vv, shape=True)
            fsoll = ncinfo(ifile, vv, shape=True)
            self.assertEqual(fout[:-1], fsoll[:-1])
            assert fout[-1] == 2 * fsoll[-1]

        fout = ncread(ofile, var='SoilTemp')
        fsoll = ncread(ifile, var='SoilTemp')
        fsoll  = np.append(fsoll, fsoll, axis=-1)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # adddim, land to fake x and y
        vtime = 'time'
        vland = 'land'
        fi = nc.Dataset(ifile, 'r')
        if 'file_format' in dir(fi):
            fo = nc.Dataset(ofile, 'w', format=fi.file_format)
        else:
            fo = nc.Dataset(ofile, 'w', format='NETCDF4')
        ntime = fi.dimensions[vtime].size
        nland = fi.dimensions[vland].size
        ncio.copy_global_attributes(fi, fo,
                                    add={'history': 'adddim'})
        ncio.copy_dimensions(fi, fo, removedim=['land'],
                             adddim={'xland': nland, 'yland': nland})
        ncio.create_variables(fi, fo, time=False, timedim=vtime, fill=True,
                              izip=False, chunksizes=False,
                              replacedim={vland: ('yland', 'xland')})
        ncio.create_variables(fi, fo, time=True, timedim=vtime, fill=True,
                              izip=True, chunksizes=False,
                              replacedim={vland: ('yland', 'xland')})
        for ivar in fi.variables.values():
            if vtime not in ivar.dimensions:
                ovar = fo.variables[ivar.name]
                if vland in ivar.dimensions:
                    if ivar.ndim == 1:
                        ovar[:] = np.tile(ivar[:], (nland, 1))
                    else:
                        np.tile(ivar[:], nland)
                else:
                    ovar[:] = ivar[:]
        for tt in range(ntime):
            for ivar in fi.variables.values():
                if vtime in ivar.dimensions:
                    ovar = fo.variables[ivar.name]
                    if vland in ivar.dimensions:
                        ovar[tt, ...] = np.tile(ivar[tt, ...], nland)
                    else:
                        if ivar.ndim == 1:
                            ovar[tt] = ivar[tt]
                        else:
                            ovar[tt, ...] = ivar[tt, ...]
        fi.close()
        fo.close()

        fout = ncinfo(ofile, variables=True)
        fsoll = ncinfo(ifile, variables=True)
        self.assertEqual(fout, fsoll)

        for vv in ['patchfrac', 'albsoil', 'ratecp', 'SoilMoist']:
            fout = list(ncinfo(ofile, vv, shape=True))
            fsoll = list(ncinfo(ifile, vv, shape=True))
            fsoll.append(fsoll[-1])
            self.assertEqual(fout, fsoll)

        fout = ncread(ofile, var='SoilTemp')
        fsoll = ncread(ifile, var='SoilTemp')
        fsoll  = np.tile(fsoll, fsoll.shape[-1])
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # clean up
        if os.path.exists(ofile):
            os.remove(ofile)

    def test_variables(self):
        import os
        import numpy as np
        import netCDF4 as nc
        import pyjams.ncio as ncio
        from pyjams import ncinfo, ncread

        ifile = 'tests/test_ncio.nc'
        ofile = 'test_ncio_variables.nc'

        # remove and rename variables
        vtime = 'time'
        rmvar = ['Cplant']
        mvvar = {'Csoil': 'CarbonSoil'}
        fi = nc.Dataset(ifile, 'r')
        if 'file_format' in dir(fi):
            fo = nc.Dataset(ofile, 'w', format=fi.file_format)
        else:
            fo = nc.Dataset(ofile, 'w', format='NETCDF4')
        ntime = fi.dimensions[vtime].size
        ncio.copy_global_attributes(fi, fo,
                                    add={'history': 'removevar/renamevar',
                                         'extra': 'Add what you want'},
                                    remove=['CABLE_input_file'])
        ncio.copy_dimensions(fi, fo)
        ncio.create_variables(fi, fo, fill=-9999.,
                              removevar=rmvar, renamevar=mvvar)
        ncio.copy_variables(fi, fo, time=False, timedim=vtime,
                            removevar=rmvar, renamevar=mvvar)
        ncio.copy_variables(fi, fo, time=True, timedim=vtime,
                            removevar=rmvar, renamevar=mvvar)
        fi.close()
        fo.close()

        fout = list(ncinfo(ofile, variables=True))
        fsoll = list(ncinfo(ifile, variables=True))
        fsoll.remove(rmvar[0])
        for rr in mvvar:
            fsoll[fsoll.index(rr)] = mvvar[rr]
        self.assertEqual(fout, fsoll)

        # create new variable
        vtime = 'time'
        fi = nc.Dataset(ifile, 'r')
        if 'file_format' in dir(fi):
            fo = nc.Dataset(ofile, 'w', format=fi.file_format)
        else:
            fo = nc.Dataset(ofile, 'w', format='NETCDF4')
        # ntime = fi.dimensions[vtime].size
        ncio.copy_global_attributes(fi, fo,
                                    add={'history': 'Create new var'})
        ncio.copy_dimensions(fi, fo)
        ncio.create_variables(fi, fo)
        dtype = fi.variables['SWdown'].dtype
        dimensions = fi.variables['SWdown'].dimensions
        shape = fi.variables['SWdown'].shape
        chunk = list(shape)
        chunk[0] = 1
        odict = {'name': 'test1',
                 'dtype': dtype,
                 'standard_name': 'test1',
                 'long_name': '1st test variable',
                 'dimensions': dimensions}
        test1 = ncio.create_new_variable(
            odict, fo, izip=True, fill=True)
        odict = {'name': 'test2',
                 'dtype': dtype,
                 'standard_name': 'test2',
                 'long_name': '2nd test variable',
                 'dimensions': dimensions}
        test2 = ncio.create_new_variable(
            odict, fo, izip=False, fill=True)
        odict = {'name': 'test3',
                 'dtype': dtype,
                 'standard_name': 'test3',
                 'long_name': '3rd test variable',
                 'dimensions': dimensions}
        test3 = ncio.create_new_variable(
            odict, fo, izip=True, fill=False)
        odict = {'name': 'test4',
                 'dtype': dtype,
                 'standard_name': 'test4',
                 'long_name': '4th test variable',
                 'dimensions': dimensions,
                 'chunksizes': chunk}
        test4 = ncio.create_new_variable(
            odict, fo, izip=True, fill=None)
        odict = {'name': 'test5',
                 'dtype': dtype,
                 'standard_name': 'test5',
                 'long_name': '5th test variable',
                 'dimensions': dimensions}
        test5 = ncio.create_new_variable(
            odict, fo, izip=True, fill=-9999.)
        odict = {'name': 'test6',
                 'dtype': dtype,
                 'standard_name': 'test6',
                 'long_name': '6th test variable',
                 'dimensions': dimensions,
                 'chunksizes': chunk}
        test6 = ncio.create_new_variable(
            odict, fo, izip=True, fill=None, chunksizes=False)
        ncio.copy_variables(fi, fo, time=False, timedim=vtime)
        ncio.copy_variables(fi, fo, time=True, timedim=vtime)
        test1[:] = 1.
        test2[:] = 2.
        test3[:] = 3.
        test4[:] = 4.
        test5[:] = 5.
        test5[::2] = -9999.
        test6[:] = 6.
        fi.close()
        fo.close()

        fout = list(ncinfo(ofile, variables=True))
        assert 'test1' in fout
        assert 'test2' in fout
        assert 'test3' in fout
        assert 'test4' in fout
        assert 'test5' in fout
        assert 'test6' in fout
        fout = [ vv for vv in fout if not vv.startswith('test') ]
        fsoll = list(ncinfo(ifile, variables=True))
        self.assertEqual(fout, fsoll)

        for iv in range(1, 7):
            fout = ncinfo(ofile, f'test{iv}', shape=True)
            fsoll = shape
            self.assertEqual(fout, fsoll)
            fout = ncinfo(ofile, f'test{iv}', dims=True)
            fsoll = dimensions
            self.assertEqual(fout, fsoll)
            fout = ncread(ofile, var=f'test{iv}')
            assert np.all(fout == float(iv))

        # clean up
        if os.path.exists(ofile):
            os.remove(ofile)


if __name__ == "__main__":
    unittest.main()
