#!/usr/bin/env python
"""
This is the unittest for fsread module.

python -m unittest -v tests/test_fsread.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_fsread.py

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


class TestFsread(unittest.TestCase):
    """
    Tests for fsread.py
    """

    def test_fsread(self):
        import os
        import numpy as np
        from pyjams import fsread

        # Create float data
        file_whitespace = 'test_fsread_whitespace.dat'
        with open(file_whitespace, 'w') as ff:
            print('head1 head2 head3 head4', file=ff)
            print('1.1 1.2 1.3 1.4', file=ff)
            print('2.1 2.2 2.3 2.4', file=ff)

        # Some mixed data
        file_semicolon = 'test_fsread_semicolon.dat'
        with open(file_semicolon, 'w') as ff:
            print('head1;head2;head3;head4', file=ff)
            print('01.12.2012;1.2;name1;1.4', file=ff)
            print('01.01.2013;2.2;name2;2.4', file=ff)

        # Some mixed data with missing values
        file_comma = 'test_fsread_comma.dat'
        with open(file_comma, 'w') as ff:
            print('head1,head2,head3,head4,', file=ff)
            print('01.12.2012,1.2,name1,1.4,', file=ff)
            print('01.01.2013,,name2,,', file=ff)

        # Data with shorter and longer columns
        file_short_columns = 'test_fsread_short_columns.dat'
        with open(file_short_columns, 'w') as ff:
            print('head1 head3 head4', file=ff)
            print('1.1 1.2 1.4', file=ff)
            print('2.1 2.2 2.3 2.4', file=ff)
            print('3.1 3.2 3.4', file=ff)

        file_short_columns2 = 'test_fsread_short_columns2.dat'
        with open(file_short_columns2, 'w') as ff:
            print('head1,head3,head4', file=ff)
            print('1.1,1.2,1.4', file=ff)
            print('2.1,2.2,2.3,2.4', file=ff)
            print('3.1,3.2,3.4', file=ff)

        # Data with blank lines
        file_blank = 'test_fsread_blank.dat'
        with open(file_blank, 'w') as ff:
            print('head1 head2 head3 head4', file=ff)
            print('1.1 1.2 1.3 1.4', file=ff)
            print('2.1 2.2 2.3 2.4', file=ff)
            print('', file=ff)
            print('', file=ff)
            print('3.1 3.2 3.3 3.4', file=ff)

        file_blank1 = 'test_fsread_blank1.dat'
        with open(file_blank1, 'w') as ff:
            print('head1 head2 head3 head4', file=ff)
            print('', file=ff)
            print('# Comment', file=ff)
            print('1.1 1.2 1.3 1.4', file=ff)
            print('2.1 2.2 2.3 2.4', file=ff)
            print('3.1 3.2 3.3 3.4', file=ff)

        file_blank2 = 'test_fsread_blank2.dat'
        with open(file_blank2, 'w') as ff:
            print('head1 head2 head3 head4', file=ff)
            print('', file=ff)
            print('1.1 1.2 1.3 1.4', file=ff)
            print('', file=ff)
            print('2.1 2.2 2.3 2.4', file=ff)
            print('', file=ff)
            print('3.1 3.2 3.3 3.4', file=ff)

        # Data with comment lines
        file_comment = 'test_fsread_comment.dat'
        with open(file_comment, 'w') as ff:
            print('head1 head2 head3 head4', file=ff)
            print('! one comment', file=ff)
            print('1.1 1.2 1.3 1.4', file=ff)
            print('# another comment', file=ff)
            print('2.1 2.2 2.3 2.4', file=ff)

        # Start tests

        # Read sample as with fread - see fread for more examples
        fout, sout = fsread(file_whitespace, nc=[1, 3], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_whitespace, nc=2, skip=1, header=True)
        fsoll = [['head1', 'head2']]
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_whitespace, nc=2, skip=1, header=True,
                            squeeze=True)
        fsoll = ['head1', 'head2']
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read sample as with sread - see sread for more examples
        fout, sout = fsread(file_whitespace, snc=[1, 3], skip=1)
        fsoll = []
        ssoll = [['1.2', '1.4'], ['2.2', '2.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read float and string columns - 1
        fout, sout = fsread(file_whitespace, nc=1, snc=-1, skip=1)
        fsoll = [[1.1], [2.1]]
        ssoll = [['1.2', '1.3', '1.4'], ['2.2', '2.3', '2.4']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_whitespace, nc=-1, skip=1)
        fsoll = [[1.1, 1.2, 1.3, 1.4], [2.1, 2.2, 2.3, 2.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_whitespace, snc=-1, skip=1)
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # strip
        fout, sout = fsread(file_whitespace, snc=-1, skip=1, strip=False)
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_whitespace, snc=-1, skip=1, strip='1')
        fsoll = []
        ssoll = [['.', '.2', '.3', '.4'], ['2.', '2.2', '2.3', '2.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read float and string columns - 2
        fout, sout = fsread(file_semicolon, nc=[1, 3], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], skip=1,
                            separator=';')
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        ssoll = [['01.12.2012', 'name1'], ['01.01.2013', 'name2']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2],
                            skip=1, transpose=True)
        fsoll = [[1.2, 2.2], [1.4, 2.4]]
        ssoll = [['01.12.2012', '01.01.2013'], ['name1', 'name2']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2],
                            skip=1, return_list=True)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        ssoll = [['01.12.2012', 'name1'], ['01.01.2013', 'name2']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=-1, skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        ssoll = [['01.12.2012', 'name1'], ['01.01.2013', 'name2']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=-1, snc=[0, 2], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        ssoll = [['01.12.2012', 'name1'], ['01.01.2013', 'name2']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=-1, snc=3, skip=1)
        fsoll = [[1.4], [2.4]]
        ssoll = [['01.12.2012', '1.2', 'name1'],
                 ['01.01.2013', '2.2', 'name2']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=-1, snc=3, skip=1,
                            squeeze=True, return_list=True)
        fsoll = [1.4, 2.4]
        ssoll = [['01.12.2012', '1.2', 'name1'],
                 ['01.01.2013', '2.2', 'name2']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read header
        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2], skip=1,
                            header=True)
        fsoll = [['head2', 'head4']]
        ssoll = [['head1', 'head3']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2], skip=1,
                            header=True, squeeze=True)
        fsoll = ['head2', 'head4']
        ssoll = ['head1', 'head3']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2],
                            skip=1, hskip=1, header=True)
        fsoll = []
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2], skip=2,
                            header=True, full_header=True, strarr=True)
        fsoll = [['head1;head2;head3;head4'],
                 ['01.12.2012;1.2;name1;1.4']]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2], skip=2,
                            header=True)
        fsoll = [['head2', 'head4'],
                 ['1.2', '1.4']]
        ssoll = [['head1', 'head3'],
                 ['01.12.2012', 'name1']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2], skip=2,
                            header=True, strarr=True)
        fsoll = [['head2', 'head4'],
                 ['1.2', '1.4']]
        ssoll = [['head1', 'head3'],
                 ['01.12.2012', 'name1']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1], snc=[0], skip=2,
                            header=True, squeeze=True)
        fsoll = ['head2', '1.2']
        ssoll = ['head1', '01.12.2012']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1], snc=[0], skip=2,
                            header=True, strarr=True, squeeze=True)
        fsoll = ['head2', '1.2']
        ssoll = ['head1', '01.12.2012']
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2], skip=2,
                            header=True, transpose=True)
        fsoll = [['head2', '1.2'],
                 ['head4', '1.4']]
        ssoll = [['head1', '01.12.2012'],
                 ['head3', 'name1']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_semicolon, nc=[1, 3], snc=[0, 2], skip=2,
                            header=True, strarr=True, transpose=True)
        fsoll = [['head2', '1.2'],
                 ['head4', '1.4']]
        ssoll = [['head1', '01.12.2012'],
                 ['head3', 'name1']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # missing values
        fout, sout = fsread(file_comma, nc=[1, 3], skip=1, fill=True,
                            fill_value=-1)
        fsoll = [[1.2, 1.4], [-1., -1.]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, nc=[1, 3], skip=1, fill=True,
                            strarr=True)
        fsoll = [[1.2, 1.4], [np.nan, np.nan]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # cname, sname
        fout, sout = fsread(file_comma, cname='head2', snc=[0, 2], skip=1,
                            fill=True, fill_value=-1, squeeze=True)
        fsoll = [1.2, -1.]
        ssoll = [['01.12.2012', 'name1'], ['01.01.2013', 'name2']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, cname=['head2', 'head4'], snc=[0],
                            skip=1, fill=True, fill_value=-1, squeeze=True)
        fsoll = [[1.2, 1.4], [-1., -1.]]
        ssoll = ['01.12.2012', '01.01.2013']
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, cname=['head2', 'head4'], snc=[0],
                            skip=1, fill=True, fill_value=-1,
                            squeeze=True, return_list=True)
        fsoll = [[1.2, 1.4], [-1., -1.]]
        ssoll = ['01.12.2012', '01.01.2013']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, cname=['head2', 'head4'], snc=-1,
                            skip=1, fill=True, fill_value=-1)
        fsoll = [[1.2, 1.4], [-1., -1.]]
        ssoll = [['01.12.2012', 'name1', ''], ['01.01.2013', 'name2', '']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, nc=[1, 3], sname=['head1', 'head3'],
                            skip=1, fill=True, fill_value=-1, strarr=True,
                            header=True)
        fsoll = [['head2', 'head4']]
        ssoll = [['head1', 'head3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, cname=['head2', 'head4'], snc=-1,
                            skip=1, header=True, full_header=True)
        fsoll = ['head1,head2,head3,head4,']
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, cname=['head2', 'head4'], snc=-1,
                            skip=1, fill=True, fill_value=-1, header=True,
                            full_header=True)
        fsoll = ['head1,head2,head3,head4,']
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, nc=[1, 3], sname='head1',
                            skip=1, fill=True, fill_value=-1, strarr=True,
                            header=True)
        fsoll = [['head2', 'head4']]
        ssoll = [['head1']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, nc=[1, 3], snc=[0, 2, 4], skip=2,
                            header=True)
        fsoll = [['head2', 'head4'],
                 ['1.2', '1.4']]
        ssoll = [['head1', 'head3', ''],
                 ['01.12.2012', 'name1', '']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, nc=[1, 3], snc=[0, 2, 4], skip=2,
                            header=True, fill=True, sfill_value='tail')
        fsoll = [['head2', 'head4'],
                 ['1.2', '1.4']]
        ssoll = [['head1', 'head3', 'tail'],
                 ['01.12.2012', 'name1', 'tail']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comma, nc=[1, 3], snc=[0, 2, 4], skip=2,
                            header=True, fill=True, sfill_value='tail',
                            strarr=True)
        fsoll = [['head2', 'head4'],
                 ['1.2', '1.4']]
        ssoll = [['head1', 'head3', 'tail'],
                 ['01.12.2012', 'name1', 'tail']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # hstrip
        fout, sout = fsread(file_comma, cname=['  head2', 'head4'], snc=-1,
                            skip=1, fill=True, fill_value=-1, hstrip=False,
                            sfill_value='tail')
        fsoll = [[1.4], [-1.]]
        ssoll = [['01.12.2012', '1.2', 'name1', 'tail'],
                 ['01.01.2013', 'tail', 'name2', 'tail']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # skip_blank
        fout, sout = fsread(file_blank, snc=-1, skip=1, skip_blank=False)
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'],
                 ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_blank, snc=-1, skip=1, skip_blank=True)
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'],
                 ['2.1', '2.2', '2.3', '2.4'],
                 ['3.1', '3.2', '3.3', '3.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_blank1, snc=-1, skip=1, skip_blank=True,
                            comment='#')
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'],
                 ['2.1', '2.2', '2.3', '2.4'],
                 ['3.1', '3.2', '3.3', '3.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_blank2, snc=-1, skip=1, skip_blank=True)
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'],
                 ['2.1', '2.2', '2.3', '2.4'],
                 ['3.1', '3.2', '3.3', '3.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # comment
        fout, sout = fsread(file_comment, snc=-1, skip=2, comment='#')
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'],
                 ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comment, snc=-1, skip=1,
                            comment=['#', '!'])
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'],
                 ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = fsread(file_comment, snc=-1, skip=1,
                            comment='#!')
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'],
                 ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # errors
        # nc and cname
        self.assertRaises(ValueError, fsread, file_comma,
                          nc=-1, cname=['head1', 'head2'])
        # snc and sname
        self.assertRaises(ValueError, fsread, file_comma,
                          snc=-1, sname=['head1', 'head2'])
        # no header line left to chose cname
        self.assertRaises(ValueError, fsread, file_comma,
                          cname=['head1', 'head2'], hskip=1)
        # no line left to read
        self.assertRaises(ValueError, fsread, file_comma, nc=-1, skip=4)
        # indices overlap
        self.assertRaises(ValueError, fsread, file_comma,
                          nc=[0, 1, 2], snc=[2, 3])
        # both nc=-1 and snc=-1
        self.assertRaises(ValueError, fsread, file_comma, nc=-1, snc=-1)
        # not enough columns to read
        self.assertRaises(ValueError, fsread, file_short_columns, nc=4, skip=1)
        # not enough columns to read in header
        self.assertRaises(ValueError, fsread, file_short_columns, nc=4, skip=1,
                          header=True)
        # not enough columns to read
        self.assertRaises(ValueError, fsread, file_short_columns, nc=4,
                          hskip=1)
        # not enough columns to read
        self.assertRaises(ValueError, fsread, file_short_columns, nc=4,
                          hskip=2)
        # not enough columns to read
        self.assertRaises(ValueError, fsread, file_short_columns2, nc=4,
                          hskip=1, separator=',')
        # different comment character
        self.assertRaises(ValueError, fsread, file_comment, snc=-1, skip=1,
                          comment='!')
        # first line is blank
        self.assertRaises(ValueError, fsread, file_blank2, snc=-1, skip=1)
        # cannot determine indices because first line blank
        self.assertRaises(ValueError, fsread, file_blank1, snc=-1, skip=1, skip_blank=False)

        if os.path.exists(file_whitespace):
            os.remove(file_whitespace)
        if os.path.exists(file_semicolon):
            os.remove(file_semicolon)
        if os.path.exists(file_comma):
            os.remove(file_comma)
        if os.path.exists(file_short_columns):
            os.remove(file_short_columns)
        if os.path.exists(file_short_columns2):
            os.remove(file_short_columns2)
        if os.path.exists(file_blank):
            os.remove(file_blank)
        if os.path.exists(file_blank1):
            os.remove(file_blank1)
        if os.path.exists(file_blank2):
            os.remove(file_blank2)
        if os.path.exists(file_comment):
            os.remove(file_comment)

    def test_fread(self):
        import os
        import numpy as np
        from pyjams import fread

        # Create float data
        file_whitespace = 'test_fsread_whitespace.dat'
        with open(file_whitespace, 'w') as ff:
            print('head1 head2 head3 head4', file=ff)
            print('1.1 1.2 1.3 1.4', file=ff)
            print('2.1 2.2 2.3 2.4', file=ff)

        # Some mixed data
        file_semicolon = 'test_fsread_semicolon.dat'
        with open(file_semicolon, 'w') as ff:
            print('head1;head2;head3;head4', file=ff)
            print('01.12.2012;1.2;name1;1.4', file=ff)
            print('01.01.2013;2.2;name2;2.4', file=ff)

        # Start tests

        fout = fread(file_whitespace, nc=[1, 3], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_whitespace, nc=[1, 3], skip=1, return_list=True)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        assert isinstance(fout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_whitespace, nc=2, skip=1, header=True)
        fsoll = [['head1', 'head2']]
        assert isinstance(fout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_whitespace, nc=2, skip=1, header=True,
                     squeeze=True)
        fsoll = ['head1', 'head2']
        assert isinstance(fout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_whitespace, nc=-1, skip=1)
        fsoll = [[1.1, 1.2, 1.3, 1.4], [2.1, 2.2, 2.3, 2.4]]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_whitespace, nc=0, skip=1)
        fsoll = [[1.1, 1.2, 1.3, 1.4], [2.1, 2.2, 2.3, 2.4]]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_whitespace, nc=0, snc=-1, skip=1)
        fsoll = [[1.1, 1.2, 1.3, 1.4], [2.1, 2.2, 2.3, 2.4]]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_semicolon, nc=[1, 3], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_semicolon, nc=[1, 3], skip=1,
                     separator=';')
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_semicolon, nc=[1], snc=[0], skip=2,
                     header=True, strarr=True, squeeze=True)
        fsoll = ['head2', '1.2']
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        # cname, sname
        fout = fread(file_semicolon, cname='head2', skip=1,
                     fill=True, fill_value=-1, squeeze=True)
        fsoll = [1.2, 2.2]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        fout = fread(file_semicolon, cname=['head2', 'head4'],
                     skip=1, fill=True, fill_value=-1, squeeze=True)
        fsoll = [[1.2, 1.4], [2.2, 2.4]]
        assert isinstance(fout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))

        if os.path.exists(file_whitespace):
            os.remove(file_whitespace)
        if os.path.exists(file_semicolon):
            os.remove(file_semicolon)

    def test_sread(self):
        import os
        import numpy as np
        from pyjams import sread

        # Create float data
        file_whitespace = 'test_fsread_whitespace.dat'
        with open(file_whitespace, 'w') as ff:
            print('head1 head2 head3 head4', file=ff)
            print('1.1 1.2 1.3 1.4', file=ff)
            print('2.1 2.2 2.3 2.4', file=ff)

        # Some mixed data
        file_semicolon = 'test_fsread_semicolon.dat'
        with open(file_semicolon, 'w') as ff:
            print('head1;head2;head3;head4', file=ff)
            print('01.12.2012;1.2;name1;1.4', file=ff)
            print('01.01.2013;2.2;name2;2.4', file=ff)

        # Some mixed data with missing values
        file_comma = 'test_fsread_comma.dat'
        with open(file_comma, 'w') as ff:
            print('head1,head2,head3,head4,', file=ff)
            print('01.12.2012,1.2,name1,1.4,', file=ff)
            print('01.01.2013,,name2,,', file=ff)

        # Start tests

        sout = sread(file_whitespace, snc=[1, 3], skip=1)
        ssoll = [['1.2', '1.4'], ['2.2', '2.4']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_whitespace, nc=[1, 3], skip=1)
        ssoll = [['1.2', '1.4'], ['2.2', '2.4']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_whitespace, snc=-1, skip=1)
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_whitespace, snc=0, skip=1)
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_whitespace, nc=-1, skip=1)
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # strip
        sout = sread(file_whitespace, snc=-1, skip=1, strip=False)
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_whitespace, snc=-1, skip=1, strip='1')
        ssoll = [['.', '.2', '.3', '.4'], ['2.', '2.2', '2.3', '2.4']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_semicolon, snc=[0, 2], skip=1)
        ssoll = [['01.12.2012', 'name1'], ['01.01.2013', 'name2']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read header
        sout = sread(file_semicolon, snc=[0, 2], skip=1,
                     header=True)
        ssoll = [['head1', 'head3']]
        assert isinstance(sout, list)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_semicolon, snc=[0, 2], skip=1,
                     header=True, squeeze=True)
        ssoll = ['head1', 'head3']
        assert isinstance(sout, list)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_semicolon, snc=[0, 2], skip=2,
                     header=True, full_header=True, strarr=True)
        ssoll = [['head1;head2;head3;head4'],
                 ['01.12.2012;1.2;name1;1.4']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_semicolon, nc=[0, 2], skip=2,
                     header=True)
        ssoll = [['head1', 'head3'],
                 ['01.12.2012', 'name1']]
        assert isinstance(sout, list)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_comma, sname=['head1', 'head3'],
                     skip=1, fill=True, fill_value=-1, strarr=True,
                     header=True)
        ssoll = [['head1', 'head3']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_comma, cname=['head1', 'head3'],
                     skip=1, fill=True, fill_value=-1, strarr=True,
                     header=True)
        ssoll = [['head1', 'head3']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_comma, cname=['head2', 'head4'],
                     sname=['head1', 'head3'],
                     skip=1, fill=True, fill_value=-1, strarr=True,
                     header=True)
        ssoll = [['head1', 'head3']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # missing values
        sout = sread(file_comma, snc=[0, 2, 4], skip=2,
                     header=True, fill=True, sfill_value='tail')
        ssoll = [['head1', 'head3', 'tail'],
                 ['01.12.2012', 'name1', 'tail']]
        assert isinstance(sout, list)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_comma, snc=[0, 2, 4], skip=2,
                     header=True, fill=True, fill_value='tail')
        ssoll = [['head1', 'head3', 'tail'],
                 ['01.12.2012', 'name1', 'tail']]
        assert isinstance(sout, list)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        sout = sread(file_comma, nc=[0, 2, 4], skip=2,
                     header=True, fill=True, fill_value='head',
                     sfill_value='tail', strarr=True)
        ssoll = [['head1', 'head3', 'tail'],
                 ['01.12.2012', 'name1', 'tail']]
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        if os.path.exists(file_whitespace):
            os.remove(file_whitespace)
        if os.path.exists(file_semicolon):
            os.remove(file_semicolon)
        if os.path.exists(file_comma):
            os.remove(file_comma)

    def test_xread(self):
        import numpy as np
        from pyjams import xread, xlsread, xlsxread

        # Excel files
        file_xls  = 'tests/test_readexcel.xls'
        file_xlsx = 'tests/test_readexcel.xlsx'

        # Start tests - xls

        # Read sample as with fread - see fread for more examples
        fout, sout = xread(file_xls, nc=[1, 3], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, nc=2, skip=1, header=True)
        fsoll = [['head1', 'head2']]
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, nc=2, skip=1, header=True,
                           squeeze=True)
        fsoll = ['head1', 'head2']
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read sample as with sread - see sread for more examples
        fout, sout = xlsread(file_xls, snc=[1, 3], skip=1)
        fsoll = []
        ssoll = [['1.2', '1.4'], ['2.2', '2.4'],
                 ['3.2', '3.4'], ['4.2', '4.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read float and string columns - 1
        fout, sout = xread(file_xls, nc=1, snc=-1, skip=1)
        fsoll = [[1.1], [2.1], [3.1], [4.1]]
        ssoll = [['1.2', '1.3', '1.4'], ['2.2', '2.3', '2.4'],
                 ['3.2', '3.3', '3.4'], ['4.2', '4.3', '4.4']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, nc=-1, skip=1)
        fsoll = [[1.1, 1.2, 1.3, 1.4], [2.1, 2.2, 2.3, 2.4],
                 [3.1, 3.2, 3.3, 3.4], [4.1, 4.2, 4.3, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, snc=-1, skip=1)
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4'],
                 ['3.1', '3.2', '3.3', '3.4'], ['4.1', '4.2', '4.3', '4.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # strip
        fout, sout = xlsread(file_xls, snc=-1, skip=1, strip=False)
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4'],
                 ['3.1', '3.2', '3.3', '3.4'], ['4.1', '4.2', '4.3', '4.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, snc=-1, skip=1, strip='1')
        fsoll = []
        ssoll = [['.', '.2', '.3', '.4'], ['2.', '2.2', '2.3', '2.4'],
                 ['3.', '3.2', '3.3', '3.4'], ['4.', '4.2', '4.3', '4.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read float and string columns - 2
        fout, sout = xlsread(file_xls, sheet='Sheet3', nc=[1, 3], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet=2, nc=[1, 3], snc=[0, 2], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['name1', 'name5'], ['name2', 'name6'],
                 ['name3', 'name7'], ['name4', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet=2, nc=[1, 3], snc=[0, 2],
                             skip=1, transpose=True)
        fsoll = [[1.2, 2.2, 3.2, 4.2], [1.4, 2.4, 3.4, 4.4]]
        ssoll = [['name1', 'name2', 'name3', 'name4'],
                 ['name5', 'name6', 'name7', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                           skip=1, return_list=True)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['name1', 'name5'], ['name2', 'name6'],
                 ['name3', 'name7'], ['name4', 'name8']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet='Sheet3', nc=[1, 3], snc=-1,
                             skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['name1', 'name5'], ['name2', 'name6'],
                 ['name3', 'name7'], ['name4', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet='Sheet3', nc=-1, snc=[0, 2], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['name1', 'name5'], ['name2', 'name6'],
                 ['name3', 'name7'], ['name4', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet='Sheet3', nc=-1, snc=3, skip=1)
        fsoll = [[1.4], [2.4], [3.4], [4.4]]
        ssoll = [['name1', '1.2', 'name5'], ['name2', '2.2', 'name6'],
                 ['name3', '3.2', 'name7'], ['name4', '4.2', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet='Sheet3', nc=-1, snc=3, skip=1,
                           squeeze=True, return_list=True)
        fsoll = [1.4, 2.4, 3.4, 4.4]
        ssoll = [['name1', '1.2', 'name5'], ['name2', '2.2', 'name6'],
                 ['name3', '3.2', 'name7'], ['name4', '4.2', 'name8']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read header
        fout, sout = xlsread(file_xls, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                             skip=1, header=True)
        fsoll = [['head2', 'head4']]
        ssoll = [['head1', 'head3']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                           skip=1, header=True, squeeze=True)
        fsoll = ['head2', 'head4']
        ssoll = ['head1', 'head3']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                             skip=1, hskip=1, header=True)
        fsoll = []
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet='Sheet4', nc=[1, 3], snc=[0, 2],
                           skip=2, hskip=1, header=True, squeeze=True)
        fsoll = ['head2', 'head4']
        ssoll = ['head1', 'head3']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                             skip=2, header=True, full_header=True,
                             strarr=True)
        fsoll = [['head1', 'head2', 'head3', 'head4'],
                 ['name1', '1.2', 'name5', '1.4']]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                           skip=2, header=True)
        fsoll = [['head2', 'head4'], ['1.2', '1.4']]
        ssoll = [['head1', 'head3'], ['name1', 'name5']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                             skip=2, header=True, strarr=True)
        fsoll = [['head2', 'head4'], ['1.2', '1.4']]
        ssoll = [['head1', 'head3'], ['name1', 'name5']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet='Sheet3', nc=[1], snc=[0], skip=2,
                           header=True, squeeze=True)
        fsoll = ['head2', '1.2']
        ssoll = ['head1', 'name1']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet='Sheet3', nc=[1], snc=[0], skip=2,
                             header=True, strarr=True, squeeze=True)
        fsoll = ['head2', '1.2']
        ssoll = ['head1', 'name1']
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet=2, nc=[1, 3], snc=[0, 2], skip=2,
                           header=True, transpose=True)
        fsoll = [['head2', '1.2'],
                 ['head4', '1.4']]
        ssoll = [['head1', 'name1'],
                 ['head3', 'name5']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet=2, nc=[1, 3], snc=[0, 2], skip=2,
                             header=True, strarr=True, transpose=True)
        fsoll = [['head2', '1.2'],
                 ['head4', '1.4']]
        ssoll = [['head1', 'name1'],
                 ['head3', 'name5']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # missing values
        fout, sout = xread(file_xls, sheet='Sheet2', nc=[1, 3], skip=1,
                           fill=True, fill_value=-1)
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet='Sheet2', nc=[1, 3], skip=1,
                             fill=True, strarr=True)
        fsoll = [[np.nan, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # cname, sname
        fout, sout = xread(file_xls, sheet=1, cname='head2', snc=[0, 2],
                           skip=1, fill=True, fill_value=-1, sfill_value='NA',
                           squeeze=True)
        fsoll = [-1., 2.2, 3.2, 4.2]
        ssoll = [['1.1', '1.3'], ['2.1', '2.3'],
                 ['3.1', 'NA'], ['4.1', '4.3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet=1, cname=['head2', 'head4'],
                             snc=[0], skip=1, fill=True, fill_value=-1,
                             squeeze=True)
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = ['1.1', '2.1', '3.1', '4.1']
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet='Sheet2', cname=['head2', 'head4'],
                           snc=[0], skip=1, fill=True, fill_value=-1,
                           squeeze=True, return_list=True)
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = ['1.1', '2.1', '3.1', '4.1']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet='Sheet2',
                             cname=['head2', 'head4'],
                             snc=-1, skip=1, fill=True, fill_value=-1,
                             sfill_value='NA')
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['1.1', '1.3'], ['2.1', '2.3'],
                 ['3.1', 'NA'], ['4.1', '4.3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet='Sheet2', nc=[1, 3],
                           sname=['head1', 'head3'], skip=1, fill=True,
                           fill_value=-1, strarr=True, header=True)
        fsoll = [['head2', 'head4']]
        ssoll = [['head1', 'head3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsread(file_xls, sheet='Sheet2',
                             cname=['head2', 'head4'],
                             snc=-1, skip=1, header=True, full_header=True)
        fsoll = [['head1', 'head2', 'head3', 'head4']]
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet=1, nc=[1, 3], sname='head1',
                           skip=1, fill=True, fill_value=-1, strarr=True,
                           header=True)
        fsoll = [['head2', 'head4']]
        ssoll = [['head1']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # hstrip
        fout, sout = xlsread(file_xls, sheet=1, cname=['  head2', 'head4'],
                             snc=-1, skip=1, fill=True, fill_value=-1,
                             hstrip=False, sfill_value='NA')
        fsoll = [[1.4, 2.4, 3.4, 4.4]]
        ssoll = [['1.1', 'NA', '1.3'],
                 ['2.1', '2.2', '2.3'],
                 ['3.1', '3.2', 'NA'],
                 ['4.1', '4.2', '4.3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xls, sheet=1, cname=['  head2', 'head4'],
                           snc=-1, skip=1, fill=True, fill_value=-1,
                           sfill_value='NA', hstrip=True)
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['1.1', '1.3'], ['2.1', '2.3'],
                 ['3.1', 'NA'], ['4.1', '4.3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Start tests - xlsx

        # Read sample as with fread - see fread for more examples
        fout, sout = xread(file_xlsx, nc=[1, 3], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, nc=2, skip=1, header=True)
        fsoll = [['head1', 'head2']]
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, nc=2, skip=1, header=True,
                           squeeze=True)
        fsoll = ['head1', 'head2']
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read sample as with sread - see sread for more examples
        fout, sout = xlsxread(file_xlsx, snc=[1, 3], skip=1)
        fsoll = []
        ssoll = [['1.2', '1.4'], ['2.2', '2.4'],
                 ['3.2', '3.4'], ['4.2', '4.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read float and string columns - 1
        fout, sout = xread(file_xlsx, nc=1, snc=-1, skip=1)
        fsoll = [[1.1], [2.1], [3.1], [4.1]]
        ssoll = [['1.2', '1.3', '1.4'], ['2.2', '2.3', '2.4'],
                 ['3.2', '3.3', '3.4'], ['4.2', '4.3', '4.4']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, nc=-1, skip=1)
        fsoll = [[1.1, 1.2, 1.3, 1.4], [2.1, 2.2, 2.3, 2.4],
                 [3.1, 3.2, 3.3, 3.4], [4.1, 4.2, 4.3, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, snc=-1, skip=1)
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4'],
                 ['3.1', '3.2', '3.3', '3.4'], ['4.1', '4.2', '4.3', '4.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # strip
        fout, sout = xlsxread(file_xlsx, snc=-1, skip=1, strip=False)
        fsoll = []
        ssoll = [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4'],
                 ['3.1', '3.2', '3.3', '3.4'], ['4.1', '4.2', '4.3', '4.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, snc=-1, skip=1, strip='1')
        fsoll = []
        ssoll = [['.', '.2', '.3', '.4'], ['2.', '2.2', '2.3', '2.4'],
                 ['3.', '3.2', '3.3', '3.4'], ['4.', '4.2', '4.3', '4.4']]
        assert isinstance(fout, list)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read float and string columns - 2
        fout, sout = xlsxread(file_xlsx, sheet='Sheet3', nc=[1, 3], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet=2, nc=[1, 3], snc=[0, 2], skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['name1', 'name5'], ['name2', 'name6'],
                 ['name3', 'name7'], ['name4', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet=2, nc=[1, 3], snc=[0, 2],
                              skip=1, transpose=True)
        fsoll = [[1.2, 2.2, 3.2, 4.2], [1.4, 2.4, 3.4, 4.4]]
        ssoll = [['name1', 'name2', 'name3', 'name4'],
                 ['name5', 'name6', 'name7', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                           skip=1, return_list=True)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['name1', 'name5'], ['name2', 'name6'],
                 ['name3', 'name7'], ['name4', 'name8']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet='Sheet3', nc=[1, 3], snc=-1,
                              skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['name1', 'name5'], ['name2', 'name6'],
                 ['name3', 'name7'], ['name4', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet='Sheet3', nc=-1, snc=[0, 2],
                           skip=1)
        fsoll = [[1.2, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['name1', 'name5'], ['name2', 'name6'],
                 ['name3', 'name7'], ['name4', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet='Sheet3', nc=-1, snc=3, skip=1)
        fsoll = [[1.4], [2.4], [3.4], [4.4]]
        ssoll = [['name1', '1.2', 'name5'], ['name2', '2.2', 'name6'],
                 ['name3', '3.2', 'name7'], ['name4', '4.2', 'name8']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet='Sheet3', nc=-1, snc=3, skip=1,
                           squeeze=True, return_list=True)
        fsoll = [1.4, 2.4, 3.4, 4.4]
        ssoll = [['name1', '1.2', 'name5'], ['name2', '2.2', 'name6'],
                 ['name3', '3.2', 'name7'], ['name4', '4.2', 'name8']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # Read header
        fout, sout = xlsxread(file_xlsx, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                              skip=1, header=True)
        fsoll = [['head2', 'head4']]
        ssoll = [['head1', 'head3']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                           skip=1, header=True, squeeze=True)
        fsoll = ['head2', 'head4']
        ssoll = ['head1', 'head3']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                              skip=1, hskip=1, header=True)
        fsoll = []
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet='Sheet4', nc=[1, 3], snc=[0, 2],
                           skip=2, hskip=1, header=True, squeeze=True)
        fsoll = ['head2', 'head4']
        ssoll = ['head1', 'head3']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                              skip=2, header=True, full_header=True,
                              strarr=True)
        fsoll = [['head1', 'head2', 'head3', 'head4'],
                 ['name1', '1.2', 'name5', '1.4']]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                           skip=2, header=True)
        fsoll = [['head2', 'head4'], ['1.2', '1.4']]
        ssoll = [['head1', 'head3'], ['name1', 'name5']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet='Sheet3', nc=[1, 3], snc=[0, 2],
                              skip=2, header=True, strarr=True)
        fsoll = [['head2', 'head4'], ['1.2', '1.4']]
        ssoll = [['head1', 'head3'], ['name1', 'name5']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet='Sheet3', nc=[1], snc=[0], skip=2,
                           header=True, squeeze=True)
        fsoll = ['head2', '1.2']
        ssoll = ['head1', 'name1']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet='Sheet3', nc=[1], snc=[0],
                              skip=2, header=True, strarr=True, squeeze=True)
        fsoll = ['head2', '1.2']
        ssoll = ['head1', 'name1']
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet=2, nc=[1, 3], snc=[0, 2], skip=2,
                           header=True, transpose=True)
        fsoll = [['head2', '1.2'],
                 ['head4', '1.4']]
        ssoll = [['head1', 'name1'],
                 ['head3', 'name5']]
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet=2, nc=[1, 3], snc=[0, 2],
                              skip=2, header=True, strarr=True, transpose=True)
        fsoll = [['head2', '1.2'],
                 ['head4', '1.4']]
        ssoll = [['head1', 'name1'],
                 ['head3', 'name5']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # missing values
        fout, sout = xread(file_xlsx, sheet='Sheet2', nc=[1, 3], skip=1,
                           fill=True, fill_value=-1)
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet='Sheet2', nc=[1, 3], skip=1,
                              fill=True, strarr=True)
        fsoll = [[np.nan, 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = []
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # cname, sname
        fout, sout = xread(file_xlsx, sheet=1, cname='head2', snc=[0, 2],
                           skip=1, fill=True, fill_value=-1, sfill_value='NA',
                           squeeze=True)
        fsoll = [-1., 2.2, 3.2, 4.2]
        ssoll = [['1.1', '1.3'], ['2.1', '2.3'],
                 ['3.1', 'NA'], ['4.1', '4.3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet=1, cname=['head2', 'head4'],
                              snc=[0], skip=1, fill=True, fill_value=-1,
                              squeeze=True)
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = ['1.1', '2.1', '3.1', '4.1']
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet='Sheet2', cname=['head2', 'head4'],
                           snc=[0], skip=1, fill=True, fill_value=-1,
                           squeeze=True, return_list=True)
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = ['1.1', '2.1', '3.1', '4.1']
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet='Sheet2',
                              cname=['head2', 'head4'],
                              snc=-1, skip=1, fill=True, fill_value=-1,
                              sfill_value='NA')
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['1.1', '1.3'], ['2.1', '2.3'],
                 ['3.1', 'NA'], ['4.1', '4.3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet='Sheet2', nc=[1, 3],
                           sname=['head1', 'head3'], skip=1, fill=True,
                           fill_value=-1, strarr=True, header=True)
        fsoll = [['head2', 'head4']]
        ssoll = [['head1', 'head3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xlsxread(file_xlsx, sheet='Sheet2',
                              cname=['head2', 'head4'],
                              snc=-1, skip=1, header=True, full_header=True)
        fsoll = [['head1', 'head2', 'head3', 'head4']]
        ssoll = []
        assert isinstance(fout, list)
        assert isinstance(sout, list)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet=1, nc=[1, 3], sname='head1',
                           skip=1, fill=True, fill_value=-1, strarr=True,
                           header=True)
        fsoll = [['head2', 'head4']]
        ssoll = [['head1']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # hstrip
        fout, sout = xlsxread(file_xlsx, sheet=1, cname=['  head2', 'head4'],
                              snc=-1, skip=1, fill=True, fill_value=-1,
                              hstrip=False, sfill_value='NA')
        fsoll = [[1.4, 2.4, 3.4, 4.4]]
        ssoll = [['1.1', 'NA', '1.3'],
                 ['2.1', '2.2', '2.3'],
                 ['3.1', '3.2', 'NA'],
                 ['4.1', '4.2', '4.3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        fout, sout = xread(file_xlsx, sheet=1, cname=['  head2', 'head4'],
                           snc=-1, skip=1, fill=True, fill_value=-1,
                           sfill_value='NA', hstrip=True)
        fsoll = [[-1., 1.4], [2.2, 2.4], [3.2, 3.4], [4.2, 4.4]]
        ssoll = [['1.1', '1.3'], ['2.1', '2.3'],
                 ['3.1', 'NA'], ['4.1', '4.3']]
        assert isinstance(fout, np.ndarray)
        assert isinstance(sout, np.ndarray)
        self.assertEqual(_flatten(fout), _flatten(fsoll))
        self.assertEqual(_flatten(sout), _flatten(ssoll))

        # errors
        # both nc=-1 and snc=-1
        self.assertRaises(ValueError, xread, file_xlsx, nc=-1, snc=-1)
        # cannot open file (2)
        self.assertRaises(IOError, xread, 'dummy', nc=-1)
        # sheet not in file - name
        self.assertRaises(ValueError, xread, file_xls, 'Sheetx', nc=-1)
        self.assertRaises(ValueError, xread, file_xlsx, 'Sheetx', nc=-1)
        # sheet not in file - number
        self.assertRaises(ValueError, xread, file_xls, 99, nc=-1)
        self.assertRaises(ValueError, xread, file_xlsx, 99, nc=-1)


if __name__ == "__main__":
    unittest.main()
