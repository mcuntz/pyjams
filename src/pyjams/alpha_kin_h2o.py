#!/usr/bin/env python
"""
Kinetic fractionation factors for molecular diffusion of water isotopologues.

This module was written by Matthias Cuntz while at Department of Computational
Hydrosystems, Helmholtz Centre for Environmental Research - UFZ, Leipzig,
Germany, and continued while at Institut National de Recherche pour
l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2014-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   alpha_kin_h2o

History
    * Written, Sep 2014, Matthias Cuntz
    * Code refactoring, Nov 2021, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz

"""
from __future__ import division, absolute_import, print_function


__all__ = ['alpha_kin_h2o']


def alpha_kin_h2o(isotope=None, eps=False, greater1=True,
                  boundary=False, cappa=False):
    """
    Kinetic fractionation factors for molecular diffusion of water
    isotopologues.

    It does not use the atmospheric convention, i.e. factor < 1, by default but
    sets factor > 1 (greater1=True).

    Parameters
    ----------
    isotope : int, optional
        Select water isotopologue: 1: HDO; 2: H218O; else: no fractionation,
        i.e. return 1 (default)
    eps : bool, optional
        Returns fractionation epsilon=alpha-1 instead of fractionation factor
        alpha if True (default: return alpha)
    greater1 : bool, optional
        alpha > 1 if True, which is not the atmospheric convention.
        alpha < 1 if False, which is the atmospheric convention.
    boundary : bool, optional
        Returns `alpha**2/3` for diffusion through boundary layer instead of
        molecular diffusion if True (default: False).
    cappa : bool, optional
        Uses factors of Cappa et al. (2003) instead of Merlivat (1978) if True
        (default: False).

    Returns
    -------
    alpha / epsilon : float or array-like
        Kinetic fractionation factor (alpha) or fractionation (epsilon)

    Notes
    -----
    Cappa, C. D., Hendricks, M. B., DePaolo, D. J., & Cohen, R. (2003)
        Isotopic fractionation of water during evaporation
        Journal of Geophysical Research, 108(D16), 4525.
        doi:10.1029/2003JD003597
    Merlivat, L. (1978)
        Molecular Diffusivities Of (H2O)-O-16 HD16O, And (H2O)-O-18 In Gases,
        The Journal of Chemical Physics, 69(6), 2864-2871.
    Merlivat, L., & Jouzel, J. (1979)
        Global climatic interpretation of the deuterium-oxygen-18 relationship
        for precipitation, Journal of Geophysical Research, 84(C8), 5029-5033.

    Examples
    --------
    Fractionation factor

    >>> import numpy as np
    >>> print(np.around(alpha_kin_h2o(isotope=0), 4))
    1.0

    Fractionations

    >>> print(np.around(alpha_kin_h2o(isotope=1, eps=True)*1000., 4))
    25.1153
    >>> print(np.around(alpha_kin_h2o(isotope=2, eps=True,
    ...                               greater1=False)*1000., 4))
    -27.3
    >>> print(np.around(alpha_kin_h2o(isotope=2, eps=True, greater1=True,
    ...                               boundary=True)*1000., 4))
    18.6244
    >>> print(np.around(alpha_kin_h2o(isotope=2, eps=True, greater1=False,
    ...                               boundary=True, cappa=True)*1000., 4))
    -20.7076

    """
    # Fractionation factors
    if (isotope == 1):  # HDO
        if cappa:
            out = 0.9839
        else:
            out = 0.9755
    elif (isotope == 2):  # H218O
        if cappa:
            out = 0.9691
        else:
            out = 0.9727
    else:
        out = 1.

    # boundary layer
    if boundary:
        out = out**(2./3.)

    # alpha+
    if greater1:
        out = 1./out

    # epsilon
    if eps:
        out -= 1.

    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
