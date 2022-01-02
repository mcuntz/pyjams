#!/usr/bin/env python
"""
Read numbers and strings from a file into 2D float and string arrays

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2009-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   fsread
   fread
   sread

History
    * Written fread and sread Jul 2009 by
      Matthias Cuntz (mc (at) macu (dot) de)
    * Keyword transpose, Feb 2012, Matthias Cuntz
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Removed bug when nc is list and contains 0, Nov 2014, Matthias Cuntz
    * Keyword hskip, Nov 2014, Matthias Cuntz
    * Do not use function lif, Feb 2015, Matthias Cuntz
    * nc can be tuple, Feb 2015, Matthias Cuntz
    * Large rewrite of code to improve speed: keep everything list until
      the very end, Feb 2015, Matthias Cuntz
    * Written fsread Feb 2015 by
      Matthias Cuntz (mc (at) macu (dot) de)
    * nc<=-1 removed in case of nc is list, Nov 2016, Matthias Cuntz
    * range instead of np.arange, Nov 2017, Matthias Cuntz
    * Keywords cname, sname, hstrip, rename file to infile,
      Nov 2017, Matthias Cuntz
    * full_header=True returns vector of strings, Nov 2017, Matthias Cuntz
    * Ignore unicode characters on read, Jun 2019, Matthias Cuntz
    * Make ignoring unicode characters campatible with Python 2 and Python 3,
      Jul 2019, Matthias Cuntz
    * Keywords encoding, errors with codecs module, Aug 2019, Matthias Cuntz
    * Return as list keyword, Dec 2019, Stephan Thober
    * Return as array as default, Jan 2020, Matthias Cuntz
    * Using numpy docstring format, May 2020, Matthias Cuntz
    * flake8 compatible, Mar 2021, Matthias Cuntz
    * Preserve trailing whitespace column delimiters, Mar 2021, Matthias Cuntz
    * Code refactoring, Sep 2021, Matthias Cuntz
    * Cleaner code by using local functions, Dec 2021, Matthias Cuntz
    * Make float and string code symmetric in behaviour,
      Dec 2021, Matthias Cuntz
    * Always return float and string, Dec 2021, Matthias Cuntz
    * Removed reform option, Dec 2021, Matthias Cuntz
    * Return always string array if not return as list option is set;
      strarr is only used with header=True now, Dec 2021, Matthias Cuntz
    * fread and sread are simple calls of fsread, Dec 2021, Matthias Cuntz
    * header returns also 2D arrays by default, Dec 2021, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz

"""
import codecs
import numpy as np


__all__ = ['fsread', 'fread', 'sread']


# --------------------------------------------------------------------


def _determine_indices(f, head, nres,
                       nc=0, cname=None,
                       snc=0, sname=None,
                       skip=0, cskip=0, hskip=0,
                       hstrip=True, sep=None):
    '''
    Determine the indices to be read from lines as floats and as strings

    Parameters
    ----------
    f : file handle
        Open file handle such as codecs.StreamReaderWriter
    nc : int or iterable, optional
        Number of columns to be read as floats [default: all (*nc<=0*)]. *nc*
        can be an int or a vector of column indexes, starting with 0. If
        *snc!=0*, then *nc* must be iterable, or -1 to read all other columns
        as floats.
    cname : iterable of str, optional
        Columns can be chosen by the values in the first header line;
        must be an iterable with strings.
    snc : int or iterable, optional
        Number of columns to be read as strings [default: none (*snc=0*)].
        *snc* can be an int or a vector of column indexes, starting with 0. If
        *nc!=0*, then *snc* must be an iterable, or -1 to read all other
        columns as strings.
    sname : iterable of str, optional
        Columns can be chosen by the values in the first header line;
        must be iterable with strings.
    skip : int, optional
        Number of lines to skip at the beginning of file (default: 0)
    cskip : int, optional
        Number of columns to skip at the beginning of each line (default: 0)
    hskip : int, optional
        Number of lines in skip that do not belong to header (default: 0)
    hstrip : bool, optional
        Strip header cells to match *cname* if True (default), else
        take the header cells literally.
    sep : str, optional
        Column separator. Whitespace is used if not given.

    Returns
    -------
    list, list
        list of indices (int) to be read as floats,
        list of indices (int) to be read as strings

    '''
    # Determine indices
    if nc != 0 and cname is not None:
        f.close()
        raise ValueError('nc and cname are mutually exclusive.')
    if snc != 0 and sname is not None:
        f.close()
        raise ValueError('snc and sname are mutually exclusive.')
    # cname or sname
    if (cname is not None) or (sname is not None):
        # from first header line
        if (skip-hskip) <= 0:
            f.close()
            raise ValueError('No header line left for choosing'
                             ' columns by name.')
        hres = head[0].split(sep)
        if hstrip:
            hres = [ h.strip() for h in hres ]
    if cname is not None:
        if not isinstance(cname, (list, tuple, np.ndarray)):
            cname = [cname]
        if hstrip:
            cname = [ h.strip() for h in cname ]
        nc = []
        for k in range(len(hres)):
            if hres[k] in cname:
                nc.append(k)
    if sname is not None:
        if not isinstance(sname, (list, tuple, np.ndarray)):
            sname = [sname]
        if hstrip:
            sname = [ h.strip() for h in sname ]
        snc = []
        for k in range(len(hres)):
            if hres[k] in sname:
                snc.append(k)
    if (isinstance(nc, (list, tuple, np.ndarray)) and
        isinstance(snc, (list, tuple, np.ndarray))):
        # both indices
        if np.in1d(nc, snc, assume_unique=True).any():
            raise ValueError('float and string indices overlap.')
        iinc  = nc
        iisnc = snc
    elif isinstance(nc, (list, tuple, np.ndarray)):
        # float indices
        iinc   = nc
        iirest = list(range(nres))
        for ii in iinc[::-1]:
            del iirest[ii]
        if snc <= -1:
            iisnc = iirest
        else:
            iisnc = iirest[:snc]
    elif isinstance(snc, (list, tuple, np.ndarray)):
        # string indices
        iisnc  = snc
        iirest = list(range(nres))
        for ii in iisnc[::-1]:
            del iirest[ii]
        if nc <= -1:
            iinc = iirest
        else:
            iinc = iirest[:nc]
    else:
        # no indices
        # cannot be nc=-1 and snc=-1
        if nc <= -1:
            if snc:
                iisnc = list(range(snc))
                iinc  = list(range(snc, nres))
            else:
                iisnc = []
                iinc  = list(range(cskip, nres))
        else:
            if snc <= -1:
                if nc:
                    iinc  = list(range(nc))
                    iisnc = list(range(nc, nres))
                else:
                    iinc  = []
                    iisnc = list(range(cskip, nres))
            else:
                # red snc first then nc
                iisnc = list(range(cskip, cskip+snc))
                iinc  = list(range(cskip+snc, cskip+snc+nc))
    return iinc, iisnc


