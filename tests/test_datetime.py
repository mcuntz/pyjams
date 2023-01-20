#!/usr/bin/env python
"""
This is the unittest for the datetime module.

python -m unittest -v tests/test_datetime.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_datetime.py

115: def _create_datetime used in __reduce__
239: _year_zero_defaults(calendar) cal in idealized calendars
301: _is_leap, np.any(myear == 0) and (not has_year_zero)
387: _int_julian_day_from_date, has_year_zero is None
422:: _int_julian_day_from_date, unknown calendar
470-474: _add_timedelta, if month < 1:
494: _add_timedelta, delta > 0, year = 1
556: _units_defaults, calendar in ['standard', 'gregorian', 'julian']
                      and has_year_zero:
563: _units_defaults, calendar in ['proleptic_gregorian'] and not has_year_zero
565: _units_defaults, calendar in _idealized_cfcalendars
573: _units_defaults, unknown calendar
729: _date2absolute, Unknown absolute units
830: _decimal2date, Unknown decimal calendar
989: _absolute2date, Unknown absolute units
1147-1149: date2num, real datetime input
1390: num2date, linux %04Y
1451: num2date, linux %04Y
1593: datetime.change_calendar, NotImplemented
1665: datetime.fromordinal, NotImplemented
1700: datetime.isoformat, if self.microsecond > 0:
1736: datetime.replace, 'year' in kwargs and kwargs['year'] == 0 and
                        'has_year_zero' not in kwargs
1864-1870: datetime.__add__, timedelta + datetime
1811: datetime.__eq__, not isinstance(other, (datetime, cf.datetime))
1936-1940: datetime.__hash__
1949-1951: datetime.__reduce__
1992: datetime.__sub__, dt.calendar != other.calendar
1995: datetime.__sub__, dt.calendar == ""
1999: datetime.__sub__, dt.has_year_zero != other.has_year_zero
2020-2028: datetime.__sub__, if not dt.datetime_compatible
2046-2061: datetime.__sub__, something - datetime

"""
import unittest


def _flatten(itr):
    import numpy as np
    fitr = np.array(itr).flatten()
    if len(fitr) == 0:
        return list(fitr)
    else:
        if isinstance(fitr[0], str):
            return [ i for i in fitr ]
        else:
            return [ i if np.isfinite(i) else np.finfo(float).max
                     for i in fitr ]


