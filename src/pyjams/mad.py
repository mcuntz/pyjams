#!/usr/bin/env python
"""
Median absolute deviation test

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2011-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   mad

History
    * Written Nov 2011 by Matthias Cuntz - mc (at) macu (dot) de
    * ND-array, act on axis=0, May 2012, Matthias Cuntz
    * Removed bug in broadcasting, axis=0 did not always work: spread md and
      MAD to input dimensions, Jun 2012, Matthias Cuntz
    * Better usage of numpy possibilities, e.g. using np.diff,
      remove spreads, Jun 2012, Matthias Cuntz
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Use bottleneck for medians, otherwise loop over axis=1,
      Jul 2013, Matthias Cuntz and Juliane Mai
    * Re-allow masked arrays and arrays with NaNs, Jul 2013, Matthias Cuntz
    * Removed bug in NaN treatment, Oct 2013, Matthias Cuntz
    * Keyword nonzero, Oct 2013, Matthias Cuntz
    * Using numpy docstring format, May 2020, Matthias Cuntz
    * Code refactoring, Sep 2021, Matthias Cuntz
    * Ported to pyjams, Jan 2022, Matthias Cuntz
    * Only one test of bottleneck availability, Jan 2022, Matthias Cuntz
    * Return all False instead of all True if all masked before MAD started,
      Jan 2022, Matthias Cuntz

"""
import numpy as np


__all__ = ['mad']


