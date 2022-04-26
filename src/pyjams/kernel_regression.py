#!/usr/bin/env python
"""
Multi-dimensional non-parametric kernel regression

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2012-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   kernel_regression_h
   kernel_regression

History
    * Written, Jun 2012 by  Matthias Cuntz - mc (at) macu (dot) de,
      inspired by Matlab routines of Yingying Dong, Boston College and
      Yi Cao, Cranfield University
    * Assert correct input, Apr 2014, Matthias Cuntz
    * Corrected bug in _boot_h: x.size->x.shape[0], Jan 2018, Matthias Cuntz
    * Code refactoring, Sep 2021, Matthias Cuntz
    * Use format strings, Apr 2022, Matthias Cuntz
    * Use minimize with method TNC instead of fmin_tnc,
      Apr 2022, Matthias Cuntz
    * Use helper function array2input to assure correct output type,
      Apr 2022, Matthias Cuntz
    * Return scalar h if 1-dimensional, Apr 2022, Matthias Cuntz
    * Output type is same as y instead of x or xout, Apr 2022, Matthias Cuntz

"""
import numpy as np
import scipy.optimize as opt
from .division import division
from .helper import array2input
# from division import division
# from helper import array2input


__all__ = ['kernel_regression_h', 'kernel_regression']


def _nadaraya_watson(z, y):
    """
    Helper function that calculates the Nadaraya-Watson estimator
    for a given kernel.
    Until now there is only the gaussian kernel.

    """
    kerf = 1. / np.sqrt(2. * np.pi) * np.exp(-0.5 * z * z)
    w = np.prod(kerf, 1)
    out = division(np.dot(w, y), np.sum(w), np.nan)

    return out


def _cross_valid_h(h, x, y):
    """
    Helper function that calculates cross-validation function for the
    Nadaraya-Watson estimator, which is basically the mean square error
    where model estimate is replaced by the jackknife estimate
    (Hardle and Muller 2000).

    """
    n = x.shape[0]
    # allocate output
    out = np.empty(n)
    # Loop through each regression point
    for i in range(n):
        # all-1 points
        xx = np.delete(x, i, axis=0)
        yy = np.delete(y, i, axis=0)
        z = (xx - x[i, :]) / h
        out[i] = _nadaraya_watson(z, yy)
    cv = np.sum((y - out)**2) / float(n)

    return cv


def _boot_h(h, x, y):
    """
    Helper function that calculates bootstrap function for the
    Nadaraya-Watson estimator, which is basically the mean square error
    where model estimate is replaced by the jackknife estimate
    (Hardle and Muller 2000).

    This does basically _cross_valid_h for 100 random points.

    """
    n = 100
    ind = np.random.randint(x.shape[0], size=n)
    # allocate output
    out = np.empty(n)
    # Loop through each bootstrap point
    for i in range(n):
        # all-1 points
        xx = np.delete(x, i, axis=0)
        yy = np.delete(y, i, axis=0)
        z = (xx - x[i, :]) / h
        out[i] = _nadaraya_watson(z, yy)
    cv = np.sum((y[ind] - out)**2) / float(n)

    return cv


