#!/usr/bin/env python
"""
Convert date representations between different regional variants.

Converts between date formats called English *YYYY-MM-DD hh:mm:ss*, US-English
*MM/DD/YYYY hh:mm:ss*, French *DD/MM/YYYY hh:mm:ss*, and standard *DD.MM.YYYY
hh:mm:ss*. The routines take list of dates of different formats and return date
strings in one of the four formats.

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2015-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   date2date
   date2en
   date2fr
   date2us
   en2date
   en2fr
   en2us
   fr2date
   fr2en
   fr2us
   us2date
   us2en
   us2fr

History
    * Written Feb 2015 by Matthias Cuntz (mc (at) macu (dot) de)
    * Removed usage of date2dec and dec2date, Nov 2016, Matthias Cuntz
    * Adapted docstrings to Python 2 and 3, Nov 2016, Matthias Cuntz
    * Written fr2ascii, Mar 2018, Matthias Cuntz
    * Added us and fr keywords, renamed eng to en, Mar 2018, Matthias Cuntz
    * Added two-digit year YY, Nov 2018, Matthias Cuntz
    * Removed bug from usage of en and old name eng, Jun 2019, Matthias Cuntz
    * Using numpy docstring format, May 2020, Matthias Cuntz
    * flake8, Dec 2021, Matthias Cuntz
    * Remove eng, Dec 2021, Matthias Cuntz
    * Renamed 'ascii' in function names to 'date', and to 'standard' in
      docstrings and comments, Dec 2021, Matthias Cuntz
    * New more versatile date2date function replacing ascii2ascii,
      Dec 2021, Matthias Cuntz
    * Wrapper functions between all standard formats, Dec 2021, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz

"""
import time as ptime
import datetime as dt
import numpy as np


__all__ = ['date2date',
           'date2en', 'date2fr', 'date2us',
           'en2date', 'en2fr', 'en2us',
           'fr2date', 'fr2en', 'fr2us',
           'us2date', 'us2en', 'us2fr',
           ]


def _leading_zero(l1):
    """
    Add leading 0 if necessary

    """
    return l1 if len(l1) == 2 else '0' + l1


def _ensure_year(yr, isyr2):
    """
    Ensure 4-digit year

    Years are supposed to be 4-digit years. If they have only 1 or 2 digits,
    then every year that is above the current year of the century will be taken
    as being in 1900, i.e. 90 will be taken as 1990, while all other years are
    taken in the 21st century, i.e. 20 will be 2020. 3-digit years will throw
    an ValueError.

    """
    lyr = len(yr)
    if lyr == 4:
        return yr
    else:
        iyr = int(yr)
        if iyr < 100:
            if iyr > isyr2:
                return '19' + _leading_zero(yr)
            else:
                return '20' + _leading_zero(yr)
        else:
            raise ValueError(f'3-digit years not supported: {yr}')


