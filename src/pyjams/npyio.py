#!/usr/bin/env python
"""
Update arrays in a single file in numpy's npz format

This module was written by Matthias Cuntz while at Institut National de
Recherche pour l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy,
France.

:copyright: Copyright 2023- Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   updatez
   updatez_compressed

History
    * Written Jan 2023 by Matthias Cuntz (mc (at) macu (dot) de)

"""
import os
import zipfile
import tempfile
import shutil
import numpy as np
import numpy.lib.format as npformat


__all__ = ['updatez', 'updatez_compressed']


# copy from numpy.lib but replace os_fspath by os.fspath (from numpy.compat)
def zipfile_factory(file, *args, **kwargs):
    """
    Create a ZipFile.

    Allows for Zip64, and the `file` argument can accept file, str, or
    pathlib.Path objects. `args` and `kwargs` are passed to the zipfile.ZipFile
    constructor.
    """
    if not hasattr(file, 'read'):
        file = os.fspath(file)
    kwargs['allowZip64'] = True
    return zipfile.ZipFile(file, *args, **kwargs)


def updatez(file, *args, **kwds):
    """
    Update arrays in a single file in uncompressed ``.npz`` format.

    Provide arrays as keyword arguments to store them under the
    corresponding name in the output file: ``updatez(fn, x=x, y=y)``.

    If arrays are specified as positional arguments, i.e., ``updatez(fn,
    x, y)``, their names will be `arr_0`, `arr_1`, etc.

    If arrays do not exist yet in the npz-file, they will be appended.
    Existing arrays with the same name will be replaced by the new arrays.

    If ``file`` does not exist yet, ``updatez`` is a simple wrapper to
    ``numpy.savez``.

    Parameters
    ----------
    file : str
        Filename where the data will be saved. The ``.npz`` extension will be
        appended to the filename if it is not already there.
    args : Arguments, optional
        Arrays to save to the file. Please use keyword arguments (see
        `kwds` below) to assign names to arrays.  Arrays specified as
        args will be named "arr_0", "arr_1", and so on.
    kwds : Keyword arguments, optional
        Arrays to save to the file. Each array will be saved to the
        output file with its corresponding keyword name.

    Returns
    -------
    None

    See Also
    --------
    numpy.savez : Save several arrays into an uncompressed ``.npz`` archive
    numpy.savez_compressed : Save arrays into a compressed ``.npz`` archive
    pyjams.updatez_compressed : Update arrays in a compressed ``.npz`` archive
    numpy.load : Load the files created by updatez.

    Notes
    -----
    The ``.npz`` file format is a zipped archive of files named after the
    variables they contain.  The archive is not compressed and each file
    in the archive contains one variable in ``.npy`` format. For a
    description of the ``.npy`` format, see :py:mod:`numpy.lib.format`.

    When opening the saved ``.npz`` file with `load` a `NpzFile` object is
    returned. This is a dictionary-like object which can be queried for
    its list of arrays (with the ``.files`` attribute), and for the arrays
    themselves.

    Keys passed in `kwds` are used as filenames inside the ZIP archive.
    Therefore, keys should be valid filenames; e.g., avoid keys that begin with
    ``/`` or contain ``.``.

    When naming variables with keyword arguments, it is not possible to name a
    variable ``file`` as this would cause the argument ``file`` to be defined
    twice in the call to ``updatez``.

    Contrary to ``numpy.savez``, ``updatez`` allows only filenames and not
    file-like or path-like objects.

    Examples
    --------
    >>> import os
    >>> from tempfile import mkstemp
    >>> import numpy as np
    >>> fd, outfile = mkstemp('.npz')
    >>> os.close(fd)
    >>> x = np.arange(10)
    >>> y = np.sin(x)
    >>> xnew = np.arange(15)
    >>> ynew = np.sin(xnew)

    Using `numpy.savez` with \\*args, the arrays are saved with default names.

    >>> np.savez(outfile, x, y)
    >>> npzfile = np.load(outfile)
    >>> npzfile.files
    ['arr_0', 'arr_1']
    >>> npzfile['arr_0']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    Using `updatez` with \\*args, the arrays with default names will
    be overwritten.

    >>> npzfile.close()
    >>> updatez(outfile, xnew, ynew)
    >>> npzfile = np.load(outfile)
    >>> npzfile.files
    ['arr_0', 'arr_1']
    >>> npzfile['arr_0']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

    Using `updatez` with \\**kwds, the arrays are saved with the keyword names.

    >>> npzfile.close()
    >>> updatez(outfile, x=x, xnew=xnew)
    >>> npzfile = np.load(outfile)
    >>> sorted(npzfile.files)
    ['arr_0', 'arr_1', 'x', 'xnew']
    >>> npzfile['x']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> npzfile['xnew']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

    Clean up.

    >>> npzfile.close()
    >>> os.remove(outfile)

    """
    _updatez(file, args, kwds, False)


