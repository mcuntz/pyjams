#!/usr/bin/env python
"""
Get variables from or print information of a netcdf file

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2009-2022 Matthias Cuntz, Stephan Thober, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   infonetcdf
   ncinfo
   readnetcdf
   ncread

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

"""


__all__ = ['infonetcdf', 'ncinfo',
           'readnetcdf', 'ncread']


def ncinfo(ncfile,
           var='', code=-1, dims=False, shape=False, attributes=False,
           variables=False, codes=False,
           long_names=False, units=False,
           sort=False):
    """
    Get information on variables in a netcdf file

    Parameters
    ----------
    ncfile : str
        netCDF file name
    var : str, optional
        Variable name, only relevant if *dims* or *attributes* are True
        *var* takes precedence over *code*.
    code : int, optional
        Variable code such as in files coming from GRIB,
        only relevant if *dims* or *attributes* are True.
        *var* takes precedence over *code*.
    dims : bool, optional
        Get tuple of dimension names for the variable with name *var*
        or number *code*.
    shape : bool, optional
        Get shape of the variable with name *var* or number *code*.
    attributes : bool, optional
        Get dictionary of all attributes of variable with name *var* or number
        *code*, or all file attributes of *ncfile* if *var* and *code* are not
        given
    variables : bool, optional
        Get list of variables in *ncfile*
    codes : bool, optional
        Get list of variable attributes *code*
        Missing codes will be filled with -1.
    long_names : bool, optional
        Get list of variable attributes *long_name*
        Missing long_names will be filled with ''.
    units : bool, optional
        Get list of variable attributes *units*.
        Missing units will be filled with ''.
    sort : bool, optional
        Sort output of *variables*, *codes*, *units*, and *long_names*
        with variable name as the sort key

    Returns
    -------
    tuple of variable dimension names,
    tuple of variable dimensions,
    list of variable names, codes, units, long_names, or
    dictionary of attributes


    Examples
    --------

    Get variable names

    >>> ncfile = 'test_readnetcdf.nc'
    >>> print([ str(i) for i in ncinfo(ncfile, variables=True) ])
    ['x', 'y', 'is1', 'is2']
    >>> print([ str(i)
    ...        for i in ncinfo(ncfile, variables=True, sort=True) ])
    ['is1', 'is2', 'x', 'y']

    Get codes

    >>> print(ncinfo(ncfile, codes=True))
    [-1, -1, 128, 129]
    >>> print(ncinfo(ncfile, codes=True, sort=True))
    [128, 129, -1, -1]

    Get special attributes units and long_names

    >>> print([ str(i) for i in ncinfo(ncfile, units=True) ])
    ['xx', 'yy', 'arbitrary', 'arbitrary']
    >>> print([ str(i) for i in ncinfo(ncfile, units=True, sort=True) ])
    ['arbitrary', 'arbitrary', 'xx', 'yy']
    >>> print([ str(i) for i in ncinfo(ncfile, long_names=True) ])
    ['x-axis', 'y-axis', 'all ones', 'all twos']
    >>> print([ str(i)
    ...        for i in ncinfo(ncfile, long_names=True, sort=True) ])
    ['all ones', 'all twos', 'x-axis', 'y-axis']

    Get dims

    >>> print([ str(i) for i in ncinfo(ncfile, var='is1', dims=True) ])
    ['y', 'x']

    Get shape

    >>> print(ncinfo(ncfile, var='is1', shape=True))
    (2, 4)

    Get attributes

    >>> t1 = ncinfo(ncfile, var='is1', attributes=True)
    >>> print([ str(i) for i in sorted(t1) ])
    ['code', 'long_name', 'units']

    """
    import netCDF4 as nc

    f = nc.Dataset(ncfile, 'r')

    # Variables
    vvars = list(f.variables.keys())
    nvars = len(vvars)

    # Sort and get sort indices
    if sort:
        # index
        ivars = sorted(range(nvars), key=vvars.__getitem__)
        # sorted variables
        svars = [ vvars[i] for i in ivars ]
    else:
        svars = vvars
        ivars = list(range(nvars))

    # variables
    if variables:
        f.close()
        return svars

    # code
    if codes:
        cods = [-1]*nvars
        for i, v in enumerate(svars):
            attr = f.variables[v].ncattrs()
            if 'code' in attr:
                cods[i] = getattr(f.variables[v], 'code')
        f.close()
        return cods

    # long_name
    if long_names:
        lnames = [''] * nvars
        for i, v in enumerate(svars):
            attr = f.variables[v].ncattrs()
            if 'long_name' in attr:
                lnames[i] = getattr(f.variables[v], 'long_name')
        f.close()
        return lnames

    # units
    if units:
        unts = [''] * nvars
        for i, v in enumerate(svars):
            attr = f.variables[v].ncattrs()
            if 'units' in attr:
                unts[i] = getattr(f.variables[v], 'units')
        f.close()
        return unts

    # dims
    if dims:
        if (not var) and (code == -1):
            raise ValueError('var or code has to be given for'
                             ' inquiring dimensions.')
        if var:
            if var not in svars:
                f.close()
                raise ValueError(f'Variable {var} not in file {ncfile}.')
            dimensions = f.variables[var].dimensions
            f.close()
            return dimensions
        if code > -1:
            cods = [-1] * nvars
            for i, v in enumerate(svars):
                attr = f.variables[v].ncattrs()
                if 'code' in attr:
                    cods[i] = getattr(f.variables[v], 'code')
            if code not in cods:
                f.close()
                raise ValueError(f'Code {code} not in file {ncfile}.')
            var = svars[cods.index(code)]
            dimensions = f.variables[var].dimensions
            f.close()
            return dimensions

    # shape
    if shape:
        if (not var) and (code == -1):
            raise ValueError('var or code has to be given for'
                             ' inquiring its shape.')
        if var:
            if var not in svars:
                f.close()
                raise ValueError(f'Variable {var} not in file {ncfile}.')
            shape = f.variables[var].shape
            f.close()
            return shape
        if code > -1:
            cods = [-1] * nvars
            for i, v in enumerate(svars):
                attr = f.variables[v].ncattrs()
                if 'code' in attr:
                    cods[i] = getattr(f.variables[v], 'code')
            if code not in cods:
                f.close()
                raise ValueError(f'Code {code} not in file {ncfile}.')
            var = svars[cods.index(code)]
            shape = f.variables[var].shape
            f.close()
            return shape

    # attributes
    if attributes:
        # file attributes
        if (not var) and (code == -1):
            attrs = dict()
            attr = f.ncattrs()
            for a in attr:
                attrs[a] = getattr(f, a)
            f.close()
            return attrs

        # variables attributes
        if var:
            if var not in svars:
                f.close()
                raise ValueError(f'Variable {var} not in file {ncfile}.')
            attrs = dict()
            attr = f.variables[var].ncattrs()
            for a in attr:
                attrs[a] = getattr(f.variables[var], a)
            f.close()
            return attrs

        if code > -1:
            cods = [-1] * nvars
            for i, v in enumerate(svars):
                attr = f.variables[v].ncattrs()
                if 'code' in attr:
                    cods[i] = getattr(f.variables[v], 'code')
            if code not in cods:
                f.close()
                raise ValueError(f'Code {code} not in file {ncfile}.')
            var = svars[cods.index(code)]
            attrs = dict()
            attr = f.variables[var].ncattrs()
            for a in attr:
                attrs[a] = getattr(f.variables[var], a)
            f.close()
            return attrs

    # no keyword
    f.close()
    return


def infonetcdf(*args, **kwargs):
    """
    Wrapper for :func:`ncinfo`
    """
    return ncinfo(*args, **kwargs)


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

    >>> ncfile = 'test_readnetcdf.nc'
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

    >>> ncfile = 'test_readnetcdf1.nc'
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
