#!/usr/bin/env python
"""
Divide two arrays, return `otherwise` if division by 0.

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2012-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   division
   div

History
    * Written Jan 2012 by Matthias Cuntz (mc (at) macu (dot) de)
    * Added wrapper div, May 2012, Matthias Cuntz
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Do not return masked array if no masked array given,
      Oct 2014, Matthias Cuntz
    * Added two-digit year, Nov 2018, Matthias Cuntz
    * Removed bug that non-masked array was returned if masked array given,
      Sep 2015, Matthias Cuntz
    * Using numpy docstring format, May 2020, Matthias Cuntz
    * Output type is input type, Oct 2021, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz
    * Use helper functions input2array and array2input,
      Mar 2022, Matthias Cuntz
    * Do not use geterr/seterr, Mar 2022, Matthias Cuntz

"""
import numpy as np
from .helper import input2array, array2input
# from helper import input2array, array2input


__all__ = ['division', 'div']


def division(a, b, otherwise=np.nan, prec=0.):
    """
    Divide two arrays, return `otherwise` if division by 0.

    Parameters
    ----------
    a : array_like
        Enumerator
    b : array_like
        Denominator
    otherwise : float
        Value to return if `b=0` (default: `np.nan`)
    prec : float
        If `|b|<|prec|` then `otherwise`

    Returns
    -------
    ratio : numpy array or masked array
        *a/b* if *|b| >  |prec|*, *otherwise* if *|b| <= |prec|*

    Notes
    -----
    Output is numpy array. It is a masked array if at least one of *a* or *b*
    is a masked array.

    Examples
    --------
    >>> a = [1., 2., 3.]
    >>> b = 2.
    >>> print('{:.1f} {:.1f} {:.1f}'.format(*division(a, b)))
    0.5 1.0 1.5

    >>> a = [1., 1., 1.]
    >>> b = [2., 1., 0.]
    >>> print(division(a, b))
    [0.5, 1.0, nan]
    >>> print(division(a, b, 0.))
    [0.5, 1.0, 0.0]
    >>> print(division(a, b, otherwise=0.))
    [0.5, 1.0, 0.0]
    >>> print(division(a, b, prec=1.))
    [0.5, nan, nan]

    >>> import numpy as np
    >>> a = np.array([1., 1., 1.])
    >>> b = [2., 1., 0.]
    >>> print(division(a, b))
    [0.5 1.  nan]
    >>> b = np.array([2., 1., 0.])
    >>> print(division(a, b))
    [0.5 1.  nan]

    >>> mask = [0, 0, 1]
    >>> b = np.ma.array([2., 1., 0.], mask=mask)
    >>> print(division(a, b))
    [0.5 1.0 --]

    """
    aa = input2array(a, undef=np.nan, default=0)
    bb = input2array(b, undef=np.nan, default=1)

    bbb = np.where(np.abs(bb) > np.abs(prec), bb, 1)
    out = np.where(np.abs(bb) > np.abs(prec), aa / bbb, otherwise)

    out = array2input(out, a, b, undef=np.nan)

    return out


def div(*args, **kwargs):
    """
    Wrapper function for :func:`division`.

    Examples
    --------
    >>> a = [1., 2., 3.]
    >>> b = 2.
    >>> print(div(a, b))
    [0.5, 1.0, 1.5]

    >>> a = [1., 1., 1.]
    >>> b = [2., 1., 0.]
    >>> print(div(a, b))
    [0.5, 1.0, nan]
    >>> print(div(a, b, 0.))
    [0.5, 1.0,  0.0]
    >>> print(div(a, b, otherwise=0.))
    [0.5, 1.0, 0.0]
    >>> print(div(a, b, prec=1.))
    [0.5, nan, nan]

    """
    return division(*args, **kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
