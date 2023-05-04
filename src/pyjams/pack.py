#!/usr/bin/env python
"""
Mimics Fortran intrinsic pack and unpack functions

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2009-2023 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   pack
   unpack

History
    * Written Jul 2009 by Matthias Cuntz (mc (at) macu (dot) de)
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Assert matching mask and array dimensions, Apr 2014, Matthias Cuntz
    * Code refactoring, Sep 2021, Matthias Cuntz
    * Port to pyjams, May 2023, Matthias Cuntz
    * Rename value keyword to fill_value as in numpy masked arrays,
      May 2023, Matthias Cuntz
    * Assert output type equals input type, May 2023, Matthias Cuntz

"""
import numpy as np


__all__ = ['pack', 'unpack']


def pack(array, mask):
    """
    Mimics Fortran intrinsic pack (without optional vector)

    Packs the last dimensions of an arbitrary shaped array
    into a one dimensional array under a mask.

    The mask can have any number of dimensions up to the array dimension.

    Parameters
    ----------
    array : array
        ND-array to be packed
    mask : array
        Boolean ND-array with number of dimensions <= `array` dimensions

    Returns
    -------
    array
        `array` with reduced dimensions by number of mask dimensions minus one.
        Last dimension has only elements that correspond to elements of
        `mask == True`.

    Notes
    -----
    Result is undefined if all mask values are False.

    Examples
    --------

    Create some data for example an island in the middle of an ocean

    >>> import numpy as np
    >>> island = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    ...                    [0., 0., 0., 1., 1., 1., 0., 0., 0., 0.],
    ...                    [0., 0., 0., 1., 1., 1., 0., 0., 0., 0.],
    ...                    [0., 0., 0., 1., 1., 1., 0., 0., 0., 0.],
    ...                    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])

    Pack array to keep only the elements of the island

    >>> mask = island == 1.0
    >>> pisland = pack(island, mask)
    >>> print(pisland.size, pisland.shape)
    9 (9,)
    >>> print(island.sum(), pisland.sum())
    9.0 9.0
    >>> print(pisland)
    [1. 1. 1. 1. 1. 1. 1. 1. 1.]

    Create data on the ocean and on the island for 2 time steps

    >>> tshape = (2, *island.shape)
    >>> temp = np.arange(np.prod(tshape)).reshape(tshape)

    Pack array to keep only the elements of the island

    >>> ptemp = pack(temp, mask)
    >>> print(ptemp.size, ptemp.shape)
    18 (2, 9)
    >>> print(ptemp)
    [[13 14 15 23 24 25 33 34 35]
     [63 64 65 73 74 75 83 84 85]]

    """
    dmask   = mask.shape
    ndmask  = np.ndim(mask)
    nmask   = mask.size
    darray  = array.shape
    ndarray = np.ndim(array)
    narray  = array.size

    # Check array and mask
    assert ndarray >= ndmask, (f'Input array has less dimensions {ndarray}'
                               f' then mask {ndmask}')
    k = 0
    while k > -ndmask:
        k -= 1
        assert dmask[k] == darray[k], (
            f'Input array and mask must have the same last dimensions.'
            f'Array: {darray}, Mask: {dmask}' )

    # Make array and mask 1d
    farray = array.ravel()  # flat in Fortran=column-major mode
    fmask  = mask.ravel()
    afmask = np.empty(narray, dtype=bool)
    nn = narray // nmask
    k  = 0
    while k < nn:
        afmask[k * nmask: (k + 1) * nmask] = fmask[:]
        k += 1

    # Mask array and reshape
    afarray = farray[afmask]
    dout = list(darray)
    k = 0
    while k < ndmask:
        del dout[-1]
        k += 1
    nnmask = int(mask.sum())
    dout.append(nnmask)
    out = np.reshape(afarray, dout)

    return out


