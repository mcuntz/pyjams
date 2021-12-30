#!/usr/bin/env python
"""
This is the unittest for fsread module.

python -m unittest -v tests/test_fsread.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_fsread.py

"""
import unittest


def _flatten(itr):
    import numpy as np
    return list(np.array(itr).flatten())


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
            print('', file=ff)
            print('2.1 2.2 2.3 2.4', file=ff)
            print('', file=ff)
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
        fsoll = [[1.2, 1.4], [0., 0.]]
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
        ssoll = [['1.1', '1.2', '1.3', '1.4']]
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


if __name__ == "__main__":
    unittest.main()
