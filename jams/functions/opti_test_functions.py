#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
"""
    Common test functions for parameter estimation and optimisation algorithms
    such as Rosenbrock and Griewank functions.

    Current functions are:
    ackley                >=2 params:     Ackley function, global optimum: 0.0 at origin
    goldstein_price       2 params:       Goldstein-Price function, global optimum: 3.0 (0.0,-1.0)
    griewank              2 or 10 params: Griewank function, global optimum: 0 at origin
    rastrigin             2 params:       Rastrigin function, global optimum: -2 (0,0)
    rosenbrock            2 params:       Rosenbrock function, global optimum: 0 (1,1)
    six_hump_camelback    2 params:       Six-hump Camelback function
                                          True Optima: -1.031628453489877, (-0.08983,0.7126), (0.08983,-0.7126)


    Input / Output
    --------------
    See the help of the individual functions for explanations of in/out, etc.


    Examples
    --------
    >>> from jams.autostring import astr
    >>> print(astr(griewank([0,0]),3,pp=True))
    0.000
    >>> print(astr(goldstein_price([0,-1]),3,pp=True))
    3.000


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

    Copyright 2012-2015 Matthias Cuntz


    History
    -------
    Written,  MC, Oct 2013 - test functions such as Rosenbrock, Griewank, etc.
    Modified, MC, Mar 2015 - in separate file
"""
import numpy as np

__all__ = ['ackley', 'griewank', 'goldstein_price', 'rastrigin', 'rosenbrock', 'six_hump_camelback']

# -----------------------------------------------------------

def ackley(x):
    '''
    This is the Ackley Function
    Global Optimum (n>=2): 0.0 at origin
    '''
    a = 20.0
    b = 0.2
    c = 2.0*np.pi

    n  = np.size(x)
    s1 = np.sum(x**2)
    s2 = np.sum(np.cos(c*x))
    f  = -a * np.exp(-b*np.sqrt(1.0/n*s1)) - np.exp(1.0/n*s2) + a + np.exp(1.0)

    return f

# -----------------------------------------------------------

def griewank(x):
    '''
    This is the Griewank Function (2-D or 10-D)
    Bound: X(i)=[-600,600], for i=1,2,...,10
    Global Optimum: 0, at origin
    '''
    nopt = np.size(x)
    #if (nopt == 2) | (nopt == 10):
    xx = x
    if nopt==2:
        d = 200.0
    else:
        d = 4000.0

    u1 = 0.0
    u2 = 1.0
    for j in range(nopt):
        u1 = u1 + xx[j]**2/d
        u2 = u2 * np.cos(xx[j]/np.sqrt(float(j+1)))

    f = u1 - u2 + 1
    return f

# -----------------------------------------------------------

def goldstein_price(x):
    '''
    This is the Goldstein-Price Function
    Bound X1=[-2,2], X2=[-2,2]
    Global Optimum: 3.0,(0.0,-1.0)
    '''
    x1 = x[0]
    x2 = x[1]
    u1 = (x1 + x2 + 1.0)**2
    u2 = 19. - 14.*x1 + 3.*x1**2 - 14.*x2 + 6.*x1*x2 +3.*x2**2
    u3 = (2.*x1 - 3.*x2)**2
    u4 = 18. - 32.*x1 + 12.*x1**2 + 48.*x2 -36.*x1*x2 + 27.*x2**2
    u5 = u1 * u2
    u6 = u3 * u4
    f = (1. + u5) * (30. + u6)
    return f

# -----------------------------------------------------------

def rastrigin(x):
    '''
    This is the Rastrigin Function
    Bound: X1=[-1,1], X2=[-1,1]
    Global Optimum: -2, (0,0)
    '''
    x1 = x[0]
    x2 = x[1]
    f = x1**2 + x2**2 - np.cos(18.0*x1) - np.cos(18.0*x2)
    return f

# -----------------------------------------------------------

def rosenbrock(x):
    '''
    This is the Rosenbrock Function
    Bound: X1=[-5,5], X2=[-2,8]; Global Optimum: 0,(1,1)
           bl=[-5 -5]; bu=[5 5]; x0=[1 1];
    '''

    x1 = x[0]
    x2 = x[1]
    a = 100.0
    f = a * (x2 - x1**2)**2 + (1 - x1)**2
    return f

# -----------------------------------------------------------

def six_hump_camelback(x):
    '''
    This is the Six-hump Camelback Function.
    Bound: X1=[-5,5], X2=[-5,5]
    True Optima: -1.031628453489877, (-0.08983,0.7126), (0.08983,-0.7126)
    '''
    x1 = x[0]
    x2 = x[1]
    f = (4 - 2.1*x1**2 + x1**4/3)*x1**2 + x1*x2 + (-4 + 4*x2**2)*x2**2
    return f

# -----------------------------------------------------------

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # print(griewank([0,0]))
    # #0.0
    # print(goldstein_price([0,-1]))
    # #3.0
