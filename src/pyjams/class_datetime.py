#!/usr/bin/env python
"""
Conversion of datetime formats

The module enhances cftime by non-CF date formats.

This module was written by Matthias Cuntz while at Institut National de
Recherche pour l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy,
France.

:copyright: Copyright 2022- Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   date2dec
   date2num
   dec2date
   num2date
   datetime

History
    * Written date2dec and dec2date Jun 2010, Arndt Piayda
    * Input can be scalar or array_like, Feb 2012, Matthias Cuntz
    * fulldate=True default in dec2date, Feb 2012, Matthias Cuntz
    * Added calendars decimal and decimal360, Feb 2012, Matthias Cuntz
    * Rename units to refdate and add units as in netcdftime in dec2date,
      Jun 2012, Matthias Cuntz
    * Add units='day as %Y%m%d.%f' in dec2date, Jun 2012, Matthias Cuntz
    * Change units of proleptic_gregorian from 'days since 0001-01-01 00:00:00'
      to 'days since 0001-01-00 00:00:00' in date2dec, Dec 2012, Matthias Cuntz
    * Bug in Excel and leap years, Feb 2013
    * Ported to Python 3, Feb 2013
    * Bug in 'eng' output of dec2date, May 2013, Arndt Piayda
    * Times with keywords ascii and eng default to 00:00:00 in date2dec,
      Jul 2013, Matthias Cuntz
    * Corrected that Excel year starts as 1 not at 0, Oct 2013, Matthias Cuntz
    * But in units keyword and Julian calendar, day was subtracted even if
      units were given, Oct 2013, Matthias Cuntz
    * Removed remnant of time treatment before time check in eng keyword in
      date2dec, Nov 2013, Matthias Cuntz
    * Adapted date2dec to new netCDF4/netcdftime (>=v1.0) and Python datetime
      (>v2.7.9), Jun 2015, Matthias Cuntz
    * Add units=='month as %Y%m.%f' and units=='year as %Y.%f' in dec2date,
      May 2016, Matthias Cuntz
    * Now possible to pass array_like to date2num instead of single
      netCDF4.datetime objects in date2dec, Oct 2016, Matthias Cuntz
    * Provide netcdftime even with netCDF4 > v1.0.0, Oct 2016, Matthias Cuntz
    * mo is always integer in date2dec, Oct 2016, Matthias Cuntz
    * leap is always integer in dec2date, Oct 2016, Matthias Cuntz
    * Corrected 00, 01, etc. in date2dec, which are not accepted as integer
      constants by Python 3, Nov 2016, Matthias Cuntz
    * numpydoc docstring format, May 2020, Matthias Cuntz
    * Renamed eng keword to en, Jul 2020, Matthias Cuntz
    * Use proleptic_gregorian calendar for Excel dates,
      Jul 2020, Matthias Cuntz
    * Change all np.int, np.float, etc. to Python equivalents,
      May 2021, Matthias Cuntz
    * flake8 compatible, May 2021, Matthias Cuntz
    * Written class_datetime, Jun 2022, Matthias Cuntz
      Complete rewrite from scratch following closely cftime but for
      non-CF-conform calendars such as decimal, Excel, and the cdo
      absolute time formats (e.g. units='day as %Y%m%d.%f').
      Provides its own datetime class.
      Use cftime notation now, i.e. date2num and num2date but provide
      date2dec and dec2date wrappers for backward compatibility (almost).
      Provide microsecond resolution with all supported calendars no matter
      of the units, which means that date2num returns np.longdouble values.
      date2num works together with date2date and can have formatted date
      strings as input.
    * calendar keyword takes precedence on calendar attribute of
      datetime objects in date2num, Jul 2022, Matthias Cuntz
    * return_arrays keyword in date2num, Jul 2022, Matthias Cuntz
    * round_microseconds method for datetime, Jul 2022, Matthias Cuntz
    * only_use_pyjams_datetimes keyword in num2date, Jan 2022, Matthias Cuntz
    * Also CF-calendars in datetime class, Jan 2023, Matthias Cuntz

ToDo
    * Check why datetime + timedelta but not timedelta + datetime
    * add date2index
    * add time2index
    * implement fromordinal
    * implement change_calendar

"""
import re
import time as ptime
from datetime import datetime as datetime_python
from datetime import timedelta
import numpy as np
import cftime as cf
from .helper import input2array, array2input
from .date2date import date2date
# from pyjams.helper import input2array, array2input
# from pyjams.date2date import date2date


# from ._cftime import num2date, date2num, date2index, time2index, num2pydate
__all__ = ['date2dec', 'date2num', 'date2dec', 'num2date', 'datetime']


# supported calendars. Includes synonyms ('excel'=='excel1900')
_excelcalendars = ['excel', 'excel1900', 'excel1904']
_decimalcalendars = ['decimal', 'decimal360', 'decimal365', 'decimal366']
_noncfcalendars = _excelcalendars + _decimalcalendars
_cfcalendars = ['standard', 'gregorian', 'proleptic_gregorian',
                'noleap', 'julian', 'all_leap', '365_day', '366_day',
                '360_day']
_idealized_cfcalendars = ['all_leap', 'noleap', '366_day', '365_day',
                          '360_day']

# number of days in year
_dayspermonth      = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_dayspermonth_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_dayspermonth_360  = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
_cumdayspermonth      = [0, 31, 59, 90, 120, 151, 181,
                         212, 243, 273, 304, 334, 365]
_cumdayspermonth_leap = [0, 31, 60, 91, 121, 152, 182,
                         213, 244, 274, 305, 335, 366]
_cumdayspermonth_360  = [0, 30, 60, 90, 120, 150, 180,
                         210, 240, 270, 300, 330, 360]

#
# Exact copies of private cftime routines
# (changed Python time to ptime)
#

_illegal_s = re.compile(r"((^|[^%])(%%)*%s)")


def _findall(text, substr):
    # Also finds overlaps
    sites = []
    i = 0
    while 1:
        j = text.find(substr, i)
        if j == -1:
            break
        sites.append(j)
        i = j + 1
    return sites


def to_tuple(dt):
    """
    Turn a datetime instance into a tuple of integers. Elements go
    in the order of decreasing significance, making it easy to compare
    datetime instances. Parts of the state that don't affect ordering
    are omitted. Compare to timetuple().

    """
    return (dt.year, dt.month, dt.day, dt.hour, dt.minute,
            dt.second, dt.microsecond)


# factory function without optional kwargs that can be used in
# datetime.__reduce_
def _create_datetime(date_type, args, kwargs):
    return date_type(*args, **kwargs)


#
# Adapted cftime routines
#

