#!/usr/bin/env python
"""
netCDF4 functions to a copy netcdf file while doing some transformations on
variables and dimensions.

This module was written by Matthias Cuntz while at Institut National de
Recherche pour l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy,
France.

It borrows the idea of get_variable_definition from the netcdf4 thin layer of
David Schaefer.

:copyright: Copyright 2020-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   copy_dimensions
   copy_file
   copy_global_attributes
   copy_variables
   create_new_variable
   create_variables
   get_fill_value_for_dtype
   get_variable_definition
   set_output_filename

History
    * Written Apr 2020 by Matthias Cuntz (mc (at) macu (dot) de)
    * Added get_fill_value_for_dtype, Mar 2021, Matthias Cuntz
    * Added create_new_variable, Mar 2021, Matthias Cuntz
    * flake8 compatible, Mar 2021, Matthias Cuntz
    * Remove keyword in copy_global_attributes, Mar 2021, Matthias Cuntz
    * Add timedim in create_variables, Dec 2021, Matthias Cuntz
    * Rename functions, e.g. create_dimensions -> copy_dimensions,
      May 2022, Matthias Cuntz
    * Add copy_variables, May 2022, Matthias Cuntz
    * Delete unnecessary HDF5 filters in variable definition for compatibility
      with netcdf4 > 1.6.0, Jun 2022, Matthias Cuntz
    * Make get_variable_definition public, Apr 2023, Matthias Cuntz

"""
import numpy as np
import netCDF4 as nc


__all__ = ['copy_dimensions', 'copy_file', 'copy_global_attributes',
           'copy_variables', 'create_new_variable', 'create_variables',
           'get_fill_value_for_dtype', 'get_variable_definition',
           'set_output_filename']


def _tolist(arg):
    """
    Assure that *arg* is a list, e.g. if string or None are given.

    Parameters
    ----------
    arg :
        Argument to make list

    Returns
    -------
    list
        list(arg)

    Examples
    --------
    >>> _tolist('string')
    ['string']
    >>> _tolist([1,2,3])
    [1, 2, 3]
    >>> _tolist(None)
    [None]

    """
    if isinstance(arg, str):
        return [arg]
    try:
        return list(arg)
    except TypeError:
        return [arg]


def get_variable_definition(ncvar):
    """
    Collect information on input variable.

    Parameters
    ----------
    ncvar : netcdf4 variable
        Variable of input file

    Returns
    -------
    dict
        Containing information on input variable withkey/value pairs.
        The following keys are returned: 'name', 'dtype', 'dimensions',
        'fill_vallue', 'chunksizes'

    Examples
    --------
    .. code-block:: python

       get_variable_definition(fi.variables['GPP'])

    """
    out = ncvar.filters() if ncvar.filters() else {}
    # Delete HDF5 filters that are False, e.g. because the plugin is not
    # available. zlib is always available.
    # Necessary for netcdf4 > 1.6.0 because it gives all possible filters,
    # installed or not, i.e. 'zlib', 'szip', 'zstd', 'bzip2', 'blosc',
    # 'shuffle', 'complevel', 'fletcher32'
    todel = [ oo for oo in out if (oo != 'zlib') and (not out[oo]) ]
    for oo in todel:
        del out[oo]
    # chunksizes
    chunks = None
    if "chunking" in dir(ncvar):
        if ncvar.chunking() is not None:
            if not isinstance(ncvar.chunking(), str):
                chunks = list(ncvar.chunking())
    # missing value
    if "missing_value" in dir(ncvar):
        ifill = ncvar.missing_value
    elif "_FillValue" in dir(ncvar):
        ifill = ncvar._FillValue
    else:
        ifill = None
    # output variable
    out.update({
        "name":       ncvar.name,
        "dtype":      ncvar.dtype,
        "dimensions": list(ncvar.dimensions),
        "fill_value": ifill,
        "chunksizes": chunks,
    })
    return out


