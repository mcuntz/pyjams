"""
Provides a variety of special functions, including common test functions for
parameter estimations such as Rosenbrock and Griewank, test functions for
parameter sensitivity analysis such as the Ishigami and Homma function, several
forms of the logistic function and its first and second derivatives, and a
variety of other functions together with robust and square cost functions to
use with the ``scipy.optimize`` package.

:copyright: Copyright 2014-2021 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

Subpackages
===========
.. autosummary::
   general_functions
   fit_functions
   logistic_function
   opti_test_functions
   sa_test_functions
"""
from .general_functions import curvature
from .fit_functions import cost_abs, cost_square
from .fit_functions import arrhenius, arrhenius_p
from .fit_functions import cost_arrhenius, cost2_arrhenius
from .fit_functions import f1x, f1x_p, cost_f1x, cost2_f1x
from .fit_functions import fexp, fexp_p, cost_fexp, cost2_fexp
from .fit_functions import gauss, gauss_p, cost_gauss, cost2_gauss
from .fit_functions import lasslop, lasslop_p, cost_lasslop, cost2_lasslop
from .fit_functions import line, line_p, cost_line, cost2_line
from .fit_functions import line0, line0_p, cost_line0, cost2_line0
from .fit_functions import lloyd_fix, lloyd_fix_p
from .fit_functions import cost_lloyd_fix, cost2_lloyd_fix
from .fit_functions import lloyd_only_rref, lloyd_only_rref_p
from .fit_functions import cost_lloyd_only_rref, cost2_lloyd_only_rref
from .fit_functions import sabx, sabx_p, cost_sabx, cost2_sabx
from .fit_functions import poly, poly_p, cost_poly, cost2_poly
from .fit_functions import cost_logistic, cost2_logistic
from .fit_functions import cost_logistic_offset, cost2_logistic_offset
from .fit_functions import cost_logistic2_offset, cost2_logistic2_offset
from .fit_functions import see, see_p, cost_see, cost2_see
from .logistic_function import logistic, logistic_p
from .logistic_function import dlogistic, dlogistic_p
from .logistic_function import d2logistic, d2logistic_p
from .logistic_function import logistic_offset, logistic_offset_p
from .logistic_function import dlogistic_offset, dlogistic_offset_p
from .logistic_function import d2logistic_offset, d2logistic_offset_p
from .logistic_function import logistic2_offset, logistic2_offset_p
from .logistic_function import dlogistic2_offset, dlogistic2_offset_p
from .logistic_function import d2logistic2_offset, d2logistic2_offset_p
from .opti_test_functions import ackley, griewank, goldstein_price, rastrigin
from .opti_test_functions import rosenbrock, six_hump_camelback
from .sa_test_functions import B, g, G, Gstar, K, bratley, fmorris, morris
from .sa_test_functions import oakley_ohagan, ishigami_homma
from .sa_test_functions import linear, product, ratio, ishigami_homma_easy

__all__ = ['curvature']
__all__ += ['cost_abs', 'cost_square',
            'arrhenius', 'arrhenius_p', 'cost_arrhenius', 'cost2_arrhenius',
            'f1x', 'f1x_p', 'cost_f1x', 'cost2_f1x',
            'fexp', 'fexp_p', 'cost_fexp', 'cost2_fexp',
            'gauss', 'gauss_p', 'cost_gauss', 'cost2_gauss',
            'lasslop', 'lasslop_p', 'cost_lasslop', 'cost2_lasslop',
            'line', 'line_p', 'cost_line', 'cost2_line',
            'line0', 'line0_p', 'cost_line0', 'cost2_line0',
            'lloyd_fix', 'lloyd_fix_p', 'cost_lloyd_fix', 'cost2_lloyd_fix',
            'lloyd_only_rref', 'lloyd_only_rref_p', 'cost_lloyd_only_rref',
            'cost2_lloyd_only_rref',
            'sabx', 'sabx_p', 'cost_sabx', 'cost2_sabx',
            'poly', 'poly_p', 'cost_poly', 'cost2_poly',
            'cost_logistic', 'cost2_logistic',
            'cost_logistic_offset', 'cost2_logistic_offset',
            'cost_logistic2_offset', 'cost2_logistic2_offset',
            'see', 'see_p', 'cost_see', 'cost2_see']
__all__ += ['logistic', 'logistic_p',
            'dlogistic', 'dlogistic_p',
            'd2logistic', 'd2logistic_p',
            'logistic_offset', 'logistic_offset_p',
            'dlogistic_offset', 'dlogistic_offset_p',
            'd2logistic_offset', 'd2logistic_offset_p',
            'logistic2_offset', 'logistic2_offset_p',
            'dlogistic2_offset', 'dlogistic2_offset_p',
            'd2logistic2_offset', 'd2logistic2_offset_p']
__all__ += ['ackley', 'griewank', 'goldstein_price', 'rastrigin',
            'rosenbrock', 'six_hump_camelback']
__all__ += ['B', 'g', 'G', 'Gstar', 'K', 'bratley', 'fmorris', 'morris',
            'oakley_ohagan', 'ishigami_homma',
            'linear', 'product', 'ratio', 'ishigami_homma_easy']