def date2date(edate, fr=False, format='', timesep=' ', full=False):
    """Convert date representations between different regional variants.

    Convert date notations between standard *DD.MM.YYYY hh:mm:ss*, English
    *YYYY-MM-DD hh:mm:ss*, American *MM/DD/YYYY hh:mm:ss*, and French
    *DD/MM/YYYY hh:mm:ss* format. The routine determines the input date format
    by the date separator '.', '-', or '/'. If the latter is detected, the
    American format is assumed. One can set *fr=True* so that '/' detects the
    French date format instead. The separator between date and time can be
    space ' ' or 'T', such as *YYYY-MM-DDThh:mm:ss*.

    Output format is given either by the calling name of the function (e.g.
    :func:`date2en`) or by the *format* keyword. It allows '', 'en', 'us', and
    'fr' for standard, English, American, and French date format, respectively.
    One can also give any format string understood by
    :func:`datetime.strftime`.

    Parameters
    ----------
    edate : array_like
        Date strings in any of three formats standard, English, or
        American/French.
    fr : bool, optional
        Input dates with '/' separators are interpreted as American format
        *MM/DD/YYYY hh:mm:ss* if False (default). Input dates with '/'
        separators are interpreted as French format *DD/MM/YYYY hh:mm:ss* if
        True.
    format : str, optional
        Output format. Can be any of '' (default), 'en', 'us', and 'fr' for
        standard *DD.MM.YYYY hh:mm:ss*, English *YYYY-MM-DD hh:mm:ss*, American
        *MM/DD/YYYY hh:mm:ss*, and French *DD/MM/YYYY hh:mm:ss* format.
        *format* can also be any format string understood by
        :func:`datetime.strftime`.
    timesep : str, optional
        Separator string between date and time if *format* is '', 'en', 'us',
        or 'fr'. Default is space ' ', but ISO 8601 uses 'T', for example.
    full : bool, optional
        Output dates are as long as input dates if False (default), e.g.
        *[YYYY-MM-DD, YYYY-MM-DD hh:mm]*. Output dates are all in full format
        *DD.MM.YYYY hh:mm:ss* if True; missing time info on input is 00 on
        output.

    Returns
    -------
    array_like
        Date representations in chosen format. Output type will be the same as
        the input type.

    Notes
    -----
    Year, month and day must be given while second, minute and hour can be
    missing (assumed zero).

    Years are supposed to be 4-digit years. If they have only 1 or 2 digits,
    then every year that is above the current year of the century will be taken
    as being in 1900, i.e. 90 will be taken as 1990, while all other years are
    taken in the 21st century, i.e. 20 will be 2020. 3-digit years will throw
    a ValueError.

    Negative years are not supported. The function uses :mod:`datetime` if a
    format string for :func:`datetime.strftime` is given. This limits the
    minimum year to the limit of :mod:`datetime` in this case, which is year
    '0001'.

    Examples
    --------
    >>> edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
    ...          '1990-12-01', '04.05.1786']
    >>> print(", ".join(date2date(edate)))
    12.11.2014 12:00, 01.03.2015 17:56:00, 01.12.1990, 04.05.1786
    >>> print(", ".join(date2date(edate, full=True)))
    12.11.2014 12:00:00, 01.03.2015 17:56:00, 01.12.1990 00:00:00, 04.05.1786 00:00:00
    >>> print(", ".join(date2date(edate, format='en')))
    2014-11-12 12:00, 2015-03-01 17:56:00, 1990-12-01, 1786-05-04
    >>> print(", ".join(date2date(edate, format='en', full=True)))
    2014-11-12 12:00:00, 2015-03-01 17:56:00, 1990-12-01 00:00:00, 1786-05-04 00:00:00
    >>> print(", ".join(date2date(edate, format='en', full=True, timesep='T')))
    2014-11-12T12:00:00, 2015-03-01T17:56:00, 1990-12-01T00:00:00, 1786-05-04T00:00:00
    >>> print(list(date2date(edate, format='%Y%m%d%H%M%S')))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']
    >>> print(date2date(tuple(edate)))
    ('12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990', '04.05.1786')
    >>> print(date2date(np.array(edate)))
    ['12.11.2014 12:00' '01.03.2015 17:56:00' '01.12.1990' '04.05.1786']
    >>> print(date2date(edate[0]))
    12.11.2014 12:00
    >>> print(", ".join(date2date(edate, format='us')))
    11/12/2014 12:00, 03/01/2015 17:56:00, 12/01/1990, 05/04/1786
    >>> print(", ".join(date2date(date2date(edate, format='en'),
    ...                           format='us', full=True)))
    11/12/2014 12:00:00, 03/01/2015 17:56:00, 12/01/1990 00:00:00, 05/04/1786 00:00:00
    >>> print(", ".join(date2date(edate, format='fr')))
    12/11/2014 12:00, 01/03/2015 17:56:00, 01/12/1990, 04/05/1786
    >>> print(", ".join(date2date(edate, format='fr', full=True)))
    12/11/2014 12:00:00, 01/03/2015 17:56:00, 01/12/1990 00:00:00, 04/05/1786 00:00:00

    2-digit year

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> print(", ".join(date2date(edate)))
    12.11.2014 12:00, 01.03.2015 17:56:00, 01.12.1990
    >>> print(", ".join(date2date(edate, format='en')))
    2014-11-12 12:00, 2015-03-01 17:56:00, 1990-12-01
    >>> print(", ".join(date2date(edate, format='us')))
    11/12/2014 12:00, 03/01/2015 17:56:00, 12/01/1990
    >>> print(", ".join(date2date(edate, format='us', full=True)))
    11/12/2014 12:00:00, 03/01/2015 17:56:00, 12/01/1990 00:00:00
    >>> print(", ".join(date2date(edate, format='fr', full=True)))
    12/11/2014 12:00:00, 01/03/2015 17:56:00, 01/12/1990 00:00:00

    """
    # Input type and shape
    if isinstance(edate, list):
        idate = edate
    elif isinstance(edate, tuple):
        idate = list(edate)
    elif isinstance(edate, np.ndarray):
        idate = list(edate.flatten())
    else:
        idate = [edate]
    ndate = len(idate)

    # Convert to given output type
    isyr2 = int(ptime.asctime()[-2:])
    odate = list()
    for i, d in enumerate(idate):
        dd = d.strip()
        # analyse date
        if '-' in dd:
            datesep = '-'
        elif '/' in dd:
            datesep = '/'
        elif '.' in dd:
            datesep = '.'
        else:
            raise ValueError(f'No date separator could be determined: {d}')
        # analyse date time separation if time present
        if ' ' in dd:
            datetimesep = ' '
        elif 'T' in dd:
            datetimesep = 'T'
        else:
            datetimesep = ''
        # split date and time
        if datetimesep:
            ddate, dtime = dd.split(datetimesep)
        else:
            ddate = dd
            dtime = ''
        # split date
        d0, d1, d2 = ddate.split(datesep)
        if datesep == '-':
            dyear  = _ensure_year(d0, isyr2)
            dmonth = _leading_zero(d1)
            dday   = _leading_zero(d2)
        elif datesep == '/':
            if fr:
                dyear  = _ensure_year(d2, isyr2)
                dmonth = _leading_zero(d1)
                dday   = _leading_zero(d0)
            else:
                dyear  = _ensure_year(d2, isyr2)
                dmonth = _leading_zero(d0)
                dday   = _leading_zero(d1)
        elif datesep == '.':
            dyear  = _ensure_year(d2, isyr2)
            dmonth = _leading_zero(d1)
            dday   = _leading_zero(d0)
        # split time
        if dtime:
            tt = dtime.split(':')
            if len(tt) == 1:
                dhour   = _leading_zero(tt[0])
                dminute = ''
                dsecond = ''
            elif len(tt) == 2:
                dhour   = _leading_zero(tt[0])
                dminute = _leading_zero(tt[1])
                dsecond = ''
            elif len(tt) == 3:
                dhour   = _leading_zero(tt[0])
                dminute = _leading_zero(tt[1])
                dsecond = _leading_zero(tt[2])
            else:
                raise ValueError(f'Only hour, minute, second supported'
                                 f' in time: {dtime}')
        else:
            # set for case that strftime is given
            dhour   = ''
            dminute = ''
            dsecond = ''
        # make output
        if format.lower() in ['', 'en', 'us', 'fr']:
            if format.lower() == 'en':
                out = dyear + '-' + dmonth + '-' + dday
            elif format.lower() == 'us':
                out = dmonth + '/' + dday + '/' + dyear
            elif format.lower() == 'fr':
                out = dday + '/' + dmonth + '/' + dyear
            else:
                out = dday + '.' + dmonth + '.' + dyear
            if dtime:
                out += timesep + dhour
                if dminute:
                    out += ':' + dminute
                else:
                    if full:
                        out += ':00'
                if dsecond:
                    out += ':' + dsecond
                else:
                    if full:
                        out += ':00'
            else:
                if full:
                    out += timesep + '00:00:00'
        else:
            dattim = dt.datetime(int(dyear), int(dmonth), int(dday),
                                 int(_leading_zero(dhour)),
                                 int(_leading_zero(dminute)),
                                 int(_leading_zero(dsecond)))
            out = dattim.strftime(format)
        odate.append(out)

    # Return right type
    if isinstance(edate, list):
        return odate
    elif isinstance(edate, tuple):
        return tuple(odate)
    elif isinstance(edate, np.ndarray):
        return np.array(odate).reshape(edate.shape)
    else:
        return odate[0]


