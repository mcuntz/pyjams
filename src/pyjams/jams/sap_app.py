#!/usr/bin/env python
import numpy as np
from pyjams.jams.date2dec import date2dec


__all__ = ['t2sap']


def t2sap(date, data, swd=None, undef=-9999.):
    """
    Conversion of temperature difference measured with sap flow sensors
    (Granier type) in (mV) to sap flux density (cm^3 cm^-2 h^-1) (Granier,
    1987).

    In addition, the correction according to Clearwater (1999) is possible.


    Definition
    ----------
    def t2sap(date, data, swd=None, undef=-9999.):


    Input
    -----
    date    1D array (n,) of ascii times in format DD.MM.YYYY hh:mm:ss
    data    ND array (n,...) of the raw data in mV. First dimension is time


    Optional Input
    --------------
    undef   values are excluded from calculations (default: -9999)
    swd     if None:     sapflux calculation according to original Granier
                         calibration function.
            if not None: sapwood depth in cm for Clearwater correction
                         T = (T - b*Tmax)/a
                         with a = active sapwood   = swd/2
                              b = inactive sapwood = 1-a


    Output
    ------
    SFD     2D array (n,m) with sap flux density in [cm^3 cm^-2 h^-1] according
            to the original Granier calibration function:
            SFD = 0.0119*K**1.231*3600 [Granier, 1985]


    References
    ----------
    Granier, A.
        Evaluation of transpiration in a Douglas-fir stand by means of
        sap flow measurements, Tree Physiology 3, 309-320, 1987
    Clearwater, M. J., Meinzer, F. C., Andrade, J. L., Goldstein, G.,
        Holbrook, N. M., Potential errors in measurement of nonuniform
        sap flow using heat dissipation probes, Tree Physiology 19, 681-687,
        1999


    Examples
    --------
    # normal sapflux conversion
    >>> data = np.array([0.434, 0.433, 0.432, 0.431, 0.431, 0.432])
    >>> date = ['18.05.2013 08:00', '18.05.2013 08:10', '18.05.2013 08:20',
    ...         '18.05.2013 08:30', '18.05.2013 08:40', '18.05.2013 08:50']
    >>> SFD = t2sap(date, data)
    >>> print(np.round(SFD,3))
    [0.    0.024 0.057 0.095 0.095 0.057]


    >>> # sapflux conversion including clearwater correction
    >>> data = np.array([0.434, 0.433, 0.432, 0.431, 0.431, 0.432])
    >>> date = ['18.05.2013 08:00', '18.05.2013 08:10', '18.05.2013 08:20',
    ...         '18.05.2013 08:30', '18.05.2013 08:40', '18.05.2013 08:50']
    >>> SFD  = t2sap(date, data, swd=1.5)
    >>> print(np.round(SFD,3))
    [0.    0.035 0.082 0.135 0.135 0.082]


    License
    -------
    This file is part of the JAMS Python package, distributed under the MIT
    License. The JAMS Python package originates from the former UFZ Python
    library, Department of Computational Hydrosystems, Helmholtz Centre for
    Environmental Research - UFZ, Leipzig, Germany.

    Copyright (c) 2014-2021 Andreas Wiedemann, Matthias Cuntz - mc (at) macu
    (dot) de

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
    Written,  Andreas Wiedemann, Jun 2014
    Modified, Matthias Cuntz, Jun 2014
                  - sap_app -> t2sap, incl. undef, first date then data
                  - squeeze 1D array, fill undef if not masked
              Matthias Cuntz, Nov 2016 - ported to Python 3
              Matthias Cuntz, Sep 2021 - code refactoring
    """
    isvec = False
    if data.ndim == 1:
        isvec = True
        data = data.reshape((-1, 1))
    # mask data
    isnotmask = True
    if type(data) == np.ma.core.MaskedArray:
        isnotmask = False
    data_masked = np.ma.array(data, mask=(data == undef))

    # julian day
    jd        = np.array(date2dec(ascii=date))
    # integer julian day
    jd_int    = jd.astype(int)
    # unique days
    jd_uni    = np.unique(jd_int)
    # Tmax per day
    tmax_day  = np.ma.ones((jd_uni.size, data.shape[1]))*undef
    # Time of Tmax per day
    jdmax_day = np.ma.zeros((jd_uni.size, data.shape[1]), dtype=int)

    # Determine Tmax per day
    for count, i in enumerate(jd_uni):
        # where is given day
        ii = np.where(jd_int == i)[0]
        # index of Tmax of day
        jj = np.ma.argmax(data_masked[ii, :], axis=0)
        # time at Tmax of day
        jdmax_day[count, :] = jd[ii[jj]]
        # Tmax per day
        tmax_day[count, :] = data_masked[ii[jj], :]

    # Tmax for every record
    tmax = np.empty(data.shape)
    for i in range(data.shape[1]):
        # time points at Tmax per day
        xx = jdmax_day[:, i]
        # Tmax per day
        yy = tmax_day[:, i]
        ii = ~yy.mask
        # Tmax per time point
        tmax[:, i] = np.interp(jd, xx[ii], yy[ii])

    if swd is None:
        Tsw = data_masked
    else:
        # sapwood depth in cm / 2cm for needle lenght =
        # portion of sensor in sapwood
        a = 0.5*swd
        # portion of sensor in inactive xylem
        b = 1.0-a
        # define weighted mean of T in the sapwood (a)
        # and T in the inactive xylem (b)
        Tsw  = (data_masked - (b*tmax)) / a

    # converts raw data [mV] into Sap Flux density [cm3*cm-2*h-1]
    SFD  = (0.0119 * ((tmax - Tsw)/Tsw)**1.231) * 3600.

    # if it was not masked then the original undef will be undef
    if isnotmask:
        SFD  = SFD.filled(undef)

    # 1D in = 1D out
    if isvec:
        SFD = np.squeeze(SFD)

    return SFD


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