def copy_file(ifile, ofile, timedim='time',
              removevar=[], renamevar={}, replacevar={}, replaceatt={},
              noclose=False):
    """
    Copy variables from input file into output file.

    Parameters
    ----------
    ifile : str
        File name of netcdf input file
    ofile : str
        File name of netcdf output file
    timedim : str, optional
        Name of time dimension in input file (default: 'time').
    removevar : list of str, optional
        Do not copy variables given in *removevar* to output file.
    renamevar : dict, optional
        Copy variables from input file with different name in output file.
        Variable names in input file are given as dictionary keys,
        corresponding variable names of output file are give as dictionary
        values.
    replacevar : dict, optional
        Replace existing variables with variables in dictionary.
        Variable names in input file are given as dictionary keys,
        dictionary values are also dictionaries where keys are the output
        variable name and values are the output variable values.
    replaceatt : dict, optional
        Replace or set attributes of variables in dictionary keys
        (case sensitive). Dictionary values are also dictionaries with
        {'attribute_name': attribute_value}. Dictionary keys are the names
        of the output variables after renaming and replacing.
    noclose : bool, optional
        Return file handle of opened output file for further manipulation
        if True (default: False)

    Returns
    -------
    nothing or file_handle
        The output file will have the altered or unaltered variables
        copied from the input file.

    Examples
    --------
    .. code-block:: python

       ovar = np.arange(100)
       copy_variable('in.nc', 'out.nc',
                     renamevar={'lon': 'longitude'},
                     replacevar={'var1': {'arange': ovar}},
                     replaceatt={'arange':
                                 {'long_name': 'A range', 'unit': '-'}})

    """
    import time as ptime
    fi = nc.Dataset(ifile, 'r')
    if 'file_format' in dir(fi):
        fo = nc.Dataset(ofile, 'w', format=fi.file_format)
    else:  # pragma: no cover
        fo = nc.Dataset(ofile, 'w', format='NETCDF4')

    # meta data
    copy_global_attributes(
        fi, fo, add={'history': ptime.asctime() + ': ' +
                     'copy_variables(' + ifile + ', ' + ofile + ')'})

    # copy dimensions
    copy_dimensions(fi, fo)

    # create variables
    # rename replace variables as well
    xreplacevar = {}
    for rr in replacevar:
        nn = replacevar[rr].copy()
        kk = nn.popitem()[0]
        xreplacevar.update({rr: kk})
    arenamevar = renamevar.copy()
    arenamevar.update(xreplacevar)
    # create static variables (independent of time)
    create_variables(fi, fo, time=False, timedim=timedim, fill=True,
                     removevar=removevar, renamevar=arenamevar)
    # create dynamic variables (time dependent)
    create_variables(fi, fo, time=True, timedim=timedim, fill=True,
                     removevar=removevar, renamevar=arenamevar)

    # set extra attributes
    for rr in replaceatt:
        ovar = fo.variables[rr]
        att = replaceatt[rr]
        for aa in att:
            ovar.setncattr(aa, att[aa])

    # copy variables
    # do not copy replace variables
    aremovevar = _tolist(removevar)
    aremovevar.extend(xreplacevar.keys())
    copy_variables(fi, fo, time=False, timedim=timedim,
                   removevar=aremovevar, renamevar=renamevar)
    copy_variables(fi, fo, time=True, timedim=timedim,
                   removevar=aremovevar, renamevar=renamevar)

    # set replace variables
    for rr in replacevar:
        odict = replacevar[rr].copy()
        oname, oval = odict.popitem()
        ovar = fo.variables[oname]
        ovar[:] = oval

    fi.close()
    if noclose:
        return fo
    else:
        fo.close()
        return


def copy_dimensions(fi, fo, removedim=[], renamedim={}, changedim={},
                    adddim={}):
    """
    Create dimensions in output file from dimensions in input file.

    Parameters
    ----------
    fi : file_handle
        File handle of opened netcdf input file
    fo : file_handle
        File handle of opened netcdf output file
    removedim : list of str, optional
        Do not create dimensions given in *removedim* in output file.
    renamedim : dict, optional
        Rename dimensions in output file compared to input file.
        Dimension names in input file are given as dictionary keys,
        corresponding dimension names of output file are give as dictionary
        values.
    changedim : dict, optional
        Change the size of the output dimension compared to the input file.
        Dimension names are given as dictionary keys, corresponding dimension
        sizes are given as dictionary values.
    adddim : dict, optional
        Add dimension to output file.
        New dimension names are given as dictionary keys and new dimension
        sizes are given as dictionary values.

    Returns
    -------
    nothing
        The output file will have the altered and unaltered dimensions
        of the input file.

    Examples
    --------
    .. code-block:: python

       copy_dimensions(fi, fo, removedim=['patch'],
                       renamedim={'x': 'lon', 'y': 'lat'},
                       changedim={'mland': 1})

    """
    removedim = _tolist(removedim)
    for d in fi.dimensions.values():
        # remove dimension if in removedim
        if d.name not in removedim:
            # change dimension size if in changedim
            if d.name in changedim.keys():
                nd = changedim[d.name]
            elif d.isunlimited():
                nd = None
            else:
                nd = len(d)
            # rename dimension if in renamedim
            if d.name in renamedim.keys():
                oname = renamedim[d.name]
            else:
                oname = d.name
            # create dimension
            fo.createDimension(oname, nd)
    # add new dimensions
    for d in adddim.keys():
        if d not in fo.dimensions:
            fo.createDimension(d, adddim[d])
    return