def date2en(edate, **kwargs):
    """
    Wrapper function for :func:`date2date` with English date format output

    That means `date2date(edate, format='en', **kwargs)`;
    but *format* given in call will overwrite *format='en'*.

    Examples
    --------
    >>> edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
    ...          '1990-12-01', '04.05.1786']
    >>> print(", ".join(date2en(edate)))
    2014-11-12 12:00, 2015-03-01 17:56:00, 1990-12-01, 1786-05-04
    >>> print(", ".join(date2en(edate, full=True)))
    2014-11-12 12:00:00, 2015-03-01 17:56:00, 1990-12-01 00:00:00, 1786-05-04 00:00:00
    >>> print(date2en(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> print(", ".join(date2en(edate, full=True)))
    2014-11-12 12:00:00, 2015-03-01 17:56:00, 1990-12-01 00:00:00

    """
    if 'format' not in kwargs:
        kwargs.update({'format': 'en'})
    return date2date(edate, **kwargs)


def date2fr(edate, **kwargs):
    """
    Wrapper function for :func:`date2date` with French date format output

    That means `date2date(edate, format='fr', **kwargs)`;
    but *format* given in call will overwrite *format='fr'*.

    Examples
    --------
    >>> edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
    ...          '1990-12-01', '04.05.1786']
    >>> print(", ".join(date2fr(edate)))
    12/11/2014 12:00, 01/03/2015 17:56:00, 01/12/1990, 04/05/1786
    >>> print(", ".join(date2fr(edate, full=True)))
    12/11/2014 12:00:00, 01/03/2015 17:56:00, 01/12/1990 00:00:00, 04/05/1786 00:00:00
    >>> print(date2fr(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> print(", ".join(date2fr(edate, full=True)))
    12/11/2014 12:00:00, 01/03/2015 17:56:00, 01/12/1990 00:00:00

    """
    if 'format' not in kwargs:
        kwargs.update({'format': 'fr'})
    return date2date(edate, **kwargs)


