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
   isundef
   filebase
   array2input
   input2array

History
    * Written input2array and array2input, Jan 2022, Matthias Cuntz
    * Added isundef, Mar 2022, Matthias Cuntz
    * Second input to array2input, Mar 2022, Matthias Cuntz
    * undef=np.nan by default, Apr 2022, Matthias Cuntz
    * Array masked or set to undef only if shapes of array and input agree in
      array2input, Apr 2022, Matthias Cuntz
    * Allow string arrays, Jun 2022, Matthias Cuntz
    * Allow undef=='' in isundef, Jun 2022, Matthias Cuntz
    * Single string input as 1-element array, Jun 2022, Matthias Cuntz
    * Allow undef=None, Jun 2022, Matthias Cuntz
    * undef=None by default, Jun 2022, Matthias Cuntz
    * Refine using undef=None with numpy.array and list,
      Jun 2022, Matthias Cuntz
    * Assure array is not 0d-array, Jun 2022, Matthias Cuntz
    * Correct treating of undef if two arrays given, Jan 2023, Matthias Cuntz
    * Add filebase, Mar 2023, Matthias Cuntz

"""
from collections.abc import Iterable
import numpy as np


__all__ = ['isundef', 'filebase', 'array2input', 'input2array']


def isundef(arr, undef):
    """
    Check if *arr* is undef

    Return arr==undef, taking care of NaN and Inf.

    Parameters
    ----------
    arr : scalar or numpy array
        Input scalar array
    undef : object
        Check if *arr == undef*.
        It is also possible to use None, '', np.nan, or np.inf for *undef*.

    Returns
    -------
    numpy array with *arr==undef*

    Examples
    --------
    >>> inp = [253.15, -9999.]
    >>> print(isundef(inp, -9999.))
    [False True]

    """
    if undef is None:
        return False
    elif not undef:
        return arr == undef
    elif np.isnan(undef):
        return np.isnan(arr)
    elif np.isinf(undef):
        return np.isinf(arr)
    else:
        return arr == undef


def filebase(f):
    """
    Returns filename without suffix

    Removes suffix from filename such as *.py* from *plot.py*.
    It removes directory information before searching for suffix using
    `os.path.basename`.

    Parameters
    ----------
    f : str
        Filename

    Returns
    -------
    filename without suffix such as .py

    Examples
    --------
    >>> f = 'plot_maps.py'
    >>> print(filebase(f))
    plot_maps

    """
    import os

    f1 = os.path.basename(f)
    if '.' in f1:
        return f[0:f.rfind(".")]
    else:
        return f


def array2input(outin, inp, inp2=None, undef=None):
    """
    Transforms numpy array to same type as input

    The numpy array *outin* will be transformed to the same type as *inp*.
    If shapes agree then masked values on *inp* will be masked on output
    and undefined values in *inp* will result in undefined output values.

    If *inp2* is given, then type of *inp* will take precedence,
    except if *inp* is a scalar or *inp2* is a masked array in which case
    the type of *inp2* will be taken.

    The function is supposed to work with :func:`input2array`, which makes the
    input a numpy array, setting masked values and undefined values to some
    default values to avoid math over- and underflow. `array2input`
    transforms the output back to the input format.

    Parameters
    ----------
    outin : numpy array
        Input array
    inp : scalar or iterable of numbers
        Original input variable that was transformed to numpy array with
        :func:`input2array`
    inp2 : scalar or iterable of numbers, optional
        Second input variable that was transformed to numpy array with
        :func:`input2array` (default: None)
    undef : float, optional
        Values in *inp* having value *undef* will result in ouput set to
        *undef* (default: None)

    Returns
    -------
    *outin* as same type as *inp*, or the type of *inp2* if *inp* is
    a scalar or *inp2* is a masked array

    Examples
    --------
    >>> inp = [253.15, -9999.]
    >>> inarray = input2array(inp, undef=-9999., default=273.15)
    >>> print(array2input(inarray, inp, undef=-9999.))
    [253.15 -9999.]

    """
    if inp2 is not None:
        if not isinstance(inp, Iterable):
            if isundef(inp, undef):
                outout = undef
            else:
                outout = outin
            return array2input(outout, inp2, undef=undef)
        elif isinstance(inp2, np.ma.MaskedArray):
            if isinstance(inp, np.ma.MaskedArray):
                outout = np.ma.where(isundef(inp, undef),
                                     undef, outin).filled(undef)
            elif isinstance(inp, str):
                outout = np.where(isundef(np.array([inp]), undef),
                                  undef, outin)
            else:
                outout = np.where(isundef(np.array(inp), undef), undef, outin)
            return array2input(outout, inp2, undef=undef)
        else:
            if isinstance(inp2, str):
                outout = np.where(isundef(np.array([inp2]), undef),
                                  undef, outin)
            else:
                outout = np.where(isundef(np.array(inp2), undef), undef, outin)
            return array2input(outout, inp, undef=undef)

    if isinstance(inp, Iterable):
        if isinstance(inp, np.ma.MaskedArray):
            if np.array(outin).shape == inp.shape:
                outout = np.ma.array(outin,
                                     mask=(isundef(inp, undef) | (inp.mask)))
            else:
                if isinstance(outin, np.ma.MaskedArray):
                    outout = outin
                else:
                    outout = np.ma.array(outin)
        elif isinstance(inp, np.ndarray):
            if np.array(outin).shape == inp.shape:
                if np.any(isundef(inp, undef)):
                    outout = np.where(isundef(inp, undef), undef, outin)
                else:
                    if isinstance(outin, np.ndarray):
                        outout = outin
                    else:
                        outout = np.array(outin)
            else:
                if isinstance(outin, np.ndarray):
                    outout = outin
                else:
                    outout = np.array(outin)
        elif isinstance(inp, str):
            if isundef(inp, undef):
                outout = undef
            else:
                if isinstance(outin, str):
                    outout = outin
                else:
                    outout = outin[0]
        else:
            if np.array(outin).shape == np.array(inp).shape:
                if np.any(isundef(np.array(inp), undef)):
                    outout = np.where(isundef(np.array(inp), undef),
                                      undef, outin)
                else:
                    outout = outin
            else:
                outout = outin
            try:
                outout = type(inp)(outout)
            except:  # pragma: no cover
                # unknown iterables so no cover
                pass
    else:
        # scalar / object
        if isundef(inp, undef):
            outout = undef
        else:
            try:
                outout = type(inp)(outin)
            except:  # pragma: no cover
                # unknown iterables so no cover
                if np.size(outin) == 1:
                    outout = outin[0]
                else:
                    outout = outin

    return outout


def input2array(inp, undef=None, default=1):
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
        (default: None)
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
            out = np.ma.where(isundef(inp, undef), default,
                              inp).filled(default)
        elif isinstance(inp, str):
            out = np.array([inp])
            out = np.where(isundef(out, undef), default, out)
        else:
            out = np.array(inp)
            out = np.where(isundef(out, undef), default, out)
    else:
        # scalar / object
        out = np.array([default]) if isundef(inp, undef) else np.array([inp])

    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