def _line2var(res, var, iinc, strip=None):
    '''
    Append output list with selected elements from input list

    Parameters
    ----------
    res : list
        Line split by separator
    var : list
        List to append selected elements of *res*
    iinc : int, optional
        Indices in *res* to select

    Returns
    -------
    list
        *var* append by selected elements of *res*

    '''
    # Helper for append var with current line already splitted into list
    nres = len(res)
    if strip is None:
        tmp = [ res[i].strip('"').strip("'") for i in iinc if i < nres ]
    elif not strip:
        tmp = [ res[i] for i in iinc if i < nres ]
    else:
        tmp = [ res[i].strip(strip) for i in iinc if i < nres ]
    rest = len([ i for i in iinc if i >= nres ])
    if rest > 0:
        tmp.extend(['']*rest)
    var.append(tmp)
    return var


def _get_header(head, sep, iinc, iisnc,
                squeeze=False,
                fill=False, fill_value=0, sfill_value='',
                strip=None, full_header=False,
                transpose=False, strarr=False):
    '''
    Return header for float and string arrays

    Parameters
    ----------
    head : list
        List of input header files
    sep : str
        Column separator.
    iinc : list
        List of column indices for float array
    iisnc : list
        List of column indices for string array
    squeeze : bool, optional
        If set to *True*, the 2-dim array will be cleaned of degenerated
        dimension, possibly resulting in a vector, otherwise output is always
        2-dimensional.
    fill : bool, optional
        Fills in `fill_value` if True and not enough columns in input line,
        otherwise raises ValueError (default).
    fill_value : float, optional
         Value to fill in float array in empty cells or if not enough columns
         in line and *fill==True* (default: 0).
    sfill_value : str, optional
         Value to fill in string array in empty cells or if not enough columns
         in line and *fill==True* (default: '').
    strip : str, optional
        Strip strings with *str.strip(strip)*. If *strip* is *None*, quotes "
        and ' are stripped from input fields (default), otherwise the character
        in *strip* is stripped from the input fields.
        If *strip* is set to *False* then nothing is stripped and reading is
        about 30% faster.
    full_header : bool, optional
        Header will be a list of the header lines if set.
    transpose : bool, optional
        `fsread` reads in row-major format, i.e. the first dimension are the
        rows and second dimension are the columns *out(:nrow, :ncol)*. This
        will be transposed to column-major format *out(:ncol, :nrow)* if
        *transpose* is set.
    strarr : bool, optional
        Return header as numpy array rather than list.

    Returns
    -------
    list or array, list or array
        Header of float columns, header of string columns

    '''
    var  = list()
    svar = list()
    nhead = len(head)
    if nhead == 0:
        return var, svar
    if full_header:
        var = head
        if strarr:
            var  = np.array(var, dtype=str)
        return var, svar
    else:
        k = 0
        while k < nhead:
            hres = head[k].split(sep)
            nhres = len(hres)
            miianc = -1
            if iinc:
                miianc = max(miianc, max(iinc))
            if iisnc:
                miianc = max(miianc, max(iisnc))
            if (miianc >= nhres) and (not fill):
                raise ValueError(f'Line has not enough columns to index:'
                                 f' {head[k]}')
            if iinc:
                null = _line2var(hres, var, iinc, strip)
            if iisnc:
                null = _line2var(hres, svar, iisnc,
                                 False if strip is None else strip)
            k += 1
    if strarr:
        if var:
            var = np.array(var, dtype=str)
            if fill:
                var = np.where(var == '', fill_value, var)
            if squeeze:
                var = var.squeeze()
            if transpose:
                var = var.T
        if svar:
            svar = np.array(svar, dtype=str)
            if fill:
                svar = np.where(svar == '', sfill_value, svar)
            if squeeze:
                svar = svar.squeeze()
            if transpose:
                svar = svar.T
    else:
        if var:
            if fill:
                var = [ [ fill_value if i == '' else i for i in row ]
                        for row in var ]
            if squeeze:
                if len(var) == 1:
                    var = var[0]
                else:
                    maxi = max([ len(i) for i in var ])
                    if maxi == 1:
                        var = [ i[0] for i in var ]
            if transpose and isinstance(var[0], list):
                var = [ list(i) for i in zip(*var) ]  # transpose
        if svar:
            if fill:
                svar = [ [ sfill_value if i == '' else i for i in row ]
                         for row in svar ]
            if squeeze:
                if len(svar) == 1:
                    svar = svar[0]
                else:
                    maxi = max([ len(i) for i in svar ])
                    if maxi == 1:
                        svar = [ i[0] for i in svar ]
            if transpose and isinstance(svar[0], list):
                svar = [list(i) for i in zip(*svar)]  # transpose

    return var, svar