def date2us(edate, **kwargs):
    """
    Wrapper function for :func:`date2date` with US-English date format output

    That means `date2date(edate, format='us', **kwargs)`;
    but *format* given in call will overwrite *format='us'*.

    Examples
    --------
    >>> edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
    ...          '1990-12-01', '04.05.1786']
    >>> print(", ".join(date2us(edate)))
    11/12/2014 12:00, 03/01/2015 17:56:00, 12/01/1990, 05/04/1786
    >>> print(", ".join(date2us(edate, full=True)))
    11/12/2014 12:00:00, 03/01/2015 17:56:00, 12/01/1990 00:00:00, 05/04/1786 00:00:00
    >>> print(date2us(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> print(", ".join(date2us(edate, full=True)))
    11/12/2014 12:00:00, 03/01/2015 17:56:00, 12/01/1990 00:00:00

    """
    if 'format' not in kwargs:
        kwargs.update({'format': 'us'})
    return date2date(edate, **kwargs)


def en2date(edate, **kwargs):
    """
    Wrapper function for date2date with standard date format output (default)

    That means `date2date(edate, **kwargs)`.

    Examples
    --------
    >>> edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
    ...          '1990-12-01', '04.05.1786']
    >>> edate = date2date(edate, format='en')
    >>> print(", ".join(en2date(edate)))
    12.11.2014 12:00, 01.03.2015 17:56:00, 01.12.1990, 04.05.1786
    >>> print(", ".join(en2date(edate, full=True)))
    12.11.2014 12:00:00, 01.03.2015 17:56:00, 01.12.1990 00:00:00, 04.05.1786 00:00:00
    >>> print(en2date(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> edate = date2en(edate)
    >>> print(", ".join(en2date(edate, full=True)))
    12.11.2014 12:00:00, 01.03.2015 17:56:00, 01.12.1990 00:00:00

    """
    return date2date(edate, **kwargs)


def en2fr(edate, **kwargs):
    """
    Wrapper function for date2date with French date format output

    That means `date2date(edate, format='fr', **kwargs)`;
    but *format* given in call will overwrite *format='fr'*.

    Examples
    --------
    >>> edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
    ...          '1990-12-01', '04.05.1786']
    >>> print(", ".join(en2fr(edate)))
    12/11/2014 12:00, 01/03/2015 17:56:00, 01/12/1990, 04/05/1786
    >>> print(", ".join(en2fr(edate, full=True)))
    12/11/2014 12:00:00, 01/03/2015 17:56:00, 01/12/1990 00:00:00, 04/05/1786 00:00:00
    >>> print(en2fr(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> print(", ".join(en2fr(edate, full=True)))
    12/11/2014 12:00:00, 01/03/2015 17:56:00, 01/12/1990 00:00:00

    """
    if 'format' not in kwargs:
        kwargs.update({'format': 'fr'})
    return date2date(edate, **kwargs)