class TestDatetime(unittest.TestCase):
    """
    Tests for class_datetime.py
    """
    def setUp(self):
        self._excelcalendars = ['excel', 'excel1900', 'excel1904']
        self._decimalcalendars = ['decimal', 'decimal360', 'decimal365',
                                  'decimal366']
        self._noncfcalendars = self._excelcalendars + self._decimalcalendars
        self._cfcalendars = ['standard', 'gregorian', 'proleptic_gregorian',
                             'noleap', 'julian', 'all_leap', '365_day',
                             '366_day', '360_day']
        self._dayspermonth      = [31, 28, 31, 30, 31, 30,
                                   31, 31, 30, 31, 30, 31]
        self._dayspermonth_leap = [31, 29, 31, 30, 31, 30,
                                   31, 31, 30, 31, 30, 31]
        self._dayspermonth_360  = [30, 30, 30, 30, 30, 30,
                                   30, 30, 30, 30, 30, 30]

        self.year   = [2000, 1810, 1630, 1510, 1271, 619, 1]
        self.month  = [1, 4, 7, 9, 3, 8, 1]
        self.day    = [5, 24, 15, 20, 18, 27, 1]
        self.hour   = [12, 16, 10, 14, 19, 11, 12]
        self.minute = [30, 15, 20, 35, 41, 8, 0]
        self.second = [15, 10, 40, 50, 34, 37, 0]
        self.microsecond = [150, 1000, 49999, 500001, 999999, 1, 0]
        self.idates = ['2000-01-05 12:30:15', '1810-04-24 16:15:10',
                       '1630-07-15 10:20:40', '1510-09-20 14:35:50',
                       '1271-03-18 19:41:34', '0619-08-27 11:08:37',
                       '0001-01-01 12:00:00']
        self.iformat = '%Y-%m-%d %H:%M:%S'

        # self.year   = [1271]
        # self.month  = [3]
        # self.day    = [18]
        # self.hour   = [19]
        # self.minute = [41]
        # self.second = [34]
        # self.microsecond = [999999]
        # self.idates = ['1271-03-18 19:41:34']
        # self.iformat = '%Y-%m-%d %H:%M:%S'

        self.year0   = [0, -1, -10, -100, -1000, 1]
        self.month0  = [1, 4, 7, 9, 3, 8]
        self.day0    = [5, 24, 15, 20, 18, 27]
        self.hour0   = [12, 16, 10, 14, 19, 11]
        self.minute0 = [30, 15, 20, 35, 41, 8]
        self.second0 = [15, 10, 40, 50, 34, 37]
        self.microsecond0 = [150, 1000, 49999, 500001, 999999, 1, 0]
        self.idates0 = ['0000-01-05 12:30:15', '-0001-04-24 16:15:10',
                        '-0010-07-15 10:20:40', '-0100-09-20 14:35:50',
                        '-1000-03-18 19:41:34', '0001-08-27 11:08:37']

    def test_date2num2date(self):
        import random
        import numpy as np
        from pyjams import date2date
        from pyjams import date2num, num2date, date2dec, dec2date
        import cftime as cf
        import datetime as dt
        from pyjams import datetime

        # Back and forth for _noncfcalendars

        # precision problem for some calendars of _cfcalendars, i.e.
        #     'noleap', 'all_leap', '365_day', '366_day', '360_day'
        calendars = self._noncfcalendars
        # calendars = self._cfcalendars
        units = ['', 'day as %Y%m%d.%f', 'month as %Y%m.%f', 'year as %Y.%f']
        formats = ['%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M:%S',
                   '%d/%m/%Y %H:%M:%S',
                   '%Y-%m-%dT%H:%M:%S', '%d.%m.%YT%H:%M:%S',
                   '%d/%m/%YT%H:%M:%S',
                   '%Y%m%d%H%M%S']
        only_pyjamss = [True, False]
        only_cftimes = [True, False]
        only_pythons = [True, False]
        has_year_zeros = [None, True, False]
        itypes = [list, tuple, np.array]
        ttypes = [list, tuple, np.ndarray]
        f2dates = [num2date, dec2date]
        f2nums = [date2num, date2dec]
        for calendar in calendars:
            for unit in units:
                for format in formats:
                    for only_pyjams in only_pyjamss:
                        for only_cftime in only_cftimes:
                            for only_python in only_pythons:
                                for has_year_zero in has_year_zeros:
                                    for itype in range(len(itypes)):
                                        # print(calendar, unit, format,
                                        #       only_cftime, only_python,
                                        #       has_year_zero, itypes[itype])
                                        indates = itypes[itype](self.idates)
                                        jdates = date2date(indates,
                                                           format=format)
                                        ihave0 = has_year_zero
                                        if ( has_year_zero and
                                             (calendar in self._excelcalendars) ):
                                            ihave0 = False
                                        f2num = f2nums[random.randint(0, 1)]
                                        idec = f2num(
                                            jdates, units=unit,
                                            calendar=calendar,
                                            has_year_zero=ihave0,
                                            format=format)
                                        f2date = f2dates[random.randint(0, 1)]
                                        odates = f2date(
                                            idec, units=unit, calendar=calendar,
                                            only_use_pyjams_datetimes=only_pyjams,
                                            only_use_cftime_datetimes=only_cftime,
                                            only_use_python_datetimes=only_python,
                                            has_year_zero=ihave0,
                                            format=self.iformat,
                                            return_arrays=False)
                                        assert isinstance(jdates, ttypes[itype])
                                        assert isinstance(idec, ttypes[itype])
                                        assert isinstance(odates, ttypes[itype])
                                        self.assertEqual(_flatten(odates),
                                                         _flatten(indates))

        # Back and forth for _cfcalendars

        # precision problem for some calendars of _cfcalendars, i.e.
        #     'noleap', 'all_leap', '365_day', '366_day', '360_day'
        # calendars = _cfcalendars
        calendars = ['standard', 'gregorian', 'proleptic_gregorian', 'julian']
        units = ['']
        formats = ['%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M:%S',
                   '%d/%m/%Y %H:%M:%S',
                   '%Y-%m-%dT%H:%M:%S', '%d.%m.%YT%H:%M:%S',
                   '%d/%m/%YT%H:%M:%S',
                   '%Y%m%d%H%M%S']
        only_pyjamss = [True, False]
        only_cftimes = [True, False]
        only_pythons = [False]  # [True, False]
        has_year_zeros = [None, True, False]
        itypes = [list, tuple, np.array]
        ttypes = [list, tuple, np.ndarray]
        f2dates = [num2date, dec2date]
        f2nums = [date2num, date2dec]
        for calendar in calendars:
            for unit in units:
                for format in formats:
                    for only_pyjams in only_pyjamss:
                        for only_cftime in only_cftimes:
                            for only_python in only_pythons:
                                for has_year_zero in has_year_zeros:
                                    for itype in range(len(itypes)):
                                        # print(calendar, unit, format,
                                        #       only_cftime, only_python,
                                        #       has_year_zero, itypes[itype])
                                        if calendar in ['',
                                                        'gregorian',
                                                        'standard']:
                                            indates = itypes[itype](
                                                self.idates[:3])
                                        else:
                                            indates = itypes[itype](self.idates)
                                        jdates = date2date(indates,
                                                           format=format)
                                        f2num = f2nums[random.randint(0, 1)]
                                        idec = f2num(
                                            jdates, units=unit,
                                            calendar=calendar,
                                            has_year_zero=has_year_zero,
                                            format=format)
                                        f2date = f2dates[random.randint(0, 1)]
                                        odates = f2date(
                                            idec, units=unit, calendar=calendar,
                                            only_use_pyjams_datetimes=only_pyjams,
                                            only_use_cftime_datetimes=only_cftime,
                                            only_use_python_datetimes=only_python,
                                            has_year_zero=has_year_zero,
                                            format=self.iformat,
                                            return_arrays=False)
                                        assert isinstance(jdates, ttypes[itype])
                                        assert isinstance(idec, ttypes[itype])
                                        assert isinstance(odates, ttypes[itype])
                                        self.assertEqual(_flatten(odates),
                                                         _flatten(indates))

        # Back and forth for calendar == ''

        calendar = ''
        units = ['', 'day as %Y%m%d.%f', 'month as %Y%m.%f', 'year as %Y.%f',
                 'days since 1900-01-01 00:00:00']
        format = ''
        itypes = [list, tuple, np.array]
        ttypes = [list, tuple, np.ndarray]
        f2dates = [num2date, dec2date]
        f2nums  = [date2num, date2dec]
        for unit in units:
            for itype in range(len(itypes)):
                # print(unit, itypes[itype])
                indates = itypes[itype](self.idates)
                jdates = date2date(indates, format=format)
                f2num = f2nums[random.randint(0, 1)]
                idec = f2num(
                    jdates, units=unit, calendar=calendar,
                    format=format)
                f2date = f2dates[random.randint(0, 1)]
                odates = f2date(
                    idec, units=unit, calendar=calendar,
                    format=self.iformat,
                    return_arrays=False)
                assert isinstance(jdates, ttypes[itype])
                assert isinstance(idec, ttypes[itype])
                assert isinstance(odates, ttypes[itype])
                self.assertEqual(_flatten(odates),
                                 _flatten(indates))

        # Back and forth for calendar == '' and single date

        calendar = ''
        units = ['', 'day as %Y%m%d.%f', 'month as %Y%m.%f', 'year as %Y.%f',
                 'days since 1900-01-01 00:00:00']
        itypes = [list, tuple, np.array]
        ttypes = [list, tuple, np.ndarray]
        f2dates = [num2date, dec2date]
        f2nums = [date2num, date2dec]
        for unit in units:
            for itype in range(len(itypes)):
                # print(unit, itypes[itype])
                indates = itypes[itype]([self.idates[0]])
                jdates = date2date(indates)
                f2num = f2nums[random.randint(0, 1)]
                idec = f2num(jdates, units=unit, calendar=calendar)
                f2date = f2dates[random.randint(0, 1)]
                odates = f2date(
                    idec, units=unit, calendar=calendar,
                    format=self.iformat,
                    return_arrays=False)
                assert isinstance(jdates, ttypes[itype])
                assert isinstance(idec, ttypes[itype])
                assert isinstance(odates, ttypes[itype])
                self.assertEqual(_flatten(odates),
                                 _flatten(indates))

        # Back and forth for calendar == '' and scalar date

        calendar = ''
        units = ['', 'day as %Y%m%d.%f', 'month as %Y%m.%f', 'year as %Y.%f',
                 'days since 1900-01-01 00:00:00']
        f2dates = [num2date, dec2date]
        f2nums = [date2num, date2dec]
        for unit in units:
            # print(unit)
            indates = self.idates[0]
            jdates = date2date(indates)
            f2num = f2nums[random.randint(0, 1)]
            idec = f2num(jdates, units=unit, calendar=calendar)
            f2date = f2dates[random.randint(0, 1)]
            odates = f2date(
                idec, units=unit, calendar=calendar,
                format=self.iformat,
                return_arrays=False)
            self.assertEqual(odates, indates)

        # Back and forth with microseconds

        calendar = 'decimal'
        units = ['', 'day as %Y%m%d.%f', 'month as %Y%m.%f', 'year as %Y.%f',
                 'days since 1900-01-01 00:00:00']
        units = ['month as %Y%m.%f']
        itypes = [list, tuple, np.array]
        ttypes = [list, tuple, np.ndarray]
        f2dates = [num2date, dec2date]
        f2nums = [date2num, date2dec]
        iform = self.iformat + '.%f'
        for unit in units:
            for itype in range(len(itypes)):
                # print(unit, itypes[itype])
                indates = itypes[itype](self.idates)
                jdates = date2date(indates, format='en')
                jdates = itypes[itype]([
                    jdates[i] + '.{:06d}'.format(self.microsecond[i])
                    for i in range(len(jdates)) ])
                f2num = f2nums[random.randint(0, 1)]
                idec = f2num(jdates, units=unit, calendar=calendar,
                             format=iform)
                f2date = f2dates[random.randint(0, 1)]
                odates = f2date(
                    idec, units=unit, calendar=calendar,
                    format=iform,
                    return_arrays=False)
                assert isinstance(jdates, ttypes[itype])
                assert isinstance(idec, ttypes[itype])
                assert isinstance(odates, ttypes[itype])
                self.assertEqual(_flatten(odates),
                                 _flatten(jdates))

        # given calendar takes precedence on calendar of datetime objects

        calendar = self._excelcalendars + self._decimalcalendars
        cdates = [ cf.datetime(self.year[i], self.month[i], self.day[i],
                               self.hour[i], self.minute[i], self.second[i],
                               calendar='julian')
                   for i in range(len(self.year)) ]
        ddates = [ datetime(self.year[i], self.month[i], self.day[i],
                            self.hour[i], self.minute[i], self.second[i],
                            calendar='decimal')
                   for i in range(len(self.year)) ]
        rdates = [ dt.datetime(self.year[i], self.month[i], self.day[i],
                            self.hour[i], self.minute[i], self.second[i])
                   for i in range(len(self.year)) ]
        for ical in calendar:
            # print(ical)
            indates = date2num(self.idates, format=self.iformat, calendar=ical)
            odates = date2num(cdates, calendar=ical)
            self.assertEqual(odates, indates)
            odates = date2num(ddates, calendar=ical)
            self.assertEqual(odates, indates)
            odates = date2num(rdates, calendar=ical)
            self.assertEqual(odates, indates)

        # return_arrays

        calendar = self._excelcalendars + self._decimalcalendars
        cdates = [ cf.datetime(self.year[i], self.month[i], self.day[i],
                               self.hour[i], self.minute[i], self.second[i],
                               calendar='julian')
                   for i in range(len(self.year)) ]
        ddates = [ datetime(self.year[i], self.month[i], self.day[i],
                            self.hour[i], self.minute[i], self.second[i],
                            calendar='decimal')
                   for i in range(len(self.year)) ]
        rdates = [ dt.datetime(self.year[i], self.month[i], self.day[i],
                            self.hour[i], self.minute[i], self.second[i])
                   for i in range(len(self.year)) ]
        for ical in calendar:
            # print(ical)
            inyr, inmo, indy, inhr, inmi, insc, inms = (
                date2num(self.idates, format=self.iformat, calendar=ical,
                         return_arrays=True))
            oyr, omo, ody, ohr, omi, osc, oms = (
                date2num(cdates, calendar=ical, return_arrays=True))
            self.assertEqual(oyr, inyr)
            self.assertEqual(omo, inmo)
            self.assertEqual(ody, indy)
            self.assertEqual(ohr, inhr)
            self.assertEqual(omi, inmi)
            self.assertEqual(osc, insc)
            self.assertEqual(oms, inms)
            oyr, omo, ody, ohr, omi, osc, oms = (
                date2num(ddates, calendar=ical, return_arrays=True))
            self.assertEqual(oyr, inyr)
            self.assertEqual(omo, inmo)
            self.assertEqual(ody, indy)
            self.assertEqual(ohr, inhr)
            self.assertEqual(omi, inmi)
            self.assertEqual(osc, insc)
            self.assertEqual(oms, inms)
            oyr, omo, ody, ohr, omi, osc, oms = (
                date2num(rdates, calendar=ical, return_arrays=True))
            self.assertEqual(oyr, inyr)
            self.assertEqual(omo, inmo)
            self.assertEqual(ody, indy)
            self.assertEqual(ohr, inhr)
            self.assertEqual(omi, inmi)
            self.assertEqual(osc, insc)
            self.assertEqual(oms, inms)

        # errors

        edate = '2014-11-12 12:00:00'
        enum = 2451914.
        # unknown calendar
        self.assertRaises(ValueError, date2num, edate, calendar='test')
        self.assertRaises(ValueError, date2dec, edate, calendar='test')
        self.assertRaises(ValueError, num2date, enum, calendar='test')
        self.assertRaises(ValueError, dec2date, enum, calendar='test')
        # unknown absolute date format
        self.assertRaises(ValueError, date2num, edate,
                          units='day as %Y%m%d')
        self.assertRaises(ValueError, date2dec, edate,
                          units='day as %Y%m%d')
        self.assertRaises(ValueError, num2date, enum,
                          units='day as %Y%m%d')
        self.assertRaises(ValueError, dec2date, enum,
                          units='day as %Y%m%d')
        # incorrectly formatted date-time unit_string
        self.assertRaises(ValueError, date2num, edate,
                          units='dayssince 1990-01-01')
        # no 'since' or 'as' in unit_string
        self.assertRaises(ValueError, date2num, edate,
                          units='days from 1990-01-01')
        # year zero out of range
        self.assertRaises(ValueError, date2num, self.idates0,
                          calendar='decimal', has_year_zero=False)
        # format and return_arrays
        self.assertRaises(ValueError, num2date, enum,
                          format='%Y-%m-%d', return_arrays=True)

    def test_datetime(self):
        from datetime import timedelta
        import numpy as np
        import cftime as cf
        from pyjams import date2date
        from pyjams import datetime
        from pyjams import date2num, num2date
        from pyjams.class_datetime import _month_lengths, _year_zero_defaults
        from numpy.testing import assert_almost_equal

        # Test methods of datetime class, years > 0

        calendars = self._noncfcalendars
        has_year_zeros = [None, True, False]
        cfequivalents = ['julian', 'julian', 'julian',
                         'proleptic_gregorian', '360_day',
                         '365_day', '366_day']
        cfcalendars = dict(zip(self._noncfcalendars, cfequivalents))
        for calendar in calendars:
            for has_year_zero in has_year_zeros:
                # print(calendar, has_year_zero)
                ihave0 = has_year_zero
                if calendar in self._excelcalendars:
                    ihave0 = False
                idt = [ datetime(self.year[i], self.month[i], self.day[i],
                                 self.hour[i], self.minute[i],
                                 self.second[i], calendar=calendar,
                                 has_year_zero=ihave0)
                        for i in range(len(self.year)) ]
                idtms = [ datetime(self.year[i], self.month[i], self.day[i],
                                   self.hour[i], self.minute[i],
                                   self.second[i], self.microsecond[i],
                                   calendar=calendar,
                                   has_year_zero=ihave0)
                          for i in range(len(self.year)) ]

                # change_calendar - NotImplemented

                # use cftime as reference
                cdt = [ cf.datetime(*dt.to_tuple(),
                                    calendar=cfcalendars[calendar],
                                    has_year_zero=ihave0)
                        for dt in idt ]

                # dayofwk, dayofyr
                ist  = [ dt.dayofyr() for dt in idt ]
                soll = [ dt.dayofyr for dt in cdt ]
                soll = [ dt._dayofyr for dt in cdt ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                ist  = [ dt.dayofwk() for dt in idt ]
                soll = [ dt.dayofwk for dt in cdt ]
                soll = [ dt._dayofwk for dt in cdt ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                # daysinmonth, _month_length
                ist  = [ dt.daysinmonth() for dt in idt ]
                mlen = [ _month_lengths(yy, calendar,
                                        has_year_zero=ihave0)
                         for yy in self.year ]
                soll = [ mlen[mm][self.month[mm]-1]
                         for mm in range(len(self.month)) ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                # format
                for dt in idt:
                    assert dt.format() == self.iformat

                # fromordinal - NotImplemented

                # isoformat
                ist  = [ dt.isoformat() for dt in idt ]
                soll = [ dd.replace(' ', 'T') for dd in self.idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat('T') for dt in idt ]
                soll = [ dd.replace(' ', 'T') for dd in self.idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ') for dt in idt ]
                soll = self.idates
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'days') for dt in idt ]
                soll = [ dd.split()[0] for dd in self.idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'hours') for dt in idt ]
                soll = [ dd[:-6] for dd in self.idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'minutes') for dt in idt ]
                soll = [ dd[:-3] for dd in self.idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'seconds') for dt in idt ]
                soll = self.idates
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'milliseconds') for dt in idt ]
                soll = [ dd+'.000' for dd in self.idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'microseconds') for dt in idt ]
                soll = [ dd+'.000000' for dd in self.idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                # replace
                # invert dates
                odt = list()
                for i in range(len(self.year)):
                    kwarg = {
                        'year': self.year[-(i+1)],
                        'month': self.month[-(i+1)],
                        'day': self.day[-(i+1)],
                        'hour': self.hour[-(i+1)],
                        'minute': self.minute[-(i+1)],
                        'second': self.second[-(i+1)],
                        'has_year_zero': False
                    }
                    odt.append(idt[i].replace(**kwarg))
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oyear   = iarrays[:, 0]
                omonth  = iarrays[:, 1]
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                self.assertEqual(_flatten(oyear), _flatten(self.year[::-1]))
                self.assertEqual(_flatten(omonth), _flatten(self.month[::-1]))
                self.assertEqual(_flatten(oday), _flatten(self.day[::-1]))
                self.assertEqual(_flatten(ohour), _flatten(self.hour[::-1]))
                self.assertEqual(_flatten(ominute),
                                 _flatten(self.minute[::-1]))
                self.assertEqual(_flatten(osecond),
                                 _flatten(self.second[::-1]))
                ist = [ dt.has_year_zero for dt in odt ]
                soll = [ False for dt in odt ]
                self.assertEqual(ist, soll)

                # round_microseconds
                ist = [ dt.round_microseconds() for dt in idtms ]
                ist = [ dt.second for dt in ist ]
                soll = [ dt.second + 1 if dt.microsecond > 500000
                         else dt.second for dt in idtms ]
                self.assertEqual(ist, soll)

                # strftime
                # using self.format
                ist = [ dt.strftime() for dt in idt ]
                soll = self.idates
                self.assertEqual(ist, soll)
                # other format
                oform = '%d.%m.%Y %H:%M:%S'
                ist = [ dt.strftime(oform) for dt in idt ]
                soll = date2date(self.idates, format='')
                self.assertEqual(ist, soll)

                # timetuple
                ist  = np.array([ dt.timetuple() for dt in idt ])
                soll = np.array([ dt.timetuple() for dt in cdt ])
                self.assertEqual(_flatten(ist), _flatten(soll))

                # toordinal
                # w/o fractional
                ord0 = 0
                if calendar == 'decimal':
                    ord0 = 1721425
                ist  = [ dt.toordinal() + ord0 for dt in idt ]
                soll = [ dt.toordinal() for dt in cdt ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                # with fractional
                ord0 = 0
                if calendar == 'decimal':
                    ord0 = 1721425
                ist  = [ dt.toordinal(fractional=True) + ord0 for dt in idt ]
                soll = [ dt.toordinal(fractional=True) for dt in cdt ]
                # self.assertEqual(_flatten(ist), _flatten(soll))
                assert_almost_equal(_flatten(ist), _flatten(soll))

                # # to_tuple
                # ist  = np.array([ dt.to_tuple() for dt in idt ])
                # soll = np.array([ dt.to_tuple() for dt in cdt ])
                # self.assertEqual(_flatten(ist), _flatten(soll))

                # to_tuple
                iarrays = np.array([ dt.to_tuple() for dt in idt ])
                oyear   = iarrays[:, 0]
                omonth  = iarrays[:, 1]
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                self.assertEqual(_flatten(oyear), _flatten(self.year))
                self.assertEqual(_flatten(omonth), _flatten(self.month))
                self.assertEqual(_flatten(oday), _flatten(self.day))
                self.assertEqual(_flatten(ohour), _flatten(self.hour))
                self.assertEqual(_flatten(ominute), _flatten(self.minute))
                self.assertEqual(_flatten(osecond), _flatten(self.second))
                # using return_arrays
                idec = date2num(idt, units='', calendar=calendar,
                                has_year_zero=ihave0)
                oyear, omonth, oday, ohour, ominute, osecond, omsecond = (
                    num2date(idec, units='', calendar=calendar,
                             has_year_zero=ihave0,
                             return_arrays=True))
                self.assertEqual(_flatten(oyear), _flatten(self.year))
                self.assertEqual(_flatten(omonth), _flatten(self.month))
                self.assertEqual(_flatten(oday), _flatten(self.day))
                self.assertEqual(_flatten(ohour), _flatten(self.hour))
                self.assertEqual(_flatten(ominute), _flatten(self.minute))
                self.assertEqual(_flatten(osecond), _flatten(self.second))

                # _add_timedelta - with __add__

                # _getstate
                odt = []
                for dt in idt:
                    arg, kwarg = dt._getstate()
                    odt.append(datetime(*arg, **kwarg))
                ist  = np.array([ dt.to_tuple() for dt in idt ])
                soll = np.array([ dt.to_tuple() for dt in odt ])
                self.assertEqual(_flatten(ist), _flatten(soll))

                # _to_real_datetime
                ist  = np.array([ dt.timetuple() for dt in idt ])
                # delete weekday because different calendar
                # and doy because of idealised calendars
                ist = np.delete(ist, (6, 7), axis=1)
                odt = [ dt._to_real_datetime() for dt in idt ]
                soll = np.array([ dt.timetuple() for dt in odt ])
                soll = np.delete(soll, (6, 7), axis=1)
                self.assertEqual(_flatten(ist), _flatten(soll))

                # __add__
                # datetime + timedelta
                odt = [ dt + timedelta(days=1, hours=-2, minutes=3, seconds=4)
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                soll = [ dd + 1 for dd in self.day ]
                self.assertEqual(_flatten(oday), _flatten(soll))
                soll = [ dd - 2 for dd in self.hour ]
                self.assertEqual(_flatten(ohour), _flatten(soll))
                soll = [ dd + 3 for dd in self.minute ]
                self.assertEqual(_flatten(ominute), _flatten(soll))
                soll = [ dd + 4 for dd in self.second ]
                self.assertEqual(_flatten(osecond), _flatten(soll))
                # # timedelta + datetime
                # odt = [ timedelta(days=1, hours=-2, minutes=3, seconds=4) +
                #         dt for dt in idt ]
                # iarrays = np.array([ dt.to_tuple() for dt in odt ])
                # oday    = iarrays[:, 2]
                # ohour   = iarrays[:, 3]
                # ominute = iarrays[:, 4]
                # osecond = iarrays[:, 5]
                # soll = [ dd + 1 for dd in self.day ]
                # self.assertEqual(_flatten(oday), _flatten(soll))
                # soll = [ dd - 2 for dd in self.hour ]
                # self.assertEqual(_flatten(ohour), _flatten(soll))
                # soll = [ dd + 3 for dd in self.minute ]
                # self.assertEqual(_flatten(ominute), _flatten(soll))
                # soll = [ dd + 4 for dd in self.second ]
                # self.assertEqual(_flatten(osecond), _flatten(soll))
                # __add__
                odt = [ dt.__add__(timedelta(days=1, hours=-2, minutes=3,
                                             seconds=4))
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                soll = [ dd + 1 for dd in self.day ]
                self.assertEqual(_flatten(oday), _flatten(soll))
                soll = [ dd - 2 for dd in self.hour ]
                self.assertEqual(_flatten(ohour), _flatten(soll))
                soll = [ dd + 3 for dd in self.minute ]
                self.assertEqual(_flatten(ominute), _flatten(soll))
                soll = [ dd + 4 for dd in self.second ]
                self.assertEqual(_flatten(osecond), _flatten(soll))
                # _add_timedelta
                odt = [ dt._add_timedelta(
                    timedelta(days=1, hours=-2, minutes=3, seconds=4))
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                soll = [ dd + 1 for dd in self.day ]
                self.assertEqual(_flatten(oday), _flatten(soll))
                soll = [ dd - 2 for dd in self.hour ]
                self.assertEqual(_flatten(ohour), _flatten(soll))
                soll = [ dd + 3 for dd in self.minute ]
                self.assertEqual(_flatten(ominute), _flatten(soll))
                soll = [ dd + 4 for dd in self.second ]
                self.assertEqual(_flatten(osecond), _flatten(soll))
                # days < 0, month - 1, year - 1
                odt = [ dt + timedelta(days=-30, hours=0, minutes=1, seconds=4)
                        for dt in idt[1:-1] ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                omonth  = iarrays[:, 1]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                soll = [ dd - 1 for dd in self.month[1:-1] ]
                self.assertEqual(_flatten(omonth), _flatten(soll))
                soll = [ dd + 1 for dd in self.minute[1:-1] ]
                self.assertEqual(_flatten(ominute), _flatten(soll))
                soll = [ dd + 4 for dd in self.second[1:-1] ]
                self.assertEqual(_flatten(osecond), _flatten(soll))
                # days > 0, month + 1
                odt = [ dt + timedelta(days=31, hours=0, minutes=1, seconds=4)
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                omonth  = iarrays[:, 1]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                soll = [ dd + 1 for dd in self.month ]
                self.assertEqual(_flatten(omonth), _flatten(soll))
                soll = [ dd + 1 for dd in self.minute ]
                self.assertEqual(_flatten(ominute), _flatten(soll))
                soll = [ dd + 4 for dd in self.second ]
                self.assertEqual(_flatten(osecond), _flatten(soll))
                # days > 0, year + 1
                odt = [ dt + timedelta(days=121, hours=0, minutes=1, seconds=4)
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                omonth  = iarrays[:, 1]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                soll = [ dd + 4 if dd < 9 else 1 for dd in self.month ]
                self.assertEqual(_flatten(omonth), _flatten(soll))
                soll = [ dd + 1 for dd in self.minute ]
                self.assertEqual(_flatten(ominute), _flatten(soll))
                soll = [ dd + 4 for dd in self.second ]
                self.assertEqual(_flatten(osecond), _flatten(soll))

                # __eq__
                odt = [ dt + timedelta(0) for dt in idt ]
                for i in range(len(idt)):
                    assert idt[i] == odt[i]

                # __format__
                # using self.format
                ist = [ dt.__format__('') for dt in idt ]
                soll = self.idates
                self.assertEqual(ist, soll)
                # other format
                oform = '%d.%m.%Y %H:%M:%S'
                ist = [ dt.__format__(oform) for dt in idt ]
                soll = date2date(self.idates, format='')
                self.assertEqual(ist, soll)

                # __hash__, __reduce__ ???

                # __repr__
                ihave = ihave0
                if has_year_zero is None:
                    ihave = _year_zero_defaults(calendar)
                for i, dt in enumerate(idt):
                    ist = dt.__repr__()
                    soll = (f'pyjams.datetime({self.year[i]},'
                            f' {self.month[i]}, {self.day[i]},'
                            f' {self.hour[i]}, {self.minute[i]},'
                            f' {self.second[i]}, 0,'
                            f' calendar={calendar},'
                            f' has_year_zero={ihave})')
                    assert ist == soll

                # __str__
                ist  = [ dt.__str__() for dt in idt ]
                soll = self.idates
                self.assertEqual(_flatten(ist), _flatten(soll))

                # __sub__
                # datetime + timedelta
                odt = [ dt - timedelta(days=-1, hours=2)
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                soll = [ dd + 1 for dd in self.day ]
                self.assertEqual(_flatten(oday), _flatten(soll))
                soll = [ dd - 2 for dd in self.hour ]
                self.assertEqual(_flatten(ohour), _flatten(soll))
                # datetime + timedelta
                dd  = timedelta(days=1, hours=-2, minutes=3, seconds=4)
                ddt = [ dt + dd for dt in idt ]
                odt = [ ddt[i] - idt[i] for i in range(len(idt)) ]
                for dt in odt:
                    assert dt == dd
                odt = [ idt[i] - ddt[i] for i in range(len(idt)) ]
                for dt in odt:
                    assert dt == -dd

        # Test methods of datetime class, years <= 0

        calendars = self._decimalcalendars
        has_year_zeros = [None, True, False]
        cfequivalents = ['proleptic_gregorian', '360_day',
                         '365_day', '366_day']
        cfcalendars = dict(zip(self._decimalcalendars, cfequivalents))
        for calendar in calendars:
            for has_year_zero in has_year_zeros:
                # print(calendar, has_year_zero)
                ihave0 = has_year_zero
                if cfcalendars[calendar] == 'proleptic_gregorian':
                    ihave0 = False
                if ihave0 or (ihave0 is None):
                    iyear   = self.year0.copy()
                    imonth  = self.month0.copy()
                    iday    = self.day0.copy()
                    ihour   = self.hour0.copy()
                    iminute = self.minute0.copy()
                    isecond = self.second0.copy()
                    imicrosecond = self.microsecond0.copy()
                    idates  = self.idates0.copy()
                else:
                    iyear   = self.year0[1:]
                    imonth  = self.month0[1:]
                    iday    = self.day0[1:]
                    ihour   = self.hour0[1:]
                    iminute = self.minute0[1:]
                    isecond = self.second0[1:]
                    imicrosecond = self.microsecond0[1:]
                    idates  = self.idates0[1:]
                idt = [ datetime(iyear[i], imonth[i], iday[i],
                                 ihour[i], iminute[i],
                                 isecond[i], calendar=calendar,
                                 has_year_zero=ihave0)
                        for i in range(len(iyear)) ]
                idtms = [ datetime(iyear[i], imonth[i], iday[i],
                                   ihour[i], iminute[i],
                                   isecond[i], imicrosecond[i],
                                   calendar=calendar,
                                   has_year_zero=ihave0)
                         for i in range(len(iyear)) ]

                # change_calendar - NotImplemented

                # use cftime as reference
                cdt = [ cf.datetime(*dt.to_tuple(),
                                    calendar=cfcalendars[calendar],
                                    has_year_zero=ihave0)
                        for dt in idt ]

                # dayofwk, dayofyr
                ist  = [ dt.dayofyr() for dt in idt ]
                soll = [ dt.dayofyr for dt in cdt ]
                soll = [ dt._dayofyr for dt in cdt ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                ist  = [ dt.dayofwk() for dt in idt ]
                soll = [ dt.dayofwk for dt in cdt ]
                soll = [ dt._dayofwk for dt in cdt ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                # daysinmonth, _month_length
                ist  = [ dt.daysinmonth() for dt in idt ]
                mlen = [ _month_lengths(yy, calendar,
                                        has_year_zero=ihave0)
                         for yy in iyear ]
                soll = [ mlen[mm][imonth[mm]-1]
                         for mm in range(len(imonth)) ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                # format
                for dt in idt:
                    assert dt.format() == self.iformat

                # fromordinal - NotImplemented

                # isoformat
                ist  = [ dt.isoformat() for dt in idt ]
                soll = [ dd.replace(' ', 'T') for dd in idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat('T') for dt in idt ]
                soll = [ dd.replace(' ', 'T') for dd in idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ') for dt in idt ]
                soll = idates
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'hours') for dt in idt ]
                soll = [ dd[:-6] for dd in idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'minutes') for dt in idt ]
                soll = [ dd[:-3] for dd in idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'seconds') for dt in idt ]
                soll = idates
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'milliseconds') for dt in idt ]
                soll = [ dd+'.000' for dd in idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'microseconds') for dt in idt ]
                soll = [ dd+'.000000' for dd in idates ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                # replace
                # invert dates
                odt = list()
                for i in range(len(iyear)):
                    if ihave0 or (ihave0 is None):
                        ihave = False
                    kwarg = {
                        'year': np.clip(iyear[-(i+1)], -9999, -1),
                        'month': imonth[-(i+1)],
                        'day': iday[-(i+1)],
                        'hour': ihour[-(i+1)],
                        'minute': iminute[-(i+1)],
                        'second': isecond[-(i+1)],
                        'has_year_zero': False
                    }
                    odt.append(idt[i].replace(**kwarg))
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oyear   = iarrays[:, 0]
                omonth  = iarrays[:, 1]
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                self.assertEqual(_flatten(oyear),
                                 _flatten(np.clip(iyear[::-1], -9999, -1)))
                self.assertEqual(_flatten(omonth), _flatten(imonth[::-1]))
                self.assertEqual(_flatten(oday), _flatten(iday[::-1]))
                self.assertEqual(_flatten(ohour), _flatten(ihour[::-1]))
                self.assertEqual(_flatten(ominute),
                                 _flatten(iminute[::-1]))
                self.assertEqual(_flatten(osecond),
                                 _flatten(isecond[::-1]))
                ist = [ dt.has_year_zero for dt in odt ]
                soll = [ False for dt in odt ]
                self.assertEqual(ist, soll)

                # round_microseconds
                ist = [ dt.round_microseconds() for dt in idtms ]
                ist = [ dt.second for dt in ist ]
                soll = [ dt.second + 1 if dt.microsecond > 500000
                         else dt.second for dt in idtms ]
                self.assertEqual(ist, soll)

                # strftime
                # using self.format
                ist = [ dt.strftime() for dt in idt ]
                soll = idates
                self.assertEqual(ist, soll)
                # other format
                oform = '%d.%m.%Y %H:%M:%S'
                ist = [ dt.strftime(oform) for dt in idt ]
                soll = date2date(idates, format='')
                self.assertEqual(ist, soll)

                # timetuple
                ist  = np.array([ dt.timetuple() for dt in idt ])
                soll = np.array([ dt.timetuple() for dt in cdt ])
                self.assertEqual(_flatten(ist), _flatten(soll))

                # toordinal
                # w/o fractional
                ord0 = 0
                if calendar == 'decimal':
                    ord0 = 1721425
                ist  = [ dt.toordinal() + ord0 for dt in idt ]
                soll = [ dt.toordinal() for dt in cdt ]
                self.assertEqual(_flatten(ist), _flatten(soll))

                # with fractional
                ord0 = 0
                if calendar == 'decimal':
                    ord0 = 1721425
                ist  = [ dt.toordinal(fractional=True) + ord0 for dt in idt ]
                soll = [ dt.toordinal(fractional=True) for dt in cdt ]
                # self.assertEqual(_flatten(ist), _flatten(soll))
                assert_almost_equal(_flatten(ist), _flatten(soll))

                # # to_tuple
                # ist  = np.array([ dt.to_tuple() for dt in idt ])
                # soll = np.array([ dt.to_tuple() for dt in cdt ])
                # self.assertEqual(_flatten(ist), _flatten(soll))

                # to_tuple
                iarrays = np.array([ dt.to_tuple() for dt in idt ])
                oyear   = iarrays[:, 0]
                omonth  = iarrays[:, 1]
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                self.assertEqual(_flatten(oyear), _flatten(iyear))
                self.assertEqual(_flatten(omonth), _flatten(imonth))
                self.assertEqual(_flatten(oday), _flatten(iday))
                self.assertEqual(_flatten(ohour), _flatten(ihour))
                self.assertEqual(_flatten(ominute), _flatten(iminute))
                self.assertEqual(_flatten(osecond), _flatten(isecond))
                # using return_arrays
                idec = date2num(idt, units='', calendar=calendar,
                                has_year_zero=ihave0)
                oyear, omonth, oday, ohour, ominute, osecond, omsecond = (
                    num2date(idec, units='', calendar=calendar,
                             has_year_zero=ihave0,
                             return_arrays=True))
                self.assertEqual(_flatten(oyear), _flatten(iyear))
                self.assertEqual(_flatten(omonth), _flatten(imonth))
                self.assertEqual(_flatten(oday), _flatten(iday))
                self.assertEqual(_flatten(ohour), _flatten(ihour))
                self.assertEqual(_flatten(ominute), _flatten(iminute))
                self.assertEqual(_flatten(osecond), _flatten(isecond))
                # using return_arrays with absolute days
                idec = date2num(idt, units='day as %Y%m%d.%f',
                                calendar=calendar, has_year_zero=ihave0)
                oyear, omonth, oday, ohour, ominute, osecond, omsecond = (
                    num2date(idec, units='day as %Y%m%d.%f', calendar=calendar,
                             has_year_zero=ihave0,
                             return_arrays=True))
                self.assertEqual(_flatten(oyear), _flatten(iyear))
                self.assertEqual(_flatten(omonth), _flatten(imonth))
                self.assertEqual(_flatten(oday), _flatten(iday))
                self.assertEqual(_flatten(ohour), _flatten(ihour))
                self.assertEqual(_flatten(ominute), _flatten(iminute))
                self.assertEqual(_flatten(osecond), _flatten(isecond))

                # _add_timedelta - with __add__

                # _getstate
                odt = []
                for dt in idt:
                    arg, kwarg = dt._getstate()
                    odt.append(datetime(*arg, **kwarg))
                ist  = np.array([ dt.to_tuple() for dt in idt ])
                soll = np.array([ dt.to_tuple() for dt in odt ])
                self.assertEqual(_flatten(ist), _flatten(soll))

                # _to_real_datetime -> no year < 0

                # __add__
                # datetime + timedelta
                odt = [ dt + timedelta(days=1, hours=-2, minutes=3, seconds=4)
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                soll = [ dd + 1 for dd in iday ]
                self.assertEqual(_flatten(oday), _flatten(soll))
                soll = [ dd - 2 for dd in ihour ]
                self.assertEqual(_flatten(ohour), _flatten(soll))
                soll = [ dd + 3 for dd in iminute ]
                self.assertEqual(_flatten(ominute), _flatten(soll))
                soll = [ dd + 4 for dd in isecond ]
                self.assertEqual(_flatten(osecond), _flatten(soll))
                # # timedelta + datetime
                # odt = [ timedelta(days=1, hours=-2, minutes=3, seconds=4) +
                #         dt for dt in idt ]
                # iarrays = np.array([ dt.to_tuple() for dt in odt ])
                # oday    = iarrays[:, 2]
                # ohour   = iarrays[:, 3]
                # ominute = iarrays[:, 4]
                # osecond = iarrays[:, 5]
                # soll = [ dd + 1 for dd in iday ]
                # self.assertEqual(_flatten(oday), _flatten(soll))
                # soll = [ dd - 2 for dd in ihour ]
                # self.assertEqual(_flatten(ohour), _flatten(soll))
                # soll = [ dd + 3 for dd in iminute ]
                # self.assertEqual(_flatten(ominute), _flatten(soll))
                # soll = [ dd + 4 for dd in isecond ]
                # self.assertEqual(_flatten(osecond), _flatten(soll))
                # __add__
                odt = [ dt.__add__(timedelta(days=1, hours=-2, minutes=3,
                                             seconds=4))
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                soll = [ dd + 1 for dd in iday ]
                self.assertEqual(_flatten(oday), _flatten(soll))
                soll = [ dd - 2 for dd in ihour ]
                self.assertEqual(_flatten(ohour), _flatten(soll))
                soll = [ dd + 3 for dd in iminute ]
                self.assertEqual(_flatten(ominute), _flatten(soll))
                soll = [ dd + 4 for dd in isecond ]
                self.assertEqual(_flatten(osecond), _flatten(soll))
                # _add_timedelta
                odt = [ dt._add_timedelta(timedelta(days=1, hours=-2,
                                                    minutes=3, seconds=4))
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                ominute = iarrays[:, 4]
                osecond = iarrays[:, 5]
                soll = [ dd + 1 for dd in iday ]
                self.assertEqual(_flatten(oday), _flatten(soll))
                soll = [ dd - 2 for dd in ihour ]
                self.assertEqual(_flatten(ohour), _flatten(soll))
                soll = [ dd + 3 for dd in iminute ]
                self.assertEqual(_flatten(ominute), _flatten(soll))
                soll = [ dd + 4 for dd in isecond ]
                self.assertEqual(_flatten(osecond), _flatten(soll))

                # __eq__
                odt = [ dt + timedelta(0) for dt in idt ]
                for i in range(len(idt)):
                    assert idt[i] == odt[i]

                # __format__
                # using self.format
                ist = [ dt.__format__('') for dt in idt ]
                soll = idates
                self.assertEqual(ist, soll)
                # other format
                oform = '%d.%m.%Y %H:%M:%S'
                ist = [ dt.__format__(oform) for dt in idt ]
                soll = date2date(idates, format='')
                self.assertEqual(ist, soll)

                # __hash__, __reduce__ ???

                # __repr__
                ihave = ihave0
                if ihave is None:
                    ihave = _year_zero_defaults(calendar)
                for i, dt in enumerate(idt):
                    ist = dt.__repr__()
                    soll = (f'pyjams.datetime({iyear[i]},'
                            f' {imonth[i]}, {iday[i]},'
                            f' {ihour[i]}, {iminute[i]},'
                            f' {isecond[i]}, 0,'
                            f' calendar={calendar},'
                            f' has_year_zero={ihave})')
                    assert ist == soll

                # __str__
                ist  = [ dt.__str__() for dt in idt ]
                soll = idates
                self.assertEqual(_flatten(ist), _flatten(soll))

                # __sub__
                # datetime + timedelta
                odt = [ dt - timedelta(days=-1, hours=2)
                        for dt in idt ]
                iarrays = np.array([ dt.to_tuple() for dt in odt ])
                oday    = iarrays[:, 2]
                ohour   = iarrays[:, 3]
                soll = [ dd + 1 for dd in iday ]
                self.assertEqual(_flatten(oday), _flatten(soll))
                soll = [ dd - 2 for dd in ihour ]
                self.assertEqual(_flatten(ohour), _flatten(soll))
                # datetime + timedelta
                dd  = timedelta(days=1, hours=-2, minutes=3, seconds=4)
                ddt = [ dt + dd for dt in idt ]
                odt = [ ddt[i] - idt[i] for i in range(len(idt)) ]
                for dt in odt:
                    assert dt == dd
                odt = [ idt[i] - ddt[i] for i in range(len(idt)) ]
                for dt in odt:
                    assert dt == -dd

        # no calendar given
        odt = [ datetime(self.year[i], self.month[i], self.day[i],
                         self.hour[i], self.minute[i],
                         self.second[i])
                for i in range(len(self.year)) ]
        for dt in odt:
            assert dt.calendar == 'decimal'

        # issue #187 of cftime: roundtrip near second boundary
        dt1 = datetime(1810, 4, 24, 16, 15, 10)
        units = 'days since -4713-01-01 12:00'
        dt2 = num2date(date2num(dt1, units, calendar='decimal'),
                       units, calendar='decimal')
        assert dt1 == dt2

        # errors

        # # calendar of cftime
        # self.assertRaises(ValueError, datetime, 1900, 1, 1,
        #                   calendar='standard')
        # unknown calendar
        self.assertRaises(ValueError, datetime, 1900, 1, 1, calendar='test')
        # assert_valid_date
        self.assertRaises(ValueError, datetime, 0, 1, 1, 1, 1, 1, 1,
                          has_year_zero=False)
        self.assertRaises(ValueError, datetime, 1900, 13, 1, 1, 1, 1, 1)
        self.assertRaises(ValueError, datetime, 1900, 1, 32, 1, 1, 1, 1)
        self.assertRaises(ValueError, datetime, 1900, 1, 1, 24, 1, 1, 1)
        self.assertRaises(ValueError, datetime, 1900, 1, 1, 1, 61, 1, 1)
        self.assertRaises(ValueError, datetime, 1900, 1, 1, 1, 1, 61, 1)
        self.assertRaises(ValueError, datetime, 1900, 1, 1, 1, 1, 1, -1)
        # illegal isoformat
        dt = datetime(1990, 1, 1)
        self.assertRaises(ValueError, dt.isoformat, timespec='test')
        # replace dayofyr, dayofwk, calendar
        dt = datetime(1990, 1, 1)
        self.assertRaises(ValueError, dt.replace, dayofyr=2)
        self.assertRaises(ValueError, dt.replace, dayofwk=2)
        self.assertRaises(ValueError, dt.replace, calendar='excel')
        # %s in format
        self.assertRaises(TypeError, dt.strftime, "%Y-%m-%d.%s")
        # %f not at end of format
        self.assertRaises(TypeError, dt.strftime, "%Y-%m-%d.%f %H")


if __name__ == "__main__":
    unittest.main()