def _get_separator(f, separator=None, skip_blank=False, comment=None):
    '''
    Return the *skip-hskip* lines after the first *hskip* lines as header

    Parameters
    ----------
    f : file handle
        Open file handle such as codecs.StreamReaderWriter
    separator : str, optional
        Column separator. If not given, columns separators are (in order):
        comma (','), semicolon (';'), whitespace.
    comment : iterable, optional
         Line gets excluded if the first non-white character is in comment
         sequence. Sequence must be iterable such as string, list and tuple,
         such as '#' or ['#', '!'].
    skip_blank : bool, optional
        Continues reading after a blank line if True, else stops reading
        at the first blank line (default).

    Returns
    -------
    str, list
        Separator, split first line after header split with separator

    '''
    split = -1
    while True:
        s = f.readline().rstrip('\r\n')
        if len(s) == 0:
            if skip_blank:
                continue
            else:
                break
        if comment is not None:
            if (s[0] in comment):
                continue
        break
    if separator is None:
        sep = ','
        res = s.split(sep)
        nres = len(res)
        if nres == 1:
            sep = ';'
            res = s.split(sep)
            nres = len(res)
            if nres == 1:
                sep = None
                res = s.split(sep)
    else:
        sep = separator
        res = s.split(sep)
    return sep, res


def _read_head(f, skip=0, hskip=0):
    '''
    Return the *skip-hskip* lines after the first *hskip* lines as header

    Parameters
    ----------
    f : file handle
        Open file handle such as codecs.StreamReaderWriter
    skip : int, optional
        Number of lines to skip at the beginning of file (default: 0)
    hskip : int, optional
        Number of lines in skip that do not belong to header (default: 0)

    Returns
    -------
    list
        List with strings of file header

    '''
    head = []
    # Skip lines
    if hskip > 0:
        ihskip = 0
        while ihskip < hskip:
            tmp = f.readline()
            ihskip += 1
    # Read header
    if skip > 0:
        head = ['']*(skip-hskip)
        iskip = 0
        while iskip < (skip-hskip):
            head[iskip] = str(f.readline().rstrip('\r\n'))
            iskip += 1
    return head


# --------------------------------------------------------------------


