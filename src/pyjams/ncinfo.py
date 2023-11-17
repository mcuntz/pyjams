#!/usr/bin/env python
"""
Information on a netcdf file

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
   ncinfo
   infonetcdf

History
    * Written Mar 2022 from ncread by moving all info abilities into separate
      routine infonetcdf with wrapper function ncinfo, Mar 2022, Matthias Cuntz
    * Invert functions and wrapper functions, Feb 2023, Matthias Cuntz
    * Move ncinfo in separate file, Nov 2023, Matthias Cuntz
    * sort=True default, Nov 2023, Matthias Cuntz
    * Enforce keywords after var, Nov 2023, Matthias Cuntz

"""


__all__ = ['ncinfo', 'infonetcdf']


def ncinfo(ncfile,
           var='', *, code=-1,
           variables=False, codes=False,
           long_names=False, units=False,
           dims=False, shape=False, attributes=False,
           sort=True):
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
    dims : bool, optional
        Get tuple of dimension names for the variable with name *var*
        or number *code*.
    shape : bool, optional
        Get shape of the variable with name *var* or number *code*.
    attributes : bool, optional
        Get dictionary of all attributes of variable with name *var* or number
        *code*, or all file attributes of *ncfile* if *var* and *code* are not
        given
    sort : bool, optional
        If True (default), sort output of *variables*, *codes*, *units*,
        and *long_names* with variable name as the sort key

    Returns
    -------
    tuple of variable dimension names,
    tuple of variable dimensions,
    list of variable names, codes, units, long_names, or
    dictionary of attributes


    Examples
    --------

    Get variable names

    >>> ncfile = 'test_ncread.nc'
    >>> print([ str(i) for i in ncinfo(ncfile, variables=True) ])
    ['x', 'y', 'is1', 'is2']
    >>> print([ str(i)
    ...        for i in ncinfo(ncfile, variables=True, sort=True) ])
    ['is1', 'is2', 'x', 'y']

    Get codes

    >>> print(ncinfo(ncfile, codes=True))
    [128, 129, -1, -1]
    >>> print(ncinfo(ncfile, codes=True, sort=True))
    [128, 129, -1, -1]
    >>> print(ncinfo(ncfile, codes=True, sort=False))
    [-1, -1, 128, 129]

    Get special attributes units and long_names

    >>> print([ str(i) for i in ncinfo(ncfile, units=True) ])
    ['arbitrary', 'arbitrary', 'xx', 'yy']
    >>> print([ str(i) for i in ncinfo(ncfile, units=True, sort=False) ])
    ['xx', 'yy', 'arbitrary', 'arbitrary']
    >>> print([ str(i) for i in ncinfo(ncfile, long_names=True) ])
    ['all ones', 'all twos', 'x-axis', 'y-axis']

    Get dims

    >>> print([ str(i) for i in ncinfo(ncfile, var='is1', dims=True) ])
    ['y', 'x']

    Get shape

    >>> print(ncinfo(ncfile, 'is1', shape=True))
    (2, 4)

    Get attributes

    >>> t1 = ncinfo(ncfile, 'is1', attributes=True)
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
        cods = [-1] * nvars
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


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
