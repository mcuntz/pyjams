#!/usr/bin/env python
"""
Helper functions for pyjams library

This module was written by Matthias Cuntz while at Institut National de
Recherche pour l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy,
France.

:copyright: Copyright 2022- Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   array2input
   input2array

History
    * Written input2array and array2input, Jan 2022, Matthias Cuntz

"""
from collections.abc import Iterable
import numpy as np


__all__ = ['array2input', 'input2array']


def array2input(outin, inp, undef=-9999.):
    """
    Transforms numpy array to same type as input

    The numpy array *outin* will be transformed to the same type as *inp*.
    Masked values on *inp* will be masked on output, undefined values in *inp*
    will result in undefined output values.

    The function is supposed to work with :func:`input2array`, which makes the
    input a numpy array, setting masked values and undefined values to some
    default values to avoid math over- and underflow. `array2input` transforms
    the output back to the input format.

    Parameters
    ----------
    outin : numpy array
        Input array
    inp : scalar or iterable of numbers
        Original input variable that was transformed to numpy array with
        :func:`input2array`
    undef : float, optional
        Values in *inp* having value *undef* will result in ouput set to
        *undef* (default: numpy.nan)

    Returns
    -------
    *outin* as same type as *inp*

    Examples
    --------
    >>> inp = [253.15, -9999.]
    >>> inarray = input2array(inp, undef=-9999., default=273.15)
    >>> print(array2input(inarray, inp, undef=-9999.))
    [253.15 -9999.]

    """
    if isinstance(inp, Iterable):
        if isinstance(inp, np.ma.MaskedArray):
            outout = np.ma.array(outin, mask=((inp == undef) | (inp.mask)))
        elif isinstance(inp, np.ndarray):
            outout = np.where(inp == undef, undef, outin)
        else:
            outout = np.where(np.array(inp) == undef, undef, outin)
            try:
                outout = type(inp)(outout)
            except:  # pragma: no cover
                # unknown iterables so no cover
                pass
    else:
        if inp == undef:
            outout = undef
        else:
            try:
                outout = type(inp)(outin)
            except:  # pragma: no cover
                # unknown iterables so no cover
                outout = outin

    return outout


def input2array(inp, undef=-9999., default=1):
    """
    Makes numpy array from iterable or scalar input with masked or undef values
    are set to a default value

    The input variable will be transformed to a numpy array so that numpy
    functions and similar will work on all input. Undefined and masked values
    will be set to a default value to avoid math over- and underflow.

    The function is supposed to work with :func:`array2input`, which sets
    the output to the same type as the input; masked values on input will be
    masked on output, undefined input values will result in undefined output
    values.

    Parameters
    ----------
    inp : scalar or iterable of numbers
        Input variable to transform to numpy array
    undef : float, optional
        Values in *inp* having value *undef* will be set to *default*
        (default: numpy.nan)
    default : number
        Values in *inp* having value *undef* will be set to *default*
        (default: 1)

    Returns
    -------
    ndarray
        Input variable transformed to numpy array with values *undef* set to
        *default*

    Examples
    --------
    >>> print(input2array([253.15, -9999.], undef=-9999., default=273.15))
    [253.15 273.15]

    """
    if isinstance(inp, Iterable):
        if isinstance(inp, np.ma.MaskedArray):
            out = np.ma.where(inp == undef, default, inp).filled(default)
        else:
            out = np.array(inp)
            out = np.where(out == undef, default, out)
    else:
        # scalar
        out = np.array(default) if (inp == undef) else np.array(inp)

    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