def fsread(infile,
           nc=0, cname=None, snc=0, sname=None,
           skip=0, cskip=0, hskip=0,
           separator=None, squeeze=False,
           skip_blank=False, comment=None,
           fill=False, fill_value=0, sfill_value='',
           strip=None, hstrip=True,
           encoding='ascii', errors='ignore',
           header=False, full_header=False,
           transpose=False, strarr=False,
           return_list=False):
    """
    Read numbers and strings from a file into 2D float and string arrays

    Columns can be picked specifically by index or name. The header can be read
    separately with the (almost) same call as reading the numbers or string.

    Parameters
    ----------
    infile : str
        Source file name
    nc : int or iterable, optional
        Number of columns to be read as floats [default: none (*nc=0*)]. *nc*
        can be an int or a vector of column indexes, starting with 0. If
        *snc!=0*, then *nc* must be iterable, or -1 to read all other columns
        as floats. If both *nc* and *snc* are int, then first *snc* string
        columns will be read and then *nc* float columns will be read.
    cname : iterable of str, optional
        Columns for floats can be chosen by the values in the first header
        line; must be an iterable with strings.
    snc : int or iterable, optional
        Number of columns to be read as strings [default: none (*snc=0*)].
        *snc* can be an int or a vector of column indexes, starting with 0. If
        *nc!=0*, then *snc* must be iterable, or -1 to read all other columns
        as strings. If both *nc* and *snc* are int, then first *snc* string
        columns will be read and then *nc* float columns will be read.
    sname : iterable of str, optional
        Columns for strings can be chosen by the values in the first header
        line; must be an iterable with strings.
    skip : int, optional
        Number of lines to skip at the beginning of file (default: 0)
    cskip : int, optional
        Number of columns to skip at the beginning of each line (default: 0)
    hskip : int, optional
        Number of lines in skip that do not belong to header (default: 0)
    separator : str, optional
        Column separator. If not given, columns separators are (in order):
        comma (','), semicolon (';'), whitespace.
    squeeze : bool, optional
        If set to *True*, the 2-dim array will be cleaned of degenerated
        dimension, possibly resulting in a vector, otherwise output is always
        2-dimensional.
    skip_blank : bool, optional
        Continues reading after a blank line if True, else stops reading
        at the first blank line (default).
    comment : iterable, optional
        Line gets excluded if the first character is in comment sequence.
        Sequence must be iterable such as string, list and tuple, .e.g '#' or
        ['#', '!'].
    fill : bool, optional
        Fills in `fill_value` if True and not enough columns in input line,
        else raises ValueError (default).
    fill_value : float, optional
        Value to fill in float array in empty cells or if not enough columns
        in line and *fill==True* (default: 0).
    sfill_value : str, optional
        Value to fill in string array in empty cells or if not enough columns
        in line and *fill==True* (default: '').
    strip : str, optional
        Strip strings with *str.strip(strip)*. If *strip* is *None*, quotes "
        and ' are stripped from input fields (default), otherwise the character
        in *strip* is stripped from the input fields.
        If *strip* is set to *False* then nothing is stripped and reading is
        about 30% faster.
    hstrip : bool, optional
        Strip header cells to match *cname* if True (default), else take header
        cells literally.
    encoding : str, optional
        Specifies the encoding which is to be used for the file
        (default: 'ascii').
        Any encoding that encodes to and decodes from bytes is allowed.
    errors : str, optional
        Errors may be given to define the error handling during encoding
        of the file.
        Possible values are 'strict', 'replace', and 'ignore' (default).
    header : bool, optional
        Return header strings instead of numbers/strings in rest of file. This
        allows to use (almost) the same call to get values and header:

        .. code-block:: python

           head, shead = fsread(ifile, nc=1, snc=1, header=True)
           data, sdata = fsread(ifile, nc=1, snc=1)
           temp = data[:, head[0].index('temp')]

    full_header : bool, optional
        Header will be a list of the header lines if set.
    transpose : bool, optional
        `fsread` reads in row-major format, i.e. the first dimension are the
        rows and second dimension are the columns *out(:nrow, :ncol)*. This
        will be transposed to column-major format *out(:ncol, :nrow)* if
        *transpose* is set.
    strarr : bool, optional
        Return header as numpy array rather than list.
    return_list : bool, optional
        Return lists rather than arrays.

    Returns
    -------
    array of floats, array of strings
        First array is also string if header. Array is replaced by an empty
        string if this output is not demanded such as with *nc=0*.

    Notes
    -----
    If *header==True* then skip is counterintuitive because it is
    actually the number of header rows to be read. This is to
    be able to have the exact same call of the function, once
    with *header=False* and once with *header=True*.

    Blank lines are not filled but are taken as end of file if *fill=True*.

    Examples
    --------
    Create some data

    >>> filename = 'test.dat'
    >>> with open(filename,'w') as ff:
    ...     print('head1 head2 head3 head4', file=ff)
    ...     print('1.1 1.2 1.3 1.4', file=ff)
    ...     print('2.1 2.2 2.3 2.4', file=ff)

    Read sample with fread - see fread for more examples

    >>> a, sa = fsread(filename, nc=[1,3], skip=1)
    >>> print(a)
    [[1.2 1.4]
     [2.2 2.4]]
    >>> print(sa)
    []
    >>> a, sa = fsread(filename, nc=2, skip=1, header=True)
    >>> print(a)
    [['head1', 'head2']]
    >>> print(sa)
    []

    Read sample with sread - see sread for more examples

    >>> a, sa = fsread(filename, snc=[1,3], skip=1)
    >>> print(a)
    []
    >>> print(sa)
    [['1.2' '1.4'] ['2.2' '2.4']]

    Create some mixed data

    >>> with open(filename,'w') as ff:
    ...     print('head1 head2 head3 head4', file=ff)
    ...     print('01.12.2012 1.2 name1 1.4', file=ff)
    ...     print('01.01.2013 2.2 name2 2.4', file=ff)

    Read float and string columns in different ways

    >>> a, sa = fsread(filename, nc=[1,3], skip=1)
    >>> print(a)
    [[1.2 1.4]
     [2.2 2.4]]
    >>> print(sa)
    []
    >>> a, sa = fsread(filename, nc=[1,3], snc=[0,2], skip=1)
    >>> print(a)
    [[1.2 1.4]
     [2.2 2.4]]
    >>> print(sa)
    [['01.12.2012' 'name1']
     ['01.01.2013' 'name2']]
    >>> a, sa = fsread(filename, nc=[1,3], snc=-1, skip=1)
    >>> print(sa)
    [['01.12.2012' 'name1']
     ['01.01.2013' 'name2']]
    >>> a, sa = fsread(filename, nc=-1, snc=[0,2], skip=1)
    >>> print(a)
    [[1.2 1.4]
     [2.2 2.4]]

    >>> a, sa = fsread(filename, nc=[1,3], snc=-1, skip=1, return_list=True)
    >>> print(a)
    [[1.2, 1.4], [2.2, 2.4]]
    >>> print(sa)
    [['01.12.2012', 'name1'], ['01.01.2013', 'name2']]

    Read header

    >>> a, sa = fsread(filename, nc=[1,3], snc=[0,2], skip=1, header=True)
    >>> print(a)
    [['head2', 'head4']]
    >>> print(sa)
    [['head1', 'head3']]
    >>> a, sa = fsread(filename, nc=[1,3], snc=[0,2], skip=1, header=True,
    ...                squeeze=True)
    >>> print(a)
    ['head2', 'head4']
    >>> print(sa)
    ['head1', 'head3']

    Create some mixed data with missing values

    >>> with open(filename,'w') as ff:
    ...     print('head1,head2,head3,head4', file=ff)
    ...     print('01.12.2012,1.2,name1,1.4', file=ff)
    ...     print('01.01.2013,,name2,2.4', file=ff)

    >>> a, sa = fsread(filename, nc=[1,3], skip=1, fill=True, fill_value=-1)
    >>> print(a)
    [[ 1.2  1.4]
     [-1.   2.4]]
    >>> print(sa)
    []
    >>> a, sa = fsread(filename, nc=[1,3], skip=1, fill=True, fill_value=-1,
    ...                strarr=True)
    >>> print(a)
    [[ 1.2  1.4]
     [-1.   2.4]]
    >>> print(sa)
    []

    Read data using column names

    >>> a, sa = fsread(filename, cname='head2', snc=[0,2], skip=1, fill=True,
    ...                fill_value=-1, squeeze=True)
    >>> print(a)
    [ 1.2 -1. ]
    >>> print(sa)
    [['01.12.2012' 'name1']
     ['01.01.2013' 'name2']]
    >>> a, sa = fsread(filename, cname=['head2','head4'], snc=-1, skip=1,
    ...                fill=True, fill_value=-1)
    >>> print(a)
    [[ 1.2  1.4]
     [-1.   2.4]]
    >>> print(sa)
    [['01.12.2012' 'name1']
     ['01.01.2013' 'name2']]
    >>> # header
    >>> a, sa = fsread(filename, nc=[1,3], sname=['head1','head3'], skip=1,
    ...                fill=True, fill_value=-1, strarr=True, header=True)
    >>> print(a)
    [['head2' 'head4']]
    >>> print(sa)
    [['head1' 'head3']]
    >>> a, sa = fsread(filename, cname=['head2','head4'], snc=-1, skip=1,
    ...                header=True, full_header=True)
    >>> print(a)
    ['head1,head2,head3,head4']
    >>> print(sa)
    []
    >>> a, sa = fsread(filename, cname=['head2','head4'], snc=-1, skip=1,
    ...                fill=True, fill_value=-1, header=True, full_header=True)
    >>> print(a)
    ['head1,head2,head3,head4']
    >>> print(sa)
    []
    >>> a, sa = fsread(filename, cname=['  head2','head4'], snc=-1, skip=1,
    ...                fill=True, fill_value=-1, hstrip=False)
    >>> print(a)
    [[1.4]
     [2.4]]
    >>> print(sa)
    [['01.12.2012' '1.2' 'name1']
     ['01.01.2013' '' 'name2']]

    Clean up doctest

    >>> import os
    >>> os.remove(filename)

    """
    # Input error
    if isinstance(nc, int) and isinstance(snc, int):
        if (nc <= -1) and (snc <= -1):
            raise ValueError('nc and snc must be integer or list of indices;'
                             ' < 0 means to read the rest of the columns.'
                             ' nc and snc cannot both be < 0.')

    # Open file
    f = codecs.open(infile, 'r', encoding=encoding, errors=errors)

    # Read header and skip lines
    head = _read_head(f, skip, hskip)

    # Read first line to determine ncolumns and separator (if not set)
    sep, res = _get_separator(f, separator, skip_blank, comment)
    nres = len(res)
    if not nres:
        raise ValueError('No line to determine separator.')

    # Determine indices
    iinc, iisnc = _determine_indices(f, head, nres,
                                     nc=nc, cname=cname,
                                     snc=snc, sname=sname,
                                     skip=skip, cskip=cskip, hskip=hskip,
                                     hstrip=hstrip, sep=sep)
    aiinc = list(iinc)
    aiinc.extend(iisnc)
    miianc = max(aiinc)

    # Header
    if header:
        var, svar = _get_header(
            head, sep, iinc, iisnc,
            squeeze=squeeze,
            fill=fill, fill_value=fill_value, sfill_value=sfill_value,
            strip=strip, full_header=full_header,
            transpose=transpose, strarr=strarr)
        f.close()
        return var, svar

    # Values - first line
    if (miianc >= nres) and (not fill):
        f.close()
        if sep is None:
            sres = ' '.join(res)
        else:
            sres = sep.join(res)
        raise ValueError('Line has not enough columns to index: ' + sres)
    var  = list()
    svar = list()
    if iinc:
        null = _line2var(res, var, iinc, strip)
    if iisnc:
        null = _line2var(res, svar, iisnc, False if strip is None else strip)

    # Values - rest of file
    for line in f:
        s = str(line.rstrip('\r\n'))
        if len(s) == 0:
            if skip_blank:
                continue
            else:
                break
        if comment is not None:
            if (s[0] in comment):
                continue
        res = s.split(sep)
        nres = len(res)
        if (miianc >= nres) and (not fill):
            f.close()
            raise ValueError('Line has not enough columns to index: ' + s)
        if iinc:
            null = _line2var(res, var, iinc, strip)
        if iisnc:
            null = _line2var(res, svar, iisnc,
                             False if strip is None else strip)
    f.close()

    # Return correct shape and type
    if var:
        var = np.array(var, dtype=str)
        if fill:
            var = np.where(var == '', str(fill_value), var)
        var = np.array(var, dtype=float)
        if squeeze:
            var = var.squeeze()
        if transpose:
            var = var.T
        if return_list:
            if var.ndim == 1:
                var = [ i for i in var ]
            else:
                var = [ [ var[i, j] for j in range(var.shape[1]) ]
                        for i in range(var.shape[0]) ]
    if svar:
        svar = np.array(svar, dtype=str)
        if fill:
            svar = np.where(svar == '', sfill_value, svar)
        if squeeze:
            svar = svar.squeeze()
        if transpose:
            svar = svar.T
        if return_list:
            if svar.ndim == 1:
                svar = [ i for i in svar ]
            else:
                svar = [ [ svar[i, j] for j in range(svar.shape[1]) ]
                         for i in range(svar.shape[0]) ]

    return var, svar


