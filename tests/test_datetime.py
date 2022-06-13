#!/usr/bin/env python
"""
This is the unittest for datetime module.

python -m unittest -v tests/test_datetime.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_datetime.py

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
    Tests for datetime.py
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
        self.idates = ['2000-01-05 12:30:15', '1810-04-24 16:15:10',
                       '1630-07-15 10:20:40', '1510-09-20 14:35:50',
                       '1271-03-18 19:41:34', '0619-08-27 11:08:37',
                       '0001-01-01 12:00:00']
        self.iformat = '%Y-%m-%d %H:%M:%S'

    def test_date2num2date(self):
        import random
        import numpy as np
        from pyjams import date2date
        from pyjams import date2num, num2date, date2dec, dec2date

        # Back and forth for _noncfcalendars

        # precision problem for some calendars of _cfcalendars, i.e.
        #     'noleap', 'all_leap', '365_day', '366_day', '360_day'
        calendars = self._noncfcalendars
        units = ['', 'day as %Y%m%d.%f', 'month as %Y%m.%f', 'year as %Y.%f']
        formats = ['%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M:%S',
                   '%d/%m/%Y %H:%M:%S',
                   '%Y-%m-%dT%H:%M:%S', '%d.%m.%YT%H:%M:%S',
                   '%d/%m/%YT%H:%M:%S',
                   '%Y%m%d%H%M%S']
        only_cftimes = [True, False]
        only_pythons = [True, False]
        has_year_zeros = [None, True, False]
        itypes = [list, tuple, np.array]
        ttypes = [list, tuple, np.ndarray]
        f2dates = [num2date, dec2date]
        f2nums  = [date2num, date2dec]
        for calendar in calendars:
            for unit in units:
                for format in formats:
                    for only_cftime in only_cftimes:
                        for only_python in only_pythons:
                            for has_year_zero in has_year_zeros:
                                for itype in range(len(itypes)):
                                    # print(calendar, unit, format,
                                    #       only_cftime, only_python,
                                    #       has_year_zero, itypes[itype])
                                    indates = itypes[itype](self.idates)
                                    jdates = date2date(indates, format=format)
                                    f2num = f2nums[random.randint(0, 1)]
                                    idec = f2num(
                                        jdates, units=unit, calendar=calendar,
                                        has_year_zero=has_year_zero,
                                        format=format)
                                    f2date = f2dates[random.randint(0, 1)]
                                    odates = f2date(
                                        idec, units=unit, calendar=calendar,
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
        only_cftimes = [True, False]
        only_pythons = [False]  # [True, False]
        has_year_zeros = [None, True, False]
        itypes = [list, tuple, np.array]
        ttypes = [list, tuple, np.ndarray]
        f2dates = [num2date, dec2date]
        f2nums  = [date2num, date2dec]
        for calendar in calendars:
            for unit in units:
                for format in formats:
                    for only_cftime in only_cftimes:
                        for only_python in only_pythons:
                            for has_year_zero in has_year_zeros:
                                for itype in range(len(itypes)):
                                    # print(calendar, unit, format,
                                    #       only_cftime, only_python,
                                    #       has_year_zero, itypes[itype])
                                    indates = itypes[itype](self.idates)
                                    jdates = date2date(indates, format=format)
                                    f2num = f2nums[random.randint(0, 1)]
                                    idec = f2num(
                                        jdates, units=unit, calendar=calendar,
                                        has_year_zero=has_year_zero,
                                        format=format)
                                    f2date = f2dates[random.randint(0, 1)]
                                    odates = f2date(
                                        idec, units=unit, calendar=calendar,
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

    def test_datetime(self):
        from datetime import timedelta
        import numpy as np
        import cftime as cf
        from pyjams import date2date
        from pyjams import datetime
        from pyjams import date2num, num2date
        from pyjams.datetime import _month_lengths, _year_zero_defaults

        # Test methods of datetime class

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
                self.month  = [1, 4, 7, 9, 3, 8, 1]
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
                ist  = [ dt.isoformat(' ') for dt in idt ]
                soll = self.idates
                self.assertEqual(_flatten(ist), _flatten(soll))
                ist  = [ dt.isoformat(' ', 'hours') for dt in idt ]
                soll = [ dd[:-6] for dd in self.idates ]
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
                self.assertEqual(_flatten(ist), _flatten(soll))

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
                # odt = [ timedelta(days=1, hours=-2, minutes=3, seconds=4) + dt
                #         for dt in idt ]
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
                odt = [ dt.__add__(
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

                # __cmp__, __richcmp__
                odt = [ dt + timedelta(0) for dt in idt ]
                for i in range(len(idt)):
                    # assert idt[i] == odt[i]
                    assert idt[i].__cmp__(odt[i])
                    assert idt[i].__richcmp__(odt[i])
                for i in range(len(idt)):
                    # assert idt[i] == cdt[i]
                    assert idt[i].__cmp__(cdt[i])
                    assert idt[i].__richcmp__(odt[i])

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


        # edate = ['2014-11-12 12:00', '01.03.2015T17:56:00',
        #          '12/01/1990', '04.05.1786']

        # # errors
        # # wrong date delimiter
        # edate = ['2014\11\12 12:00', '01.03.2015 17:56:00',
        #          '1990-12-01 01', '04.05.1786']
        # self.assertRaises(ValueError, date2date, edate)
        # # milliseconds
        # edate = ['2014-11-12 12:00', '01.03.2015 17:56:00:00',
        #          '1990-12-01 01', '04.05.1786']
        # self.assertRaises(ValueError, date2date, edate)
        # # 3-digit year
        # edate = ['1-11-12 12:00', '1.3.15 17:56:00', '190-12-1']
        # self.assertRaises(ValueError, date2date, edate)


if __name__ == "__main__":
    unittest.main()