def copy_global_attributes(fi, fo, add={}, remove=[]):
    """
    Create global output file attributes from input global file attributes.

    Parameters
    ----------
    fi : file_handle
        File handle of opened netcdf input file
    fo : file_handle
        File handle of opened netcdf output file
    add : dict, optional
        dict values will be given to attributes given in dict keys.
        Attributes will be created if they do not exist yet.
    remove : list, optional
        Do not create global attributes given in *remove* in the output file.

    Returns
    -------
    nothing
        Output will have global file attributes

    Examples
    --------
    .. code-block:: python

       copy_global_attributes(
           fi, fo, add={'history': time.asctime()+': '+' '.join(sys.argv)})

    """
    for k in fi.ncattrs():
        if k not in remove:
            iattr = fi.getncattr(k)
            # add to existing global attribute
            if k in add.keys():
                iattr += '\n'+add[k]
            fo.setncattr(k, iattr)
    # add if global attribute does not exist yet
    for k in add.keys():
        if k not in fi.ncattrs():
            fo.setncattr(k, add[k])
    return


def copy_variables(fi, fo, time=None, timedim='time',
                   removevar=[], renamevar={}):
    """
    Copy variables from input file into output file.

    Parameters
    ----------
    fi : file_handle
        File handle of opened netcdf input file
    fo : file_handle
        File handle of opened netcdf output file
    time : None or bool, optional
        None:  copy all variables (default).
        True:  copy only variables having dimension *timedim*.
        False: copy only variables that do not have dimension *timedim*.
    timedim : str, optional
        Name of time dimension (default: 'time').
    removevar : list of str, optional
        Do not copy variables given in *removevar* to output file.
    renamevar : dict, optional
        Copy variables from input file with different name in output file.
        Variable names in input file are given as dictionary keys,
        corresponding variable names of output file are give as dictionary
        values.

    Returns
    -------
    nothing
        The output file will have the altered or unaltered variables
        copied from the input file.

    Examples
    --------
    .. code-block:: python

       copy_variable(fi, fo, fill=True, renamevar={'lon': 'longitude'})

    """
    removevar = _tolist(removevar)
    # just copy all variables if no time dimension or
    # time dimension not known
    # Could be improved by looking for the unlimited dimension
    if timedim not in fi.dimensions:
        time = False
        ntime = 0
    else:
        ntime = fi.dimensions[timedim].size

    # collect variables with and without time dimension
    itvar = []     # w time dimension
    inottvar = []  # w/o time dimension
    if time or (time is None):
        for ivar in fi.variables.values():
            # remove variable if in removevar
            if ivar.name not in removevar:
                if timedim in ivar.dimensions:
                    itvar.append(ivar)

    if (not time) or (time is None):
        for ivar in fi.variables.values():
            # remove variable if in removevar
            if ivar.name not in removevar:
                if timedim not in ivar.dimensions:
                    inottvar.append(ivar)

    # copy static variables (not time-dependent)
    for ivar in inottvar:
        oname = ivar.name
        if ivar.name in renamevar.keys():
            oname = renamevar[ivar.name]
        ovar = fo.variables[oname]
        ovar[:] = ivar[:]

    # copy dynamic variables (time-dependent)
    for tt in range(ntime):
        for ivar in itvar:
            oname = ivar.name
            if ivar.name in renamevar.keys():
                oname = renamevar[ivar.name]
            ovar = fo.variables[oname]
            if ivar.ndim == 1:
                ovar[tt] = ivar[tt]
            else:
                ovar[tt, ...] = ivar[tt, ...]
    return