# --------------------------------------------------------------------


def fread(infile,
          nc=0, cname=None, snc=0, sname=None,
          **kwargs):
    """
    Read floats from a file into 2D float array

    Columns can be picked specifically by index or name. The header can be read
    separately with the (almost) same call as reading the floats.

    Parameters
    ----------
    infile : str
        Source file name
    nc : int or iterable, optional
        Number of columns to be read as floats [default: all (*nc=0*)]. *nc*
        can be an int or a vector of column indexes, starting with 0.
        *nc<=0* reads all columns.
    cname : iterable of str, optional
        Columns for floats can be chosen by the values in the first header
        line; must be an iterable with strings.
    snc : int or iterable, optional
        Not used in fread; will be silently ignored.
    sname : iterable of str, optional
        Not used in fread; will be silently ignored.
    **kwargs : dict, optional
        All other keywords will be passed to `fsread`.

    Returns
    -------
    array of floats
        Array of numbers in file, or header.

    Notes
    -----
    If *header==True* then skip is counterintuitive because it is
    actually the number of header rows to be read. This is to
    be able to have the exact same call of the function, once
    with *header=False* and once with *header=True*.

    Blank lines are not filled but are taken as end of file if *fill=True*.

    Examples
    --------
    Create some data

    >>> filename = 'test.dat'
    >>> with open(filename,'w') as ff:
    ...     print('head1 head2 head3 head4', file=ff)
    ...     print('1.1 1.2 1.3 1.4', file=ff)
    ...     print('2.1 2.2 2.3 2.4', file=ff)

    Read sample file in different ways

    >>> # data
    >>> print(fread(filename, skip=1))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]]
    >>> print(fread(filename, skip=2))
    [[2.1 2.2 2.3 2.4]]
    >>> print(fread(filename, skip=1, cskip=1))
    [[1.2 1.3 1.4]
     [2.2 2.3 2.4]]
    >>> print(fread(filename, nc=2, skip=1, cskip=1))
    [[1.2 1.3]
     [2.2 2.3]]
    >>> print(fread(filename, nc=[1,3], skip=1))
    [[1.2 1.4]
     [2.2 2.4]]
    >>> print(fread(filename, nc=1, skip=1))
    [[1.1]
     [2.1]]
    >>> print(fread(filename, nc=1, skip=1, squeeze=True))
    [1.1 2.1]

    >>> # header
    >>> print(fread(filename, nc=2, skip=1, header=True))
    [['head1', 'head2']]
    >>> print(fread(filename, nc=2, skip=1, header=True, full_header=True))
    ['head1 head2 head3 head4']
    >>> print(fread(filename, nc=1, skip=2, header=True))
    [['head1'], ['1.1']]
    >>> print(fread(filename, nc=1, skip=2, header=True, squeeze=True))
    ['head1', '1.1']
    >>> print(fread(filename, nc=1, skip=2, header=True, strarr=True))
    [['head1']
     ['1.1']]

    Create data with blank lines

    >>> with open(filename, 'a') as ff:
    ...     print('', file=ff)
    ...     print('3.1 3.2 3.3 3.4', file=ff)

    >>> print(fread(filename, skip=1))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]]
    >>> print(fread(filename, skip=1, skip_blank=True, comment='#!'))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]
     [3.1 3.2 3.3 3.4]]

    Create data with comment lines

    >>> with open(filename, 'a') as ff:
    ...     print('# First comment', file=ff)
    ...     print('! Second 2 comment', file=ff)
    ...     print('4.1 4.2 4.3 4.4', file=ff)

    >>> print(fread(filename, skip=1))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]]
    >>> print(fread(filename, skip=1, nc=[2], skip_blank=True, comment='#'))
    [[1.3]
     [2.3]
     [3.3]
     [2. ]
     [4.3]]
    >>> print(fread(filename, skip=1, skip_blank=True, comment='#!'))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]
     [3.1 3.2 3.3 3.4]
     [4.1 4.2 4.3 4.4]]
    >>> print(fread(filename, skip=1, skip_blank=True, comment=('#','!')))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]
     [3.1 3.2 3.3 3.4]
     [4.1 4.2 4.3 4.4]]
    >>> print(fread(filename, skip=1, skip_blank=True, comment=['#','!']))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]
     [3.1 3.2 3.3 3.4]
     [4.1 4.2 4.3 4.4]]

    Add a line with fewer columns

    >>> with open(filename, 'a') as ff:
    ...     print('5.1 5.2', file=ff)

    >>> print(fread(filename, skip=1))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]]
    >>> print(fread(filename, skip=1, skip_blank=True, comment='#!',
    ...             fill=True, fill_value=-1))
    [[ 1.1  1.2  1.3  1.4]
     [ 2.1  2.2  2.3  2.4]
     [ 3.1  3.2  3.3  3.4]
     [ 4.1  4.2  4.3  4.4]
     [ 5.1  5.2 -1.  -1. ]]

    >>> # transpose
    >>> print(fread(filename, skip=1))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]]
    >>> print(fread(filename, skip=1, transpose=True))
    [[1.1 2.1]
     [1.2 2.2]
     [1.3 2.3]
     [1.4 2.4]]

    Create some more data with Nan and Inf

    >>> filename1 = 'test1.dat'
    >>> with open(filename1,'w') as ff:
    ...     print('head1 head2 head3 head4', file=ff)
    ...     print('1.1 1.2 1.3 1.4', file=ff)
    ...     print('2.1 nan Inf "NaN"', file=ff)

    Treat Nan and Inf with automatic strip of " and '

    >>> print(fread(filename1, skip=1, transpose=True))
    [[1.1 2.1]
     [1.2 nan]
     [1.3 inf]
     [1.4 nan]]

    Create some more data with escaped numbers

    >>> filename2 = 'test2.dat'
    >>> with open(filename2,'w') as ff:
    ...     print('head1 head2 head3 head4', file=ff)
    ...     print('"1.1" "1.2" "1.3" "1.4"', file=ff)
    ...     print('2.1 nan Inf "NaN"', file=ff)

    Strip

    >>> print(fread(filename2,  skip=1,  transpose=True,  strip='"'))
    [[1.1 2.1]
     [1.2 nan]
     [1.3 inf]
     [1.4 nan]]

    Create more data with an extra (shorter) header line

    >>> filename3 = 'test3.dat'
    >>> with open(filename3,'w') as ff:
    ...     print('Extra header', file=ff)
    ...     print('head1 head2 head3 head4', file=ff)
    ...     print('1.1 1.2 1.3 1.4', file=ff)
    ...     print('2.1 2.2 2.3 2.4', file=ff)

    >>> print(fread(filename3, skip=2, hskip=1))
    [[1.1 1.2 1.3 1.4]
     [2.1 2.2 2.3 2.4]]
    >>> print(fread(filename3, nc=2, skip=2, hskip=1, header=True))
    [['head1', 'head2']]

    >>> # cname
    >>> print(fread(filename, cname='head2', skip=1, skip_blank=True,
    ...             comment='#!', squeeze=True))
    [1.2 2.2 3.2 4.2 5.2]
    >>> print(fread(filename, cname=['head1','head2'], skip=1,
    ...             skip_blank=True, comment='#!'))
    [[1.1 1.2]
     [2.1 2.2]
     [3.1 3.2]
     [4.1 4.2]
     [5.1 5.2]]
    >>> print(fread(filename, cname=['head1','head2'], skip=1, skip_blank=True,
    ...             comment='#!', header=True))
    [['head1', 'head2']]
    >>> print(fread(filename, cname=['head1','head2'], skip=1, skip_blank=True,
    ...             comment='#!', header=True, full_header=True))
    ['head1 head2 head3 head4']
    >>> print(fread(filename, cname=['  head1','head2'], skip=1,
    ...             skip_blank=True, comment='#!', hstrip=False))
    [[1.2]
     [2.2]
     [3.2]
     [4.2]
     [5.2]]

    Clean up doctest

    >>> import os
    >>> os.remove(filename)
    >>> os.remove(filename1)
    >>> os.remove(filename2)
    >>> os.remove(filename3)

    """
    # nc=0 in fread and sread reads all columns
    if (nc == 0) and (cname is None):
        nc = -1
    dat, sdat = fsread(infile, nc=nc, cname=cname, snc=0, sname=None,
                       **kwargs)
    return dat