def updatez_compressed(file, *args, **kwds):
    """
    Update arrays in a single file in compressed ``.npz`` format.

    Provide arrays as keyword arguments to store them under the
    corresponding name in the output file:
    ``updatez_compressed(fn, x=x, y=y)``.

    If arrays are specified as positional arguments, i.e.,
    ``updatez_compressed(fn, x, y)``, their names will be `arr_0`, `arr_1`,
    etc.

    If arrays do not exist yet in the npz-file, they will be appended.
    Existing arrays with the same name will be replaced by the new arrays.

    If ``file`` does not exist yet, ``updatez_compressed`` is a simple wrapper
    to ``numpy.savez_compressed``.

    Parameters
    ----------
    file : str
        Filename where the data will be saved. The ``.npz`` extension will be
        appended to the filename if it is not already there.
    args : Arguments, optional
        Arrays to save to the file. Please use keyword arguments (see
        `kwds` below) to assign names to arrays.  Arrays specified as
        args will be named "arr_0", "arr_1", and so on.
    kwds : Keyword arguments, optional
        Arrays to save to the file. Each array will be saved to the
        output file with its corresponding keyword name.

    Returns
    -------
    None

    See Also
    --------
    numpy.savez : Save arrays into an uncompressed ``.npz`` file format
    numpy.savez_compressed : Save arrays into a compressed ``.npz`` file format
    pyjams.updatez : Update arrays in uncompressed ``.npz`` file format
    numpy.load : Load the files created by updatez_compressed.

    Notes
    -----
    The ``.npz`` file format is a zipped archive of files named after the
    variables they contain.  The archive is compressed with
    ``zipfile.ZIP_DEFLATED`` and each file in the archive contains one variable
    in ``.npy`` format. For a description of the ``.npy`` format, see
    :py:mod:`numpy.lib.format`.

    When opening the saved ``.npz`` file with `load` a `NpzFile` object is
    returned. This is a dictionary-like object which can be queried for
    its list of arrays (with the ``.files`` attribute), and for the arrays
    themselves.

    Keys passed in `kwds` are used as filenames inside the ZIP archive.
    Therefore, keys should be valid filenames; e.g., avoid keys that begin with
    ``/`` or contain ``.``.

    When naming variables with keyword arguments, it is not possible to name a
    variable ``file`` as this would cause the argument ``file`` to be defined
    twice in the call to ``updatez_compressed``.

    Contrary to ``numpy.savez_compressed``, ``updatez_compressed`` allows only
    filenames and not file-like or path-like objects.

    Examples
    --------
    >>> import os
    >>> from tempfile import mkstemp
    >>> import numpy as np
    >>> fd, outfile = mkstemp('.npz')
    >>> os.close(fd)
    >>> x = np.arange(10)
    >>> y = np.sin(x)
    >>> xnew = np.arange(15)
    >>> ynew = np.sin(xnew)

    Using `numpy.savez_compressed` with \\*args, the arrays are saved with
    default names.

    >>> np.savez_compressed(outfile, x, y)
    >>> npzfile = np.load(outfile)
    >>> npzfile.files
    ['arr_0', 'arr_1']
    >>> npzfile['arr_0']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    Using `updatez_compressed` with \\*args, the arrays with default names will
    be overwritten.

    >>> npzfile.close()
    >>> updatez_compressed(outfile, xnew, ynew)
    >>> npzfile = np.load(outfile)
    >>> npzfile.files
    ['arr_0', 'arr_1']
    >>> npzfile['arr_0']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

    Using `updatez_compressed` with \\**kwds, the arrays are saved with
    the keyword names.

    >>> npzfile.close()
    >>> updatez_compressed(outfile, x=x, xnew=xnew)
    >>> npzfile = np.load(outfile)
    >>> sorted(npzfile.files)
    ['arr_0', 'arr_1', 'x', 'xnew']
    >>> npzfile['x']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> npzfile['xnew']
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

    Clean up.

    >>> npzfile.close()
    >>> os.remove(outfile)

    """
    _updatez(file, args, kwds, True)


def _updatez(file, args, kwds, compress,
             allow_pickle=True, pickle_kwargs=None):

    if hasattr(file, 'write'):
        raise ValueError('Only filenames allowed, not file-like or'
                         ' path-like objects.')
    file = os.fspath(file)
    if not file.endswith('.npz'):
        file = file + '.npz'
    if not os.path.exists(file):
        if compress:
            np.savez_compressed(file, *args, **kwds)
        else:
            np.savez(file, *args, **kwds)
        return
    elif not zipfile.is_zipfile(file):
        if compress:
            np.savez_compressed(file, *args, **kwds)
        else:
            np.savez(file, *args, **kwds)
        return

    namedict = kwds
    for i, val in enumerate(args):
        key = 'arr_%d' % i
        if key in namedict.keys():
            raise ValueError("Cannot use un-named variables and keyword %s" %
                             key)
        namedict[key] = val

    if compress:
        compression = zipfile.ZIP_DEFLATED
    else:
        compression = zipfile.ZIP_STORED

    # memmap original file again
    zipfo = np.load(file, mmap_mode='r')

    # open temporary file
    dtemp = tempfile.mkdtemp()
    ftemp = os.path.join(dtemp, 'update.npz')
    zipf = zipfile_factory(ftemp, mode='w', compression=compression)

    # write arrays of original file without new arrays
    for key in zipfo.keys():
        if key not in namedict.keys():
            fname = key + '.npy'
            with zipf.open(fname, 'w', force_zip64=True) as fid:
                npformat.write_array(fid, zipfo[key],
                                     allow_pickle=allow_pickle,
                                     pickle_kwargs=pickle_kwargs)

    # write new arrays
    for key, val in namedict.items():
        fname = key + '.npy'
        val = np.asanyarray(val)
        with zipf.open(fname, 'w', force_zip64=True) as fid:
            npformat.write_array(fid, val,
                                 allow_pickle=allow_pickle,
                                 pickle_kwargs=pickle_kwargs)

    # close and move temporary file back to original file
    zipfo.close()
    zipf.close()
    shutil.move(ftemp, file)
    shutil.rmtree(dtemp)