def en2us(edate, **kwargs):
    """
    Wrapper function for :func:`date2date` with US-English date format output

    That means `date2date(edate, format='us', **kwargs)`;
    but *format* given in call will overwrite *format='us'*.

    Examples
    --------
    >>> edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
    ...          '1990-12-01', '04.05.1786']
    >>> print(", ".join(en2us(edate)))
    11/12/2014 12:00, 03/01/2015 17:56:00, 12/01/1990, 05/04/1786
    >>> print(", ".join(en2us(edate, full=True)))
    11/12/2014 12:00:00, 03/01/2015 17:56:00, 12/01/1990 00:00:00, 05/04/1786 00:00:00
    >>> print(en2us(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> print(", ".join(en2us(edate, full=True)))
    11/12/2014 12:00:00, 03/01/2015 17:56:00, 12/01/1990 00:00:00

    """
    if 'format' not in kwargs:
        kwargs.update({'format': 'us'})
    return date2date(edate, **kwargs)


def fr2date(edate, **kwargs):
    """
    Wrapper function for :func:`date2date` with French input and
    standard output date formats

    That means `date2date(edate, fr=True, **kwargs)`;
    but *fr* given in call will overwrite *fr=True*.

    Examples
    --------
    >>> edate = ['12/11/2014 12:00', '01/03/2015 17:56:00',
    ...          '01/12/1990', '04/05/1786']
    >>> print(", ".join(fr2date(edate)))
    12.11.2014 12:00, 01.03.2015 17:56:00, 01.12.1990, 04.05.1786
    >>> print(", ".join(fr2date(edate, full=True)))
    12.11.2014 12:00:00, 01.03.2015 17:56:00, 01.12.1990 00:00:00, 04.05.1786 00:00:00
    >>> print(fr2date(list(edate), format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']
    >>> print(fr2date(tuple(edate)))
    ('12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990', '04.05.1786')
    >>> print(fr2date(np.array(edate)))
    ['12.11.2014 12:00' '01.03.2015 17:56:00' '01.12.1990' '04.05.1786']
    >>> print(fr2date(edate[0]))
    12.11.2014 12:00

    2-digit year

    >>> edate = ['12/11/14 12:00', '01/03/15 17:56:00', '01/12/90']
    >>> print(", ".join(fr2date(edate)))
    12.11.2014 12:00, 01.03.2015 17:56:00, 01.12.1990
    >>> print(", ".join(fr2date(edate, full=True)))
    12.11.2014 12:00:00, 01.03.2015 17:56:00, 01.12.1990 00:00:00

    """
    if 'fr' not in kwargs:
        kwargs.update({'fr': True})
    return date2date(edate, **kwargs)


def fr2en(edate, **kwargs):
    """
    Wrapper function for :func:`date2date` with French input and
    English output date formats

    That means `date2date(edate, fr=True, format='en', **kwargs)`;
    but *format* and *fr* given in call will overwrite *fr=True* and
    *format='en'*.

    Examples
    --------
    >>> edate = ['12/11/2014 12:00', '01/03/2015 17:56:00',
    ...          '01/12/1990', '04/05/1786']
    >>> print(", ".join(fr2en(edate)))
    2014-11-12 12:00, 2015-03-01 17:56:00, 1990-12-01, 1786-05-04
    >>> print(", ".join(fr2en(edate, full=True)))
    2014-11-12 12:00:00, 2015-03-01 17:56:00, 1990-12-01 00:00:00, 1786-05-04 00:00:00
    >>> print(fr2en(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['12/11/14 12:00', '01/03/15 17:56:00', '01/12/90']
    >>> print(", ".join(fr2en(edate, full=True)))
    2014-11-12 12:00:00, 2015-03-01 17:56:00, 1990-12-01 00:00:00

    """
    if 'fr' not in kwargs:
        kwargs.update({'fr': True})
    if 'format' not in kwargs:
        kwargs.update({'format': 'en'})
    return date2date(edate, **kwargs)


