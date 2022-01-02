#!/usr/bin/env python
"""
Convert integer to and from Roman numerals

This module was written by Matthias Cuntz while at Department of Computational
Hydrosystems, Helmholtz Centre for Environmental Research - UFZ, Leipzig,
Germany, and continued while at Institut National de Recherche pour
l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2012-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   int2roman
   roman2int

Notes
-----
Code adapted from Tim Valenta:
http://code.activestate.com/recipes/81611-roman-numerals


History
-------
    * Written May 2012 by Matthias Cuntz (mc (at) macu (dot) de)
    * Option lower in int2roman, May 2012, Matthias Cuntz
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Use assert mechanism, Apr 2014, Matthias Cuntz
    * Make numpy docstring format, Nov 2021, Matthias Cuntz
    * Ported into pyjams, Nov 2021, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz

"""


__all__ = ['int2roman', 'roman2int']


_numeral_map = list(zip((1000, 900, 500, 400, 100, 90,
                         50, 40, 10, 9, 5, 4, 1),
                        ('M', 'CM', 'D', 'CD', 'C', 'XC',
                         'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')))


def int2roman(i, lower=False):
    """
    Convert an integer to a Roman numeral

    Parameters
    ----------
    i : int
        Integer number to convert
    lower : bool, optional
        Output lowercase numerals if True,
        else output uppercase numerals (default)

    Returns
    -------
    str
        Roman numeral

    Notes
    -----
    Code adapted from Tim Valenta:
    http://code.activestate.com/recipes/81611-roman-numerals

    Examples
    --------
    >>> print(int2roman(1))
    I
    >>> print(int2roman(19))
    XIX
    >>> print(int2roman(159))
    CLIX
    >>> print(int2roman(159, lower=True))
    clix

    """
    assert i >= 1, 'integer must be > 0.'

    result = []
    for integer, numeral in _numeral_map:
        count = int(i // integer)
        result.append(numeral * count)
        i -= integer * count

    if lower:
        result = [ i.lower() for i in result ]

    return ''.join(result)


def roman2int(n):
    """
    Convert a Roman numeral to an integer

    Parameters
    ----------
    i : str
        String with Roman numeral to convert to integer

    Returns
    -------
    Int
        Integer

    Notes
    -----
    Input can only be one single numeral.

    Code adapted from Tim Valenta:
    http://code.activestate.com/recipes/81611-roman-numerals

    Examples
    --------
    >>> print(roman2int('I'))
    1
    >>> print(roman2int('i'))
    1
    >>> print(roman2int('iv'))
    4
    >>> print(roman2int('MCCCLIV'))
    1354

    """
    n = str(n).upper()
    result = 0
    i = 0
    for integer, numeral in _numeral_map:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)

    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