# --------------------------------------------------------------------


def sread(infile,
          nc=0, cname=None, snc=0, sname=None,
          fill_value='', sfill_value='',
          header=False, full_header=False,
          **kwargs):
    """
    Read strings from a file into 2D string array

    Columns can be picked specifically by index or name. The header can be read
    separately with the (almost) same call as reading the strings.

    Parameters
    ----------
    infile : str
        Source file name
    nc : int or iterable, optional
        Number of columns to be read as strings [default: all (*nc=0*)]. *nc*
        can be an int or a vector of column indexes, starting with 0.
        *nc<=0* reads all columns.
        *snc* takes precedence if *nc* and *snc* are set.
    cname : iterable of str, optional
        Columns for floats can be chosen by the values in the first header
        line; must be an iterable with strings.
        *sname* takes precedence if *cname* and *sname* are set.
    snc : int or iterable, optional
        Number of columns to be read as strings [default: all (*snc=0*)].
        *snc* can be an int or a vector of column indexes, starting with 0.
        *snc<=0* reads all columns.
        *snc* takes precedence if *nc* and *snc* are set.
    sname : iterable of str, optional
        Columns for strings can be chosen by the values in the first header
        line; must be an iterable with strings.
        *sname* takes precedence if *cname* and *sname* are set.
    fill_value : str, optional
        Value to fill in string array in empty cells or if not enough columns
        in line and *fill==True* (default: '').
        *sfill_value* takes precedence if *fill_value* and *sfill_value* are
        set.
    sfill_value : str, optional
        Value to fill in string array in empty cells or if not enough columns
        in line and *fill==True* (default: '').
        *sfill_value* takes precedence if *fill_value* and *sfill_value* are
        set.
    fill_value : float, optional
        value to fill in array in empty cells or if not enough columns in line
        and `fill==True` (default: '').
    header : bool, optional
        Return header strings instead of strings in rest of file. This
        allows to use (almost) the same call to get values and header:

        .. code-block:: python

           shead = sread(ifile, nc=2, header=True)
           sdata = sread(ifile, nc=2)
           date = sdata[:, head[0].index('Datetime')]

    full_header : bool, optional
        Header will be a list of the header lines if set.
    **kwargs : dict, optional
        All other keywords will be passed to `fsread`.

    Returns
    -------
    array of strings
        Array of strings in file, or of header.

    Notes
    -----
    If *header==True* then skip is counterintuitive because it is
    actually the number of header rows to be read. This is to
    be able to have the exact same call of the function, once
    with *header=False* and once with *header=True*.

    Blank lines are not filled but are taken as end of file if *fill=True*.

    Examples
    --------
    Create some data

    >>> filename = 'test.dat'
    >>> with open(filename,'w') as ff:
    ...     print('head1 head2 head3 head4', file=ff)
    ...     print('1.1 1.2 1.3 1.4', file=ff)
    ...     print('2.1 2.2 2.3 2.4', file=ff)

    Read sample file in different ways

    >>> # data
    >>> print(sread(filename, skip=1))
    [['1.1' '1.2' '1.3' '1.4']
     ['2.1' '2.2' '2.3' '2.4']]
    >>> print(sread(filename, skip=2, return_list=True))
    [['2.1', '2.2', '2.3', '2.4']]
    >>> print(sread(filename, skip=2))
    [['2.1' '2.2' '2.3' '2.4']]
    >>> print(sread(filename, skip=1, cskip=1))
    [['1.2' '1.3' '1.4'] ['2.2' '2.3' '2.4']]
    >>> print(sread(filename, nc=2, skip=1, cskip=1))
    [['1.2' '1.3'] ['2.2' '2.3']]
    >>> print(sread(filename, nc=[1,3], skip=1))
    [['1.2' '1.4'] ['2.2' '2.4']]
    >>> print(sread(filename, nc=1, skip=1))
    [['1.1'] ['2.1']]
    >>> print(sread(filename, nc=1, skip=1, squeeze=True))
    ['1.1' '2.1']

    >>> # header
    >>> print(sread(filename, nc=2, skip=1, header=True))
    [['head1', 'head2']]
    >>> print(sread(filename, nc=2, skip=1, header=True, full_header=True))
    ['head1 head2 head3 head4']
    >>> print(sread(filename, nc=1, skip=2, header=True))
    [['head1'], ['1.1']]
    >>> print(sread(filename, nc=1, skip=2, header=True, squeeze=True))
    ['head1', '1.1']
    >>> print(sread(filename, nc=1, skip=2, header=True, squeeze=True,
    ...             strarr=True))
    ['head1' '1.1']
    >>> print(sread(filename, nc=1, skip=2, header=True, squeeze=True,
    ...             transpose=True))
    ['head1', '1.1']

    Data with blank lines

    >>> with open(filename, 'a') as ff:
    ...     print('', file=ff)
    ...     print('3.1 3.2 3.3 3.4', file=ff)

    >>> print(sread(filename, skip=1))
    [['1.1' '1.2' '1.3' '1.4'] ['2.1' '2.2' '2.3' '2.4']]
    >>> print(sread(filename, skip=1, skip_blank=True))
    [['1.1' '1.2' '1.3' '1.4'] ['2.1' '2.2' '2.3' '2.4']
    ['3.1' '3.2' '3.3' '3.4']]
    >>> print(sread(filename, skip=1))
    [['1.1' '1.2' '1.3' '1.4']
     ['2.1' '2.2' '2.3' '2.4']]
    >>> print(sread(filename, skip=1, transpose=True))
    [['1.1' '2.1']
     ['1.2' '2.2']
     ['1.3' '2.3']
     ['1.4' '2.4']]
    >>> print(sread(filename, skip=1, transpose=True))
    [['1.1' '2.1'] ['1.2' '2.2'] ['1.3' '2.3'] ['1.4' '2.4']]

    Data with comment lines

    >>> with open(filename, 'a') as ff:
    ...     print('# First comment', file=ff)
    ...     print('! Second second comment', file=ff)
    ...     print('4.1 4.2 4.3 4.4', file=ff)

    >>> print(sread(filename, skip=1))
    [['1.1' '1.2' '1.3' '1.4'] ['2.1' '2.2' '2.3' '2.4']]
    >>> print(sread(filename, skip=1, skip_blank=True, comment='#'))
    [['1.1' '1.2' '1.3' '1.4'] ['2.1' '2.2' '2.3' '2.4']
    ['3.1' '3.2' '3.3' '3.4'] ['!' 'Second' 'second' 'comment']
    ['4.1' '4.2' '4.3' '4.4']]
    >>> print(sread(filename, skip=1, skip_blank=True, comment='#!'))
    [['1.1' '1.2' '1.3' '1.4'] ['2.1' '2.2' '2.3' '2.4']
    ['3.1' '3.2' '3.3' '3.4'] ['4.1' '4.2' '4.3' '4.4']]
    >>> print(sread(filename, skip=1, skip_blank=True, comment=('#','!')))
    [['1.1' '1.2' '1.3' '1.4'] ['2.1' '2.2' '2.3' '2.4']
    ['3.1' '3.2' '3.3' '3.4'] ['4.1' '4.2' '4.3' '4.4']]
    >>> print(sread(filename, skip=1, skip_blank=True, comment=['#','!']))
    [['1.1' '1.2' '1.3' '1.4'] ['2.1' '2.2' '2.3' '2.4']
    ['3.1' '3.2' '3.3' '3.4'] ['4.1' '4.2' '4.3' '4.4']]

    Data with escaped numbers

    >>> filename2 = 'test2.dat'
    >>> with open(filename2,'w') as ff:
    ...     print('"head1" "head2" "head3" "head4"', file=ff)
    ...     print('"1.1" "1.2" "1.3" "1.4"', file=ff)
    ...     print('2.1 nan Inf "NaN"', file=ff)

    >>> print(sread(filename2, skip=1, transpose=True, strip='"'))
    [['1.1' '2.1']
     ['1.2' 'nan']
     ['1.3' 'Inf']
     ['1.4' 'NaN']]

    Data with an extra (shorter) header line

    >>> filename3 = 'test3.dat'
    >>> with open(filename3,'w') as ff:
    ...     print('Extra header', file=ff)
    ...     print('head1 head2 head3 head4', file=ff)
    ...     print('1.1 1.2 1.3 1.4', file=ff)
    ...     print('2.1 2.2 2.3 2.4', file=ff)

    >>> print(sread(filename3, skip=2, return_list=True))
    [['1.1', '1.2', '1.3', '1.4'], ['2.1', '2.2', '2.3', '2.4']]
    >>> print(sread(filename3, skip=2, hskip=1))
    [['1.1' '1.2' '1.3' '1.4'] ['2.1' '2.2' '2.3' '2.4']]
    >>> print(sread(filename3, nc=2, skip=2, hskip=1, header=True))
    [['head1', 'head2']]

    Data with missing values

    >>> filename4 = 'test4.dat'
    >>> with open(filename4,'w') as ff:
    ...     print('Extra header', file=ff)
    ...     print('head1,head2,head3,head4', file=ff)
    ...     print('1.1,1.2,1.3,1.4', file=ff)
    ...     print('2.1,,2.3,2.4', file=ff)

    >>> print(sread(filename4, skip=2, return_list=True))
    [['1.1', '1.2', '1.3', '1.4'], ['2.1', '', '2.3', '2.4']]
    >>> print(sread(filename4, skip=2, fill=True, fill_value='-1'))
    [['1.1' '1.2' '1.3' '1.4'] ['2.1' '-1' '2.3' '2.4']]

    >>> # cname
    >>> print(sread(filename, cname='head2', skip=1, skip_blank=True,
    ...             comment='#!', squeeze=True))
    ['1.2' '2.2' '3.2' '4.2']
    >>> print(sread(filename, cname=['head1','head2'], skip=1, skip_blank=True,
    ...             comment='#!'))
    [['1.1' '1.2'] ['2.1' '2.2'] ['3.1' '3.2'] ['4.1' '4.2']]
    >>> print(sread(filename, cname=['head1','head2'], skip=1, skip_blank=True,
    ...             comment='#!', header=True))
    [['head1', 'head2']]
    >>> print(sread(filename, cname=['head1','head2'], skip=1, skip_blank=True,
    ...             comment='#!', header=True, full_header=True))
    ['head1 head2 head3 head4']
    >>> print(sread(filename, cname=['  head1','head2'], skip=1,
    ...             skip_blank=True, comment='#!', hstrip=False))
    [['1.2'] ['2.2'] ['3.2'] ['4.2']]

    Clean up doctest

    >>> import os
    >>> os.remove(filename)
    >>> os.remove(filename2)
    >>> os.remove(filename3)
    >>> os.remove(filename4)

    """
    # string keywords overwrite float keywords
    if snc != 0:
        nc = snc
    if sname is not None:
        cname = sname
    if sfill_value:
        fill_value = sfill_value
    # nc=0 in fread and sread reads all columns
    if (nc == 0) and (cname is None):
        nc = -1
    dat, sdat = fsread(infile,
                       nc=0, cname=None, snc=nc, sname=cname,
                       fill_value=0, sfill_value=fill_value,
                       header=header, full_header=full_header,
                       **kwargs)
    if header and full_header:
        return dat
    else:
        return sdat


# --------------------------------------------------------------------


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