def unpack(array, mask, fill_value=0):
    """
    Mimics Fortran intrinsic unpack (without optional field)

    Unpacks the last dimension into several dimensions under a mask.
    The unpacked elements will be set to a user-defined fill_value.
    The mask can have any number of dimensions up to the array dimensions.

    Parameters
    ----------
    array : array
        ND-array to be unpacked
    mask : array
        Boolean ND-array
    fill_value : float, optional
        Value of the new elements (default: 0)

    Returns
    -------
    array
        `array` having more dimensions by number of mask dimensions minus one.
        The new elements have the user-defined `fill_value`.

    Notes
    -----
    Result is undefined if all mask values are False.


    Examples
    --------

    Create some data for example an island in the middle of an ocean

    >>> import numpy as np
    >>> island = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
    ...                    [0., 0., 0., 1., 1., 1., 0., 0., 0., 0.],
    ...                    [0., 0., 0., 1., 1., 1., 0., 0., 0., 0.],
    ...                    [0., 0., 0., 1., 1., 1., 0., 0., 0., 0.],
    ...                    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
    >>> print(island.size, island.shape)
    50 (5, 10)

    Pack array to keep only the elements of the island

    >>> mask = island == 1.0
    >>> pisland = pack(island, mask)
    >>> print(pisland.size, pisland.shape)
    9 (9,)

    Unpack the ocean and island data again

    >>> uisland = unpack(pisland, mask)
    >>> print(uisland.size, uisland.shape)
    50 (5, 10)
    >>> print(np.all(uisland == island))
    True

    Unpack the ocean and island data, filling ocean with -9

    >>> uisland = unpack(pisland, mask, -9)
    >>> print(uisland.size, uisland.shape)
    50 (5, 10)
    >>> print(uisland)
    [[-9. -9. -9. -9. -9. -9. -9. -9. -9. -9.]
     [-9. -9. -9.  1.  1.  1. -9. -9. -9. -9.]
     [-9. -9. -9.  1.  1.  1. -9. -9. -9. -9.]
     [-9. -9. -9.  1.  1.  1. -9. -9. -9. -9.]
     [-9. -9. -9. -9. -9. -9. -9. -9. -9. -9.]]

    Create data on the ocean and on the island for 2 time steps

    >>> tshape = (2, *island.shape)
    >>> temp = np.arange(np.prod(tshape)).reshape(tshape)

    >>> print(temp.size, temp.shape)
    100 (2, 5, 10)

    Pack array to keep only the elements of the island

    >>> ptemp = pack(temp, mask)
    >>> print(ptemp.size, ptemp.shape)
    18 (2, 9)

    Unpack the ocean and island data.
    Note the ocean will have the fill_value -1 not its original data.

    >>> utemp = unpack(ptemp, mask, fill_value=-1.)
    >>> print(utemp.size, utemp.shape)
    100 (2, 5, 10)
    >>> ii = np.where(utemp != -1.)
    >>> print(np.all(utemp[ii] == temp[ii]))
    True

    """
    dmask   = np.shape(mask)
    ndmask  = len(dmask)
    nmask   = mask.size
    darray  = np.shape(array)
    ndarray = len(darray)
    narray  = array.size

    # Check array and mask
    ntmask = int(mask.sum())
    assert darray[-1] == ntmask, (
        f'Last dimension of input array {darray[-1]} must have same size'
        f' as true values in mask {ntmask}.' )

    # Make multi mask array array
    icount = nmask
    for i in range(ndarray - 1):
        icount *= darray[i]
    mask1d = np.ravel(mask)
    masknd = np.empty(icount, dtype='bool')
    for i in range(icount // nmask):
        masknd[i * nmask:(i + 1) * nmask] = mask1d[:]

    # Make indeces
    index = np.arange(icount)
    ii = index[masknd]
    if len(ii) != narray:
        raise ValueError(f'Index creation failed. Index {len(ii)} Array'
                         f' {narray}.')

    # Flat output array
    array1d = np.ravel(array)
    arraynd = np.ones(icount, dtype=array.dtype) * fill_value
    arraynd[ii] = array1d[:]

    # Reshaped output array
    newdim = list(darray[0:-1])
    for i in range(ndmask):
        newdim.append(dmask[i])
    out = np.reshape(arraynd, newdim)

    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
