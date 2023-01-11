#!/usr/bin/env python
"""
This is the unittest for sce module.

python -m unittest -v tests/test_sce.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_sce.py

"""
import unittest
import os
import numpy as np
from scipy.optimize._constraints import Bounds
from scipy.optimize import rosen

from pytest import raises as assert_raises, warns
from numpy.testing import assert_equal, assert_almost_equal

from pyjams.sce import SCESolver, _strtobool
from pyjams import sce


def rosenbrock_args(x, a, b=100):
    """
    Rosenbrock, global optimum: f(a, a^2) = 0.0.

    """
    f = (a - x[0])**2 + b*(x[1] - x[0]**2)**2

    return f


def rosenbrock_kwargs(x, a=1, b=100):
    """
    Rosenbrock, global optimum: f(a, a^2) = 0.0.

    """
    f = (a - x[0])**2 + b*(x[1] - x[0]**2)**2

    return f


# Some lines are not covered:
#   117-118: second args is empty dict
#   893: if npt < 1
#   916: redo random number if exactly 0 in sampling='open'
#   931-934: if lb and ub <=0 with sampling='log'
class TestSCESolver(unittest.TestCase):

    def setUp(self):
        self.x0 = [0.5, 0.1]
        self.lb = [0., 0.]
        self.ub = np.array([2., 2.])
        self.rosenx = [1., 1.]

    def negative_rosen(self, x):
        return -rosen(x)

    def test_defaults(self):
        # test that defaults are set correctly
        solver = SCESolver(rosen, self.x0, self.lb, self.ub)
        assert_equal(solver.sampling, 'half-open')
        assert_equal(solver.maxn, 1000)
        assert_equal(solver.kstop, 10)
        assert_equal(solver.pcento, 0.0001)
        assert_equal(solver.ngs, 2)
        assert_equal(solver.npg, 2 * len(self.lb) + 1)
        assert_equal(solver.nps, len(self.lb) + 1)
        assert_equal(solver.nspl, 2 * len(self.lb) + 1)
        assert_equal(solver.mings, 2)
        assert_equal(solver.peps, 0.001)
        assert_equal(solver.alpha, 0.8)
        assert_equal(solver.beta, 0.45)
        assert_equal(solver.maxit, False)
        assert_equal(solver.printit, 2)
        assert_equal(solver.polish, True)
        assert_equal(solver.restartfile1, '')
        assert_equal(solver.restartfile2, '')

        solver = SCESolver(rosen, self.x0, self.lb, self.ub,
                           sampling='left-half-open',
                           maxn=100, kstop=1, pcento=0.001,
                           ngs=20, npg=10, nps=20, nspl=10, mings=20,
                           peps=0.01,
                           alpha=0.9, beta=0.55, maxit=True, printit=1,
                           polish=False,
                           restart=False, restartfile1='sce.restart.npz',
                           restartfile2='sce.restart.txt')
        assert_equal(solver.sampling, 'left-half-open')
        assert_equal(solver.maxn, 100)
        assert_equal(solver.kstop, 1)
        assert_equal(solver.pcento, 0.001)
        assert_equal(solver.ngs, 20)
        assert_equal(solver.npg, 10)
        assert_equal(solver.nps, 20)
        assert_equal(solver.nspl, 10)
        assert_equal(solver.mings, 20)
        assert_equal(solver.peps, 0.01)
        assert_equal(solver.alpha, 0.9)
        assert_equal(solver.beta, 0.55)
        assert_equal(solver.maxit, True)
        assert_equal(solver.printit, 1)
        assert_equal(solver.polish, False)
        assert_equal(solver.restartfile1, 'sce.restart.npz')
        assert_equal(solver.restartfile2, 'sce.restart.txt')

        solver = SCESolver(rosen, self.x0, self.lb, self.ub,
                           sampling='left-half-open',
                           maxn=100, kstop=1, pcento=0.001,
                           ngs=20, npg=10, nps=20, nspl=10, mings=20,
                           peps=0.01,
                           alpha=0.9, beta=0.55, maxit=True, printit=1,
                           polish=False,
                           restart=True, restartfile1='sce.restart.npz',
                           restartfile2='sce.restart.txt')
        assert_equal(solver.sampling, 'left-half-open')
        assert_equal(solver.maxn, 100)
        assert_equal(solver.kstop, 1)
        assert_equal(solver.pcento, 0.001)
        assert_equal(solver.ngs, 20)
        assert_equal(solver.npg, 10)
        assert_equal(solver.nps, 20)
        assert_equal(solver.nspl, 10)
        assert_equal(solver.mings, 20)
        assert_equal(solver.peps, 0.01)
        assert_equal(solver.alpha, 0.9)
        assert_equal(solver.beta, 0.55)
        assert_equal(solver.maxit, True)
        assert_equal(solver.printit, 1)
        assert_equal(solver.polish, False)
        assert_equal(solver.restartfile1, 'sce.restart.npz')
        assert_equal(solver.restartfile2, 'sce.restart.txt')

        toremove = [solver.restartfile1, solver.restartfile2]
        for ff in toremove:
            if os.path.exists(ff):
                os.remove(ff)

    def test_SCESolver(self):
        solver = SCESolver(rosen, self.x0, self.lb, self.ub, maxn=100,
                           polish=False)
        result = solver.solve()
        assert_equal(result.fun, rosen(result.x))

        solver = SCESolver(rosen, self.x0, self.lb, self.ub, maxn=100,
                           polish=True)
        result = solver.solve()
        assert_equal(result.fun, rosen(result.x))

    def test_sce(self):
        # standard
        result = sce(rosen, self.x0, self.lb, self.ub)
        assert_equal(result.fun, rosen(result.x))

        # bounds
        result = sce(rosen, self.x0, self.lb, self.ub)
        assert_almost_equal(result.x, self.rosenx, decimal=3)
        result = sce(rosen, self.x0, list(zip(self.lb, self.ub)))
        assert_almost_equal(result.x, self.rosenx, decimal=3)
        result = sce(rosen, self.x0, Bounds(self.lb, self.ub))
        assert_almost_equal(result.x, self.rosenx, decimal=3)
        result = sce(rosen, self.x0, self.lb[0], self.ub[0])
        assert_almost_equal(result.x, self.rosenx, decimal=3)
        result = sce(rosen, self.x0, self.lb[0:1], self.ub[0:1])
        assert_almost_equal(result.x, self.rosenx, decimal=3)
        # degenerated bounds
        x0 = [0.999, 0.5, 0.1]
        lb = [3., 0., 0.]
        ub = [2., 2., 2.]
        rosenx = [x0[0], 1., 1.]
        with warns(UserWarning):
            result = sce(rosen, x0, lb, ub)
        assert_almost_equal(result.x, rosenx, decimal=2)

        # seed
        result = sce(rosen, self.x0, self.lb, self.ub, polish=False, seed=1)
        result2 = sce(rosen, self.x0, self.lb, self.ub, polish=False, seed=1)
        assert_equal(result.x, result2.x)
        assert_equal(result.nfev, result2.nfev)

        # restart
        restartfile1 = 'sce.restart.npz'
        restartfile2 = restartfile1 + '.txt'
        result = sce(rosen, self.x0, self.lb, self.ub, polish=False, seed=1)
        _ = sce(rosen, self.x0, self.lb, self.ub, polish=False, seed=1,
                restart=False, restartfile1=restartfile1, maxn=10)
        result2 = sce(rosen, self.x0, self.lb, self.ub, polish=False, seed=1,
                      restart=True)
        assert_equal(result.x, result2.x)
        assert_equal(result.nfev, result2.nfev)

        toremove = [restartfile1, restartfile2]
        for ff in toremove:
            if os.path.exists(ff):
                os.remove(ff)

        # printit
        result = sce(rosen, self.x0, self.lb, self.ub, printit=0)
        assert_equal(result.fun, rosen(result.x))
        result = sce(rosen, self.x0, self.lb, self.ub, printit=1)
        assert_equal(result.fun, rosen(result.x))
        result = sce(rosen, self.x0, self.lb, self.ub, printit=2)
        assert_equal(result.fun, rosen(result.x))
        result = sce(rosen, self.x0, self.lb, self.ub, printit=1, maxn=10)
        assert_equal(result.fun, rosen(result.x))
        result = sce(rosen, self.x0, self.lb, self.ub, printit=2, maxn=10)
        assert_equal(result.fun, rosen(result.x))
        result = sce(rosen, [0.5]*5, [0.]*5, [2.]*5, printit=1, pcento=10)
        print(result.message)
        assert_equal(result.fun, rosen(result.x))

        # sampling
        result = sce(rosen, self.x0, self.lb, self.ub,
                     sampling=['half-open']*len(self.lb))
        assert_almost_equal(result.x, self.rosenx, decimal=3)
        smpls = ['half-open', 'right-half-open', 'left-half-open', 'open',
                 'log']
        for sm in smpls:
            result = sce(rosen, self.x0, self.lb, self.ub, sampling=sm)
            assert_almost_equal(result.x, self.rosenx, decimal=3)
        lb = [-1, -1.]
        result = sce(rosen, self.x0, lb, self.ub, sampling='log')
        assert_almost_equal(result.x, self.rosenx, decimal=3)
        lb = [0., 0.]
        result = sce(rosen, self.x0, lb, self.ub, sampling='log')
        assert_almost_equal(result.x, self.rosenx, decimal=3)

        # maxit
        result = sce(self.negative_rosen, self.x0, self.lb, self.ub, maxn=100,
                     polish=True, maxit=True)
        assert_equal(result.fun, self.negative_rosen(result.x))

    def test_errors(self):
        # test that the bounds checking works
        func = rosen
        x0 = [1.]
        bounds = [(-3)]
        assert_raises(TypeError, sce, func, x0, bounds)
        bounds = [(-1, 1), (-1, 1)]
        assert_raises(ValueError, sce, func, x0, bounds, sampling='unknown')
        assert_raises(ValueError, _strtobool, 'Ja')

    def test_sce_args(self):
        # args
        a = 0.5
        result = sce(rosenbrock_args, self.x0, self.lb, self.ub,
                     args=(a,))
        assert_equal(result.fun, rosenbrock_args(result.x, a))
        assert_almost_equal(result.x, (a, a**2), decimal=3)
        # args and kwargs
        a = 0.5
        b = 200
        result = sce(rosenbrock_args, self.x0, self.lb, self.ub,
                     args=(a,), kwargs={'b': b})
        assert_equal(result.fun, rosenbrock_args(result.x, a, b=b))
        assert_almost_equal(result.x, (a, a**2), decimal=3)
        # kwargs
        a = 0.5
        b = 200
        result = sce(rosenbrock_kwargs, self.x0, self.lb, self.ub,
                     kwargs={'a': a, 'b': b})
        assert_equal(result.fun, rosenbrock_kwargs(result.x, a=a, b=b))
        assert_almost_equal(result.x, (a, a**2), decimal=3)


if __name__ == "__main__":
    unittest.main()
