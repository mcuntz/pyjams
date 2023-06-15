#!/usr/bin/env python
from __future__ import division, absolute_import, print_function
import numpy as np
from pyjams.jams.around import around
from pyjams.const import eps


__all__ = ['yrange']


def yrange(*args, **kwargs):
    """
    Calculates plot range from input array


    Definition
    ----------
    def yrange(arr, symmetric=False):


    Input
    -----
    arr        number array


    Optional Input
    --------------
    symmetric  if True, range will be symmetric around 0.
               if min(arr)<0 and max(arr)>0.


    Output
    ------
    Range to be used as [xyz]range


    Restrictions
    ------------
    Uses around.
    Does not work well for 0<range<1. Use yrange(arr*10.)/10.


    Examples
    --------
    >>> import numpy as np
    >>> print(yrange(range(102)))
    [0.0, 101.0]

    >>> print(yrange(np.arange(102)-10.))
    [-10.0, 91.0]

    >>> print(yrange(np.arange(102)-10., symmetric=True))
    [-91.0, 91.0]

    >>> print(yrange(range(102), range(1002), np.arange(10002)))
    [0.0, 10001.0]

    >>> print(yrange(-np.arange(102), np.arange(1002), np.arange(10002)))
    [-101.0, 10001.0]

    >>> print(yrange(-np.arange(102), np.arange(1002), np.arange(10002), symmetric=True))
    [-10001.0, 10001.0]

    >>> print(yrange(-np.arange(102), np.arange(1002), np.arange(10002), symmetric=False))
    [-101.0, 10001.0]

    >>> a = np.ma.arange(102)
    >>> a[-1] = np.ma.masked
    >>> print(yrange(a))
    [0.0, 100.0]

    >>> a = np.ma.arange(102, dtype=float)
    >>> a[-1] = np.ma.masked
    >>> a[-2] = np.nan
    >>> print(yrange(a))
    [0.0, 99.0]


    License
    -------
    This file is part of the JAMS Python package, distributed
    under the MIT License. The JAMS Python package originates from the former
    UFZ Python library, Department of Computational Hydrosystems, Helmholtz
    Centre for Environmental Research - UFZ, Leipzig, Germany.

    Copyright (c) 2012-2016 Matthias Cuntz - mc (at) macu (dot) de

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.


    History
    -------
    Written,  Matthias Cuntz, Jan 2012
    Modified, Matthias Cuntz, Feb 2013 - ported to Python 3
              Matthias Cuntz, Nov 2013 - accept more than 1 array as input
              Matthias Cuntz, Nov 2013 - masked arrays
              Matthias Cuntz, Apr 2014 - assert
              Matthias Cuntz, Nov 2016 - const.tiny -> const.eps
              Matthias Cuntz, Nov 2019 - mask NaN values, e.g. from Pandas
    """
    # Check input
    assert len(args) > 0, 'no input argument given.'
    counter = 0
    for i in args:
        if np.any(np.isnan(i)):
            arr = np.ma.array(i, mask=np.isnan(i))
        else:
            arr    = np.ma.array(i)
        minarr = np.ma.amin(arr)
        maxarr = np.ma.amax(arr)
        # Round to max difference between adjacent values
        if arr.size == 1:
            expom = 0
        else:
            sarr    = np.ma.sort(arr)
            maxdiff = np.ma.amax(np.diff(sarr))
            expom   = np.ma.log10(maxdiff)
            if expom > 0:
                expom = int(np.floor(expom + 10. * eps * 10.))
            else:
                expom = int(np.floor(expom - 10. * eps))
        if counter == 0:
            minall   = minarr
            maxall   = maxarr
            expomall = expom
        else:
            minall   = np.minimum(minall, minarr)
            maxall   = np.maximum(maxall, maxarr)
            if expomall > 0:
                expomall = np.maximum(expomall, expom)
            else:
                expomall = np.minimum(expomall, expom)
        counter += 1

    # Round range
    mini = around(minall, expomall, floor=True)
    maxi = around(maxall, expomall, ceil=True)

    if 'symmetric' in kwargs:
        if kwargs['symmetric']:
            if (mini * maxi < 0.):
                maxmax = np.maximum(np.abs(mini), np.abs(maxi))
                maxi   = maxmax
                mini   = -maxmax

    # Return range
    return [mini, maxi]


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # import numpy as np

    # print(yrange(np.arange(102)))
    # #[0.0, 101.0]

    # print(yrange(np.arange(102)-10.))
    # #[-10.0, 91.0]

    # print(yrange(np.arange(102)-10., symmetric=True))
    # #[-91.0, 91.0]

    # print(yrange(np.arange(102), np.arange(1002), np.arange(10002)))
    # #[0.0, 10001.0]

    # print(yrange(-np.arange(102), np.arange(1002), np.arange(10002)))
    # #[-101.0, 10001.0]

    # print(yrange(-np.arange(102), np.arange(1002), np.arange(10002), symmetric=True))
    # #[-10001.0, 10001.0]

    # print(yrange(-np.arange(102), np.arange(1002), np.arange(10002), symmetric=False))
    # #[-101.0, 10001.0]

    # a = np.ma.arange(102)
    # a[-1] = np.ma.masked
    # print(yrange(a))
    # #[0.0, 100.0]