def kernel_regression_h(x, y, silverman=False):
    """
    Optimal bandwidth for multi-dimensional non-parametric kernel regression

    Optimal bandwidth is determined using cross-validation or
    Silverman's rule-of-thumb.

    Parameters
    ----------
    x : array_like (n, k)
        Independent values
    y : array_like (n)
        Dependent values
    silverman : bool, optional
        Use Silverman's rule-of-thumb to calculate bandwidth *h* if True,
        otherwise determine *h* via cross-validation

    Returns
    -------
    float or array
        Optimal bandwidth *h*. If multidimensional regression then *h* is a
        1d-array, assuming a diagonal bandwidth matrix.

    References
    ----------
    Hardle W and Muller M (2000) Multivariate and semiparametric kernel
       regression. In MG Schimek (Ed.), Smoothing and regression: Approaches,
       computation, and application (pp. 357-392). Hoboken, NJ, USA: John Wiley
       & Sons, Inc. doi: 10.1002/9781118150658.ch12


    Examples
    --------
    >>> n = 10
    >>> x = np.zeros((n, 2))
    >>> x[:, 0] = np.arange(n, dtype=float) / float(n-1)
    >>> x[:, 1] = 1. / (np.arange(n, dtype=float) / float(n-1) + 0.1)
    >>> y = 1. + x[:, 0]**2 - np.sin(x[:, 1])**2

    >>> h = kernel_regression_h(x, y)
    >>> print(np.allclose(h, [0.172680, 9.516907], atol=0.0001))
    True

    >>> h = kernel_regression_h(x, y, silverman=True)
    >>> print(np.allclose(h, [0.229190, 1.903381], atol=0.0001))
    True

    >>> n = 10
    >>> x = np.arange(n, dtype=float) / float(n-1)
    >>> y = 1. + x**2 - np.sin(x)**2

    >>> h = kernel_regression_h(x, y)
    >>> print(np.around(h, 4))
    0.045

    >>> h = kernel_regression_h(x, y, silverman=True)
    >>> print(np.around(h, 4))
    0.2248

    """
    xx = np.array(x)
    yy = np.array(y)
    # Check input
    assert xx.shape[0] == yy.size, (
        f'size(x, 0) != size(y): {xx.shape[0]} != {yy.size}' )
    if xx.ndim == 1:  # deal with 1d-arrays
        xx = xx[:, np.newaxis]
    n = xx.shape[0]
    d = xx.shape[1]

    # Silverman (1986), Scott (1992), Bowman and Azzalini (1997)
    # Very similar to stats.gaussian_kde
    # h has dimension d
    h = ( (4. / float(d + 2) / float(n))**(1. / float(d + 4)) *
          np.std(xx, axis=0, ddof=1) )

    if not silverman:
        # Find the optimal h
        bounds = [(0.2*i, 5.0*i) for i in h]
        if n <= 100:
            res = opt.minimize(
                _cross_valid_h, h, args=(xx, yy), method='TNC', bounds=bounds,
                options={'ftol': 1e-10, 'xtol': 1e-10, 'maxfun': 1000})
            h = res.x
        else:
            res = opt.minimize(
                _boot_h, h, args=(xx, yy), method='TNC', bounds=bounds,
                options={'ftol': 1e-10, 'xtol': 1e-10, 'maxfun': 1000})
            h = res.x

    if len(h) == 1:
        h = h[0]

    return h


