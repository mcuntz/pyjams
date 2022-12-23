#!/usr/bin/env python
"""
Calculate daily, monthly, yearly, etc. means

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2013-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   means

History
    * Written Jul 2013 by Matthias Cuntz (mc (at) macu (dot) de)
    * Added meanday, Jul 2013, Matthias Cuntz
    * Added max and min, Apr 2014, Matthias Cuntz
    * Added onlydat and meanmonth, Jun 2015, Matthias Cuntz
    * Added seasonal, Oct 2018, Matthias Cuntz
    * Bug in minute averaging: compared minutes to hours,
      Jun 2019, Matthias Cuntz
    * Added half_hour, inspired by Robin Leucht for UFZ level1 data;
      did not take retrospective keyword but added Note for this case,
      Jun 2019, Matthias Cuntz
    * Use pyjams datetime, Jul 2022, Matthias Cuntz
    * More possible date formats, Jul 2022, Matthias Cuntz
    * Rename seasonal to seasonalday, Jul 2022, Matthias Cuntz
    * Add seasonalmonth, Jul 2022, Matthias Cuntz
    * Add seasonalmeanday, Jul 2022, Matthias Cuntz

"""
import datetime as dt
import cftime as cf
import numpy as np
from .class_datetime import datetime
from .class_datetime import date2num, num2date
from .helper import input2array, array2input
# from pyjams import datetime
# from pyjams import date2num, num2date
# from pyjams.helper import input2array, array2input


__all__ = ['means']


def _to_tuple(dt):
    """
    Turn a datetime instance into a tuple of integers. Elements go
    in the order of decreasing significance, making it easy to compare
    datetime instances. Parts of the state that don't affect ordering
    are omitted.

    """
    return (dt.year, dt.month, dt.day, dt.hour, dt.minute,
            dt.second, dt.microsecond)


def _output_date(dout, ical, date0, idatetime, idkwargs):
    """
    Conversion of output dates to input date format

    """
    aout = num2date(dout, calendar=ical)
    if idatetime:
        if isinstance(date0, dt.datetime):
            ddout = [ idatetime(*_to_tuple(aa)) for aa in aout ]
        else:
            ddout = [ idatetime(*_to_tuple(aa), calendar=date0.calendar)
                      for aa in aout ]
    elif isinstance(date0, str):
        oform = idkwargs['format']
        if not oform:
            oform = None
        ddout = [ aa.strftime(oform) for aa in aout ]
    else:
        okwargs = {'units': idkwargs['units'],
                   'calendar': idkwargs['calendar'],
                   'has_year_zero': idkwargs['has_year_zero']}
        ddout = date2num(aout, **okwargs)

    return ddout