def fr2us(edate, **kwargs):
    """
    Wrapper function for :func:`date2date` with French input and
    US-English output date formats

    That means `date2date(edate, fr=True, format='us', **kwargs)`;
    but *format* and *fr* given in call will overwrite *fr=True* and
    *format='us'*.

    Examples
    --------
    >>> edate = ['12/11/2014 12:00', '01/03/2015 17:56:00',
    ...          '01/12/1990', '04/05/1786']
    >>> print(", ".join(fr2us(edate)))
    11/12/2014 12:00, 03/01/2015 17:56:00, 12/01/1990, 05/04/1786
    >>> print(", ".join(fr2us(edate, full=True)))
    11/12/2014 12:00:00, 03/01/2015 17:56:00, 12/01/1990 00:00:00, 05/04/1786 00:00:00
    >>> print(fr2us(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['12/11/14 12:00', '01/03/15 17:56:00', '01/12/90']
    >>> print(", ".join(fr2us(edate, full=True)))
    11/12/2014 12:00:00, 03/01/2015 17:56:00, 12/01/1990 00:00:00

    """
    if 'fr' not in kwargs:
        kwargs.update({'fr': True})
    if 'format' not in kwargs:
        kwargs.update({'format': 'us'})
    return date2date(edate, **kwargs)


def us2date(edate, **kwargs):
    """
    Wrapper function for date2date with standard date format output (default)

    That means `date2date(edate, **kwargs)`.

    Examples
    --------
    >>> edate = ['11/12/2014 12:00', '01.03.2015 17:56:00',
    ...          '12/01/1990', '1786-05-04']
    >>> print(", ".join(us2date(edate)))
    12.11.2014 12:00, 01.03.2015 17:56:00, 01.12.1990, 04.05.1786
    >>> print(", ".join(us2date(edate, full=True)))
    12.11.2014 12:00:00, 01.03.2015 17:56:00, 01.12.1990 00:00:00, 04.05.1786 00:00:00
    >>> print(us2date(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> edate = date2en(edate)
    >>> print(", ".join(us2date(edate, full=True)))
    12.11.2014 12:00:00, 01.03.2015 17:56:00, 01.12.1990 00:00:00

    """
    return date2date(edate, **kwargs)


def us2en(edate, **kwargs):
    """
    Wrapper function for :func:`date2date` with English date format output

    That means `date2date(edate, format='en', **kwargs)`;
    but *format* given in call will overwrite *format='en'*.

    Examples
    --------
    >>> edate = ['11/12/2014 12:00', '01.03.2015 17:56:00',
    ...          '12/01/1990', '1786-05-04']
    >>> print(", ".join(us2en(edate)))
    2014-11-12 12:00, 2015-03-01 17:56:00, 1990-12-01, 1786-05-04
    >>> print(", ".join(us2en(edate, full=True)))
    2014-11-12 12:00:00, 2015-03-01 17:56:00, 1990-12-01 00:00:00, 1786-05-04 00:00:00
    >>> print(us2en(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> print(", ".join(us2en(edate, full=True)))
    2014-11-12 12:00:00, 2015-03-01 17:56:00, 1990-12-01 00:00:00

    """
    if 'format' not in kwargs:
        kwargs.update({'format': 'en'})
    return date2date(edate, **kwargs)


def us2fr(edate, **kwargs):
    """
    Wrapper function for date2date with French date format output

    That means `date2date(edate, format='fr', **kwargs)`;
    but *format* given in call will overwrite *format='fr'*.

    Examples
    --------
    >>> edate = ['11/12/2014 12:00', '01.03.2015 17:56:00',
    ...          '12/01/1990', '1786-05-04']
    >>> print(", ".join(us2fr(edate)))
    12/11/2014 12:00, 01/03/2015 17:56:00, 01/12/1990, 04/05/1786
    >>> print(", ".join(us2fr(edate, full=True)))
    12/11/2014 12:00:00, 01/03/2015 17:56:00, 01/12/1990 00:00:00, 04/05/1786 00:00:00
    >>> print(us2fr(edate, format='%Y%m%d%H%M%S'))
    ['20141112120000', '20150301175600', '19901201000000', '17860504000000']

    >>> edate = ['14-11-12 12:00', '01.03.15 17:56:00', '90-12-01']
    >>> print(", ".join(us2fr(edate, full=True)))
    12/11/2014 12:00:00, 01/03/2015 17:56:00, 01/12/1990 00:00:00

    """
    if 'format' not in kwargs:
        kwargs.update({'format': 'fr'})
    return date2date(edate, **kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
