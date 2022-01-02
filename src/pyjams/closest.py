#!/usr/bin/env python
"""
Index in array which entry is closest to a given number.

This module was written by Matthias Cuntz while at Department of Computational
Hydrosystems, Helmholtz Centre for Environmental Research - UFZ, Leipzig,
Germany, and continued while at Institut National de Recherche pour
l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2012-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   closest

History
    * Written Jan 2012 by Matthias Cuntz (mc (at) macu (dot) de)
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Make numpy docstring format, Apr 2020, Matthias Cuntz
    * Ported into pyjams, Oct 2021, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz

"""
from __future__ import division, absolute_import, print_function
import numpy as np


__all__ = ['closest']


def closest(arr, num, value=False):
    """
    Index in array which entry is closest to a given number.

    Closest returns the index of an array (arr) at which the entry is closest
    to a given number (num), which is `argmin(abs(arr-num))`.

    Parameters
    ----------
    arr : array_like
        Array to search closest entry
    num : number
        Number to which the closest entry is searched for in arr
    value : bool, optional
        Returns closest array element instead of index if True (default: False)

    Returns
    -------
    index : int
        Index of element closest to given number in flattend array.
        Use np.unravel_index to get index tuple.

    Examples
    --------
    >>> arr = np.arange(100)/99.*5.
    >>> print(closest(arr, 3.125))
    62
    >>> out = closest(arr, 3.125, value=True)
    >>> print('{:.3f}'.format(out))
    3.131

    >>> arr = np.arange(100).reshape((10,10))/99.*5.
    >>> out = closest(arr, 3.125, value=True)
    >>> print('{:.3f}'.format(out))
    3.131
    >>> print(closest(arr, 3.125))
    62
    >>> ii = np.unravel_index(closest(arr, 3.125), arr.shape)
    >>> print(ii)
    (6, 2)
    >>> out = arr[ii]
    >>> print('{:.3f}'.format(out))
    3.131

    """
    out = np.ma.argmin(np.ma.abs(np.ma.array(arr)-num))
    if value:
        return arr.flat[out]
    else:
        return out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
