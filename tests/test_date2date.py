#!/usr/bin/env python
"""
This is the unittest for date2date module.

python -m unittest -v tests/test_date2date.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_date2date.py

"""
import unittest


class TestDate2Date(unittest.TestCase):
    """
    Tests for date2date.py
    """

    def test_date2date(self):
        import numpy as np
        from pyjams import date2date

        edate = ['2014-11-12 12:00', '01.03.2015T17:56:00',
                 '12/01/1990', '04.05.1786']

        out  = date2date(edate)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990',
                '04.05.1786']
        self.assertEqual(soll, out)

        out  = date2date(edate, full=True)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00:00', '01.03.2015 17:56:00',
                '01.12.1990 00:00:00', '04.05.1786 00:00:00']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='en')
        assert isinstance(out, list)
        soll = ['2014-11-12 12:00', '2015-03-01 17:56:00', '1990-12-01',
                '1786-05-04']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='en', full=True)
        assert isinstance(out, list)
        soll = ['2014-11-12 12:00:00', '2015-03-01 17:56:00',
                '1990-12-01 00:00:00', '1786-05-04 00:00:00']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='en', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['2014-11-12T12:00:00', '2015-03-01T17:56:00',
                '1990-12-01T00:00:00', '1786-05-04T00:00:00']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        out  = date2date(list(edate))
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990',
                '04.05.1786']
        self.assertEqual(soll, out)

        out  = date2date(tuple(edate))
        assert isinstance(out, tuple)
        soll = ('12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990',
                '04.05.1786')
        self.assertEqual(list(soll), list(out))

        out  = date2date(np.array(edate))
        assert isinstance(out, np.ndarray)
        soll = ['12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990',
                '04.05.1786']
        self.assertEqual(soll, list(out))

        out  = date2date(edate[0])
        assert isinstance(out, str)
        soll = '12.11.2014 12:00'
        assert soll == out

        out  = date2date(edate, format='us')
        assert isinstance(out, list)
        soll = ['11/12/2014 12:00', '03/01/2015 17:56:00', '12/01/1990',
                '05/04/1786']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='us', full=True)
        assert isinstance(out, list)
        soll = ['11/12/2014 12:00:00', '03/01/2015 17:56:00',
                '12/01/1990 00:00:00', '05/04/1786 00:00:00']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='fr')
        assert isinstance(out, list)
        soll = ['12/11/2014 12:00', '01/03/2015 17:56:00', '01/12/1990',
                '04/05/1786']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='fr', full=True)
        assert isinstance(out, list)
        soll = ['12/11/2014 12:00:00', '01/03/2015 17:56:00',
                '01/12/1990 00:00:00', '04/05/1786 00:00:00']
        self.assertEqual(soll, out)

        # fr
        edate = ['2014-11-12 12:00', '01.03.2015T17:56:00',
                 '01/12/1990', '04.05.1786']

        out  = date2date(edate, fr=True)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990',
                '04.05.1786']
        self.assertEqual(soll, out)

        out  = date2date(edate, fr=True, full=True)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00:00', '01.03.2015 17:56:00',
                '01.12.1990 00:00:00', '04.05.1786 00:00:00']
        self.assertEqual(soll, out)

        # 1-2 digits
        edate = ['1-11-12 12:00', '1.3.15 17:56:00', '90-12-1']

        out  = date2date(edate)
        assert isinstance(out, list)
        soll = ['12.11.2001 12:00', '01.03.2015 17:56:00', '01.12.1990']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='en')
        assert isinstance(out, list)
        soll = ['2001-11-12 12:00', '2015-03-01 17:56:00', '1990-12-01']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='us')
        assert isinstance(out, list)
        soll = ['11/12/2001 12:00', '03/01/2015 17:56:00', '12/01/1990']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='us', full=True)
        assert isinstance(out, list)
        soll = ['11/12/2001 12:00:00', '03/01/2015 17:56:00',
                '12/01/1990 00:00:00']
        self.assertEqual(soll, out)

        out  = date2date(edate, format='fr', full=True)
        assert isinstance(out, list)
        soll = ['12/11/2001 12:00:00', '01/03/2015 17:56:00',
                '01/12/1990 00:00:00']
        self.assertEqual(soll, out)

        # times
        edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
                 '1990-12-01 01', '04.05.1786']

        out  = date2date(edate)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990 01',
                '04.05.1786']
        self.assertEqual(soll, out)

        out  = date2date(edate, full=True)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00:00', '01.03.2015 17:56:00',
                '01.12.1990 01:00:00', '04.05.1786 00:00:00']
        self.assertEqual(soll, out)

        # errors
        # wrong date delimiter
        edate = ['2014\11\12 12:00', '01.03.2015 17:56:00',
                 '1990-12-01 01', '04.05.1786']
        self.assertRaises(ValueError, date2date, edate)
        # milliseconds
        edate = ['2014-11-12 12:00', '01.03.2015 17:56:00:00',
                 '1990-12-01 01', '04.05.1786']
        self.assertRaises(ValueError, date2date, edate)
        # 3-digit year
        edate = ['1-11-12 12:00', '1.3.15 17:56:00', '190-12-1']
        self.assertRaises(ValueError, date2date, edate)

    def test_date2en(self):
        from pyjams import date2en

        edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
                 '1990-12-01', '04.05.1786']

        out  = date2en(edate)
        assert isinstance(out, list)
        soll = ['2014-11-12 12:00', '2015-03-01 17:56:00', '1990-12-01',
                '1786-05-04']
        self.assertEqual(soll, out)

        out  = date2en(edate, full=True)
        assert isinstance(out, list)
        soll = ['2014-11-12 12:00:00', '2015-03-01 17:56:00',
                '1990-12-01 00:00:00', '1786-05-04 00:00:00']
        self.assertEqual(soll, out)

        out  = date2en(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['1-11-12 12:00', '1.3.15 17:56:00', '90-12-1']

        out  = date2en(edate, full=True)
        assert isinstance(out, list)
        soll = ['2001-11-12 12:00:00', '2015-03-01 17:56:00',
                '1990-12-01 00:00:00']
        self.assertEqual(soll, out)

    def test_date2fr(self):
        from pyjams import date2fr

        edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
                 '1990-12-01', '04.05.1786']

        out  = date2fr(edate)
        assert isinstance(out, list)
        soll = ['12/11/2014 12:00', '01/03/2015 17:56:00', '01/12/1990',
                '04/05/1786']
        self.assertEqual(soll, out)

        out  = date2fr(edate, full=True)
        assert isinstance(out, list)
        soll = ['12/11/2014 12:00:00', '01/03/2015 17:56:00',
                '01/12/1990 00:00:00', '04/05/1786 00:00:00']
        self.assertEqual(soll, out)

        out  = date2fr(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['1-11-12 12:00', '1.3.15 17:56:00', '90-12-1']

        out  = date2fr(edate, full=True)
        assert isinstance(out, list)
        soll = ['12/11/2001 12:00:00', '01/03/2015 17:56:00',
                '01/12/1990 00:00:00']
        self.assertEqual(soll, out)

    def test_date2us(self):
        from pyjams import date2us

        edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
                 '1990-12-01', '04.05.1786']

        out  = date2us(edate)
        assert isinstance(out, list)
        soll = ['11/12/2014 12:00', '03/01/2015 17:56:00', '12/01/1990',
                '05/04/1786']
        self.assertEqual(soll, out)

        out  = date2us(edate, full=True)
        assert isinstance(out, list)
        soll = ['11/12/2014 12:00:00', '03/01/2015 17:56:00',
                '12/01/1990 00:00:00', '05/04/1786 00:00:00']
        self.assertEqual(soll, out)

        out  = date2us(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['1-11-12 12:00', '1.3.15 17:56:00', '90-12-1']

        out  = date2us(edate, full=True)
        assert isinstance(out, list)
        soll = ['11/12/2001 12:00:00', '03/01/2015 17:56:00',
                '12/01/1990 00:00:00']
        self.assertEqual(soll, out)

    def test_en2date(self):
        from pyjams import en2date

        edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
                 '1990-12-01', '04.05.1786']

        out  = en2date(edate)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990',
                '04.05.1786']
        self.assertEqual(soll, out)

        out  = en2date(edate, full=True)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00:00', '01.03.2015 17:56:00',
                '01.12.1990 00:00:00', '04.05.1786 00:00:00']
        self.assertEqual(soll, out)

        out  = en2date(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['1-11-12 12:00', '1.3.15 17:56:00', '90-12-1']

        out  = en2date(edate, full=True)
        assert isinstance(out, list)
        soll = ['12.11.2001 12:00:00', '01.03.2015 17:56:00',
                '01.12.1990 00:00:00']
        self.assertEqual(soll, out)

    def test_en2fr(self):
        from pyjams import en2fr

        edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
                 '1990-12-01', '04.05.1786']

        out  = en2fr(edate)
        assert isinstance(out, list)
        soll = ['12/11/2014 12:00', '01/03/2015 17:56:00', '01/12/1990',
                '04/05/1786']
        self.assertEqual(soll, out)

        out  = en2fr(edate, full=True)
        assert isinstance(out, list)
        soll = ['12/11/2014 12:00:00', '01/03/2015 17:56:00',
                '01/12/1990 00:00:00', '04/05/1786 00:00:00']
        self.assertEqual(soll, out)

        out  = en2fr(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['1-11-12 12:00', '1.3.15 17:56:00', '90-12-1']

        out  = en2fr(edate, full=True)
        assert isinstance(out, list)
        soll = ['12/11/2001 12:00:00', '01/03/2015 17:56:00',
                '01/12/1990 00:00:00']
        self.assertEqual(soll, out)

    def test_en2us(self):
        from pyjams import en2us

        edate = ['2014-11-12 12:00', '01.03.2015 17:56:00',
                 '1990-12-01', '04.05.1786']

        out  = en2us(edate)
        assert isinstance(out, list)
        soll = ['11/12/2014 12:00', '03/01/2015 17:56:00', '12/01/1990',
                '05/04/1786']
        self.assertEqual(soll, out)

        out  = en2us(edate, full=True)
        assert isinstance(out, list)
        soll = ['11/12/2014 12:00:00', '03/01/2015 17:56:00',
                '12/01/1990 00:00:00', '05/04/1786 00:00:00']
        self.assertEqual(soll, out)

        out  = en2us(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['1-11-12 12:00', '1.3.15 17:56:00', '90-12-1']

        out  = en2us(edate, full=True)
        assert isinstance(out, list)
        soll = ['11/12/2001 12:00:00', '03/01/2015 17:56:00',
                '12/01/1990 00:00:00']
        self.assertEqual(soll, out)

    def test_fr2date(self):
        from pyjams import fr2date

        edate = ['12/11/2014 12:00', '01/03/2015 17:56:00',
                 '01/12/1990', '04/05/1786']

        out  = fr2date(edate)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990',
                '04.05.1786']
        self.assertEqual(soll, out)

        out  = fr2date(edate, full=True)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00:00', '01.03.2015 17:56:00',
                '01.12.1990 00:00:00', '04.05.1786 00:00:00']
        self.assertEqual(soll, out)

        out  = fr2date(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['12/11/1 12:00', '1/3/15 17:56:00', '1/12/90']

        out  = fr2date(edate, full=True)
        assert isinstance(out, list)
        soll = ['12.11.2001 12:00:00', '01.03.2015 17:56:00',
                '01.12.1990 00:00:00']
        self.assertEqual(soll, out)

    def test_fr2en(self):
        from pyjams import fr2en

        edate = ['12/11/2014 12:00', '01/03/2015 17:56:00',
                 '01/12/1990', '04/05/1786']

        out  = fr2en(edate)
        assert isinstance(out, list)
        soll = ['2014-11-12 12:00', '2015-03-01 17:56:00', '1990-12-01',
                '1786-05-04']
        self.assertEqual(soll, out)

        out  = fr2en(edate, full=True)
        assert isinstance(out, list)
        soll = ['2014-11-12 12:00:00', '2015-03-01 17:56:00',
                '1990-12-01 00:00:00', '1786-05-04 00:00:00']
        self.assertEqual(soll, out)

        out  = fr2en(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['12/11/1 12:00', '1/3/15 17:56:00', '1/12/90']

        out  = fr2en(edate, full=True)
        assert isinstance(out, list)
        soll = ['2001-11-12 12:00:00', '2015-03-01 17:56:00',
                '1990-12-01 00:00:00']
        self.assertEqual(soll, out)

    def test_fr2us(self):
        from pyjams import fr2us

        edate = ['12/11/2014 12:00', '01/03/2015 17:56:00',
                 '01/12/1990', '04/05/1786']

        out  = fr2us(edate)
        assert isinstance(out, list)
        soll = ['11/12/2014 12:00', '03/01/2015 17:56:00', '12/01/1990',
                '05/04/1786']
        self.assertEqual(soll, out)

        out  = fr2us(edate, full=True)
        assert isinstance(out, list)
        soll = ['11/12/2014 12:00:00', '03/01/2015 17:56:00',
                '12/01/1990 00:00:00', '05/04/1786 00:00:00']
        self.assertEqual(soll, out)

        out  = fr2us(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['12/11/1 12:00', '1/3/15 17:56:00', '1/12/90']

        out  = fr2us(edate, full=True)
        assert isinstance(out, list)
        soll = ['11/12/2001 12:00:00', '03/01/2015 17:56:00',
                '12/01/1990 00:00:00']
        self.assertEqual(soll, out)

    def test_us2date(self):
        from pyjams import us2date, date2us

        edate = ['11/12/2014 12:00', '03/01/2015 17:56:00',
                 '1990-12-01', '04.05.1786']

        out  = us2date(edate)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00', '01.03.2015 17:56:00', '01.12.1990',
                '04.05.1786']
        self.assertEqual(soll, out)

        out  = us2date(edate, full=True)
        assert isinstance(out, list)
        soll = ['12.11.2014 12:00:00', '01.03.2015 17:56:00',
                '01.12.1990 00:00:00', '04.05.1786 00:00:00']
        self.assertEqual(soll, out)

        out  = us2date(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['11/12/1 12:00', '3/1/15 17:56:00', '90-12-1']

        out  = us2date(date2us(edate), full=True)
        assert isinstance(out, list)
        soll = ['12.11.2001 12:00:00', '01.03.2015 17:56:00',
                '01.12.1990 00:00:00']
        self.assertEqual(soll, out)

    def test_us2en(self):
        from pyjams import us2en

        edate = ['11/12/2014 12:00', '03/01/2015 17:56:00',
                 '1990-12-01', '04.05.1786']

        out  = us2en(edate)
        assert isinstance(out, list)
        soll = ['2014-11-12 12:00', '2015-03-01 17:56:00', '1990-12-01',
                '1786-05-04']
        self.assertEqual(soll, out)

        out  = us2en(edate, full=True)
        assert isinstance(out, list)
        soll = ['2014-11-12 12:00:00', '2015-03-01 17:56:00',
                '1990-12-01 00:00:00', '1786-05-04 00:00:00']
        self.assertEqual(soll, out)

        out  = us2en(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['11/12/1 12:00', '3/1/15 17:56:00', '90-12-1']

        out  = us2en(edate, full=True)
        assert isinstance(out, list)
        soll = ['2001-11-12 12:00:00', '2015-03-01 17:56:00',
                '1990-12-01 00:00:00']
        self.assertEqual(soll, out)

    def test_us2fr(self):
        from pyjams import us2fr

        edate = ['11/12/2014 12:00', '03/01/2015 17:56:00',
                 '1990-12-01', '04.05.1786']

        out  = us2fr(edate)
        assert isinstance(out, list)
        soll = ['12/11/2014 12:00', '01/03/2015 17:56:00', '01/12/1990',
                '04/05/1786']
        self.assertEqual(soll, out)

        out  = us2fr(edate, full=True)
        assert isinstance(out, list)
        soll = ['12/11/2014 12:00:00', '01/03/2015 17:56:00',
                '01/12/1990 00:00:00', '04/05/1786 00:00:00']
        self.assertEqual(soll, out)

        out  = us2fr(edate, format='%Y%m%d%H%M%S', full=True, timesep='T')
        assert isinstance(out, list)
        soll = ['20141112120000', '20150301175600',
                '19901201000000', '17860504000000']
        self.assertEqual(soll, out)

        edate = ['11/12/1 12:00', '3/1/15 17:56:00', '90-12-1']

        out  = us2fr(edate, full=True)
        assert isinstance(out, list)
        soll = ['12/11/2001 12:00:00', '01/03/2015 17:56:00',
                '01/12/1990 00:00:00']
        self.assertEqual(soll, out)


if __name__ == "__main__":
    unittest.main()
