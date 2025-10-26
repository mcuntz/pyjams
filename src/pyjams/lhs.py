#!/usr/bin/env python
"""
Function for Latin Hypercube Sampling

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2012-2025 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   lhs

History
   * Written May 2012 by Matthias Cuntz making a combination of a Matlab
     routine of Budiman (2003) and a Python routine of Flavio Codeco Coelho (2008)
   * Ported to Python 3, Feb 2013, Matthias Cuntz
   * Preserve shape of dist parameter, Nov 2016, Matthias Cuntz
   * Code refactoring, Sep 2021, Matthias Cuntz
   * Porting into pyjams, Oct 2025, Matthias Cuntz

"""
import numpy as np
import scipy.stats as stats


__all__ = ['lhs']


def lhs(dist, param, nsample):
    """
    Latin Hypercube Sampling of any distribution after Stein (1987)

    There can be no correlation between parameters.

    Parameters
    ----------
    dist : instance or list of scipy.stats distributions
        Instance(s) of random number generator from scipy.stats such as
        scipy.stats.norm, scipy.stats.beta, etc.
    param : tuple or list of tuple
        Tuple of parameters as required for *dist*
    nsample : int
        Number of samples per parameter, i.e. per *dist*

    Returns
    -------
    [len(dist), nsample] ndarray
        Latin Hypercube Samples of dist

    Notes
    -----
    Stein, M. 1987. Large Sample Properties of Simulations Using
        Latin Hypercube Sampling. Technometrics 29:143-151

    Examples
    --------
    >>> import numpy as np
    >>> import scipy.stats as stats
    >>> # seed for reproducible results in doctest
    >>> np.random.seed(1)

    >>> dist = [stats.norm, stats.uniform] # for uniform (min, max-min)
    >>> pars = [(50, 2), (1, 5)]
    >>> c = lhs(dist, pars, 20)
    >>> print(c[0:2, 0:4])
    [[52.8216393  51.95643181 46.71040364 50.58536004]
     [ 4.95018614  2.49206539  2.07835604  4.67308065]]

    >>> np.random.seed(1)
    >>> dist = [stats.norm]
    >>> pars = [(50,2)]
    >>> c = lhs(dist, pars, 20)
    >>> print(c.shape)
    (1, 20)

    >>> print(c[0, 0:4])
    [51.17074344 48.56164788 51.68328332 50.58536004]

    >>> np.random.seed(1)
    >>> dist = stats.norm
    >>> pars = (50,2)
    >>> c = lhs(dist, pars, 20)

    >>> print(c.shape)
    (20,)

    >>> print(c[0:4])
    [51.17074344 48.56164788 51.68328332 50.58536004]

    """
    # Check input
    if not isinstance(dist, (list, tuple)):
        nodim = True
        dist  = [dist]
        param = [param]
    else:
        nodim = False
        assert len(dist) == len(param)
    ndist = len(dist)

    # LHS
    ran = np.random.uniform(0., 1., (ndist, nsample))
    lhsout = np.empty((ndist, nsample))
    for j, d in enumerate(dist):
        if not isinstance(d, (stats.rv_discrete, stats.rv_continuous)):
            raise TypeError('dist is not a scipy.stats distribution object')
        # force type to float for sage compatibility
        pars = ( float(k) for k in param[j] )
        idx = np.array(np.random.permutation(nsample), dtype=float)
        p = (idx + ran[j, :]) / float(nsample)  # probability of cdf
        lhsout[j, :] = d(*pars).ppf(p)          # inverse of cdf

    if nodim:
        return lhsout[0, :]
    else:
        return lhsout


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # import matplotlib.pyplot as plt
    # dist = [stats.norm, stats.uniform]
    # pars = [(50, 2), (1, 5)]
    # c    = lhs(dist, pars, 20000)

    # plt.figure()
    # plt.hist(c[0, :], bins=1000)

    # plt.figure()
    # plt.hist(c[1, :], bins=1000)

    # dist = [stats.uniform, stats.uniform]
    # pars = [(50, 2), (1, 5)]
    # c    = lhs(dist, pars, 20000)

    # plt.figure()
    # plt.plot(c[0, :], c[1, :], 'ko', markersize=1.0)
    # plt.show()
