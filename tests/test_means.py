#!/usr/bin/env python
"""
This is the unittest for the means module.

python -m unittest -v tests/test_means.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_means.py

355: seasonalmonth
457-471: month
542-564: minute
581: meanday with one hour == undef
585-598: meanmonth
602-629: seasonalday
633-650: seasonalmeanday

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


class TestMeans(unittest.TestCase):
    """
    Tests for means.py
    """
    def setUp(self):
        import numpy as np
        from pyjams import num2date
        # 2 years at 00:15 and 00:45
        self.year0 = 1990
        self.nyears = 2
        self.ndays = 365
        self.nhours = 24
        self.nminutes = 2
        self.jdates = []
        for i in range(self.nyears):
            for j in range(self.ndays):
                for k in range(self.nhours):
                    for m in range(self.nminutes):
                        self.jdates.append(
                            self.year0 + i +
                            j / 365 +
                            k / (24 * 365) +
                            (15 + m * 30) /
                            (60 * 24 * 365))
        # to stay above second (rounding errors) when calculations with jdates
        muleps = np.finfo(float).eps
        self.jdates = [ dd + np.abs(dd) * muleps for dd in self.jdates ]
        self.ddates = num2date(self.jdates, calendar='decimal')
        self.ddates = [ dd.round_microseconds() for dd in self.ddates ]
        self.format = '%Y-%m-%d %H:%M:%S'
        self.dates = [ dd.strftime(self.format) for dd in self.ddates ]
        self.n = len(self.dates)
        self.x = np.arange(self.n) + 1
        self.undef = -9999.

    def test_means(self):
        import cftime as cf
        import datetime as pydatetime
        import numpy as np
        from pyjams import means
        from pyjams import date2num, num2date

        excelcalendars = ['excel', 'excel1900', 'excel1904']
        decimalcalendars = ['decimal', 'decimal365']
        calendars = excelcalendars + decimalcalendars
        # CF calendars are not working because of microsecond precision
        # cfcalendars = ['standard', 'gregorian', 'proleptic_gregorian',
        #                'noleap', 'julian', 'all_leap', '365_day', '366_day',
        #                '360_day']
        # calendars = cfcalendars
        ncal = len(calendars)
        itest = -1

        # different date formats

        dsoll = (min(self.jdates) + max(self.jdates)) * 0.5
        dsoll = num2date(dsoll, calendar='decimal', format=self.format)
        # dsoll = dsoll.round_microseconds()
        # dsoll = dsoll.strftime('%Y-%m-%d %H:%M:%S')
        n = self.nyears * self.ndays * self.nhours * self.nminutes
        xsoll = n//2 * (n + 1) / n
        print('')

        # dates = str
        itest += 1
        print('itest', itest)
        dates = self.dates  # str
        dout, xout = means(dates, self.x)
        assert isinstance(dout, type(dates[0]))
        assert dout == dsoll
        assert xout == xsoll

        # dates = str w/ format
        itest += 1
        print('itest', itest)
        iform = '%Y-%m-%d %H:%M'
        dates = [ dd[:16] for dd in self.dates ]
        dout, xout = means(dates, self.x, format=iform)
        assert isinstance(dout, type(dates[0]))
        dsoll1 = dsoll[:16]
        assert dout == dsoll1
        assert xout == xsoll

        # dates = pyjams.datetime
        itest += 1
        print('itest', itest)
        dates = self.ddates  # datetime
        dout, xout = means(dates, self.x)
        assert isinstance(dout, type(dates[0]))
        dout = dout.strftime(self.format)
        assert dout == dsoll
        assert xout == xsoll

        # dates = cf.datetime
        itest += 1
        print('itest', itest)
        dates = [ cf.datetime(*dd.to_tuple())
                  for dd in self.ddates ]
        dout, xout = means(dates, self.x)
        assert isinstance(dout, type(dates[0]))
        dout = dout.strftime(self.format)
        assert dout == dsoll
        assert xout == xsoll

        # dates = datetime.datetime
        itest += 1
        print('itest', itest)
        dates = [ pydatetime.datetime(*dd.to_tuple())
                  for dd in self.ddates ]
        dout, xout = means(dates, self.x)
        assert isinstance(dout, type(dates[0]))
        dout = dout.strftime(self.format)
        assert dout == dsoll
        assert xout == xsoll

        # dates = numeric
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)  # num
        dout, xout = means(dates, self.x, calendar=cal)
        assert isinstance(dout, (type(dates[0]), np.int64))
        dout = num2date(dout, calendar=cal)
        dout = dout.strftime(self.format)
        assert dout == dsoll
        assert xout == xsoll

        # data = ndarray
        itest += 1
        print('itest', itest)
        dates = self.dates
        dout, xout = means(dates, np.vstack([self.x, self.x]).T)
        assert isinstance(dout, type(dates[0]))
        xsoll1 = [xsoll, xsoll]
        assert dout == dsoll
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll1))

        # sum
        itest += 1
        print('itest', itest)
        dates = self.dates  # str
        dout, xout = means(dates, self.x, sum=True)
        assert isinstance(dout, type(dates[0]))
        xsoll1 = xsoll * n
        assert dout == dsoll
        assert xout == xsoll1

        # min
        itest += 1
        print('itest', itest)
        dates = self.dates  # str
        dout, xout = means(dates, self.x, min=True)
        assert isinstance(dout, type(dates[0]))
        xsoll1 = self.x[0]
        assert dout == dsoll
        assert xout == xsoll1

        # max
        itest += 1
        print('itest', itest)
        dates = self.dates  # str
        dout, xout = means(dates, self.x, max=True)
        assert isinstance(dout, type(dates[0]))
        xsoll1 = self.x[-1]
        assert dout == dsoll
        assert xout == xsoll1

        # onlydat
        itest += 1
        print('itest', itest)
        dates = self.dates
        xout = means(dates, self.x, onlydat=True)
        assert xout == xsoll

        # onlydat with dat = ndarray
        itest += 1
        print('itest', itest)
        dates = self.dates
        xout = means(dates, np.vstack([self.x, self.x]).T, onlydat=True)
        xsoll1 = [xsoll, xsoll]
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll1))

        # masked
        itest += 1
        print('itest', itest)
        dates = self.dates
        n2 = self.n // 2
        xout = means(dates,
                     np.ma.array(self.x, mask=(self.x > n2)), onlydat=True)
        xsoll1 = n2//2 * (n2 + 1) / n2
        assert xout == xsoll1

        # different means

        # year
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        dout, xout = means(dates, self.x, year=True, calendar=cal)
        assert isinstance(dout[0], (type(dates[0]), np.int64))
        dsoll = [ '{:04d}-06-15 12:00:00'.format(self.year0 + yy)
                  for yy in range(self.nyears) ]
        n = self.ndays * self.nhours * self.nminutes
        xsoll = (n//2 * (n + 1) + np.arange(self.nyears) * n * n) / n
        # ToDo: output type wrong
        # assert isinstance(dout, list)
        assert isinstance(dout, np.ndarray)
        assert isinstance(xout, np.ndarray)
        dout = num2date(dout, calendar=cal)
        dout = [ dd.strftime(self.format) for dd in dout ]
        self.assertEqual(_flatten(dout),
                         _flatten(dsoll))
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll))

        # year with dat = ndarray
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        dout, xout = means(dates, np.vstack([self.x, self.x]).T,
                           year=True, calendar=cal)
        assert isinstance(dout[0], (type(dates[0]), np.int64))
        dsoll = [ '{:04d}-06-15 12:00:00'.format(self.year0 + yy)
                  for yy in range(self.nyears) ]
        n = self.ndays * self.nhours * self.nminutes
        xsoll = (n//2 * (n + 1) + np.arange(self.nyears) * n * n) / n
        xsoll1 = np.vstack([xsoll, xsoll]).T
        # ToDo: output type wrong
        # assert isinstance(dout, list)
        assert isinstance(dout, np.ndarray)
        assert isinstance(xout, np.ndarray)
        dout = num2date(dout, calendar=cal)
        dout = [ dd.strftime(self.format) for dd in dout ]
        self.assertEqual(_flatten(dout),
                         _flatten(dsoll))
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll1))

        # year and onlydat
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        xout = means(dates, self.x, year=True, calendar=cal, onlydat=True)
        n = self.ndays * self.nhours * self.nminutes
        xsoll = (n//2 * (n + 1) + np.arange(self.nyears) * n * n) / n
        assert isinstance(xout, np.ndarray)
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll))

        # year and onlydat and masked array
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        xout = means(dates, np.ma.array(self.x), year=True,
                     calendar=cal, onlydat=True)
        n = self.ndays * self.nhours * self.nminutes
        xsoll = (n//2 * (n + 1) + np.arange(self.nyears) * n * n) / n
        assert isinstance(xout, np.ndarray)
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll))

        # year and onlydat and mask
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        n2 = self.n // 2
        xout = means(dates, np.ma.array(self.x, mask=(self.x > n2)),
                     year=True, calendar=cal, onlydat=True)
        assert isinstance(xout, np.ma.MaskedArray)
        n = self.ndays * self.nhours * self.nminutes
        assert np.ma.count_masked(xout) > 0
        assert not np.ma.is_masked(xout[0])
        assert np.ma.is_masked(xout[1])
        xsoll = n//2 * (n + 1) / n
        assert xout[0] == xsoll

        # year and onlydat with dat = ndarray
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        xout = means(dates, np.vstack([self.x, self.x]).T,
                     year=True, calendar=cal, onlydat=True)
        n = self.ndays * self.nhours * self.nminutes
        xsoll = (n//2 * (n + 1) + np.arange(self.nyears) * n * n) / n
        xsoll1 = np.vstack([xsoll, xsoll]).T
        assert isinstance(xout, np.ndarray)
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll1))

        # month=True

        # day
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        dout, xout = means(dates, self.x, day=True, calendar=cal)
        assert isinstance(dout[0], (type(dates[0]), np.int64))
        dlen = self.nhours * self.nminutes
        dsoll = [ dd[:10] + ' 12:00:00'
                  for dd in self.dates[::dlen] ]
        xsoll = np.mean(np.array(self.x).reshape(-1, dlen), axis=1)
        # assert isinstance(dout, list)
        assert isinstance(dout, np.ndarray)
        assert isinstance(xout, np.ndarray)
        dout = num2date(dout, calendar=cal)
        dout = [ dd.strftime(self.format) for dd in dout ]
        self.assertEqual(_flatten(dout),
                         _flatten(dsoll))
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll))

        # hour
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        dout, xout = means(dates, self.x, hour=True, calendar=cal)
        assert isinstance(dout[0], (type(dates[0]), np.int64))
        dlen = self.nminutes
        dsoll = [ dd[:14] + '30:00' for dd in self.dates[::dlen] ]
        xsoll = np.mean(np.array(self.x).reshape(-1, dlen), axis=1)
        # assert isinstance(dout, list)
        assert isinstance(dout, np.ndarray)
        assert isinstance(xout, np.ndarray)
        dout = num2date(dout, calendar=cal)
        dout = [ dd.strftime(self.format) for dd in dout ]
        self.assertEqual(_flatten(dout),
                         _flatten(dsoll))
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll))

        # half_hour
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        dout, xout = means(dates, self.x, half_hour=True,
                           calendar=cal)
        assert isinstance(dout[0], (type(dates[0]), np.int64))
        dsoll = self.dates
        xsoll = np.array(self.x, dtype=float)
        # assert isinstance(dout, list)
        assert isinstance(dout, np.ndarray)
        assert isinstance(xout, np.ndarray)
        dout = num2date(dout, calendar=cal)
        dout = [ dd.strftime(self.format) for dd in dout ]
        self.assertEqual(_flatten(dout),
                         _flatten(dsoll))
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll))

        # minutes=True takes very long
        # dsoll = self.dates
        # xsoll = np.array(self.x, dtype=float)

        # meanday
        itest += 1
        print('itest', itest)
        cal = calendars[itest % ncal]
        dates = date2num(self.dates, calendar=cal)
        dout, xout = means(dates, self.x, meanday=True,
                           calendar=cal)
        assert isinstance(dout[0], (type(dates[0]), np.int64))
        dsoll = [ '{:04d}-01-01 {:02d}:30:00'.format(self.year0, dd)
                  for dd in range(24) ]
        dlen = self.nhours * self.nminutes
        xsoll = [ np.mean(self.x[i::dlen]) for i in range(dlen) ]
        xsoll = np.mean(np.array(xsoll).reshape(-1, self.nminutes), axis=1)
        # assert isinstance(dout, list)
        assert isinstance(dout, np.ndarray)
        assert isinstance(xout, (np.ndarray, np.ma.MaskedArray))
        dout = num2date(dout, calendar=cal)
        dout = [ dd.strftime(self.format) for dd in dout ]
        self.assertEqual(_flatten(dout),
                         _flatten(dsoll))
        self.assertEqual(_flatten(xout),
                         _flatten(xsoll))

        # meanmonth=True == seasonalmonth=True

        # seasonalday=True

        # seasonalmeanday=True


if __name__ == "__main__":
    unittest.main()
