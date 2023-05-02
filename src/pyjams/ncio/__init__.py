"""
netCDF4 functions to copy a netcdf file while doing some transformations on
variables and dimensions.

An elaborate example of copying a netcdf file could remove one variable
(removevar), rename another variable (renamevar), replace name and values of a
third variable (replacevar), setting some attributes of old and new variables
(replaceatt), and leave the output file open for further modification
(noclose):

.. code-block:: python

   import numpy as np
   import pyjams.ncio as ncio

   newarr = np.full((720, 360), 273.15)
   fo = ncio.copy_file('infile.nc', 'infile.nc',
                       removevar=['var0'],
                       renamevar={'var1': 'varnew1'},
                       replacevar={'var2': {'varnew2': newvar}},
                       replaceatt={'varnew1': {'long_name': 'renamed var1'},
                                   'varnew2': {'long_name': 'new variable for var2',
                                               'units': 'arbitrary'}},
                       noclose=True)
   # change var3 afterwards
   ovar = fo.variables['var3']
   ovar[:] = ovar[:] * 3.
   fo.close()


Using the individual routines for manipulating dimensions and variables could
copy all variables in a file while making latitudinal means (assume longitudes
in the last dimension), and add a new variable:

.. code-block:: python

   import netCDF4 as nc
   import pyjams.ncio as ncio

   ifile = 'input.nc'  # name of input file
   vtime = 'time'      # name of time variable
   vlon  = 'lon'       # name of longitude variable

   # open files
   ofile = ncio.set_output_filename(ifile, '-latmean.nc')
   fi = nc.Dataset(ifile, 'r')
   if 'file_format' in dir(fi):
       fo = nc.Dataset(ofile, 'w', format=fi.file_format)
   else:
       fo = nc.Dataset(ofile, 'w', format='NETCDF4')
   ntime = fi.dimensions[vtime].size

   # meta data
   ncio.copy_global_attributes(fi, fo, add={'history': 'latitudinal mean'})

   # copy dimensions
   ncio.copy_dimensions(fi, fo, removedim=[vlon])

   # create variables
   # this could be one command (time=None or keyword time left out)
   # but I like to have the non-time dependent variables at the beginning
   # of the netcdf file
   # create static variables (independent of time)
   ncio.create_variables(fi, fo, time=False, timedim=vtime, fill=True,
                         removedim=[vlon])
   # create dynamic variables (time dependent)
   ncio.create_variables(fi, fo, time=True, timedim=vtime, fill=True,
                         removedim=[vlon])

   # create new variable
   dims = list(fi.variables['var1'].dimensions)
   dims = dims[:-1]
   odict = {'name': 'var2',
            'dtype': fi.variables['var1'].dtype,
            'standard_name': 'var2',
            'long_name': '2nd variable',
            'dimensions': dims}
   var2 = ncio.create_new_variable(odict, fo, izip=True, fill=True)

   # copy static variables (not time-dependent) making latitudinal means
   for ivar in fi.variables.values():
       if vtime not in ivar.dimensions:
           ovar = fo.variables[ivar.name]
           if vlon in ivar.dimensions:
               ovar[:] = ivar.mean(axis=-1)
           else:
               ovar[:] = ivar[:]

   # copy dynamic variables (time-dependent) making latitudinal means
   for tt in range(ntime):
       for ivar in fi.variables.values():
           if vtime in ivar.dimensions:
               ovar = fo.variables[ivar.name]
               if vlon in ivar.dimensions:
                   ovar[tt, ...] = ivar[tt, ...].mean(axis=-1)
               else:
                   if ivar.ndim == 1:
                       ovar[tt] = ivar[tt]
                   else:
                       ovar[tt, ...] = ivar[tt, ...]

   # set new variable
   shape1 = fi.variables['var1'].shape
   shape1 = shape1[:-1]
   var2[:] = np.arange(np.prod(shape1)).reshape(shape1)

   # finish
   fi.close()
   fo.close()

:copyright: Copyright 2020-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

Subpackages
===========
.. autosummary::
   netcdfio

"""
from .netcdfio import copy_dimensions, copy_file
from .netcdfio import copy_global_attributes, copy_variables
from .netcdfio import create_new_variable, create_variables
from .netcdfio import get_fill_value_for_dtype, get_variable_definition
from .netcdfio import set_output_filename

__all__ = ['copy_dimensions', 'copy_file', 'copy_global_attributes',
           'copy_variables', 'create_new_variable', 'create_variables',
           'get_fill_value_for_dtype', 'get_variable_definition',
           'set_output_filename']
