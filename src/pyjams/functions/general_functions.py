#!/usr/bin/env python
"""
General functions that are not specialised for fitting, optimisation,
sensitivity analysis, etc.

The current functions are:
    curvature - Curvature of a function f: f''/(1+f'^2)^3/2

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2015-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

Functions:

.. autosummary::
   curvature

History
    * Written Mar 2015 by Matthias Cuntz (mc (at) macu (dot) de)
    * Changed to Sphinx docstring and numpydoc, Dec 2019, Matthias Cuntz
    * Split logistic and curvature into separate files,
      May 2020, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz

"""


__all__ = ['curvature']


# -----------------------------------------------------------
# curvature of function
def curvature(x, dfunc, d2func, *args, **kwargs):
    """
    Curvature of a function f

    .. math::
       f''/(1+f'^2)^{3/2}

    Parameters
    ----------
    x : array_like
        Independent variable to evalute curvature
    dfunc : callable
        Function giving first derivative of function *f*: *f'*, to be called
        `dfunc(x, *args, **kwargs)`
    d2func : callable
        Function giving second derivative of function *f*: *f''*, to be called
        `d2func(x, *args, **kwargs)`
    args : iterable
        Arguments passed to *dfunc* and *d2func*
    kwargs : dict
        Keyword arguments passed to *dfunc* and *d2func*

    Returns
    -------
    float or ndarray
        Curvature of function *f* at *x*

    Examples
    --------
    .. code-block:: python

       from pyjams.functions import dlogistic_offset, d2logistic_offset
       curvature(1., dlogistic_offset, d2logistic_offset,
                 [1., 2., 2., 1.])

    """
    return ( d2func(x, *args, **kwargs) /
             (1. + dfunc(x, *args, **kwargs)**2)**1.5 )


# -----------------------------------------------------------

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # import numpy as np
    # from logistic_function import dlogistic_offset, d2logistic_offset
    # from logistic_function import dlogistic_offset_p, d2logistic_offset_p
    # print(np.around(curvature(1., dlogistic_offset, d2logistic_offset,
    #                           1., 2., 2., 1.), 4))
    # # 0.2998
    # print(np.around(curvature(1., dlogistic_offset_p, d2logistic_offset_p,
    #                           [1., 2., 2., 1.]), 4))
    # # 0.2998
