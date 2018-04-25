#!/usr/bin/env python
from __future__ import division, absolute_import, print_function
"""
    Defines general functions, derivatives, etc.


    Definition
    ----------
    Current functions are:

    curvature             Curvature of function f: f''/(1+f'^2)^3/2
    logistic              logistic function L/(1+exp(-k(x-x0)))
    logistic_p
    dlogistic             First derivative of logistic function
    d2logistic            Second derivative of logistic function
    logistic_offset       logistic function with offset L/(1+exp(-k(x-x0))) + a
    logistic_offset_p
    dlogistic_offset      First derivative of logistic function with offset
    d2logistic_offset     Second derivative of logistic function with offset


    Input / Output
    --------------
    See the help of the individual functions for explanations of in/out, etc.


    Examples
    --------
    ToDo.


    License
    -------
    This file is part of the JAMS Python package.

    The JAMS Python package is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The JAMS Python package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with the JAMS Python package (cf. gpl.txt and lgpl.txt).
    If not, see <http://www.gnu.org/licenses/>.

    Copyright 2015 Matthias Cuntz


    History
    -------
    Written,  MC, Mar 2015
    Modified, MC, Dec 2017 - logistic_p, logistic_offset_p
"""
import numpy as np
import scipy.special as sp

__all__ = ['curvature',
           'logistic', 'dlogistic', 'd2logistic', 'logistic_p',
           'logistic_offset', 'dlogistic_offset', 'd2logistic_offset', 'logistic_offset_p']

# -----------------------------------------------------------
# curvature of function
def curvature(x, dfunc, d2func, *args, **kwargs):
    """ Curvature of function f''/(1+f'^2)^3/2
          x         independent variable
          dfunc     first derivative of function f: f'
          d2func    second derivative of function f: f''
          args      arguments for dfunc and d2func
          kwargs    keyword arguments for dfunc and d2func
    """
    return d2func(x, *args, **kwargs)/(1.+dfunc(x, *args, **kwargs)**2)**1.5

# -----------------------------------------------------------
# a/(1+exp(-b(x-c))) - logistic function
def logistic(x, L, k, x0):
    """ logistic function L/(1+exp(-k(x-x0)))
          x         independent variable
          L         maximum
          k         steepness
          x0        inflection point
    """
    return L*sp.expit(k*(x-x0))

def logistic_p(x, p):
  """ logistic function p[0]/(1+exp(-p[1](x-p[2])))
        x        independent variable
        p        array of size 3, parameters
  """
  return logistic(x, p[0], p[1], p[2])

# -----------------------------------------------------------
# 1st derivative of logistic functions
def dlogistic(x, L, k, x0):
    """ First derivative of logistic function L/(1+exp(-k(x-x0)))
          x         independent variable
          L         maximum
          k         steepness
          x0        inflection point
    """
    return k*L/(2.*(np.cosh(k*(x-x0))+1.))

# -----------------------------------------------------------
# 2nd derivative of logistic functions
def d2logistic(x, L, k, x0):
    """ Second derivative of logistic function L/(1+exp(-k(x-x0)))
          x         independent variable
          L         maximum
          k         steepness
          x0        inflection point
    """
    return -k**2 * L * np.sinh(k*(x-x0))/(2.*(np.cosh(k*(x-x0))+1.)**2)

# -----------------------------------------------------------
# L/(1+exp(-k(x-x0))) + a - logistic function with offset
def logistic_offset(x, L, k, x0, a):
    """ logistic function with offset L/(1+exp(-k(x-x0))) + a
          x         independent variable
          L         maximum
          k         steepness
          x0        inflection point
          a         offset
    """
    return L*sp.expit(k*(x-x0)) + a

def logistic_offset_p(x, p):
  """ logistic function with offset p[0]/(1+exp(-p[1](x-p[2]))) + p[3]
        x    independent variable
        p    4D-array of parameters
  """
  return logistic_offset(x, p[0], p[1], p[2], p[3])

# -----------------------------------------------------------
# 1st derivative of logistic functions with offset
def dlogistic_offset(x, L, k, x0, a):
    """ First derivative of logistic function L/(1+exp(-k(x-x0))) + a
          x         independent variable
          L         maximum
          k         steepness
          x0        inflection point
          a         offset
    """
    return k*L/(2.*(np.cosh(k*(x-x0))+1.))

# -----------------------------------------------------------
# 2nd derivative of logistic functions with offset
def d2logistic_offset(x, L, k, x0, a):
    """ Second derivative of logistic function L/(1+exp(-k(x-x0))) + a
          x         independent variable
          L         maximum
          k         steepness
          x0        inflection point
          a         offset
    """
    return -k**2 * L * np.sinh(k*(x-x0))/(2.*(np.cosh(k*(x-x0))+1.)**2)

# -----------------------------------------------------------

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
