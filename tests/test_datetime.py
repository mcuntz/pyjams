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

    def test_date2num2date(self):
        import random
        import numpy as np
        from pyjams import date2date
        from pyjams import date2num, num2date, date2dec, dec2date

        _excelcalendars = ['excel', 'excel1900', 'excel1904']
        _decimalcalendars = ['decimal', 'decimal360', 'decimal365', 'decimal366']
        _noncfcalendars = _excelcalendars + _decimalcalendars
        _cfcalendars = ['standard', 'gregorian', 'proleptic_gregorian',
                        'noleap', 'julian', 'all_leap', '365_day', '366_day',
                        '360_day']
        _idealized_cfcalendars = ['all_leap', 'noleap', '366_day', '365_day',
                                  '360_day']

        idates = ['2000-01-05 12:30:15', '1810-04-24 16:15:10',
                  '1630-07-15 10:20:40', '1510-09-20 14:35:50',
                  '1271-03-18 19:41:34', '0619-08-27 11:08:37',
                  '0001-01-01 12:00:00']
        iformat = '%Y-%m-%d %H:%M:%S'

        # Back and forth for _noncfcalendars

        # precision problem for some calendars of _cfcalendars, i.e.
        #     'noleap', 'all_leap', '365_day', '366_day', '360_day'
        calendars = _noncfcalendars
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
                                    # print(calendar, unit, format, only_cftime,
                                    #       only_python, has_year_zero,
                                    #       itypes[itype])
                                    indates = itypes[itype](idates)
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
                                        format=iformat, return_arrays=False)
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
                                    # print(calendar, unit, format, only_cftime,
                                    #       only_python, has_year_zero,
                                    #       itypes[itype])
                                    indates = itypes[itype](idates)
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
                                        format=iformat, return_arrays=False)
                                    assert isinstance(jdates, ttypes[itype])
                                    assert isinstance(idec, ttypes[itype])
                                    assert isinstance(odates, ttypes[itype])
                                    self.assertEqual(_flatten(odates),
                                                     _flatten(indates))

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