def mad(datin, z=7, deriv=0, nozero=False):
    """
    Median absolute deviation test

    The test acts either on raw values, or on 1st or 2nd derivatives.

    Return mask with True where value is out of range, i.e.
    :math:`< (median - z.MAD/0.6745)` or :math:`> (md + z.MAD/0.6745)`.

    Parameters
    ----------
    datin : array or masked array
        `mad` acts on ``axis=0``
    z : float, optional
        Input is allowed to deviate maximum *z* (estimators of) standard
        deviations from the median (default: 7)
    deriv : int, optional
        Act on raw input (0, default), on first derivatives (1), or on 2nd
        derivatives (2)
    nozero : bool, optional
        Exclude zeros (0.) from input *datin* if True.

    Returns
    -------
    array of bool
        False everywhere except where input deviates more than
        *z* standard deviations from median

    Notes
    -----
    If input is an nd-array then mad is checked along the first axis for
    outliers.

    1st derivative is calculated simply as ``d = datin[1:n]-datin[0:n-1]``
    because mean of left and right difference would give 0 for spikes.

    If ``all(d.mask==True)`` then return ``d.mask``, which is all True.

    NaN does not return True because this would remove points adjacent to NaN
    if ``deriv>0``.

    Examples
    --------
    >>> import numpy as np
    >>> y = np.array([-0.25, 0.68, 0.94, 1.15, 2.26, 2.35, 2.37, 2.40, 2.47,
    ...               2.54, 2.62, 2.64, 2.90, 2.92, 2.92, 2.93, 3.21, 3.26,
    ...               3.30, 3.59, 3.68, 4.30, 4.64, 5.34, 5.42, 8.01])

    MAD on raw data

    >>> print(mad(y))
    [False False False False False False False False False False False False
     False False False False False False False False False False False False
     False False]
    >>> print(mad(y, z=4))
    [False False False False False False False False False False False False
     False False False False False False False False False False False False
     False  True]
    >>> print(mad(y, z=3))
    [ True False False False False False False False False False False False
     False False False False False False False False False False False False
      True  True]

    MAD on 2nd derivatives

    >>> print(mad(y, z=4, deriv=2))
    [False False False False False False False False False False False False
     False False False False False False False False False False False  True]

    Use for masking arrays

    >>> my = np.ma.array(y, mask=mad(y, z=4))
    >>> print(my)
    [-0.25 0.68 0.94 1.15 2.26 2.35 2.37 2.4 2.47 2.54 2.62 2.64 2.9 2.92 2.92
     2.93 3.21 3.26 3.3 3.59 3.68 4.3 4.64 5.34 5.42 --]

    MAD on several dimensions

    >>> yy = np.transpose(np.array([y, y]))
    >>> print(np.transpose(mad(yy, z=4)))
    [[False False False False False False False False False False False False
      False False False False False False False False False False False False
      False  True]
     [False False False False False False False False False False False False
      False False False False False False False False False False False False
      False  True]]
    >>> yyy = np.transpose(np.array([y, y, y]))
    >>> print(np.transpose(mad(yyy, z=3)))
    [[ True False False False False False False False False False False False
      False False False False False False False False False False False False
       True  True]
     [ True False False False False False False False False False False False
      False False False False False False False False False False False False
       True  True]
     [ True False False False False False False False False False False False
      False False False False False False False False False False False False
       True  True]]

    Masked arrays

    >>> my = np.ma.array(y, mask=np.zeros(y.shape))
    >>> my.mask[-1] = True
    >>> print(mad(my, z=4))
    [True False False False False False False False False False False False
     False False False False False False False False False False False False
     False --]
    >>> print(mad(my, z=3))
    [True False False False False False False False False False False False
     False False False False False False False False False False False True
     True --]

    Arrays with NaNs

    >>> ny = y.copy()
    >>> ny[-1] = np.nan
    >>> print(mad(ny, z=4))
    [ True False False False False False False False False False False False
     False False False False False False False False False False False False
     False False]
    >>> print(mad(ny, z=3))
    [ True False False False False False False False False False False False
     False False False False False False False False False False False  True
      True False]

    Exclude zeros

    >>> zy = y.copy()
    >>> zy[1] = 0.
    >>> print(mad(zy, z=3))
    [ True  True False False False False False False False False False False
     False False False False False False False False False False False False
      True  True]
    >>> print(mad(zy, z=3, nozero=True))
    [ True False False False False False False False False False False False
     False False False False False False False False False False False False
      True  True]

    """
    if nozero:
        idatin = datin.copy()
        ii = np.where(idatin == 0.)[0]
        if ii.size > 0:
            idatin[ii] = np.nan
    else:
        idatin = datin
    sn = list(np.shape(idatin))
    n  = sn[0]
    if deriv == 0:
        m      = n
        d      = idatin
    elif deriv == 1:
        m      = n-1
        sm     = sn
        sm[0]  = m
        d      = np.diff(idatin, axis=0)
    elif deriv == 2:
        m      = n-2
        sm     = sn
        sm[0]  = m
        d      = np.diff(idatin, n=2, axis=0)
    else:
        raise ValueError('Unimplemented option.')

    # Shortcut if all masked
    ismasked = isinstance(d, np.ma.MaskedArray)
    if not ismasked:
        ii = np.where(~np.isfinite(d))[0]
        d  = np.ma.array(d)
        if ii.size > 0:
            d[ii] = np.ma.masked

    if np.all(d.mask):
        if ismasked:
            return d.mask
        else:
            return np.zeros(d.shape, dtype=bool)

    # Use bottleneck if available
    try:     # pragma: no cover
        import bottleneck as bn
        med = bn.median
    except:  # pragma: no cover
        med = np.median

    # Median
    oldsettings = np.geterr()
    np.seterr(invalid='ignore')
    if d.ndim == 1:
        dd = d.compressed()
        md = med(dd)
        # Median absolute deviation
        MAD = med(np.abs(dd-md))
        # Range around median
        thresh = MAD * (z/0.6745)
        # True where outside z-range
        res = (d < (md-thresh)) | (d > (md+thresh))
    elif d.ndim == 2:
        res = np.empty(d.shape, dtype=bool)
        for i in range(d.shape[1]):
            di = d[:, i]
            dd = di.compressed()
            md = med(dd)
            # Median absolute deviation
            MAD = med(np.abs(dd-md))
            # Range around median
            thresh = MAD * (z/0.6745)
            # True where outside z-range
            res[:, i] = (d[:, i] < (md-thresh)) | (d[:, i] > (md+thresh))
    else:
        np.seterr(**oldsettings)
        raise ValueError('datin.ndim must be <= 2')

    np.seterr(**oldsettings)
    if ismasked:
        return res
    else:
        # got masked because of NaNs
        if isinstance(res, np.ma.MaskedArray):
            return np.where(res.mask, False, res)
        else:
            return res


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # import numpy as np
    # y = np.array([-0.25,0.68,0.94,1.15,2.26,2.35,2.37,2.40,2.47,2.54,2.62,
    #                2.64,2.90,2.92,2.92,2.93,3.21,3.26,3.30,3.59,3.68,4.30,
    #                4.64,5.34,5.42,8.01],dtype=float)
    # print(mad(y))
    # #[False False False False False False False False False False False False
    # # False False False False False False False False False False False False
    # # False False]

    # print(mad(y,z=4))
    # #[False False False False False False False False False False False False
    # # False False False False False False False False False False False False
    # # False  True]

    # print(mad(y,z=3))
    # #[ True False False False False False False False False False False False
    # # False False False False False False False False False False False False
    # #  True  True]

    # print(mad(y,z=4,deriv=2))
    # #[False False False False False False False False False False False False
    # # False False False False False False False False False False False  True]

    # my = np.ma.array(y, mask=mad(y,z=4))
    # print(my)
    # #[-0.25 0.68 0.94 1.15 2.26 2.35 2.37 2.4 2.47 2.54 2.62 2.64 2.9 2.92 2.92
    # # 2.93 3.21 3.26 3.3 3.59 3.68 4.3 4.64 5.34 5.42 --]

    # yy = np.transpose(np.array([y,y]))
    # print(np.transpose(mad(yy,z=4)))
    # #[[False False False False False False False False False False False False
    # #  False False False False False False False False False False False False
    # #  False  True]
    # # [False False False False False False False False False False False False
    # #  False False False False False False False False False False False False
    # #  False  True]]

    # yyy = np.transpose(np.array([y,y,y]))
    # print(np.transpose(mad(yyy,z=3)))
    # #[[ True False False False False False False False False False False False
    # #  False False False False False False False False False False False False
    # #   True  True]
    # # [ True False False False False False False False False False False False
    # #  False False False False False False False False False False False False
    # #   True  True]
    # # [ True False False False False False False False False False False False
    # #  False False False False False False False False False False False False
    # #   True  True]]

    # my = np.ma.array(y, mask=np.zeros(y.shape))
    # my.mask[-1] = True
    # print(mad(my,z=4))
    # #[False False False False False False False False False False False False
    # # False False False False False False False False False False False False
    # # False --]

    # print(mad(my,z=3))
    # #[True False False False False False False False False False False False
    # # False False False False False False False False False False False True
    # # True --]

    # ny = y
    # ny[-1] = np.nan
    # print(mad(ny,z=4))
    # #[False False False False False False False False False False False False
    # # False False False False False False False False False False False False
    # # False False]

    # print(mad(ny,z=3))
    # #[True False False False False False False False False False False False
    # # False False False False False False False False False False False True
    # # True False]
