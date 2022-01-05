#!/usr/bin/env python
"""
Saturation vapour pressure over water and ice

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
   esat

History
    * Written Jan 2012 by Matthias Cuntz (mc (at) macu (dot) de)
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Changed handling of masked arrays, Oct 2013, Matthias Cuntz
    * Assert T>0, Apr 2014, Matthias Cuntz
    * Using numpy docstring format, May 2020, Matthias Cuntz
    * Ported to pyjams, Jan 2022, Matthias Cuntz
    * Return same type as input type, Jan 2022, Matthias Cuntz
    * Raise AssertionError rather than assuming Celcius,
      Jan 2022, Matthias Cuntz
    * Use warnings for T < 100 K, Jan 2022, Matthias Cuntz

"""
import numpy as np


__all__ = ['esat']


def esat(T, formula='GoffGratch', undef=-9999., liquid=False):
    """
    Calculates the saturation vapour pressure over water and/or ice

    For temperatures above (and equal to) 0 degree C (273.15 K),
    the vapour pressure over liquid water is calculated;
    for temperatures below 0 degree C, the vapour pressure over ice
    is calculated.

    Parameters
    ----------
    T : float or array_like
        Temperature [K]
    formula : str, optional
        Formula name to use for calculations; case-insensitive.
        Available formulations are:
        GoffGratch (default) [1]_, WMO [2]_, IAPWS [3]_, MagnusTeten [4]_,
        MartiMauersberger [5]_, Buck_original [6]_, Buck [7]_, Wexler [8]_,
        Sonntag [9]_, Bolton [10]_, Fukuta [11]_, HylandWexler [12]_,
        MurphyKoop [13]_

        Note that several formulations do not provide a vapour pressure
        formulation over ice and Marti and Mauersberger do not provide
        a formula over liquid: GoffGratch is used in theses cases.
    undef : float, optional
        Exclude `T == undef` from calculations (default: -9999.)
    liquid : bool, optional
        If True, use liquid formula for all temperatures.

    Returns
    -------
    float or array_like
        Saturation water pressure at temperature T in Pascal [Pa].

    Notes
    -----
    Taken from Holger Voemel:
    http://cires.colorado.edu/~voemel/vp.html

    References
    ----------
    .. [1] Goff Gratch formulation
       Smithsonian Meteorological Tables, 5th edition, p. 350, 1984
       Original source: Goff and Gratch (1946), p. 107

    .. [2] Intended WMO formulation, originally published by Goff (1957)
       incorrectly referenced by WMO technical regulations,
       WMO-NO 49, Vol I, General Meteorological Standards and
       Recommended Practices, App. A, 1988, Corrigendum Aug 2000

    .. [3] Wagner W. and A. Pruss (2002)
       The IAPWS formulation 1995 for the thermodynamic properties
       of ordinary water substance for general and scientific use,
       J. Phys. Chem. Ref. Data, 31(2), 387-535
       This is the 'official' formulation from the International
       Association for the Properties of Water and Steam
       The valid range of this formulation is 273.16 <= T <= 647.096 K
       and is based on the ITS90 temperature scale.

    .. [4] Murray, F. W., On the computation of saturation vapour pressure,
       J. Appl. Meteorol., 6, 203-204, 1967

    .. [5] Marti, J. and K Mauersberger, A survey and new measurements of
       ice vapour pressure at temperatures between 170 and 250 K,
       GRL 20, 363-366, 1993

    .. [6] Bucks vapour pressure formulation based on Tetens formula
       Buck, A. L., New equations for computing vapour pressure and
       enhancement factor, J. Appl. Meteorol., 20, 1527-1532, 1981

    .. [7] Bucks vapour pressure formulation based on Tetens formula
       Buck Research, Model CR-1A Hygrometer Operating Manual, Sep 2001

    .. [8] Wexler, A., Vapour pressure formulation for ice
       Journal of Research of the National Bureau of Standards-A.
       81A, 5-20, 1977

    .. [9] Sonntag, D., Advancements in the field of hygrometry,
       Meteorol. Z., N. F., 3, 51-66, 1994

    .. [10] Bolton, D., The computation of equivalent potential temperature
       Monthly Weather Report, 108, 1046-1053, 1980. equation (10)

    .. [11] Fukuta, N. and C. M. Gramada, Vapour pressure measurement of
       supercooled water, J. Atmos. Sci., 60, 1871-1875, 2003
       This paper does not give a vapour pressure formulation,
       but rather a correction over the Smithsonian Tables.
       Thus calculate the table value first, then use the correction
       to get to the measured value.
       This is done only for -39 < TC < 0.

    .. [12] Hyland, R. W. and A. Wexler, Formulations for the Thermodynamic
       Properties of the saturated Phases of H2O from 173.15K to
       473.15K, ASHRAE Trans, 89(2A), 500-519, 1983

    .. [13] Murphy and Koop, Review of the vapour pressure of ice and
       supercooled water for atmospheric applications
       Q. J. R. Meteorol. Soc (2005), 131, pp. 1539-1565

    Examples
    --------
    >>> print('{:.3f}'.format(esat(293.15)))
    2335.847
    >>> print('{:.3f}'.format(esat(253.15)))
    103.074

    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15])))
    2335.847 103.074
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],
    ...     formula='GoffGratch')))
    2335.847 103.074
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],
    ...     formula='MartiMauersberger')))
    2335.847 103.650
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],
    ...     formula='MagnusTeten')))
    2335.201 102.771
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],formula='buck')))
    2338.340 103.286
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],
    ...     formula='Buck_original')))
    2337.282 103.267
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],formula='wmo')))
    2337.080 103.153
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],formula='WEXLER')))
    2323.254 103.074
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],formula='Sonntag')))
    2339.249 103.249
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],formula='Bolton')))
    2336.947 103.074
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],formula='Fukuta')))
    2335.847 103.074
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],
    ...     formula='HylandWexler')))
    2338.804 103.260
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],formula='IAPWS')))
    2339.194 103.074
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15],
    ...     formula='MurphyKoop')))
    2339.399 103.252

    >>> print('{:.3f} {:.3f}'.format(*esat(np.array([293.15,253.15]),
    ...     liquid=True)))
    2335.847 125.292
    >>> print('{:.3f} {:.3f}'.format(*esat([293.15,253.15], formula='Fukuta',
    ...     liquid=True)))
    2335.847 125.079

    >>> out = esat(np.ma.array([253.15,-9999.], mask=[False,True]))
    >>> print('{:.3f} {:.3f}'.format(*out.filled(-9999.)))
    103.074 -9999.000

    """
    # Constants
    T0 = 273.15  # Celcius <-> Kelvin [K]
    knownforms = ['Buck', 'Buck_original', 'Bolton', 'Fukuta', 'GoffGratch',
                  'HylandWexler', 'IAPWS', 'MagnusTeten', 'MartiMauersberger',
                  'MurphyKoop', 'Sonntag', 'Vaisala', 'Wexler', 'WMO']
    lknown = [ i.lower() for i in knownforms ]

    # Check input
    # Check scalar, list or array
    # -1: scalar, 0: tuple, 1: list, 2: ndarray, 3. masked_array
    if np.iterable(T):
        if isinstance(T, list):
            islist = 1
            mT = np.array(T)
            mT = np.where(mT == undef, T0, mT)
        elif isinstance(T, np.ma.MaskedArray):
            islist = 2
            mT = np.ma.where(T == undef, T0, T)
        elif isinstance(T, np.ndarray):
            islist = 3
            # do not use masked array to avoid overflow
            mT = np.where(T == undef, T0, T)
        else:
            islist = 0
            mT = np.array(T)
            mT = np.where(mT == undef, T0, mT)
    else:
        # scalar
        islist = -1
        if T == undef:
            mT = np.array(T0)
        else:
            mT = np.array(T)
    # Check unfeasible temperatures
    assert np.ma.all(mT > 0.), (
        'Temperature below 0 K; probably given in Celsius instead of Kelvin.')
    assert np.ma.all(mT < T0 + 100.), ('Temperature above 373.15 K')
    if np.ma.any(mT < 100.):
        import warnings
        warnings.warn('Temperature < 100 K; probably given in Celsius'
                      ' instead of Kelvin.', UserWarning)
    # Check formulas
    form = formula.lower()
    if form not in lknown:
        raise ValueError('Formula not known. Known formulas are'
                         ' (default: GoffGratch):'
                         '{:s}'.format(', '.join(knownforms)))

    # Split input into masked arrays
    if liquid:
        Tlim = 1e-3
    else:
        Tlim = T0
    if mT.size > 1:
        ii = np.ma.where(mT >= Tlim)[0]
        jj = np.ma.where(mT < Tlim)[0]
        if ii.size > 0:
            T_liq  = mT[ii]
        if jj.size > 0:
            T_ice  = mT[jj]
    else:
        if mT >= Tlim:
            ii = np.array([0])
            jj = np.array([])
            T_liq = mT
        else:
            ii = np.array([])
            jj = np.array([0])
            T_ice = mT
    out = mT.copy()  # to conserve mask

    #
    # Calc
    #

    # Liquid
    if ii.size > 0:
        TC_liq = T_liq - T0
        if form == 'buck':
            esat_liq = 6.1121 * np.ma.exp(
                (18.678 - (TC_liq) / 234.5) * (TC_liq) / (257.14+TC_liq))
        elif form == 'buck_original':
            esat_liq = 6.1121 * np.ma.exp(17.502 * TC_liq / (240.97+TC_liq))
        elif form == 'bolton':
            esat_liq = 6.112 * np.ma.exp(17.67 * TC_liq / (TC_liq+243.5))
        elif form == 'fukuta':
            # steam point temperature in K
            Ts  = 373.16
            # saturation pressure at steam point temperature, normal atmosphere
            ews = 1013.246
            esat_liq = (10.**(-7.90298 * (Ts/T_liq-1.)
                              + 5.02808 * np.ma.log10(Ts/T_liq)
                              - 1.3816e-7 * (10.**(11.344*(1.-T_liq/Ts))-1.)
                              + 8.1328e-3 * (10.**(-3.49149*(Ts/T_liq-1))-1.)
                              + np.ma.log10(ews)))
            mm = (TC_liq < 0.) & (TC_liq > -39.)
            if np.ma.any(mm):
                x = TC_liq + 19.
                esat_liq = (np.where(mm,
                                     esat_liq * (0.9992
                                                 + 7.113e-4*x
                                                 - 1.847e-4*x**2
                                                 + 1.189e-5*x**3
                                                 + 1.130e-7*x**4
                                                 - 1.743e-8*x**5),
                                     esat_liq))
        elif ((form == 'goffgratch') | (form == 'martimauersberger')):
            # steam point temperature in K
            Ts  = 373.16
            # saturation pressure at steam point temperature, normal atmosphere
            ews = 1013.246
            esat_liq = (10.**(-7.90298*(Ts/T_liq-1.)
                              + 5.02808 * np.ma.log10(Ts/T_liq)
                              - 1.3816e-7 * (10.**(11.344*(1.-T_liq/Ts))-1.)
                              + 8.1328e-3 * (10.**(-3.49149*(Ts/T_liq-1.))-1.)
                              + np.ma.log10(ews)))
        elif form == 'hylandwexler':
            esat_liq = (np.ma.exp(- 0.58002206e4/T_liq
                                  + 0.13914993e1 - 0.48640239e-1*T_liq
                                  + 0.41764768e-4*T_liq**2
                                  - 0.14452093e-7*T_liq**3
                                  + 0.65459673e1 * np.ma.log(T_liq)) / 100.)
        elif form == 'iapws':
            Tc = 647.096      # K   : Temperature at the critical point
            Pc = 22.064e4     # hPa : Vapour pressure at the critical point
            nu = (1. - T_liq/Tc)
            a1 = -7.85951783
            a2 = 1.84408259
            a3 = -11.7866497
            a4 = 22.6807411
            a5 = -15.9618719
            a6 = 1.80122502
            esat_liq = Pc * np.ma.exp(Tc/T_liq
                                      * (a1*nu + a2*nu**1.5
                                         + a3*nu**3 + a4*nu**3.5
                                         + a5*nu**4 + a6*nu**7.5))
        elif form == 'magnusteten':
            esat_liq = 10.**(7.5 * (TC_liq) / (TC_liq+237.5) + 0.7858)
        elif form == 'murphykoop':
            esat_liq = (np.exp(54.842763 - 6763.22 / T_liq
                               - 4.210 * np.ma.log(T_liq)
                               + 0.000367 * T_liq
                               + np.tanh(0.0415 * (T_liq - 218.8))
                               * (53.878 - 1331.22 / T_liq - 9.44523
                                  * np.ma.log(T_liq) + 0.014025 * T_liq))
                        / 100.)
        elif form == 'sonntag':
            esat_liq = (np.ma.exp(- 6096.9385 * 1./T_liq
                                  + 16.635794
                                  - 2.711193e-2 * T_liq
                                  + 1.673952e-5 * T_liq**2
                                  + 2.433502 * np.ma.log(T_liq)))
        elif form == 'wexler':
            esat_liq = (np.ma.exp(- 2.9912729e3 * 1./T_liq**2
                                  - 6.0170128e3 * 1./T_liq
                                  + 1.887643854e1
                                  - 2.8354721e-2 * T_liq**1
                                  + 1.7838301e-5 * T_liq**2
                                  - 8.4150417e-10 * T_liq**3
                                  - 4.4412543e-13 * T_liq**4
                                  + 2.858487 * np.ma.log(T_liq)) / 100.)
        elif form == 'wmo':
            Ts   = 273.16  # steam point temperature in K
            esat_liq = (10.**(10.79574 * (1.-Ts/T_liq)
                              - 5.02800 * np.ma.log10(T_liq/Ts)
                              + 1.50475e-4 * (1.-10.**(-8.2969*(T_liq/Ts-1.)))
                              + 0.42873e-3 * (10.**(+4.76955*(1.-Ts/T_liq))-1.)
                              + 0.78614))
        else:
            # should not come here, hence no cover
            raise ValueError('Formula not known for liquid:'
                             ' {:s}'.format(formula))  # pragma: no cover
        esat_liq *= 100.  # hPa -> Pa
        if islist > -1:
            out[ii] = esat_liq
        else:
            out = esat_liq

    # Ice
    if jj.size > 0:
        TC_ice = T_ice - T0
        if form == 'buck':
            esat_ice = 6.1115 * np.exp((23.036 - TC_ice / 333.7)
                                       * TC_ice / (279.82+TC_ice))
        elif form == 'buck_original':
            esat_ice = 6.1115 * np.exp(22.452 * TC_ice / (272.55+TC_ice))
        elif ((form == 'goffgratch') | (form == 'bolton')
              | (form == 'fukuta') | (form == 'iapws') | (form == 'wexler')):
            ei0 = 6.1071  # mbar
            Ts  = 273.16  # freezing point in K
            esat_ice = np.ma.exp(np.log(10.)*(-9.09718 * (Ts/T_ice-1.)
                                              - 3.56654 * np.ma.log10(Ts/T_ice)
                                              + 0.876793 * (1.-T_ice/Ts)
                                              + np.log10(ei0)))
        elif (form == 'hylandwexler'):
            esat_ice = (np.exp(- 0.56745359E4 / T_ice
                               + 0.63925247E1
                               - 0.96778430E-2 * T_ice
                               + 0.62215701E-6 * T_ice**2
                               + 0.20747825E-8 * T_ice**3
                               - 0.94840240E-12 * T_ice**4
                               + 0.41635019E1 * np.log(T_ice)) / 100.)
        elif form == 'magnusteten':
            esat_ice = 10.**(9.5 * TC_ice/(265.5+TC_ice) + 0.7858)
        elif form == 'martimauersberger':
            esat_ice = 10.**(-2663.5/T_ice + 12.537) / 100.
        elif form == 'murphykoop':
            esat_ice = np.exp(9.550426 - 5723.265/T_ice
                              + 3.53068 * np.log(T_ice)
                              - 0.00728332 * T_ice) / 100.
        elif form == 'sonntag':
            esat_ice = (np.exp(- 6024.5282 * 1./T_ice
                               + 24.721994
                               + 1.0613868E-2 * T_ice
                               - 1.3198825E-5 * T_ice**2
                               - 0.49382577 * np.log(T_ice)))
        elif form == 'wmo':
            Ts = 273.16  # steam point temperature in K
            esat_ice = (10.**(-9.09685 * (Ts/T_ice-1.)
                              - 3.56654 * np.log10(Ts/T_ice)
                              + 0.87682 * (1.-T_ice/Ts) + 0.78614))
        else:
            # should not come here, hence no cover
            raise ValueError('Formula not known for ice:'
                             ' {:s}'.format(formula))  # pragma: no cover
        esat_ice *= 100.  # hPa -> Pa
        if islist > -1:
            out[jj] = esat_ice
        else:
            out = esat_ice

    # return same type as input type
    if islist == 0:
        mT = np.array(T)
        out = tuple(np.where(mT == undef, undef, out))
    elif islist == 1:
        mT = np.array(T)
        out = list(np.where(mT == undef, undef, out))
    elif islist == 2:
        out = np.ma.array(out, mask=((T == undef) | (T.mask)))
    elif islist == 3:
        out = np.where(T == undef, undef, out)
    else:
        if T == undef:
            out = undef

    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