def means(date, dat,
          year=False, month=False, day=False, hour=False, half_hour=False,
          minute=False,
          meanday=False, meanmonth=False, seasonalday=False,
          seasonalmonth=False, seasonalmeanday=False,
          sum=False, max=False, min=False,
          onlydat=False, **kwargs):
    """
    Calculate daily, monthly, yearly, etc. means of data

    dat will be averaged over columns, i.e. assuming that the first
    dimension is the time dimension.

    If no keyword argument is given, the mean will be over the whole
    first column.

    date can be either string or datetime object of Python, numpy, cftime, or
    pyjams, which will be interpreted by pyjams.date2num; or date can be a
    numeric value, which will be interpreted by pyjams.num2date; any extra
    keyword argument will be passed to the appropriate datetime routine.
    Returned dates will be in same format as incoming dates.

    Parameters
    ----------
    date : 1D array with dates
        Can either be strings or *datetime* objects of *Python*, *cftime* or
        *pyjams*, which will be interpreted by *pyjams.date2num*, or it
        can be a numeric value, which will be interpreted by *pyjams.num2date*.
        date should be centred on the input time period, i.e. half-hourly data
        should have dates at 15 min and 45 min of each hour, for example.
    dat : ND (masked-)array
    year : bool, optional
        If True, return annual means
    month : bool, optional
        If True, return monthly means
    day : bool, optional
        If True, return daily means
    hour : bool, optional
        If True, return hourly means
    half_hour : bool, optional
        If True, return half-hourly means
    minute : bool, optional
        If True, return minute means. Note that this can take very long.
    meanday : bool, optional
        If True, return one mean daily cycle
    meanmonth : bool, optional
        If True, return mean monthly cycle
    seasonalday : bool, optional
        If True, return daily means seasonal cycle
    seasonalmonth : bool, optional
        Same as meanmonth. If True, return mean monthly cycle
    seasonalmeanday : bool, optional
        If True, return one mean daily cycle per month
    sum : bool, optional
        If True, calculate sums instead of means
    max : bool, optional
        If True, calculate maxima instead of means
    min : bool, optional
        If True, calculate minima instead of means
    onlydat : bool, optional
        If True, return only meandat, else return [outdate, meandat]
    **kwargs : dict, optional
        Any other keyword argument will be passed to either *pyjams.date2num*
        or *pyjams.num2date* depending on type of *date*

    Returns
    -------
    outdate, meandat
       centred date on year, month, day, etc.; and
       averaged data in 1st dimension

    Notes
    -----
    *outdate* is same format as *date* input. Output *meandat* is scalar,
    numpy array, or masked array if needed.

    Returns centred [dates, averages]:
        * Yearly dates are centred on June 15, 12:00 h
        * Monthly dates are centred on 15th, 12:00 h
        * Daily dates are centred on 12:00 h
        * Hourly dates are centred on 30 min
        * Half hourly dates are centred on 15 and 45 min
        * Minute dates are centred on 30 sec
        * Mean daily dates are centred on 30 min of January 01 of the first
          year
        * Mean monthly (seasonal monthly) dates are centred on the 15th of
          each month at 12:00 h of the first year
        * Seasonal daily dates are centred on 12:00 h of each day of the
          first (leap) year
        * Seasonal mean daily dates are centred on 30 min of each first day of
          each month of the first year

    If meanday/seasonal/meanday/seasonalday/meanmonth/seasonalmonth==True,
    then all hours/months/days will be written;
    as a masked-array if hours/days/months are missing.

    If seasonalday==True, input data has to be spaced <= days, otherwise
    consider meanmonth/seasonalmonth.

    If input date represent the beginning/end of the time step, the user should
    add/remove half a time step before using the routine. Otherwise the routine
    would have to guess the time step, which is error prone.
    For example, remove 15 minutes by subtracting
    `datetime.timedelta(minutes=15)` from datetime, `15./(24.*60.)` from Julian
    dates, or `pyjams.date2num('2010-01-01 12:15', units, calendar) -
    pyjams.date2num('2010-01-01 12:00', units, calendar)` from any *calendar*
    and *units* understood by *pyjams.datetime* or *cftime.datetime*.

    Examples
    --------
    >>> dates = ['01.01.1990 12:00:00', '01.02.1990 12:00:00',
    ...          '01.03.1990 12:00:00', '01.01.1990 12:10:00',
    ...          '01.01.1990 13:00:00', '01.01.1990 14:00:00']
    >>> jdates = date2num(dates, calendar='decimal')
    >>> x = np.arange(len(jdates)) + 1.
    >>> odates, xout = means(jdates, x, calendar='decimal')
    >>> oodates = num2date(odates, calendar='decimal')
    >>> oodates = oodates.strftime('%Y-%m-%d %H:%M:%S')
    >>> print(oodates, xout)
    1990-01-31 00:00:00 3.5

    >>> odates, xout = means(jdates, x, year=True, calendar='decimal')
    >>> print(xout)
    [3.5]

    >>> odates, xout = means(dates, x, month=True)
    >>> print(xout)
    [4. 2. 3.]

    >>> odates, xout = means(dates, x, day=True)
    >>> print(xout)
    [4. 2. 3.]

    >>> odates, xout = means(dates, x, hour=True)
    >>> print(xout)
    [2.5 5.  6.  2.  3. ]

    >>> odates, xout = means(jdates, x, half_hour=True, calendar='decimal')
    >>> print(xout)
    [2.5 5.  6.  2.  3. ]

    >>> odates, xout = means(jdates, x, meanday=True, calendar='decimal')
    >>> print(xout[10:16])
    [-- -- 2.5 5.0 6.0 --]

    >>> odates, xout = means(jdates, x, meanmonth=True, calendar='decimal')
    >>> print(xout[0:5])
    [4.0 2.0 3.0 --  --]

    >>> odates, xout = means(jdates, x, seasonalday=True, calendar='decimal')
    >>> print(xout[0:5])
    [4.0 -- -- -- --]

    >>> odates, xout = means(jdates, x, seasonalmonth=True, calendar='decimal')
    >>> print(xout[0:5])
    [4.0 2.0 3.0 --  --]

    >>> print(means(jdates, x, month=True, onlydat=True, calendar='decimal'))
    [4. 2. 3.]

    Masked arrays

    >>> x = np.ma.array(x, mask=np.zeros(x.size, dtype=bool))
    >>> x.mask[0] = True
    >>> odates, xout = means(jdates, x, calendar='decimal')
    >>> print(np.around(odates, 1), xout)
    1990.1 4.0

    >>> odates, xout = means(dates, x, year=True)
    >>> print(xout)
    [4.0]

    >>> odates, xout = means(dates, x, month=True)
    >>> print(xout)
    [5.0 2.0 3.0]

    >>> odates, xout = means(jdates, x, day=True, calendar='decimal')
    >>> print(xout)
    [5.0 2.0 3.0]

    sum

    >>> odates, xout = means(jdates, x, sum=True, calendar='decimal')
    >>> print(np.around(odates, 1), xout)
    1990.1 20.0
    >>> odates, xout = means(jdates, x, year=True, sum=True,
    ...                      calendar='decimal')
    >>> print(xout)
    [20.0]
    >>> odates, xout = means(dates, x, month=True, sum=True)
    >>> print(xout)
    [15.0 2.0 3.0]
    >>> odates, xout = means(jdates, x, day=True, sum=True, calendar='decimal')
    >>> print(xout)
    [15.0 2.0 3.0]

    max

    >>> odates, xout = means(jdates, x, max=True, calendar='decimal')
    >>> print(np.around(odates, 1), xout)
    1990.1 6.0
    >>> odates, xout = means(dates, x, year=True, max=True)
    >>> print(xout)
    [6.0]
    >>> odates, xout = means(jdates, x, month=True, max=True,
    ...                      calendar='decimal')
    >>> print(xout)
    [6.0 2.0 3.0]
    >>> odates, xout = means(jdates, x, day=True, max=True, calendar='decimal')
    >>> print(xout)
    [6.0 2.0 3.0]

    min

    >>> odates, xout = means(jdates, x, min=True, calendar='decimal')
    >>> print(np.around(odates, 1), xout)
    1990.1 2.0
    >>> odates, xout = means(jdates, x, year=True, min=True,
    ...                      calendar='decimal')
    >>> print(xout)
    [2.0]
    >>> odates, xout = means(dates, x, month=True, min=True)
    >>> print(xout)
    [4.0 2.0 3.0]
    >>> odates, xout = means(jdates, x, day=True, min=True, calendar='decimal')
    >>> print(xout)
    [4.0 2.0 3.0]

    2D and masked arrays

    >>> x  = np.repeat(x,2).reshape((x.size,2))
    >>> odates, xout = means(jdates, x, calendar='decimal')
    >>> print(np.around(odates, 1), xout)
    1990.1 [4.0 4.0]

    >>> odates, xout = means(jdates, x, year=True, calendar='decimal')
    >>> print(xout)
    [[4.0 4.0]]

    >>> odates, xout = means(dates, x, month=True)
    >>> print(xout)
    [[5.0 5.0]
     [2.0 2.0]
     [3.0 3.0]]

    >>> odates, xout = means(jdates, x, day=True, calendar='decimal')
    >>> print(xout)
    [[5.0 5.0]
     [2.0 2.0]
     [3.0 3.0]]

    """
    # Constants
    myundef = 9e33
    ismasked = isinstance(dat, np.ma.MaskedArray)

    # Assure array
    date = np.array(date)
    if not ismasked:
        dat = np.array(dat)

    # Assure ND-array
    isone = False
    if dat.ndim == 1:
        isone = True
        dat = dat[:, np.newaxis]

    # Check options
    if seasonalmonth:
        meanmonth = True
    allopts = (day + month + year + hour + half_hour + minute + meanday +
               meanmonth + seasonalday + seasonalmeanday)
    assert allopts <= 1, (
        "only one averaging option day, month, year, etc. possible")

    # Check aggregation
    allaggs = sum + max + min
    assert allaggs <= 1, "only one aggregation option sum, min, max possible"

    # transform date
    iform = '%Y-%m-%d %H:%M:%S'
    ical = 'decimal'
    idatetime = ''
    idkwargs = {}
    date0 = date[0]
    if isinstance(date0, (dt.datetime, cf.datetime, datetime)):
        if isinstance(date0, dt.datetime):
            idatetime = dt.datetime
        elif isinstance(date0, cf.datetime):
            idatetime = cf.datetime
        elif isinstance(date0, datetime):
            idatetime = datetime
        # datetime
        adate = [ dd.strftime(iform) for dd in date ]
        idate = date2num(adate, calendar=ical)
    elif isinstance(date0, str):
        # str
        idkwargs = {'format': '', 'timesep': ' ', 'fr': False}
        for kk in kwargs:
            if kk in idkwargs:
                idkwargs.update({kk: kwargs[kk]})
        idate = date2num(date, calendar=ical, **idkwargs)
    else:
        # num - should throw an error if other
        idkwargs = {'units': '', 'calendar': 'standard',
                    'only_use_cftime_datetimes': True,
                    'only_use_python_datetimes': False,
                    'has_year_zero': None,
                    'format': '', 'return_arrays': False}
        for kk in kwargs:
            if kk in idkwargs:
                idkwargs.update({kk: kwargs[kk]})
        ddate = num2date(date, **idkwargs)
        adate = [ dd.strftime(iform) for dd in ddate ]
        idate = date2num(adate, calendar=ical)
    idate = input2array(idate, default=1.)

    # select operator
    if sum:
        meanop = np.ma.sum
    elif max:
        meanop = np.ma.amax
    elif min:
        meanop = np.ma.amin
    else:
        meanop = np.ma.mean
    if ismasked:
        ones = np.ma.ones
    else:
        ones = np.ones

    # average 1st dim
    if allopts == 0:
        dout = [0.5 * (idate.max() + idate.min())]
        ddout = _output_date(dout, ical, date0, idatetime, idkwargs)
        ddout = ddout[0]
        out = meanop(dat, 0)
        if isone:
            if onlydat:
                return out[0]
            else:
                return ddout, out[0]
        else:
            if onlydat:
                return out
            else:
                return ddout, out

    # if allopts > 0
    # yr, mo, dy, hr, mn, sc = dec2date(date)
    yr, mo, dy, hr, mn, sc, ms = num2date(
        idate, calendar='decimal', return_arrays=True)

    # year
    if year:
        yrs = np.unique(yr)
        nout = yrs.size
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in yrs:
            ii = np.where(yr == i)[0]
            if np.size(ii) > 0:
                dout[zahl] = ('{:04d}-{:02d}-{:02d}'
                              ' {:02d}:{:02d}:{:02d}'.format(
                                  i, 6, 15, 12, 0, 0))
                out[zahl, :] = meanop(dat[ii, :], 0)
                zahl += 1

    # month
    if month:
        yrs = np.unique(yr)
        mos = np.unique(mo)
        nout = yrs.size * mos.size
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in yrs:
            for j in mos:
                ii = np.where((yr == i) & (mo == j))[0]
                if np.size(ii) > 0:
                    dout[zahl] = ('{:04d}-{:02d}-{:02d}'
                                  ' {:02d}:{:02d}:{:02d}'.format(
                                      i, j, 15, 12, 0, 0))
                    out[zahl, :] = meanop(dat[ii, :], 0)
                    zahl += 1

    # day
    if day:
        yrs = np.unique(yr)
        mos = np.unique(mo)
        dys = np.unique(dy)
        nout = yrs.size * mos.size * dys.size
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in yrs:
            for j in mos:
                for k in dys:
                    ii = np.where((yr == i) & (mo == j) & (dy == k))[0]
                    if np.size(ii) > 0:
                        dout[zahl] = ('{:04d}-{:02d}-{:02d}'
                                      ' {:02d}:{:02d}:{:02d}'.format(
                                          i, j, k, 12, 0, 0))
                        out[zahl, :] = meanop(dat[ii, :], 0)
                        zahl += 1

    # hour
    if hour:
        yrs = np.unique(yr)
        mos = np.unique(mo)
        dys = np.unique(dy)
        hrs = np.unique(hr)
        nout = yrs.size * mos.size * dys.size * hrs.size
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in yrs:
            for j in mos:
                for k in dys:
                    for l in hrs:
                        ii = np.where((yr == i) & (mo == j) &
                                      (dy == k) & (hr == l))[0]
                        if np.size(ii) > 0:
                            dout[zahl] = ('{:04d}-{:02d}-{:02d}'
                                          ' {:02d}:{:02d}:{:02d}'.format(
                                              i, j, k, l, 30, 0))
                            out[zahl, :] = meanop(dat[ii, :], 0)
                            zahl += 1
    # half_hour
    if half_hour:
        yrs = np.unique(yr)
        mos = np.unique(mo)
        dys = np.unique(dy)
        hrs = np.unique(hr)
        nout = yrs.size * mos.size * dys.size * hrs.size * 2
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in yrs:
            for j in mos:
                for k in dys:
                    for l in hrs:
                        for m in range(2):
                            ii = np.where((yr == i) & (mo == j) &
                                          (dy == k) & (hr == l) &
                                          ((mn // 30) == m))[0]
                            if np.size(ii) > 0:
                                dout[zahl] = ('{:04d}-{:02d}-{:02d}'
                                              ' {:02d}:{:02d}:{:02d}'.format(
                                                  i, j, k, l, 15 + m * 30, 0))
                                out[zahl, :] = meanop(dat[ii, :], 0)
                                zahl += 1

    # minute
    if minute:
        yrs = np.unique(yr)
        mos = np.unique(mo)
        dys = np.unique(dy)
        hrs = np.unique(hr)
        mns = np.unique(mn)
        nout = yrs.size * mos.size * dys.size * hrs.size * mns.size
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in yrs:
            for j in mos:
                for k in dys:
                    for l in hrs:
                        for m in mns:
                            ii = np.where((yr == i) & (mo == j) &
                                          (dy == k) & (hr == l) &
                                          (mn == m))[0]
                            if np.size(ii) > 0:
                                dout[zahl] = ('{:04d}-{:02d}-{:02d}'
                                              ' {:02d}:{:02d}:{:02d}'.format(
                                                  i, j, k, l, m, 30))
                                out[zahl, :] = meanop(dat[ii, :], 0)
                                zahl += 1

    # Mean daily
    if meanday:
        nout = 24
        hrs = range(nout)
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in hrs:
            dout[zahl] = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
                yr[0], 1, 1, i, 30, 0)
            ii = np.where(hr == i)[0]
            if np.size(ii) > 0:
                out[zahl, :] = meanop(dat[ii, :], 0)
            zahl += 1
        if np.any(out == myundef):
            out = np.ma.array(out, mask=(out == myundef), keep_mask=True)

    # Mean monthly = seasonal monthly
    if meanmonth:  # seasonalmonth
        nout = 12
        mos = range(1, nout + 1)
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in mos:
            dout[zahl] = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
                yr[0], i, 15, 12, 0, 0)
            ii = np.where(mo == i)[0]
            if np.size(ii) > 0:
                out[zahl, :] = meanop(dat[ii, :], 0)
            zahl += 1
        if np.any(out == myundef):
            out = np.ma.array(out, mask=(out == myundef), keep_mask=True)

    # Seasonalday
    if seasonalday:
        dim = np.array([[-9, 31, 28, 31, 30, 31, 30, 31, 31,
                         30, 31, 30, 31],
                        [-9, 31, 29, 31, 30, 31, 30, 31, 31,
                         30, 31, 30, 31]])
        leaps = (((yr % 4) == 0) & ((yr % 100) != 0)) | ((yr % 400) == 0)
        leap = np.any(leaps)
        ileap = int(leap)
        if leap:
            iileap = np.argmax(leaps)
            nout = 366
        else:
            iileap = 0
            nout = 365
        dys = range(1, nout + 1)
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in range(1, 13):
            for j in range(1, dim[ileap, i]+1):
                dout[zahl] = ('{:04d}-{:02d}-{:02d}'
                              ' {:02d}:{:02d}:{:02d}'.format(
                                  yr[iileap], i, j, 12, 0, 0))
                ii = np.where((mo == i) & (dy == j))[0]
                if np.size(ii) > 0:
                    out[zahl, :] = meanop(dat[ii, :], 0)
                zahl += 1
        if np.any(out == myundef):
            out = np.ma.array(out, mask=(out == myundef), keep_mask=True)

    # seasonal mean daily
    if seasonalmeanday:
        nmonth = 12
        mos = range(1, nmonth+1)
        nhour = 24
        hrs = range(nhour)
        nout = nmonth * nhour
        dout = ['9999-01-01 00:00:00'] * nout
        out = ones([nout] + list(dat.shape[1:])) * myundef
        zahl = 0
        for i in mos:
            for j in hrs:
                dout[zahl] = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
                    yr[0], i, 1, j, 30, 0)
                ii = np.where((mo == i) & (hr == j))[0]
                if np.size(ii) > 0:
                    out[zahl, :] = meanop(dat[ii, :], 0)
                zahl += 1
        if np.any(out == myundef):
            out = np.ma.array(out, mask=(out == myundef), keep_mask=True)

    # remove mask if possible
    if np.ma.count_masked(out) == 0:
        out = np.array(out)

    # decimal date
    dout = np.array(date2num(dout, calendar=ical))

    ii = np.where(dout != 9999.)[0]
    if len(ii) > 0:
        dout = dout[ii]
        out = out[ii, :]
    else:  # pragma: no cover
        # should not end up here
        print(dout)
        raise ValueError("all date values undefined after mean.")

    # decimal date to initial date format
    ddout = _output_date(dout, ical, date0, idatetime, idkwargs)
    ddout = array2input(ddout, date)

    if isone:
        if onlydat:
            return out[:, 0]
        else:
            return ddout, out[:, 0]
    else:
        if onlydat:
            return out
        else:
            return ddout, out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # from jams.autostring import astr
    # from jams.date2dec import date2dec
    # from jams.dec2date import dec2date
    # dates = ['01.01.1990 12:00:00', '01.02.1990 12:00:00',
    #          '01.03.1990 12:00:00', '01.01.1990 12:10:00',
    #          '01.01.1990 13:00:00', '01.01.1990 14:00:00']
    # jdates = date2dec(ascii=dates)
    # x = np.arange(len(jdates)) + 1.
    # odates, xout = means(jdates, x)
    # oodates = dec2date(odates, en=True)
    # print(oodates, xout)
    # # 1990-01-31 00:00:00 3.5

    # odates, xout = means(jdates, x, year=True)
    # print(xout)
    # # [3.5]

    # odates, xout = means(jdates, x, month=True)
    # print(xout)
    # # [4. 2. 3.]

    # Odates, xout = means(jdates, x, day=True)
    # print(xout)
    # # [4. 2. 3.]

    # odates, xout = means(jdates, x, hour=True)
    # print(xout)
    # # [2.5 5.  6.  2.  3. ]

    # odates, xout = means(jdates, x, half_hour=True)
    # print(xout)
    # # ['2.500' '5.000' '6.000' '2.000' '3.000']

    # odates, xout = means(jdates, x, meanday=True)
    # print(astr(xout[10:16], 3, pp=True))
    # # ['--   ' '--   ' '2.500' '5.000' '6.000' '--   ']

    # odates, xout = means(jdates, x, meanmonth=True)
    # print(astr(xout[0:5], 3, pp=True))
    # # ['4.000' '2.000' '3.000' '--   ' '--   ']

    # odates, xout = means(jdates, x, seasonalday=True)
    # print(astr(xout[0:5], 3, pp=True))
    # # ['4.000' '--   ' '--   ' '--   ' '--   ']

    # print(astr(means(jdates, x, month=True, onlydat=True), 3, pp=True))
    # # ['4.000' '2.000' '3.000']

    # # Masked arrays
    # x = np.ma.array(x, mask=np.zeros(x.size, dtype=bool))
    # x.mask[0] = True
    # odates, xout = means(jdates, x)
    # print(astr(odates, 3, pp=True), astr(xout, 3, pp=True))
    # # 2.448e+06 4.000

    # odates, xout = means(jdates, x, year=True)
    # print(astr(xout, 3, pp=True))
    # # ['4.000']

    # odates, xout = means(jdates, x, month=True)
    # print(astr(xout, 3, pp=True))
    # # ['5.000' '2.000' '3.000']

    # odates, xout = means(jdates, x, day=True)
    # print(astr(xout, 3, pp=True))
    # # ['5.000' '2.000' '3.000']

    # # sum
    # odates, xout = means(jdates, x, sum=True)
    # print(astr(odates, 3, pp=True), astr(xout, 3, pp=True))
    # # 2.448e+06 20.000
    # odates, xout = means(jdates, x, year=True, sum=True)
    # print(astr(xout, 3, pp=True))
    # # ['20.000']
    # odates, xout = means(jdates, x, month=True, sum=True)
    # print(astr(xout, 3, pp=True))
    # # ['15.000' ' 2.000' ' 3.000']
    # odates, xout = means(jdates, x, day=True, sum=True)
    # print(astr(xout, 3, pp=True))
    # # ['15.000' ' 2.000' ' 3.000']

    # # max
    # odates, xout = means(jdates, x, max=True)
    # print(astr(odates, 3, pp=True), astr(xout, 3, pp=True))
    # # 2.448e+06 6.000
    # odates, xout = means(jdates, x, year=True, max=True)
    # print(astr(xout, 3, pp=True))
    # # ['6.000']
    # odates, xout = means(jdates, x, month=True, max=True)
    # print(astr(xout, 3, pp=True))
    # # ['6.000' '2.000' '3.000']
    # odates, xout = means(jdates, x, day=True, max=True)
    # print(astr(xout, 3, pp=True))
    # # ['6.000' '2.000' '3.000']

    # # min
    # odates, xout = means(jdates, x, min=True)
    # print(astr(odates, 3, pp=True), astr(xout, 3, pp=True))
    # # 2.448e+06 2.000
    # odates, xout = means(jdates, x, year=True, min=True)
    # print(astr(xout, 3, pp=True))
    # # ['2.000']
    # odates, xout = means(jdates, x, month=True, min=True)
    # print(astr(xout, 3, pp=True))
    # # ['4.000' '2.000' '3.000']
    # odates, xout = means(jdates, x, day=True, min=True)
    # print(astr(xout, 3, pp=True))
    # # ['4.000' '2.000' '3.000']

    # # 2D and masked arrays
    # x  = np.repeat(x,2).reshape((x.size,2))
    # odates, xout = means(jdates, x)
    # print(astr(odates, 3, pp=True), astr(xout, 3, pp=True))
    # # 2.448e+06 ['4.000' '4.000']

    # odates, xout = means(jdates, x, year=True)
    # print(astr(xout, 3, pp=True))
    # # [['4.000' '4.000']]

    # odates, xout = means(jdates, x, month=True)
    # print(astr(xout, 3, pp=True))
    # # [['5.000' '5.000']
    # #  ['2.000' '2.000']
    # #  ['3.000' '3.000']]

    # odates, xout = means(jdates, x, day=True)
    # print(astr(xout, 3, pp=True))
    # # [['5.000' '5.000']
    # #  ['2.000' '2.000']
    # #  ['3.000' '3.000']]
