#!/usr/bin/env python
"""
Isotopic fractionation factors during liquid-water vapour equilibration.

This module was written by Matthias Cuntz while at Department of Computational
Hydrosystems, Helmholtz Centre for Environmental Research - UFZ, Leipzig,
Germany, and continued while at Institut National de Recherche pour
l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2014-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   alpha_equ_h2o

History
    * Written, Sep 2014, Matthias Cuntz
    * Code refactoring, Sep 2021, Matthias Cuntz
    * Tuple in/out, Oct 2021, Matthias Cuntz
    * Do not use masked arrays for undef to avoid overflow warning,
      Oct 2021, Matthias Cuntz
    * Bug masked array, need to check masked array before ndarray because the
      former is also the latter, Nov 2021, Matthias Cuntz
    * Bug if scalar, was still masked array, Jan 2022, Matthias Cuntz
    * Do not use astr in docstring examples, Jan 2022, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz
    * Bug in return type if list or tuple and undef,
      Jan 2022, Matthias Cuntz
    * Change handling of return type to allow more (unspecific) iterable types
      such as pandas time series, Jan 2022, Matthias Cuntz
    * Return numpy array if type(input)(output) fails for unknown iterable
      types, Jan 2022, Matthias Cuntz
    * Use helper functions input2array and array2input,
      Jan 2022, Matthias Cuntz

"""
import numpy as np
from .helper import input2array, array2input


__all__ = ['alpha_equ_h2o']


def alpha_equ_h2o(temp, isotope=None, undef=-9999., eps=False, greater1=True):
    """
    Isotopic fractionation factors during liquid-water vapour equilibration.

    Calculates isotopic fractionation factors during liquid-water vapour
    equilibration at temperature temp [K].
    It does not use the atmospheric convention, i.e. factor < 1, by default
    but sets factor > 1 (greater1=True).

    Parameters
    ----------
    temp : float or array-like
        Temperature [K]
    isotope : int, optional
        Select water isotopologue: 1: HDO; 2: H218O; else: no fractionation,
        i.e. return 1 (default)
    undef : float, optional
        Exclude `temp == undef` from calculations (default: -9999.)
    eps : bool, optional
        Reports fractionation epsilon=alpha-1 instead of fractionation
        factor alpha if True (default: return alpha)
    greater1 : bool, optional
        alpha > 1 if True (default), which is not the atmospheric convention.
        alpha < 1 if False, which is the atmospheric convention.

    Returns
    -------
    alpha / epsilon : float or array-like
        Equilibrium fractionation factor (alpha) or fractionation (epsilon)

    Notes
    -----
    Majoube, M. (1971) Fractionnement en oxygene-18 entre la glace et la vapeur
        d'eau Journal De Chimie Physique Et De Physico-Chimie Biologique,
        68(4), 625-636.

    Examples
    --------
    Fractionation factors

    >>> T0 = 273.15
    >>> T  = np.array([0, 10., 15., 25.])
    >>> print(np.around(alpha_equ_h2o(T+T0, isotope=0), 4))
    [1. 1. 1. 1.]
    >>> print(np.around(alpha_equ_h2o(T+T0, isotope=2), 4))
    [1.0117 1.0107 1.0102 1.0094]
    >>> print(np.around(alpha_equ_h2o(np.ma.array(T+T0, mask=(T==0.)),
    ...                               isotope=2, greater1=False), 4))
    [-- 0.9894 0.9899 0.9907]

    Fractionations

    >>> print(np.around(alpha_equ_h2o(T+T0, isotope=1, eps=True)*1000., 4))
    [112.3194 97.6829 91.1296 79.3443]
    >>> print(np.around(alpha_equ_h2o(0.+T0, isotope=2, eps=True)*1000., 4))
    11.7187

    """
    # Constants
    T0 = 273.15  # Celcius <-> Kelvin [K]
    # Check input type
    mtemp = input2array(temp, undef=undef, default=T0)

    # Coefficients of exponential function
    if (isotope == 1):    # HDO
        a = +2.4844e+4
        b = -7.6248e+1
        c = +5.261e-2
    elif (isotope == 2):  # H218O
        a = +1.137e+3
        b = -4.156e-1
        c = -2.067e-3
    else:
        a = 0.
        b = 0.
        c = 0.

    # alpha+
    out = np.exp( (a / mtemp + b) / mtemp + c)

    # alpha-
    if not greater1:
        out = 1. / out

    # epsilon
    if eps:
        out -= 1.

    # return same type as input type
    out = array2input(out, temp, undef=undef)

    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