def create_new_variable(invardef, fo, izip=False, fill=None,
                        chunksizes=True):
    """
    Create variable in output file from dictionary with variable attributes.

    Parameters
    ----------
    invardef : dict
        Dictionary with name and dtype plus further attributes
        used in netCDF4.Dataset.createVariable; all other entries are set as
        variable attributes:
        'dimensions', 'zlib', 'complevel', 'shuffle', 'fletcher32',
        'contiguous', 'chunksizes', 'endian', 'least_significant_digit',
        'fill_value', 'chunk_cache'
    fo : file_handle
        File handle of opened netcdf output file
    izip : bool, optional
        True: the data will be compressed in the netCDF file using gzip
        compression independent of 'zlib' entry in input dictionary *invardef*
        (default: False).
    fill : float, bool or None, optional
        Determine the behaviour if variable has no _FillValue or missing_value.
        If None or False: no _FillValue will be set.
        If True: _FillValue will be set to default value of the Python netCDF4
        package for this type.
        If number: _FillValue will be set to number.
    chunksizes : bool, optional
        True: include possible chunksizes in output file (default).
        False: do not include chunksize information from input file in output
        file, even if given in input dictionary *invardef*.

    Returns
    -------
    variable handle
        Handle to newly created variable in output file.

    Examples
    --------
    .. code-block:: python

       nvar = {'name': 'new_field',
               'dtype': np.dtype(np.float),
               'dimensions': ('time', 'y', 'x'),
               'units': 'kg/m2/s',
               }
       ovar = create_new_variable(nvar, fo, fill=True, izip=True)

    """
    assert 'name' in invardef, 'name not in input dictionary'
    assert 'dtype' in invardef, 'dtype not in input dictionary'
    varname  = invardef.pop("name")
    datatype = invardef.pop("dtype")
    nckwargs = ['dimensions', 'zlib', 'complevel', 'shuffle', 'fletcher32',
                'contiguous', 'chunksizes', 'endian',
                'least_significant_digit', 'fill_value', 'chunk_cache']
    ncdict = dict()
    for nn in nckwargs:
        if nn in invardef:
            ncdict.update({nn: invardef.pop(nn)})
    if izip:
        ncdict.update({'zlib': True})
    if not chunksizes:
        if 'chunksizes' in ncdict:
            _ = ncdict.pop('chunksizes')
    if 'fill_value' not in ncdict:
        ncdict.update({'fill_value': None})
    # set missing value if None
    if ncdict['fill_value'] is None:
        if fill:
            if isinstance(fill, bool):
                ncdict['fill_value'] = get_fill_value_for_dtype(datatype)
            else:
                ncdict['fill_value'] = fill
    # create variable
    ovar = fo.createVariable(varname, datatype, **ncdict)
    # all other dict entries are attributes
    for k in invardef:
        ovar.setncattr(k, invardef[k])
    return ovar


