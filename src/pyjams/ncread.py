#!/usr/bin/env python
"""
Get variables from netcdf file

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2009-2023 Matthias Cuntz, Stephan Thober, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   ncread
   readnetcdf

History
    * Written Jul 2009 by
      Matthias Cuntz (mc (at) macu (dot) de)
    * Removed quiet keyword, Jun 2012, Matthias Cuntz
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Wrapper functions netcdfread, ncread, readnc, Oct 2013, Matthias Cuntz
    * overwrite keyword, Apr 2014, Stephan Thober
    * dims keyword, May 2014, Stephan Thober
    * attributes keyword, Jun 2016, Stephan Thober
    * Restrict overwrite to files with only one variables,
      Aug 2016, Stephan Thober
    * Do not count dimension variables in variable count for overwrite,
      Oct 2016, Matthias Cuntz
    * Remove wrappers netcdfread and readnc, Mar 2022, Matthias Cuntz
    * Remove reform keyword, Mar 2022, Matthias Cuntz
    * Put all info abilities into separate routine infonetcdf
      with wrapper function ncinfo, Mar 2022, Matthias Cuntz
    * Invert functions and wrapper functions, Feb 2023, Matthias Cuntz
    * Rename file to ncread, Nov 2023, Matthias Cuntz
    * Move ncinfo in separate file, Nov 2023, Matthias Cuntz

"""
from .ncinfo import ncinfo


__all__ = ['ncread', 'readnetcdf']


def ncread(ncfile, var='', code=-1, squeeze=False,
               pointer=False, overwrite=False):
    """
    Gets variables of a netcdf file

    Parameters
    ----------
    ncfile : str
        netCDF file name
    variables : bool, optional
        Get list of variables in *ncfile*
    codes : bool, optional
        Get list of variable attributes *code*
        Missing codes will be filled with -1.
    squeeze : bool, optional
        Squeeze output array, i.e. remove dimensions of size 1.
    pointer : bool, optional
        Return pointers to the open file and to the variable if True,
        i.e. without actually reading the variable.
        The file will be open in read-only 'r' mode.
        *overwrite* precedes over *pointer*.
    overwrite : bool, optional
        Return pointers to the open file and to the variable if True,
        where the file is opened in append 'a' mode allowing to modify
        the variable. ``ncread`` allows *overwrite* only if the file
        contains a single variable (without the dimension variables).
        *overwrite* precedes over *pointer*.

    Returns
    -------
    numpy array of the variable with name *var* or number *code*, or
    (file pointer, variable pointer)


    Examples
    --------

    Read variable or code

    >>> ncfile = 'test_ncread.nc'
    >>> print(ncread(ncfile, var='is1'))
    [[1. 1. 1. 1.]
     [1. 1. 1. 1.]]
    >>> print(ncread(ncfile, code=129))
    [[2. 2. 2. 2.]
     [2. 2. 2. 2.]]

    Just get file handle so that read is done later at indexing
    useful for example to inquire remote netcdf files first

    >>> fh, var = ncread(ncfile, var='is1', pointer=True)
    >>> print(var.shape)
    (2, 4)
    >>> print(var[:])
    [[1. 1. 1. 1.]
     [1. 1. 1. 1.]]
    >>> fh.close()

    Change a variable in a file

    >>> ncfile = 'test_ncread1.nc'
    >>> print(ncread(ncfile, var='is1'))
    [[1. 1. 1. 1.]
     [1. 1. 1. 1.]]
    >>> fh, var = ncread(ncfile, var='is1', overwrite=True)
    >>> var[:] *= 2.
    >>> fh.close()
    >>> print(ncread(ncfile, var='is1'))
    [[2. 2. 2. 2.]
     [2. 2. 2. 2.]]
    >>> fh, var = ncread(ncfile, var='is1', overwrite=True)
    >>> var[:] *= 0.5
    >>> fh.close()

    """
    import netCDF4 as nc

    if (not var) and (code == -1):
        raise ValueError('var or code has to be given.')

    vvars = ncinfo(ncfile, variables=True)
    if var:
        if var not in vvars:
            raise ValueError(f'Variable {var} not in file {ncfile}.')
    else:
        cods = ncinfo(ncfile, codes=True)
        if code not in cods:
            raise ValueError(f'Code {code} not in file {ncfile}.')
        var = vvars[cods.index(code)]

    fmode = 'r'
    if overwrite:
        fmode = 'a'
        # check that only one variable
        dims = ncinfo(ncfile, var=var, dims=True)
        vvars1 = [ v for v in vvars if v not in dims ]
        if len(vvars1) > 1:
            raise ValueError('overwrite is only allowed on files with a single'
                             ' variable (without dimension variables).')

    f = nc.Dataset(ncfile, fmode)
    v = f.variables[var]

    if pointer or overwrite:
        return f, v

    v = v[:]
    if squeeze:
        v = v.squeeze()

    f.close()
    return v


def readnetcdf(*args, **kwargs):
    """
    Wrapper for :func:`ncread`
    """
    return ncread(*args, **kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