def kernel_regression(x, y, h=None, silverman=False, xout=None):
    """
    Multi-dimensional non-parametric kernel regression

    Optimal bandwidth can be estimated by cross-validation
    or by using Silverman's rule-of-thumb.

    Parameters
    ----------
    x : array_like (n, k)
        Independent values
    y : array_like (n)
        Dependent values
    h : float or array_like(k), optional
        Use *h* as bandwidth for calculating regression values if given,
        otherwise determine optimal *h* using cross-validation or by using
        Silverman's rule-of-thumb if *silverman==True*.
    silverman : bool, optional
        Use Silverman's rule-of-thumb to calculate bandwidth *h* if True,
        otherwise determine *h* via cross-validation.
        Only used if *h* is not given.
    xout : ndarray(n, k), optional
        Return fitted values at *xout* if given,
        otherwise return fitted values at *x*.

    Returns
    -------
    array_like with same type as *x*, or *xout* if given
        Fitted values at *x*, or at *xout* if given

    References
    ----------
    Hardle W and Muller M (2000) Multivariate and semiparametric kernel
       regression. In MG Schimek (Ed.), Smoothing and regression: Approaches,
       computation, and application (pp. 357-392). Hoboken, NJ, USA: John Wiley
       & Sons, Inc. doi: 10.1002/9781118150658.ch12

    Examples
    --------
    >>> n = 10
    >>> x = np.zeros((n, 2))
    >>> x[:, 0] = np.arange(n, dtype=float) / float(n-1)
    >>> x[:, 1] = 1. / (np.arange(n, dtype=float) / float(n-1) + 0.1)
    >>> y = 1. + x[:, 0]**2 - np.sin(x[:, 1])**2

    Separate determination of h and kernel regression

    >>> h = kernel_regression_h(x, y)
    >>> yk = kernel_regression(x, y, h)
    >>> print(np.allclose(yk[0:6],
    ...       [0.52241, 0.52570, 0.54180, 0.51781, 0.47644, 0.49230],
    ...       atol=0.0001))
    True

    Single call to kernel regression

    >>> yk = kernel_regression(x, y)
    >>> print(np.allclose(yk[0:6],
    ...       [0.52241, 0.52570, 0.54180, 0.51781, 0.47644, 0.49230],
    ...       atol=0.0001))
    True

    Single call to kernel regression using Silverman's rule-of-thumb for h

    >>> yk = kernel_regression(x, y, silverman=True)
    >>> print(np.allclose(yk[0:6],
    ...       [0.691153, 0.422809, 0.545844, 0.534315, 0.521494, 0.555426],
    ...       atol=0.0001))
    True

    >>> n = 5
    >>> xx = np.empty((n, 2))
    >>> xx[:, 0] = (np.amin(x[:, 0]) + (np.amax(x[:, 0]) - np.amin(x[:, 0])) *
    ...                                 np.arange(n, dtype=float) / float(n))
    >>> xx[:, 1] = (np.amin(x[:, 1]) + (np.amax(x[:, 1]) - np.amin(x[:, 1])) *
    ...                                 np.arange(n, dtype=float) / float(n))
    >>> yk = kernel_regression(x, y, silverman=True, xout=xx)
    >>> print(np.allclose(yk,
    ...       [0.605485, 0.555235, 0.509529, 0.491191, 0.553325],
    ...       atol=0.0001))
    True

    """
    xx = np.array(x)
    yy = np.array(y)
    # Check input
    assert xx.shape[0] == yy.size, (
        f'size(x,0) != size(y): {xx.shape[0]} != {yy.size}' )
    # deal with 1d-arrays and save 1d input type
    if xx.ndim == 1:
        xx = xx[:, np.newaxis]
    d = xx.shape[1]

    # determine h
    if h is None:
        hh = kernel_regression_h(xx, yy, silverman=silverman)
    else:
        if np.size(np.shape(h)) == 0:
            hh = np.repeat(h, d)  # use h for all dimensions if one h given
        else:
            hh = np.array(h)
        assert np.size(hh) == d, 'size(h) must be 1 or x.shape[1]'

    # Calc regression
    if xout is None:
        xxout = xx
    else:
        xxout = np.array(xout)
    if xxout.ndim == 1:
        xxout = xxout[:, np.newaxis]
    nout  = xxout.shape[0]
    dout  = xxout.shape[1]
    assert d == dout, f'size(x, 1) != size(xout, 1): {d} != {dout}'
    # allocate output
    out = np.empty(nout)
    # Loop through each regression point
    for i in range(nout):
        # scaled deference from regression point
        z = (xx - xxout[i, :]) / hh
        # nadaraya-watson estimator of gaussian multivariate kernel
        out[i] = _nadaraya_watson(z, y)

    out = array2input(out, y, undef=np.nan)

    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # nn = 1000
    # x = np.zeros((nn, 2))
    # x[:, 0] = np.arange(nn, dtype=float) / float(nn-1)
    # x[:, 1] = 1. / (x[:, 0] + 0.1)
    # y      = 1. + x[:, 0]**2 - np.sin(x[:, 1])**2
    # h = kernel_regression_h(x, y)
    # print(h)
    # yy = kernel_regression(x, y, h, xout=x)
    # print(yy[0], yy[-1])
    # print(kernel_regression(x, y))
    # h = kernel_regression_h(x, y, silverman=True)
    # print(h)
    # print(kernel_regression(x, y, h))
    # ss = np.shape(x)
    # nn = 5
    # xx = np.empty((nn, ss[1]))
    # xx[:,0] = (np.amin(x[:,0]) + (np.amax(x[:,0])-np.amin(x[:,0])) *
    #                               np.arange(nn,dtype=float)/float(nn))
    # xx[:,1] = (np.amin(x[:,1]) + (np.amax(x[:,1])-np.amin(x[:,1])) *
    #                               np.arange(nn,dtype=float)/float(nn))
    # print(kernel_regression(x, y, h, xout=xx))