def create_variables(fi, fo, time=None, timedim='time', izip=False, fill=None,
                     chunksizes=True, removevar=[], renamevar={}, removedim=[],
                     renamedim={}, replacedim={}):
    """
    Create variables in output from variables in input file.

    Parameters
    ----------
    fi : file_handle
        File handle of opened netcdf input file
    fo : file_handle
        File handle of opened netcdf output file
    time : None or bool, optional
        None:  create all variables (default).
        True:  create only variables having dimension *timedim*.
        False: create only variables that do not have dimension *timedim*.
    timedim : str, optional
        Name of time dimension (default: 'time').
    izip : bool, optional
        True: the data will be compressed in the netCDF file using gzip
        compression (default: False).
    fill : float, bool or None, optional
        Determine the behaviour if variable have no _FillValue or
        missing_value.
        If None or False: no _FillValue will be set.
        If True: _FillValue will be set to default value of the Python
        package netCDF4 for this type.
        If number: _FillValue will be set to number.
    chunksizes : bool, optional
        True: include possible chunksizes in output file (default).
        False: do not include chunksize information from input file in output
        file.
        Set to False, for example, if dimension size gets changed because the
        chunksize on a dimension can not be greater than the dimension size.
    removevar : list of str, optional
        Do not create variables given in *removevar* in output file.
    renamevar : dict, optional
        Rename variables in output file compared to input file.
        Variable names in input file are given as dictionary keys,
        corresponding variable names of output file are give as dictionary
        values.
    removedim : list of str, optional
        Remove dimensions from variable definitions in output file.
    renamedim : dict, optional
        Rename dimensions for variables in output file.
        Dimension names in input file are given as dictionary keys,
        corresponding dimension names of output file are give as dictionary
        values.
    replacedim : dict, optional
        Replace dimensions for variables in output file.
        Dimension names in input file are given as dictionary keys,
        corresponding dimension names of output file are given as dictionary
        values.
        The output names can be tuples or lists to extend dimensions of a
        variable.

    Returns
    -------
    nothing
        The output file will have the altered or unaltered variables
        of the input file defined.

    Examples
    --------
    .. code-block:: python

       create_variable(fi, fo, fill=True, izip=True, removedim=['patch'],
                       renamevar={'lon': 'longitude'},
                       replacedim={'land': ('y', 'x')})

    """
    removevar = _tolist(removevar)
    removedim = _tolist(removedim)
    for ivar in fi.variables.values():
        # remove variable if in removevar
        if ivar.name not in removevar:
            if time is None:
                itime = True
            else:
                if time:
                    itime = timedim in ivar.dimensions
                else:
                    itime = timedim not in ivar.dimensions
            if itime:
                invardef = get_variable_definition(ivar)
                if izip:
                    invardef.update({'zlib': True})
                # rename variable if in renamevar
                if ivar.name in renamevar.keys():
                    invardef['name'] = renamevar[ivar.name]
                # remove dimension if in removedim
                dims   = invardef['dimensions']
                chunks = invardef['chunksizes']
                for dd in removedim:
                    if dd in dims:
                        ip = dims.index(dd)
                        dims.remove(dd)
                        if chunks:
                            _ = chunks.pop(ip)
                # rename dimension if in renamedim
                for dd in renamedim.keys():
                    if dd in dims:
                        dims[dims.index(dd)] = renamedim[dd]
                # replace dimensions if in replacedim
                for dd in replacedim.keys():
                    if dd in dims:
                        rdim = _tolist(replacedim[dd])
                        ip = dims.index(dd)
                        dims = dims[:ip] + rdim + dims[ip+1:]
                        if chunks:
                            rchunk = []
                            for cc in rdim:
                                # use fo not fi because new dims perhaps
                                # not yet in fi
                                rchunk.append(len(fo.dimensions[cc]))
                            chunks = chunks[:ip] + rchunk + chunks[ip+1:]
                invardef['dimensions'] = dims
                invardef['chunksizes'] = chunks
                # set missing value if None
                if invardef['fill_value'] is None:
                    if fill:
                        if isinstance(fill, bool):
                            invardef['fill_value'] = get_fill_value_for_dtype(
                                invardef['dtype'])
                        else:
                            invardef['fill_value'] = fill
                # exclude chunksizes
                if not chunksizes:
                    _ = invardef.pop('chunksizes')
                oname = invardef.pop("name")
                otype = invardef.pop("dtype")
                ovar = fo.createVariable(oname, otype, **invardef)
                for k in ivar.ncattrs():
                    iattr = ivar.getncattr(k)
                    if (k != 'missing_value') and (k != '_FillValue'):
                        ovar.setncattr(k, iattr)
    return


def get_fill_value_for_dtype(dtype):
    """
    Get default _FillValue of netCDF4 for the given data type.

    Parameters
    ----------
    dtype : np.dtype
        numpy data type

    Returns
    -------
    default _FillValue of given numpy data type

    Examples
    --------
    .. code-block:: python

       fill_value = get_fill_value_for_dtype(var.dtype)

    """
    if dtype == np.dtype(np.int8):
        return nc.default_fillvals['i1']
    elif dtype == np.dtype(np.int16):
        return nc.default_fillvals['i2']
    elif dtype == np.dtype(np.int32):
        return nc.default_fillvals['i4']
    elif dtype == np.dtype(np.int64):
        return nc.default_fillvals['i8']
    elif dtype == np.dtype(np.uint8):
        return nc.default_fillvals['u1']
    elif dtype == np.dtype(np.uint16):
        return nc.default_fillvals['u2']
    elif dtype == np.dtype(np.uint32):
        return nc.default_fillvals['u4']
    elif dtype == np.dtype(np.uint64):
        return nc.default_fillvals['u8']
    elif dtype == np.dtype(np.float32):
        return nc.default_fillvals['f4']
    elif dtype == np.dtype(np.float64):
        return nc.default_fillvals['f8']
    else:
        import warnings
        warnings.warn("data type unknown: "+str(dtype))
        return None


def set_output_filename(ifile, ext):
    """
    Create output file name from input file name by adding *ext* before
    the file suffix.

    Parameters
    ----------
    ifile : str
        input file name
    ext : str
        string to add before file suffix

    Returns
    -------
    str
        output filename with ext before file suffix

    Examples
    --------
    >>> set_output_filename('in.nc', '-no_patch')
    in-no_patch.nc
    >>> set_output_filename('in.nc', '.nop')
    in.nop.nc

    """
    sifile = ifile.split('.')
    sifile[-2] = sifile[-2]+ext
    ofile = '.'.join(sifile)
    return ofile


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
