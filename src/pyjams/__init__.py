#!/usr/bin/env python
"""
Purpose
=======

pyjams is a general Python package with miscellaneous utility functions used in
several other packages. It is offering miscellaneous functions in different
categories, such as reading different file formats, julian date routines, or
meteorological functions. It has several subpackages offering constants or
special functions as well as objective functions to be used with
scipy.optimize.fmin or scipy.optimize.curvefit, and much more.

The package has evolved from its predecessor the JAMS Python package
https://github.com/mcuntz/jams_python

:copyright: Copyright 2021 Matthias Cuntz, see AUTHORS.md for details.
:license: MIT License, see LICENSE for details.

Subpackages
===========
.. autosummary::
   argsort
   const
   division
   functions
   morris_method
   screening
   tee

History
    * Written Oct 2021 by Matthias Cuntz (mc (at) macu (dot) de)
    * v1.0, initial Github, PyPI, Zenodo commit, Oct 2021, Matthias Cuntz
    * v1.1, automatic versioning, zenodo defaults, Oct 2021, Matthias Cuntz
    * v1.2, added closest, Oct 2021, Matthias Cuntz
    * v1.3, added division, Oct 2021, Matthias Cuntz
    * v1.4, added alpha_equ_h2o, Oct 2021, Matthias Cuntz
    * v1.5, added alpha_kin_h2o, Nov 2021, Matthias Cuntz
    * v1.6, added mcPlot, Nov 2021, Matthias Cuntz

"""
# version, author
try:
    from ._version import __version__
except ImportError:  # pragma: nocover
    # package is not installed
    __version__ = "0.0.0.dev0"
__author__  = "Matthias Cuntz, Juliane Mai, Stephan Thober, Arndt Piayda"

# sub-packages without dependencies to rest of pyjams
from . import const
from . import functions

# isotopic fractionation factors during liquid-water vapour equilibration
from .alpha_equ_h2o import alpha_equ_h2o
# kinetic fractionation of molecular diffusion of water vapour.
from .alpha_kin_h2o import alpha_kin_h2o
# argmax, argmin and argsort for array_like and Python iterables
from .argsort import argmax, argmin, argsort
# (index of) closest element in an array
from .closest import closest
# catch division by zero
from .division import division, div
# Matthias Cuntz' standard plotting class.
from .mcplot import mcPlot
# has to be ordered for import: morris -> screening
# Sampling of optimised trajectories for and calculation of Morris Measures / Elementary Effects
from .morris_method import morris_sampling, elementary_effects
# Sample trajectories, run model and return Morris Elementary Effects
from .screening import screening, ee
# like unix tee
from .tee import tee


__all__ = ["__version__", "__author__",
           "const", "functions",
           "alpha_equ_h2o", "alpha_kin_h2o",
           "argmax", "argmin", "argsort",
           "closest",
           "division", "div",
           "mcPlot",
           "morris_sampling", "elementary_effects",
           "screening", "ee",
           "tee",
           ]