# Every 28 years the calendar repeats, except through century leap
# years where it's 6 years. But only if you're using the Gregorian
# calendar. ;-)
# Make also 4-digit negative years
# Allow .%f for microseconds
def _strftime(dt, fmt):
    if _illegal_s.search(fmt):
        raise TypeError("This strftime implementation does not handle %s")
    if '%f' in fmt:
        if not fmt.endswith('.%f'):
            raise TypeError('If %f is used for microseconds it must be the'
                            ' at the end as .%f')
        else:
            ihavems = True
            fmt1 = fmt[:-3]
    else:
        ihavems = False
        fmt1 = fmt

    # don't use strftime method at all.
    # if dt.year > 1900:
    #    return dt.strftime(fmt)

    year = dt.year
    # For every non-leap year century, advance by
    # 6 years to get into the 28-year repeat cycle
    delta = 2000 - year
    off = 6 * (delta // 100 + delta // 400)
    year = year + off

    # Move to around the year 2000
    year = year + ((2000 - year) // 28) * 28
    # timetuple does not include microseconds
    timetuple = dt.timetuple()
    # time.strftime does hence not treat microseconds. i.e. format code %f
    s1 = ptime.strftime(fmt1, (year,) + timetuple[1:])
    sites1 = _findall(s1, str(year))

    s2 = ptime.strftime(fmt1, (year + 28,) + timetuple[1:])
    sites2 = _findall(s2, str(year + 28))

    sites = []
    for site in sites1:
        if site in sites2:
            sites.append(site)

    s = s1
    if dt.year < 0:
        syear = "%05d" % (dt.year,)
    else:
        syear = "%04d" % (dt.year,)
    for site in sites:
        s = s[:site] + syear + s[site + 4:]
    if ihavems:
        s = s + '.{:06d}'.format(dt.microsecond)
    return s


def _datesplit(timestr):
    """
    Split a unit string for time into its three components:
    unit, string 'since' or 'as', and the remainder

    """
    try:
        (units, sincestring, remainder) = timestr.split(None, 2)
    except ValueError:
        raise ValueError(f'Incorrectly formatted date-time unit_string:'
                         f' {timestr}')

    if sincestring.lower() not in ['since', 'as']:
        raise ValueError(f"No 'since' or 'as' in unit_string:"
                         f" {timestr}")

    return units.lower(), sincestring.lower(), remainder


def _year_zero_defaults(calendar):
    """
    Set calendar specific defaults for having year 0 or not

    Excel calendars *excel*, *excel1900*, *excel1904* start only 1900
    or above, i.e. no year 0.

    Decimal calendars *decimal*, *decimal360*, *decimal365*, *decimal366*
    have year 0 by default but might also omit it.

    Real-world calendars *standard*, *gregorian*, *julian* have no year 0.

    *proleptic_gregorian* (ISO 8601) and the idealized calendars
    *noleap*/*365_day*, *360_day*, *366_day*/*all_leap* have by default
    a year 0.

    Parameters
    ----------
    calendar : str
        One of the supported calendar names in *_noncfcalendars*

    Returns
    -------
    bool
       True if calendar includes year 0 by default

    Examples
    --------
    >>> print(_year_zero_defaults('Excel'))
    False
    >>> print(_year_zero_defaults('decimal'))
    True

    """
    calendar = calendar.lower()
    if calendar in ['standard', 'gregorian', 'julian']:
        return False
    elif calendar in ['proleptic_gregorian']:
        return True  # ISO 8601 year zero=1 BC
    elif calendar in _idealized_cfcalendars:
        return True
    elif calendar in _excelcalendars:
        return False
    elif calendar in _decimalcalendars:
        return True
    else:
        raise ValueError(f'Unknown calendar: {calendar}')


def _is_leap(year, calendar, has_year_zero=None):
    """
    Determines if a specific year in a given calendar is a leap year

    *has_year_zero* controls whether astronomical year numbering
    is used and the year zero exists. If not specified,
    calendar-specific default is assumed.

    Excel calendars *excel*, *excel1900*, *excel1904* start only in 1900
    or above, i.e. no year 0 allowed.

    Decimal calendars *decimal*, *decimal360*, *decimal365*, *decimal366*
    have year 0 by default but might omit it by setting *has_year_zero=False*.

    Parameters
    ----------
    year : int or array_like of int
        Year(s) to check if leap year
    calendar : str
        One of the supported calendar names in *_noncfcalendars*
    has_year_zero : bool, optional
        Astronomical year numbering is used, i.e. year zero exists, if True
        and possible for the given *calendar*. If *None* (default),
        calendar-specific defaults are assumed.

    Returns
    -------
    bool or array of bool
       True if year is a leap year

    Notes
    -----
    If there is no year 0 in a calendar, years -1, -5, -9, etc. are leap years.
    Year 0 is a leap year if it exists.

    Examples
    --------
    >>> years = [1900, 1904]
    >>> print(_is_leap(years, 'decimal'))
    [False, True]
    >>> print(_is_leap(years, 'Excel'))
    [True, True]

    """
    myear = input2array(year, default=1990)

    # set calendar-specific defaults for has_year_zero
    if has_year_zero is None:
        has_year_zero = _year_zero_defaults(calendar)

    if has_year_zero and (calendar in _excelcalendars):
        raise ValueError('year 0 not allowed with Excel calendars')
    if np.any(myear == 0) and (not has_year_zero):
        raise ValueError(f'year 0 does not exist in the calendar {calendar}')

    if calendar in _cfcalendars:
        leap = [ cf.is_leap_year(yy, calendar, has_year_zero) for yy in myear ]
    else:
        # If there is no year 0 in the calendar, years -1, -5, -9, etc.
        # are leap years. year 0 is a leap year if it exists.
        if not has_year_zero:
            myear = np.where(myear < 0, myear + 1, myear)

        if calendar in _excelcalendars:
            # Excel calendars are supposedly Julian calendars
            leap = (myear % 4) == 0
        elif calendar == 'decimal':
            leap = ( (((myear % 4) == 0) & ((myear % 100) != 0)) |
                     ((myear % 400) == 0) )
        elif calendar in ['decimal360', 'decimal365']:
            leap = np.zeros_like(myear, dtype=bool)
        elif calendar == 'decimal366':
            leap = np.ones_like(myear, dtype=bool)
        else:
            raise ValueError(f'Calendar not known: {calendar}')

    oleap = array2input(leap, year)

    return oleap


def _month_lengths(year, calendar, has_year_zero=None):
    """
    Number of days of the 12 months in specific year for a given calendar

    Parameters
    ----------
    year : int
        Year to inquire
    calendar : str
        One of the supported calendar names in *_noncfcalendars*
    has_year_zero : bool, optional
        Astronomical year numbering is used, i.e. year zero exists, if True
        and possible for the given *calendar*. If *None* (default),
        calendar-specific defaults are assumed.

    Returns
    -------
    list
       Lengths of the 12 months in specified *year*

    Examples
    --------
    >>> print(_month_lengths(1990, 'decimal'))
    [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    >>> print(_month_lengths(1990, 'decimal360'))
    [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

    """
    leap = _is_leap(year, calendar, has_year_zero)
    if calendar == 'decimal360':
        return _dayspermonth_360
    else:
        if leap:
            return _dayspermonth_leap
        else:
            return _dayspermonth


def _int_julian_day_from_date(year, month, day, calendar,
                              skip_transition=False, has_year_zero=None):
    """
    Compute integer Julian Day from year, month, day, and calendar

    Integer julian day is number of days since noon UTC -4713-1-1
    in the julian or mixed julian/gregorian calendar, or noon UTC
    -4714-11-24 in the proleptic_gregorian calendar (without year zero).
    Reference date is noon UTC 0000-01-01 for other calendars.

    Excel calendars are supposedly Julian calendars with other reference dates.
    Julian calendar is hence used for the Excel calendars *excel*, *excel1900*,
    *excel1904*, i.e. integer julian day is the same number of days since
    -4713-01-01 12:00:00 in the Julian calendar.

    Integer julian day in the decimal calendars *decimal*, *decimal360*,
    *decimal365*, *decimal366* is the number of days after 0000-01-01 12:00:00.

    If the has_year_zero kwarg is set to True, astronomical year numbering
    is used and the year zero exists for the decimal calendars.
    If set to False, then historical year numbering is used and the year 1 is
    preceded by year -1 and no year zero exists.
    The defaults (has_year_zero=None) uses astronomical year numbering
    for the decimal calendars.
    CF version 1.9 conventions are:
    False for 'julian', 'gregorian'/'standard',
    True for 'proleptic_gregorian' (ISO 8601), and
    True for the idealized calendars 'noleap'/'365_day', '360_day',
    366_day'/'all_leap'

    'skip_transition': When True, leave a 10-day
    gap in Julian day numbers between Oct 4 and Oct 15 1582 (the transition
    from Julian to Gregorian calendars). Default: False,
    ignored unless calendar = 'standard' or 'gregorian'.

    """
    if calendar:
        calendar = calendar.lower()
    if has_year_zero is None:
        has_year_zero = _year_zero_defaults(calendar)
    if (calendar == 'decimal360') or (calendar == '360_day'):
        # return year * 360 + (month - 1) * 30 + day - 1
        return year * 360 + _cumdayspermonth_360[month - 1] + day - 1
    elif ( (calendar == 'decimal365') or (calendar == '365_day') or
           (calendar == 'noleap')):
        return year * 365 + _cumdayspermonth[month - 1] + day - 1
    elif ( (calendar == 'decimal366') or (calendar == '366_day') or
           (calendar == 'all_leap')):
        return year * 366 + _cumdayspermonth_leap[month - 1] + day - 1
    else:
        leap = _is_leap(year, calendar, has_year_zero=has_year_zero)
        if leap:
            jday = day + _cumdayspermonth_leap[month - 1]
        else:
            jday = day + _cumdayspermonth[month - 1]
        # If there is no year 0, years -1, -5, -9, etc,
        # are leap years. year zero is a leap year if it exists.
        if (year < 0) and (not has_year_zero):
            year += 1
        if calendar == 'decimal':
            # 1st term is the number of days in the last year
            # 2nd term is the number of days in each preceding non-leap year
            # last terms are the number of preceding leap years
            jday_greg = (jday + 365 * (year - 1) +
                         (year - 1) // 4 - (year - 1) // 100 +
                         (year - 1) // 400)
            return jday_greg
        elif (calendar in _excelcalendars) or (calendar == 'julian'):
            year += 4800  # add offset so -4800 is year 0.
            # 1st term is the number of days in the last year
            # 2nd term is the number of days in each preceding non-leap year
            # last terms are the number of preceding leap years
            jday_jul = jday + 365 * (year - 1) + (year - 1) // 4
            # remove offset for 87 years before -4713 (including leap days)
            jday_jul -= 31777
            return jday_jul
        elif ( (calendar == 'standard') or (calendar == 'gregorian') or
               (calendar == 'proleptic_gregorian') ):
            year += 4800  # add offset so -4800 is year 0.
            # 1st term is the number of days in the last year
            # 2nd term is the number of days in each preceding non-leap year
            # last terms are the number of preceding leap years since -4800
            jday_jul = jday + 365 * (year - 1) + (year - 1) // 4
            # remove offset for 87 years before -4713 (including leap days)
            jday_jul -= 31777
            jday_greg = (jday + 365 * (year - 1) +
                         (year - 1) // 4 - (year - 1) // 100 +
                         (year - 1) // 400)
            # remove offset, and account for the fact that -4713/1/1 is jday=38
            # in gregorian calendar.
            jday_greg -= 31739
            if calendar == 'proleptic_gregorian':
                return jday_greg
            else:
                # check for invalid days in mixed calendar
                # (there are 10 missing)
                if jday_jul >= 2299161 and jday_jul < 2299171:
                    raise ValueError('invalid date in mixed calendar')
                if jday_jul < 2299161:  # 1582 October 15
                    return jday_jul
                else:
                    if skip_transition:
                        return jday_greg + 10
                    else:
                        return jday_greg
        else:
            raise ValueError(f'Unknown calendar: {calendar}')


# Add a datetime.timedelta to a pyjams.datetime instance. Uses
# integer arithmetic to avoid rounding errors and preserve
# microsecond accuracy.
def _add_timedelta(dt, delta):
    # extract these inputs here to avoid type conversion in the code below
    delta_microseconds = delta.microseconds
    delta_seconds = delta.seconds
    delta_days = delta.days

    # shift microseconds, seconds, days
    calendar = dt.calendar
    has_year_zero = dt.has_year_zero
    microsecond = dt.microsecond + delta_microseconds
    second = dt.second + delta_seconds
    minute = dt.minute
    hour = dt.hour
    day = dt.day
    month = dt.month
    year = dt.year

    month_length = _month_lengths(year, calendar, has_year_zero)

    # Normalize microseconds, seconds, minutes, hours.
    second += microsecond // 1000000
    microsecond = microsecond % 1000000
    minute += second // 60
    second = second % 60
    hour += minute // 60
    minute = minute % 60
    extra_days = hour // 24
    hour = hour % 24

    delta_days += extra_days

    while delta_days < 0:
        # not done compared to cftime because Excel dates > 1900 and
        # decimal dates include 1582-10-05 to 1582-10-14
        # if (year == 1582 and month == 10 and day > 14 and
        #     day + delta_days < 15):
        #     delta_days -= n_invalid_dates    # skip over invalid dates
        if (day + delta_days) < 1:
            delta_days += day
            # decrement month
            month -= 1
            if month < 1:
                month = 12
                year -= 1
                if (year == 0) and (not has_year_zero):
                    year = -1
                month_length = _month_lengths(year, calendar, has_year_zero)
            day = month_length[month - 1]
        else:
            day += delta_days
            delta_days = 0

    while delta_days > 0:
        # not done compared to cftime because Excel dates > 1900 and
        # decimal dates include 1582-10-05 to 1582-10-14
        # if (year == 1582 and month == 10 and day < 5 and
        #     day + delta_days > 4):
        #     delta_days += n_invalid_dates    # skip over invalid dates
        if (day + delta_days) > month_length[month - 1]:
            delta_days -= month_length[month - 1] - (day - 1)
            # increment month
            month += 1
            if month > 12:
                month = 1
                year += 1
                if (year == 0) and (not has_year_zero):
                    year = 1
                month_length = _month_lengths(year, calendar, has_year_zero)
            day = 1
        else:
            day += delta_days
            delta_days = 0

    return (year, month, day, hour, minute, second, microsecond)


#
# New routines
#

def _units_defaults(calendar, has_year_zero=None):
    """
    Set calendar specific default units as 'days since reference_date'

    Day 0 of *excel* and *excel1900* starts at 1899-12-31 00:00:00.

    Day 0 of *excel1904* starts at 1903-12-31 00:00:00.

    Decimal calendars *decimal*, *decimal360*, *decimal365*, and
    *decimal366* do not need units so 0001-01-01 00:00:00 is taken.

    Day 0 of *julian*, *gregorian* and *standard* starts at
    -4713-01-01 12:00:00 if not has_year_zero, and at
    -4712-01-01 12:00:00 if has_year_zero.

    Day 0 of *proleptic_gregorian* starts at
    -4714-11-24 12:00:00 if not has_year_zero, and at
    -4713-11-24 12:00:00 if has_year_zero.

    Day 0 of *360_day*, *365_day*, *366_day*, *all_leap*, and
    *noleap* starts at 0000-01-01 12:00:00.

    Parameters
    ----------
    calendar : str
        One of the supported calendar names in *_cfcalendars* and
        *_noncfcalendars*
    has_year_zero : bool, optional
        Astronomical year numbering is used, i.e. year zero exists, if True
        and possible for the given *calendar*. If *None* (default),
        calendar-specific defaults are assumed.

    Returns
    -------
    str
       'days since reference_date' with calendar-specific reference_date

    Examples
    --------
    >>> print(_units_defaults('Excel'))
    'days since 1899-12-31 00:00:00'

    """
    calendar = calendar.lower()
    if has_year_zero is None:
        has_year_zero = _year_zero_defaults(calendar)
    if calendar in ['standard', 'gregorian', 'julian']:
        if has_year_zero:
            return 'days since -4712-01-01 12:00:00'
        else:
            return 'days since -4713-01-01 12:00:00'
    elif calendar in ['proleptic_gregorian']:
        if has_year_zero:
            return 'days since -4713-11-24 12:00:00'
        else:
            return 'days since -4714-11-24 12:00:00'
    elif calendar in _idealized_cfcalendars:
        return 'days since 0000-01-01 12:00:00'
    elif calendar in ['excel', 'excel1900']:
        return 'days since 1899-12-31 00:00:00'
    elif calendar in ['excel1904']:
        return 'days since 1903-12-31 00:00:00'
    elif calendar in _decimalcalendars:
        return 'days since 0001-01-01 00:00:00'
    else:
        raise ValueError(f'Unknown calendar: {calendar}')


def _date2decimal(date, calendar):
    """
    Decimal date from datetime object

    Parameters
    ----------
    date : datetime instance
        Instance of pyjams.datetime class
    calendar : str
        One of the decimal calendar names *decimal*, *decimal360*,
        *decimal365*, or *decimal366*

    Returns
    -------
    longdouble
       decimal date

    Examples
    --------
    >>> dt = datetime(1990, 1, 1)
    >>> dec = _date2decimal(dt, 'decimal')
    >>> print(dec)
    1990.

    """
    year     = date.year
    month    = date.month
    day      = np.longdouble(date.day)
    hour     = np.longdouble(date.hour)
    minute   = np.longdouble(date.minute)
    second   = np.longdouble(date.second)
    msecond  = np.longdouble(date.microsecond)
    calendar = calendar.lower()

    days_year = np.longdouble(365)
    diy = np.array([ [-9] + _cumdayspermonth,
                     [-9] + _cumdayspermonth_leap ], dtype=np.longdouble)
    if calendar == 'decimal':
        leap = int( (((year % 4) == 0) & ((year % 100) != 0)) |
                    ((year % 400) == 0) )
    elif calendar == 'decimal360':
        leap = 0
        days_year = np.longdouble(360)
        diy  = np.array([ [-9] + _cumdayspermonth_360,
                          [-9] + _cumdayspermonth_360 ], dtype=np.longdouble)
    elif calendar == 'decimal365':
        leap = 0
    elif calendar == 'decimal366':
        leap = 1
    fleap = np.longdouble(leap)
    tday  = diy[leap, month] + day
    thour = ( (tday - 1.) * 24. +
              hour +
              minute / 60. +
              second / 3600. +
              msecond / 3600000000. )
    out = np.longdouble(year) + thour / ((days_year + fleap) * 24.)

    return out


def _dates2decimal(dates, calendar):
    """
    Decimal dates from datetime objects

    Parameters
    ----------
    dates : datetime instance or array_like of datetime instances
        Instances of pyjams.datetime class
    calendar : str
        One of the decimal calendar names *decimal*, *decimal360*,
        *decimal365*, or *decimal366*

    Returns
    -------
    array_like of longdouble
       decimal dates

    Examples
    --------
    >>> dt = [datetime(1990, 1, 1), datetime(1991, 1, 1)]
    >>> dec = _dates2decimal(dt, 'decimal')
    >>> print(dec)
    [1990., 1991.]

    """
    mdates = input2array(dates, default=datetime(1990, 1, 1))

    # wrapper might be slow
    out = [ _date2decimal(dd, calendar) for dd in mdates ]

    out = array2input(out, dates)
    return out


def _date2absolute(date, units):
    """
    Absolute date from datetime object

    Parameters
    ----------
    date : datetime instance
        Instances of pyjams.datetime class
    units : str
        'day as %Y%m%d.%f', 'month as %Y%m.%f', or 'year as %Y.%f'

    Returns
    -------
    longdouble
       absolute date

    Examples
    --------
    >>> dt = datetime(1990, 1, 1)
    >>> dec = _date2absolute(dt, 'day as %Y%m%d.%f')
    >>> print(np.around(dec, 1))
    19900101.0

    """
    year     = date.year
    month    = date.month
    day      = np.longdouble(date.day)
    hour     = np.longdouble(date.hour)
    minute   = np.longdouble(date.minute)
    second   = np.longdouble(date.second)
    msecond  = np.longdouble(date.microsecond)

    if units == 'day as %Y%m%d.%f':
        tday  = (np.longdouble(year) * 10000. +
                 np.longdouble(month) * 100. +
                 day)
        thour = (hour +
                 minute / 60. +
                 second / 3600. +
                 msecond / 3600000000.)
        out = tday + thour / 24.
    elif units == 'month as %Y%m.%f':
        leap = int( (((year % 4) == 0) & ((year % 100) != 0)) |
                    ((year % 400) == 0) )
        dim = np.array([ [-9] + _dayspermonth,
                         [-9] + _dayspermonth_leap ], dtype=np.longdouble)
        tmonth = (np.longdouble(year) * 100. +
                  np.longdouble(month))
        thour = (day * 24. +
                 hour +
                 minute / 60. +
                 second / 3600. +
                 msecond / 3600000000.)
        out = tmonth + thour / (dim[leap, month] * 24.)
    elif units == 'year as %Y.%f':
        # same as decimal date
        out = _date2decimal(date, 'decimal')
    else:
        raise ValueError(f'Unknown absolute units: {units}')

    return out


def _dates2absolute(dates, units):
    """
    Absolute dates from datetime object

    Parameters
    ----------
    dates : datetime instance or array_like of datetime instances
        Instances of pyjams.datetime class
    units : str
        'day as %Y%m%d.%f', 'month as %Y%m.%f', or 'year as %Y.%f'

    Returns
    -------
    longdouble or array_like of longdouble
       absolute dates

    Examples
    --------
    >>> dt = [datetime(1990, 1, 1), datetime(1991, 1, 1)]
    >>> dec = _dates2absolute(dt, 'day as %Y%m%d.%f')
    >>> print(np.around(dec, 1))
    [19900101.0, 19910101.0]

    """
    mdates = input2array(dates, default=datetime(1990, 1, 1))

    # wrapper might be slow
    out = [ _date2absolute(dd, units) for dd in mdates ]

    out = array2input(out, dates)
    return out


def _decimal2date(times, calendar):
    """
    Split decimal dates into year, month, day, hour, minute, second,
    microsecond

    Parameters
    ----------
    times : float or array_like
        Decimal dates such as 1990.5102
    calendar : str
        One of the decimal calendar names *decimal*, *decimal360*,
        *decimal365*, or *decimal366*

    Returns
    -------
    tuple
       arrays of year, month, day, hour, minute, second, microsecond

    Examples
    --------
    >>> dec = [1990., 1991.5]
    >>> yr, mo, dy, hr, mi, sc, ms = _decimal2date(dec, 'decimal')
    >>> print(yr)
    [1990, 1991]
    >>> print(mo)
    [1, 7]
    >>> print(dy)
    [1, 3]

    """
    # old algorithm does decomposition on all array elements
    # should try similar to decode_dates_from_array for speed
    # where decomposition is done for the first (oldest) element only
    # and then timedeltas are added subsequently
    mtimes = input2array(times, default=1.)
    mtimes = np.array(mtimes, dtype=np.longdouble)
    calendar = calendar.lower()

    # year
    fyear = np.trunc(mtimes)
    fyear = np.where(mtimes < 0., fyear - 1., fyear)
    year = fyear.astype(np.int64)
    frac_year = mtimes - fyear
    days_year = np.longdouble(365)
    diy = np.array([ [-9] + _cumdayspermonth,
                     [-9] + _cumdayspermonth_leap ])
    if calendar == 'decimal':
        leap = ( (((year % 4) == 0) & ((year % 100) != 0)) |
                 ((year % 400) == 0) ).astype(int)
        fleap = leap.astype(np.longdouble)
    elif calendar == 'decimal360':
        leap  = np.zeros_like(mtimes, dtype=int)
        fleap = np.zeros_like(mtimes, dtype=np.longdouble)
        days_year = np.longdouble(360)
        diy  = np.array([ [-9] + _cumdayspermonth_360,
                          [-9] + _cumdayspermonth_360 ])
    elif calendar == 'decimal365':
        leap  = np.zeros_like(mtimes, dtype=int)
        fleap = np.zeros_like(mtimes, dtype=np.longdouble)
    elif calendar == 'decimal366':
        leap  = np.ones_like(mtimes, dtype=int)
        fleap = np.ones_like(mtimes, dtype=np.longdouble)
    else:
        raise ValueError(f'Unknown decimal calendar: {calendar}')
    # change to microseconds to catch round-off errors,
    # i.e. cases 1 microsec less or greater than a second
    # cf. issue #187 of cftime
    # day of year in microseconds
    fhoy = frac_year * (days_year + fleap) * 86400000000.
    ihoy = np.rint(fhoy).astype(np.int64)
    # Done in cftime for issue #187
    # ihoy = np.where(ihoy%1000000 == 1,
    #                 np.floor(fhoy).astype(np.int64), ihoy)
    # ihoy = np.where(ihoy%1000000 == 999999,
    #                 np.ceil(fhoy).astype(np.int64), ihoy)
    # microsecond
    msecond = ihoy % 1000000
    ihoy    = ihoy // 1000000
    # second
    second = ihoy % 60
    ihoy   = ihoy // 60
    # minute
    minute = ihoy % 60
    ihoy   = ihoy // 60
    # hour
    hour = ihoy % 24
    ihoy = ihoy // 24
    # day and month
    idoy = ihoy + 1
    month = np.zeros_like(mtimes, dtype=np.int64)
    day   = np.zeros_like(mtimes, dtype=np.int64)
    for i in range(mtimes.size):
        ii = np.where(idoy[i] > diy[leap[i], :])[0]
        month[i] = ii[-1]
        day[i]   = idoy[i] - diy[leap[i], month[i]]

    return year, month, day, hour, minute, second, msecond


def _absolute2date(times, units):
    """
    Split date(s) in absolute date format into
    year, month, day, hour, minute, second, microsecond

    Parameters
    ----------
    times : float or array_like
        Absolute dates such as 20070102.0034722
    units : str
        'day as %Y%m%d.%f', 'month as %Y%m.%f', or 'year as %Y.%f'

    Returns
    -------
    tuple
       arrays of year, month, day, hour, minute, second, microsecond

    Examples
    --------
    >>> absolut = [20070102.0034722, 20070102.0069444]
    >>> yr, mo, dy, hr, mi, sc, ms = _absolute2date(absolut,
    ...                                             'day as %Y%m%d.%f')
    >>> print(yr)
    [2007, 2007]
    >>> print(mi)
    [5, 10]

    """
    # old algorithm does decomposition on all array elements
    # should try similar to decode_dates_from_array for speed
    # where decomposition is done for the first (oldest) element only
    # and then timedeltas are added subsequently
    mtimes = input2array(times, default=10101.)
    mtimes = np.array(mtimes, dtype=np.longdouble)

    if units == 'day as %Y%m%d.%f':
        # change to microseconds to catch round-off errors,
        # i.e. cases 1 microsec less or greater than a second
        # cf. issue #187 of cftime
        # day of year in microseconds
        fhoy = mtimes * 86400000000.
        ihoy = np.rint(fhoy).astype(np.int64)
        # Done in cftime for issue #187
        # ihoy = np.where(ihoy%1000000 == 1,
        #                 np.floor(fhoy).astype(np.int64), ihoy)
        # ihoy = np.where(ihoy%1000000 == 999999,
        #                 np.ceil(fhoy).astype(np.int64), ihoy)
        # microsecond
        msecond = ihoy % 1000000
        ihoy    = ihoy // 1000000
        # second
        second = ihoy % 60
        ihoy   = ihoy // 60
        # minute
        minute = ihoy % 60
        ihoy   = ihoy // 60
        # hour
        hour = ihoy % 24
        ihoy = ihoy // 24
        # day
        day = ihoy % 100
        ihoy = ihoy // 100
        # month
        month = ihoy % 100
        ihoy = ihoy // 100
        # year
        year = ihoy
    elif units == 'month as %Y%m.%f':
        fmo     = mtimes % 1.  # month fraction
        # month
        mtimes -= fmo
        month   = np.rint(mtimes % 100.).astype(np.int64)
        # year
        mtimes -= month
        year    = np.rint(mtimes / 100.).astype(np.int64)
        # day of month in microseconds
        leap    = np.where((((year % 4) == 0) & ((year % 100) != 0)) |
                           ((year % 400) == 0), 1, 0)
        dim     = np.array([ [-9] + _dayspermonth,
                             [-9] + _dayspermonth_leap ])
        fhoy = dim[(leap, month)] * fmo * 86400000000.
        ihoy = np.rint(fhoy).astype(np.int64)
        # Done in cftime for issue #187
        # ihoy = np.where(ihoy%1000000 == 1,
        #                 np.floor(fhoy).astype(np.int64), ihoy)
        # ihoy = np.where(ihoy%1000000 == 999999,
        #                 np.ceil(fhoy).astype(np.int64), ihoy)
        # microsecond
        msecond = ihoy % 1000000
        ihoy    = ihoy // 1000000
        # second
        second = ihoy % 60
        ihoy   = ihoy // 60
        # minute
        minute = ihoy % 60
        ihoy   = ihoy // 60
        # hour
        hour = ihoy % 24
        ihoy = ihoy // 24
        # day
        day = ihoy
        # mtimes  = dim[(leap, month)] * fmo
        # fdy     = mtimes % 1.  # day fraction
        # mtimes -= fdy
        # day     = np.rint(mtimes % 100.).astype(np.int64)
        # # hour
        # secs    = fdy * 86400.
        # fsecs   = secs % 1.  # second fraction
        # secs    = np.rint(secs)
        # hour    = np.floor(secs / 3600.).astype(np.int64)
        # # minute
        # secs   -= 3600. * hour
        # minute  = np.floor(secs / 60.).astype(np.int64)
        # # second
        # secs   -= 60. * minute
        # second  = np.rint(secs).astype(np.int64)
        # # millisecond
        # msecond  = np.rint(fsecs * 1000000.).astype(np.int64)
    elif units == 'year as %Y.%f':
        # same as decimal date
        year, month, day, hour, minute, second, msecond = _decimal2date(
            times, 'decimal')
    else:
        raise ValueError(f'Unknown absolute units: {units}')

    return year, month, day, hour, minute, second, msecond


#
# Main routines and class
#

def date2num(dates, units='', calendar=None, has_year_zero=None,
             format='', timesep=' ', fr=False, return_arrays=False):
    """
    Return numeric time values given datetime objects or strings

    The units of the numeric time values are described by the
    *units* and *calendar* keywords for CF-conform calendars, i.e.
    *standard*, *gregorian*, *julian*, *proleptic_gregorian*,
    *360_day*, *365_day*, *366_day*, *noleap*, *all_leap*.
    See http://cfconventions.org/cf-conventions/cf-conventions#calendar
    These times will be passed to cftime.num2date.

    Standard *units* are used for the non-CF-conform calendars
    *excel*, *excel1900*, *excel1904*, and
    *decimal*, *decimal360*, *decimal365*, *decimal366*,
    and given *units* will hence be ignored.

    Parameters
    ----------
    dates : datetime instance or str, or array_like of datetime or str
        datetime objects or strings with string representations.
        datetime objects can either be Python datetime.datetime,
        cf.datetime, or pyjams.datetime objects. If *dates* are strings,
        then *format* keyword is relevant.
    units : str, optional
        Units string such as 'seconds since 1900-01-01 00:00:00' or
        'day as %Y%m%d.%f'. Standard units corresponding to days after
        day 0 of a given calendar will be used if omitted, i.e. assuming
        Julian day ordinals.

        In the form *time_units since reference_time*,
        *time_units* can be days, hours, minutes, seconds, milliseconds,
        or microseconds. *reference_time* is the time origin.
        *months since* is allowed only for the *360_day* calendar
        and *common_years since* is allowed only for the *365_day* calendar.

        There are currently only three valid forms for *time_units as format*:
        'day as %Y%m%d.%f', 'month as %Y%m.%f', 'year as %Y.%f'. The latter is
        the same as 'calendar=decimal'. *calendar='decimal' will be set in
        case units *time_units as format*.
    calendar : str, optional
        One of the supported calendars, i.e. the CF-conform calendars
        *standard*, *gregorian*, *julian*, *proleptic_gregorian*,
        *360_day*, *365_day*, *366_day*, *noleap*, *all_leap*,
        as well as the non-CF-conform calendars
        *excel*, *excel1900*, *excel1904*, and
        *decimal*, *decimal360*, *decimal365*, *decimal366*.
        *standard* will be taken by default, which is a mixed
        Julian/Gregorian calendar.
        The keyword takes precedence on calendar in datetime objects.
    has_year_zero : bool, optional
        Astronomical year numbering is used and the year zero exists, if set to
        True. If set to False for real-world calendars, then historical year
        numbering is used and the year 1 is preceded by year -1 and no year
        zero exists.
        The defaults are set to conform with CF version 1.9 conventions, i.e.
        False for 'standard', 'gregorian', and 'julian', True
        for 'proleptic_gregorian' (ISO 8601), and True for the idealized
        calendars 'noleap'/'365_day', '360_day', 366_day'/'all_leap'.
        Excel calendars *excel*, *excel1900*, *excel1904* start only 1900
        or above so *has_year_zero* is always False.
        Decimal calendars *decimal*, *decimal360*, *decimal365*, *decimal366*
        have always year 0, i.e. *has_year_zero* is True.
    format : str, optional
        If *dates* are strings, then *format* is the Python
        datetime.strftime/strptime format string if given. If empty (default),
        then the routine pyjams.date2date will be used, which converts between
        formats '%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M:%S', and '%m/%d/%Y
        %H:%M:%S' (called English *YYYY-MM-DD hh:mm:ss*, standard
        *DD.MM.YYYY hh:mm:ss*, and American *MM/DD/YYYY hh:mm:ss* in
        pyjams.date2date), where times can be partial or missing.
    timesep : str, optional
        Separator string between date and time used by pyjams.date2date if
        if *dates* are strings and *format* is empty (default: ' ')
    fr : bool, optional
        If True, pyjams.date2date will interpret input dates with '/'
        separators not as the American format '%m/%d/%Y %H:%M:%S' but the
        French way as '%d/%m/%Y %H:%M:%S', if *dates* are strings and
        *format* is empty
    return_arrays : bool, optional
        If True, then return a tuple with individual arrays for
        year, month, day, hour, minute, second, microsecond

    Returns
    -------
    array_like
       numeric time values

    Examples
    --------
    >>> idates = ['2000-01-05 12:30:15', '1810-04-24 16:15:10',
    ...           '1630-07-15 10:20:40', '1510-09-20 14:35:50',
    ...           '1271-03-18 19:41:34', '0619-08-27 11:08:37',
    ...           '0001-01-01 12:00:00']
    >>> decimal = date2num(idates, calendar='decimal')
    >>> num2date(decimal, calendar='decimal', format='%Y-%m-%d %H:%M:%S')
    ['2000-01-05 12:30:15',
     '1810-04-24 16:15:10',
     '1630-07-15 10:20:40',
     '1510-09-20 14:35:50',
     '1271-03-18 19:41:34',
     '0619-08-27 11:08:37',
     '0001-01-01 12:00:00']

    """
    date0 = np.ravel(dates)[0]
    if isinstance(date0, str):
        if format:
            iform = format
        else:
            iform = '%Y-%m-%d %H:%M:%S'
        default = cf.real_datetime(1990, 1, 1).strftime(iform)
    else:
        default = cf.real_datetime(1990, 1, 1)
    mdates = input2array(dates, default=default)

    # datetime with calendar
    date0 = mdates[0]
    if calendar is not None:
        icalendar = calendar
    else:
        try:
            icalendar = date0.calendar
        except AttributeError:
            # take standard otherwise
            icalendar = 'standard'

    if icalendar:
        icalendar = icalendar.lower()
    else:
        icalendar = 'standard'
    if (icalendar not in _cfcalendars) and (icalendar not in _noncfcalendars):
        raise ValueError(f'Unknown calendar: {icalendar}')
    if not units:
        units = _units_defaults(icalendar)

    # transform strings to datetime objects
    # only possible for year > 0
    isstr = all([ isinstance(dd, str) for dd in mdates ])
    if isstr:
        if format:
            iform = format
        else:
            mdates = date2date(mdates, format='en', full=True,
                               timesep=timesep, fr=fr)
            iform = '%Y-%m-%d %H:%M:%S'
        mmdates = [ cf.real_datetime.strptime(dd, iform)
                    for dd in mdates ]

        if icalendar in _cfcalendars:
            mmdates = [ cf.datetime(*to_tuple(dt), calendar=icalendar,
                                    has_year_zero=has_year_zero)
                        for dt in mmdates ]
        else:
            mmdates = [ datetime(*to_tuple(dt), calendar=icalendar,
                                 has_year_zero=has_year_zero)
                        for dt in mmdates ]
        mdates = input2array(mmdates, default=cf.datetime(1990, 1, 1))
    else:
        mdates = input2array(dates, default=cf.real_datetime(1990, 1, 1))

    # if year, month, ... wanted, no need to go further
    if return_arrays:
        out = np.array([ to_tuple(dt) for dt in mdates ])
        year        = array2input(out[:, 0], dates)
        month       = array2input(out[:, 1], dates)
        day         = array2input(out[:, 2], dates)
        hour        = array2input(out[:, 3], dates)
        minute      = array2input(out[:, 4], dates)
        second      = array2input(out[:, 5], dates)
        microsecond = array2input(out[:, 6], dates)
        return year, month, day, hour, minute, second, microsecond

    # check if we can parse to cftime
    if icalendar in _cfcalendars:
        iscf = True
    elif icalendar in _noncfcalendars:
        iscf = False
    else:  # pragma: no cover
        # should be impossible to reach
        raise ValueError(f'Unknown calendar: {icalendar}')

    unit, sincestr, remainder = _datesplit(units)
    if sincestr == 'as':
        iscf = False
        icalendar = ''

    # use cftime.date2num if possible
    if iscf:
        if not remainder.startswith('-'):
            if int(remainder.split('-')[0]) == 0:
                if has_year_zero is not None:
                    has_year_zero = True
        out = cf.date2num(mdates, units, calendar=icalendar,
                          has_year_zero=has_year_zero)

    if sincestr == 'as':
        if units not in ['day as %Y%m%d.%f', 'month as %Y%m.%f',
                         'year as %Y.%f']:
            raise ValueError(f'Absolute date format unknown: {units}')
        out = _dates2absolute(mdates, units)

    # use cftime.date2num with Excel
    if icalendar in _excelcalendars:
        cfcalendar = 'julian'
        cfdates = [ cf.datetime(*to_tuple(dt), calendar=cfcalendar)
                    for dt in mdates ]
        out = cf.date2num(cfdates, units, calendar=cfcalendar,
                          has_year_zero=has_year_zero)

    # no cftime.num2date possible
    if icalendar in _decimalcalendars:
        out = _dates2decimal(mdates, icalendar)

    out = array2input(out, dates)
    return out


def date2dec(*args, **kwargs):
    """
    Wrapper for :func:`date2num`
    """
    return date2num(*args, **kwargs)


def num2date(times, units='', calendar='standard',
             only_use_pyjams_datetimes=True,
             only_use_cftime_datetimes=True,
             only_use_python_datetimes=False,
             has_year_zero=None,
             format='', return_arrays=False):
    """
    Return datetime objects given numeric time values

    The units of the numeric time values are described by the
    *units* and *calendar* keywords for CF-conform calendars, i.e.
    *standard*, *gregorian*, *julian*, *proleptic_gregorian*,
    *360_day*, *365_day*, *366_day*, *noleap*, *all_leap*.
    See http://cfconventions.org/cf-conventions/cf-conventions#calendar
    These times will be passed to cftime.num2date.

    Standard *units* are used for the non-CF-conform calendars
    *excel*, *excel1900*, *excel1904*, and
    *decimal*, *decimal360*, *decimal365*, *decimal366*,
    and given *units* will hence be ignored.

    Parameters
    ----------
    times : float or array_like
        Numeric time values
    units : str, optional
        Units string such as 'seconds since 1900-01-01 00:00:00' or
        'day as %Y%m%d.%f'. Standard units corresponding to days after
        day 0 of a given calendar will be used if omitted, i.e. assuming
        Julian day ordinals.

        In the form *time_units since reference_time*,
        *time_units* can be days, hours, minutes, seconds, milliseconds,
        or microseconds. *reference_time* is the time origin.
        *months since* is allowed only for the *360_day* calendar
        and *common_years since* is allowed only for the *365_day* calendar.

        There are currently only three valid forms for *time_units as format*:
        'day as %Y%m%d.%f', 'month as %Y%m.%f', 'year as %Y.%f'. The latter is
        the same as 'calendar=decimal'. *calendar='decimal' will be set in
        case units *time_units as format*.
    calendar : str, optional
        One of the support calendars, i.e. the CF-conform calendars
        *standard*, *gregorian*, *julian*, *proleptic_gregorian*,
        *360_day*, *365_day*, *366_day*, *noleap*, *all_leap*,
        as well as the non-CF-conform calendars
        *excel*, *excel1900*, *excel1904*, and
        *decimal*, *decimal360*, *decimal365*, *decimal366*.
        *standard* will be taken by default, which is a mixed
        Julian/Gregorian calendar.
    only_use_pyjams_datetimes : bool, optional
        pyjams.datetime objects are returned by default.
        Only if only_use_pyjams_datetimes is set to False (default: True) and
        only_use_cftime_datetimes is set to True then cftime.datetime objects
        will be returned where possible.
        Only if only_use_pyjams_datetimes and only_use_cftime_datetimes are set
        to False and only_use_python_datetimes is set to True then Python
        datetime.datetime objects will be returned where possible.
    only_use_cftime_datetimes : bool, optional
        pyjams.datetime objects are returned by default.
        Only if only_use_pyjams_datetimes is set to False and
        only_use_cftime_datetimes is set to True (default: False) then
        cftime.datetime objects will be returned where possible.
        Only if only_use_pyjams_datetimes and only_use_cftime_datetimes are set
        to False and only_use_python_datetimes is set to True then Python
        datetime.datetime objects will be returned where possible.
    only_use_python_datetimes : bool, optional
        pyjams.datetime objects are returned by default.
        Only if only_use_pyjams_datetimes is set to False and
        only_use_cftime_datetimes is set to True then cftime.datetime objects
        will be returned where possible.
        Only if only_use_pyjams_datetimes and only_use_cftime_datetimes are set
        to False and only_use_python_datetimes is set to True (default: False)
        then Python datetime.datetime objects will be returned where possible.
    has_year_zero : bool, optional
        Astronomical year numbering is used and the year zero exists, if set to
        True. If set to False for real-world calendars, then historical year
        numbering is used and the year 1 is preceded by year -1 and no year
        zero exists.
        The defaults are set to conform with CF version 1.9 conventions, i.e.
        False for 'standard', 'gregorian', and 'julian', True
        for 'proleptic_gregorian' (ISO 8601), and True for the idealized
        calendars 'noleap'/'365_day', '360_day', 366_day'/'all_leap'.
        Excel calendars *excel*, *excel1900*, *excel1904* start only 1900
        or above so *has_year_zero* is always False.
        Decimal calendars *decimal*, *decimal360*, *decimal365*, *decimal366*
        have always year 0, i.e. *has_year_zero* is True.
    format : str, optional
        If format string is given than a string representation of the
        datetime objects will be returned.
    return_arrays : bool, optional
        If True, then return a tuple with individual arrays for
        year, month, day, hour, minute, second, microsecond

    Returns
    -------
    array_like
       datetime instances or string representations of datetime objects, or
       tuple with individual arrays for year, month, day, hour, minute,
       second, microsecond

    Examples
    --------
    >>> idates = ['2000-01-05 12:30:15', '1810-04-24 16:15:10',
    ...           '1630-07-15 10:20:40', '1510-09-20 14:35:50',
    ...           '1271-03-18 19:41:34', '0619-08-27 11:08:37',
    ...           '0001-01-01 12:00:00']
    >>> decimal = date2num(idates, calendar='decimal')
    >>> num2date(decimal, calendar='decimal', format='%Y-%m-%d %H:%M:%S')
    ['2000-01-05 12:30:15',
     '1810-04-24 16:15:10',
     '1630-07-15 10:20:40',
     '1510-09-20 14:35:50',
     '1271-03-18 19:41:34',
     '0619-08-27 11:08:37',
     '0001-01-01 12:00:00']

    """
    if format and return_arrays:
        raise ValueError('Keywords format and return_arrays mutually'
                         ' exclusive')
    if calendar:
        calendar = calendar.lower()
    else:
        calendar = 'standard'
    # check if we can parse to cftime
    if calendar in _cfcalendars:
        iscf = True
    elif calendar in _noncfcalendars:
        iscf = False
    else:
        raise ValueError(f'Unknown calendar: {calendar}')
    if not units:
        units = _units_defaults(calendar)
    unit, sincestr, remainder = _datesplit(units)
    if sincestr == 'as':
        iscf = False
        calendar = ''

    mtimes = input2array(times, default=1)

    # use cftime.num2date if possible
    if iscf:
        if remainder.startswith('-'):
            # negative years
            only_use_python_datetimes = False
        else:
            if int(remainder.split('-')[0]) == 0:
                # reference year is year 0
                only_use_python_datetimes = False
                if has_year_zero is not None:
                    has_year_zero = True
        out = cf.num2date(
            mtimes, units, calendar=calendar,
            only_use_cftime_datetimes=only_use_cftime_datetimes,
            only_use_python_datetimes=only_use_python_datetimes,
            has_year_zero=has_year_zero)
        if only_use_pyjams_datetimes:
            out = [ datetime(*to_tuple(dt), calendar=calendar)
                    for dt in out ]

    # cdo absolute time format
    if sincestr == 'as':
        if units not in ['day as %Y%m%d.%f', 'month as %Y%m.%f',
                         'year as %Y.%f']:
            raise ValueError(f'Absolute date format unknown: {units}')
        # old algorithm does decomposition on all array elements
        # should try similar to decode_dates_from_array for speed
        # where decomposition is done for the first (oldest) element only
        # and then timedeltas are added subsequently
        year, month, day, hour, minute, second, microsecond = (
            _absolute2date(mtimes, units))

        # shortcut
        if return_arrays:
            year        = array2input(year, times)
            month       = array2input(month, times)
            day         = array2input(day, times)
            hour        = array2input(hour, times)
            minute      = array2input(minute, times)
            second      = array2input(second, times)
            microsecond = array2input(microsecond, times)
            return year, month, day, hour, minute, second, microsecond

        out = np.empty_like(year, dtype=object)
        if ( (not only_use_pyjams_datetimes) and
             (not only_use_cftime_datetimes) and
             only_use_python_datetimes and
             (year.min() > 0) ):
            for i in range(year.size):
                out[i] = cf.real_datetime(year[i], month[i], day[i],
                                          hour[i], minute[i], second[i],
                                          microsecond[i])
        elif ( (not only_use_pyjams_datetimes) and
               only_use_cftime_datetimes ):
            for i in range(year.size):
                out[i] = cf.datetime(year[i], month[i], day[i],
                                     hour[i], minute[i], second[i],
                                     microsecond[i])
        else:
            for i in range(year.size):
                out[i] = datetime(year[i], month[i], day[i],
                                  hour[i], minute[i], second[i],
                                  microsecond[i],
                                  calendar='decimal',
                                  has_year_zero=has_year_zero)

    # use cftime.num2date for Excel but return pyjams.datetime
    if calendar in _excelcalendars:
        cfcalendar = 'julian'
        cfunits = _units_defaults(calendar)
        cfdates = cf.num2date(
            mtimes, cfunits, calendar=cfcalendar,
            only_use_cftime_datetimes=only_use_cftime_datetimes,
            only_use_python_datetimes=False,
            has_year_zero=has_year_zero)

        # shortcut
        if format:
            # Assure 4 digit years on all platforms
            # see https://github.com/python/cpython/issues/76376
            iform = format
            if '%Y' in format:
                format04 = format.replace('%Y', '%04Y')
                try:
                    dttest = cfdates[0].strftime(format04)
                    if '4Y' in dttest:
                        iform = format
                    else:
                        iform = format04
                except ValueError:
                    iform = format
            out = [ dt.strftime(iform) for dt in cfdates ]
            out = array2input(out, times)
            return out

        out = [ datetime(*to_tuple(dt), calendar=calendar)
                for dt in cfdates ]

    # no cftime.num2date possible
    if calendar in _decimalcalendars:
        # old algorithm does decomposition on all array elements
        # should try similar to decode_dates_from_array for speed
        # where decomposition is done for the first (oldest) element only
        # and then timedeltas are added subsequently
        year, month, day, hour, minute, second, microsecond = (
            _decimal2date(mtimes, calendar))

        # shortcut
        if return_arrays:
            year        = array2input(year, times)
            month       = array2input(month, times)
            day         = array2input(day, times)
            hour        = array2input(hour, times)
            minute      = array2input(minute, times)
            second      = array2input(second, times)
            microsecond = array2input(microsecond, times)
            return year, month, day, hour, minute, second, microsecond

        out = np.empty_like(year, dtype=object)
        if ( (not only_use_pyjams_datetimes) and
             (not only_use_cftime_datetimes) and
             only_use_python_datetimes and (year.min() > 0) ):
            for i in range(year.size):
                out[i] = cf.real_datetime(year[i], month[i], day[i],
                                          hour[i], minute[i], second[i],
                                          microsecond[i])
        elif ( (not only_use_pyjams_datetimes) and
               only_use_cftime_datetimes ):
            for i in range(year.size):
                out[i] = cf.datetime(year[i], month[i], day[i],
                                     hour[i], minute[i], second[i],
                                     microsecond[i])
        else:
            for i in range(year.size):
                out[i] = datetime(year[i], month[i], day[i],
                                  hour[i], minute[i], second[i],
                                  microsecond[i],
                                  calendar=calendar,
                                  has_year_zero=has_year_zero)

    if return_arrays:
        out = np.array([ to_tuple(dt) for dt in out ])
        year        = array2input(out[:, 0], times)
        month       = array2input(out[:, 1], times)
        day         = array2input(out[:, 2], times)
        hour        = array2input(out[:, 3], times)
        minute      = array2input(out[:, 4], times)
        second      = array2input(out[:, 5], times)
        microsecond = array2input(out[:, 6], times)
        return year, month, day, hour, minute, second, microsecond
    else:
        if format:
            # Assure 4 digit years on all platforms
            # see https://github.com/python/cpython/issues/76376
            iform = format
            if '%Y' in format:
                years0 = [ dd.year < 0 for dd in out ]
                if any(years0):
                    y4 = '%05Y'
                else:
                    y4 = '%04Y'
                format04 = format.replace('%Y', y4)
                try:
                    dttest = out[0].strftime(format04)
                    if ('4Y' in dttest) or ('5Y' in dttest):
                        iform = format
                    else:
                        iform = format04
                except ValueError:
                    iform = format
            out = [ dt.strftime(iform) for dt in out ]

        out = array2input(out, times)
        return out


def dec2date(*args, **kwargs):
    """
    Wrapper for :func:`num2date`
    """
    return num2date(*args, **kwargs)


# Could not inherit from cf.datetime because all methods are read-only,
# so had to re-code all methods, even identical ones
class datetime(object):
    """
    This class mimics cftime.datetime but for non-CF-conform calendars

    The cftime.datetime class mimics itself datetime.datetime but
    supports calendars other than the proleptic Gregorian calendar.

    This class supports timedelta operations by overloading +/-, and
    comparisons with other instances using the same calendar.

    Current supported calendars are *excel*, *excel1900*, *excel1904*,
    and *decimal*, *decimal360*, *decimal365*, *decimal366*. Excel
    calendars are supposedly Julian calendars with other reference dates.
    Day 0 of *excel*/*excel1900* starts at 1899-12-31 00:00:00 and day 0
    of *excel1904* (old Lotus date) starts at 1903-12-31 00:00:00.
    Decimal calendars have the form "%Y.%f", where the fractional year
    assumes leap years as the proleptic Gregorian calendar, or fixed 360,
    365, or 366 days per year.

    If the has_year_zero keyword argument is set to True, astronomical year
    numbering is used and the year zero exists, which is the default for the
    decimal calendars. The keyword will be ignored for Excel calendars.

    The class has the methods isoformat, strftime, timetuple, replace,
    dayofwk, dayofyr, daysinmonth, __repr__, __format__, __add__, __sub__,
    __str__, and comparison methods.

    The default format of the string produced by strftime is controlled by
    self.format (default %Y-%m-%d %H:%M:%S).

    """
    # Python's datetime.datetime uses the proleptic Gregorian
    # calendar. This boolean is used to decide whether a
    # cftime.datetime instance can be converted to
    # datetime.datetime.
    def __init__(self, year, month, day,
                 hour=0, minute=0, second=0, microsecond=0,
                 dayofwk=-1, dayofyr=-1,
                 calendar='decimal', has_year_zero=None):
        """
        Initialise new datetime instance

        """
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        self._dayofwk = dayofwk
        self._dayofyr = dayofyr
        self.tzinfo = None
        self.cf = None
        if calendar:
            self.calendar = calendar.lower()
        else:
            self.calendar = 'decimal'
        # if self.calendar in _cfcalendars:
        #     raise ValueError(f'Use cftime.datetime for CF-conform'
        #                      f' calendars: {self.calendar}')
        if has_year_zero is None:
            self.has_year_zero = _year_zero_defaults(self.calendar)
        else:
            self.has_year_zero = has_year_zero
        # if self.calendar and (self.calendar not in _noncfcalendars):
        #     raise ValueError(f'Unknown calendar: {self.calendar}')
        if ( self.calendar and (self.calendar not in _cfcalendars) and
             (self.calendar not in _noncfcalendars) ):
            raise ValueError(f'Unknown calendar: {self.calendar}')
        if self.calendar in _cfcalendars:
            self.cf = cf.datetime(self.year, self.month, self.day,
                                  self.hour, self.minute, self.second,
                                  self.microsecond,
                                  calendar=self.calendar,
                                  has_year_zero=self.has_year_zero)
            self.datetime_compatible = self.cf.datetime_compatible
        elif self.calendar in _excelcalendars:
            self.cf = cf.datetime(self.year, self.month, self.day,
                                  self.hour, self.minute, self.second,
                                  self.microsecond,
                                  calendar='julian',
                                  has_year_zero=self.has_year_zero)
            self.datetime_compatible = self.cf.datetime_compatible
        else:
            self.datetime_compatible = False
        self.assert_valid_date()

    def assert_valid_date(self):
        """
        Check that datetime is a valid date for given calendar

        """
        # year
        if not self.has_year_zero:
            if self.year == 0:
                raise ValueError("Invalid year provided in {0!r}".format(self))
        # Comment next block to allow negative days with Excel calendars,
        # which does not exist in Excel
        # if ( ((self.calendar == 'excel') or (self.calendar == 'excel1900'))
        #      and self.year < 1900):
        #     raise ValueError('Year must be >= 1900 for Excel dates')
        # if ( (self.calendar == 'excel1904') and self.year < 1904):
        #     raise ValueError('Year must be >= 1904 for Excel1904 dates')

        # month
        if (self.month < 1) or (self.month > 12):
            raise ValueError("Invalid month provided in {0!r}".format(self))

        # day
        month_length = _month_lengths(self.year, self.calendar,
                                      self.has_year_zero)
        if (self.day < 1) or (self.day > month_length[self.month - 1]):
            raise ValueError(
                "Invalid day number provided in {0!r}".format(self))

        # hour
        if (self.hour < 0) or (self.hour > 23):
            raise ValueError("Invalid hour provided in {0!r}".format(self))

        # minute
        if (self.minute < 0) or (self.minute > 59):
            raise ValueError("Invalid minute provided in {0!r}".format(self))

        # second
        if (self.second < 0) or (self.second > 59):
            raise ValueError("Invalid second provided in {0!r}".format(self))

        # microsecond
        if (self.microsecond) < 0 or (self.microsecond > 999999):
            raise ValueError(
                "Invalid microsecond provided in {0!r}".format(self))

    def change_calendar(self, calendar, has_year_zero=None):
        return NotImplemented

    def dayofwk(self):
        """
        Day of the week

        Identical to cftime.datetime

        """
        if (self._dayofwk < 0) and self.calendar:
            ord0 = 0
            if self.calendar == 'decimal':
                ord0 = 1721425
            jd = self.toordinal() + ord0
            dayofwk = (jd + 1) % 7
            # convert to ISO 8601 (0 = Monday, 6 = Sunday), like python
            # datetime
            dayofwk -= 1
            if dayofwk == -1:
                dayofwk = 6
            # cache results for dayofwk
            self._dayofwk = dayofwk
            return dayofwk
        else:
            return self._dayofwk

    def dayofyr(self):
        """
        Day of year

        """
        if (self._dayofyr < 0) and self.calendar:
            if self.calendar == 'decimal360':
                # dayofyr = (self.month - 1) * 30 + self.day
                dayofyr = _cumdayspermonth_360[self.month - 1] + self.day
            else:
                if _is_leap(self.year, self.calendar,
                            has_year_zero=self.has_year_zero):
                    dayofyr = _cumdayspermonth_leap[self.month - 1] + self.day
                else:
                    dayofyr = _cumdayspermonth[self.month - 1] + self.day
            # cache results for dayofyr
            self._dayofyr = dayofyr
            return dayofyr
        else:
            return self._dayofyr

    def daysinmonth(self):
        """
        Number of days in current month

        """
        if self.calendar == 'decimal360':
            # return 30
            return _dayspermonth_360[self.month - 1]
        else:
            if _is_leap(self.year, self.calendar,
                        has_year_zero=self.has_year_zero):
                return _dayspermonth_leap[self.month - 1]
            else:
                return _dayspermonth[self.month - 1]

    def format(self):
        """
        Standard date representation

        Identical to cftime.datetime

        """
        return '%Y-%m-%d %H:%M:%S'

    def fromordinal(jday, calendar='decimal', has_year_zero=None):
        return NotImplemented

    def isoformat(self, sep='T', timespec='auto'):
        """
        ISO date representation

        """
        if self.year < 0:
            form0 = '{:05d}-{:02d}-{:02d}'
        else:
            form0 = '{:04d}-{:02d}-{:02d}'
        if timespec == 'days':
            form = form0
            return form.format(self.year, self.month, self.day)
        elif timespec == 'hours':
            form = form0 + '{:s}{:02d}'
            return form.format(self.year, self.month, self.day, sep,
                               self.hour)
        elif timespec == 'minutes':
            form = form0 + '{:s}{:02d}:{:02d}'
            return form.format(self.year, self.month, self.day, sep,
                               self.hour, self.minute)
        elif timespec == 'seconds':
            form = form0 + '{:s}{:02d}:{:02d}:{:02d}'
            return form.format(self.year, self.month, self.day, sep,
                               self.hour, self.minute, self.second)
        elif timespec in ['auto', 'microseconds', 'milliseconds']:
            second = '{:02d}'.format(self.second)
            if timespec == 'milliseconds':
                millisecs = int(round(self.microsecond / 1000, 0))
                second += '.{:03d}'.format(millisecs)
            elif timespec == 'microseconds':
                second += '.{:06d}'.format(self.microsecond)
            else:
                if self.microsecond > 0:
                    second += '.{:06d}'.format(self.microsecond)
            form = form0 + '{:s}{:02d}:{:02d}:{:s}'
            return form.format(self.year, self.month, self.day, sep,
                               self.hour, self.minute, second)
        else:
            raise ValueError('illegal timespec')

    def replace(self, **kwargs):
        """
        Return datetime with new specified fields

        Identical to cftime.datetime

        """
        args = {"year": self.year,
                "month": self.month,
                "day": self.day,
                "hour": self.hour,
                "minute": self.minute,
                "second": self.second,
                "microsecond": self.microsecond,
                "has_year_zero": self.has_year_zero,
                "calendar": self.calendar}

        if 'dayofyr' in kwargs or 'dayofwk' in kwargs:
            raise ValueError('Replacing the dayofyr or dayofwk of a datetime'
                             ' is not supported.')

        if 'calendar' in kwargs:
            raise ValueError('Replacing the calendar of a datetime is '
                             'not supported.')

        # if attempting to set year to zero, also set has_year_zero=True
        # (issue #248)
        if 'year' in kwargs:
            if (kwargs['year'] == 0) and ('has_year_zero' not in kwargs):
                kwargs['has_year_zero'] = True

        for name, value in kwargs.items():
            args[name] = value

        return self.__class__(**args)

    def round_microseconds(self):
        """
        Mathematically round microseconds to nearest second.

        """
        iadd = round(self.microsecond / 1000000.)
        if iadd:
            other = timedelta(seconds=1)
            odt = self.__add__(other)
        else:
            odt = self
        odt.microsecond = 0
        return odt

    def strftime(self, format=None):
        """
        Return a string representing the date, controlled by an explicit format
        string

        For a complete list of formatting directives, see section 'strftime()
        and strptime() Behavior' in the base Python documentation.

        Identical to cftime.datetime

        """
        if format is None:
            format = self.format()
        return _strftime(self, format)

    def timetuple(self):
        """
        Return a time.struct_time such as returned by time.localtime()

        The DST flag is -1. d.timetuple() is equivalent to
        time.struct_time((d.year, d.month, d.day, d.hour, d.minute,
        d.second, d.weekday(), yday, dst)), where yday is the
        day number within the current year starting with 1 for January 1st.

        Identical to cftime.datetime

        """
        return ptime.struct_time((self.year, self.month, self.day, self.hour,
                                  self.minute, self.second, self.dayofwk(),
                                  self.dayofyr(), -1))

    def toordinal(self, fractional=False):
        """
        Julian day (integer) ordinal

        Day 0 starts at noon January 1 of the year -4713 for the
        Excel calendars.

        Day 0 starts at noon on January 1 of the year zero for
        the decimal calendars.

        If fractional=True, fractional part of day is included (default
        False).

        """
        ijd = _int_julian_day_from_date(
            self.year, self.month, self.day, self.calendar,
            has_year_zero=self.has_year_zero)
        if fractional:
            # At this point ijd is an integer representing noon UTC on the
            # given year, month, day.
            # Compute fractional day from hour, minute, second, microsecond
            fracday = ( self.hour / np.array(24., np.longdouble) +
                        self.minute / np.array(1440., np.longdouble) +
                        (self.second +
                         self.microsecond / (np.array(1.e6, np.longdouble))) /
                        np.array(86400., np.longdouble) )
            return ijd - 0.5 + fracday
        else:
            return ijd

    def to_tuple(self):
        """
        Turn a datetime instance into a tuple of integers. Elements go
        in the order of decreasing significance, making it easy to compare
        datetime instances. Parts of the state that don't affect ordering
        are omitted.
        to_tuple(dt) is identical to (dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second, dt.microsecond).
        Compare to timetuple().

        Identical to cftime.datetime

        """
        return (self.year, self.month, self.day, self.hour, self.minute,
                self.second, self.microsecond)

    def _add_timedelta(self, other):
        return self.__add__(other)

    def _getstate(self):
        """
        return args and kwargs needed to create class instance

        Identical to cftime.datetime

        """
        args = (self.year, self.month, self.day)
        kwargs = {'hour': self.hour,
                  'minute': self.minute,
                  'second': self.second,
                  'microsecond': self.microsecond,
                  'dayofwk': self._dayofwk,
                  'dayofyr': self._dayofyr,
                  'calendar': self.calendar,
                  'has_year_zero': self.has_year_zero}
        return args, kwargs

    def _to_real_datetime(self):
        """
        Extended Python datetime class

        Extra attributes are  dayofwk, dayofyr, and daysinmonth.

        Identical to cftime.datetime

        """
        return cf.real_datetime(self.year, self.month, self.day,
                                self.hour, self.minute, self.second,
                                self.microsecond)

    def __add__(self, other):
        """
        Add timedelta to datetime

        """
        if isinstance(self, datetime) and isinstance(other, timedelta):
            dt = self
            calendar = self.calendar
            # has_year_zero = self.has_year_zero
            delta = other
        elif isinstance(self, timedelta) and isinstance(other, datetime):
            dt = other
            calendar = other.calendar
            # has_year_zero = other.has_year_zero
            delta = self
        else:
            return NotImplemented
        # dt = self
        # calendar = self.calendar
        # has_year_zero = self.has_year_zero
        # delta = other
        if calendar == 'decimal360':
            cfdt = cf.datetime(*to_tuple(dt), calendar='360_day',
                               has_year_zero=dt.has_year_zero)
            cfdt = cfdt + delta
            year, month, day, hour, minute, second, microsecond = (
                cfdt.year, cfdt.month, cfdt.day, cfdt.hour, cfdt.minute,
                cfdt.second, cfdt.microsecond)
        else:
            year, month, day, hour, minute, second, microsecond = (
                _add_timedelta(dt, delta))
        return datetime(year, month, day,
                        hour, minute, second, microsecond,
                        calendar=dt.calendar, has_year_zero=dt.has_year_zero)

    def __eq__(self, other):
        """
        Compare two datetime instances

        """
        dt = self
        if isinstance(other, (datetime, cf.datetime)):
            dt_other = other
            # comparing two datetime instances
            if ( (dt.calendar == dt_other.calendar) and
                 (dt.has_year_zero == dt_other.has_year_zero) ):
                return to_tuple(dt) == to_tuple(dt_other)
            else:
                ord1 = 0
                if dt.calendar == 'decimal':
                    ord1 = 1721425
                ord2 = 0
                if dt_other.calendar == 'decimal':  # pragma: no cover
                    ord2 = 1721425
                return (dt.toordinal(fractional=True) + ord1 ==
                        dt_other.toordinal(fractional=True) + ord2)
        else:
            return NotImplemented

    def __format__(self, format):
        """
        Return a string representing the date, controlled by an explicit format
        string

        For a complete list of formatting directives, see section 'strftime()
        and strptime() Behavior' in the base Python documentation.

        Identical to cftime.datetime

        """
        # the string format "{t_obj}".format(t_obj=t_obj)
        # without an explicit format gives an empty string (format='')
        # so set this to None to get the default strftime behaviour
        if not format:
            format = None
        return self.strftime(format)

    def __hash__(self):
        """
        Identical to cftime.datetime

        """
        try:
            d = self._to_real_datetime()
        except ValueError:
            return hash(self.timetuple())
        return hash(d)

    def __reduce__(self):
        """
        Special method that allows instance to be pickled

        Identical to cftime.datetime

        """
        args, kwargs = self._getstate()
        date_type = type(self)
        return (_create_datetime, (date_type, args, kwargs))

    def __repr__(self):
        """
        String representation

        """
        return ("{0}.{1}({2}, {3}, {4}, {5}, {6}, {7}, {8},"
                " calendar={9}, has_year_zero={10})".format(
                    'pyjams',
                    self.__class__.__name__,
                    self.year, self.month, self.day,
                    self.hour, self.minute, self.second,
                    self.microsecond, self.calendar, self.has_year_zero))

    def __str__(self):
        """
        ISO date representation

        Identical to cftime.datetime

        """
        return self.isoformat(' ')

    def __sub__(self, other):
        """
        Substract timedelta or datetime from the datetime instance

        """
        if isinstance(self, datetime):  # left arg is a datetime instance
            dt = self
            if isinstance(other, datetime):
                # datetime - datetime
                if dt.calendar != other.calendar:
                    raise TypeError("Cannot compute the time difference"
                                    " between dates with different calendars")
                if dt.calendar == "":
                    raise TypeError("Cannot compute the time difference"
                                    " between dates that are not"
                                    " calendar-aware")
                if dt.has_year_zero != other.has_year_zero:
                    raise TypeError("Cannot compute the time difference"
                                    " between dates with different year zero"
                                    " conventions")
                ord1 = 0
                if self.calendar == 'decimal':
                    ord1 = 1721425
                ord2 = 0
                if other.calendar == 'decimal':
                    ord2 = 1721425
                ordinal_self = self.toordinal() + ord1  # julian day
                ordinal_other = other.toordinal() + ord2
                days = ordinal_self - ordinal_other
                seconds_self = dt.second + 60 * dt.minute + 3600 * dt.hour
                seconds_other = (other.second + 60 * other.minute +
                                 3600 * other.hour)
                seconds = seconds_self - seconds_other
                microseconds = dt.microsecond - other.microsecond
                return timedelta(days, seconds, microseconds)
            elif (isinstance(other, datetime_python) or
                  isinstance(other, cf.real_datetime)):
                # datetime - real_datetime
                if not dt.datetime_compatible:
                    msg = ("Cannot compute the time difference between dates"
                           " with different calendars. One of the datetime"
                           " objects may have been converted to a native"
                           " python datetime instance. Try using"
                           " only_use_cftime_datetimes=True when creating the"
                           " datetime object.")
                    raise TypeError(msg)
                return dt._to_real_datetime() - other
            elif isinstance(other, timedelta):
                # datetime - timedelta
                if dt.calendar == 'decimal360':
                    cfdt = cf.datetime(*to_tuple(dt), calendar='360_day',
                                       has_year_zero=dt.has_year_zero)
                    cfdt = cfdt - other
                    year, month, day, hour, minute, second, microsecond = (
                        cfdt.year, cfdt.month, cfdt.day, cfdt.hour,
                        cfdt.minute, cfdt.second, cfdt.microsecond)
                else:
                    year, month, day, hour, minute, second, microsecond = (
                        _add_timedelta(dt, -other))
                return datetime(year, month, day,
                                hour, minute, second, microsecond,
                                calendar=dt.calendar,
                                has_year_zero=dt.has_year_zero)
            else:
                return NotImplemented
        else:
            if ( isinstance(self, datetime_python) or
                 isinstance(self, cf.real_datetime) ):
                # real_datetime - datetime
                if not other.datetime_compatible:
                    msg = ("Cannot compute the time difference between dates"
                           " with different calendars. One of the datetime"
                           " objects may have been converted to a native"
                           " python datetime instance. Try using"
                           " only_use_cftime_datetimes=True when creating the"
                           " datetime object.")
                    raise TypeError(msg)
                return self - other._to_real_datetime()
            else:
                return NotImplemented
