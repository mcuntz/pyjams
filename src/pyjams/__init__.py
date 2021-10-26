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
   const
   functions
   morris_method
   screening
   tee

History
    * Written Oct 2021 by Matthias Cuntz (mc (at) macu (dot) de)
    * v1.0, initial Github, PyPI, Zenodo commit, Oct 2021, Matthias Cuntz

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

# (index of) closest element in an array
from .closest import closest
# has to be ordered for import: morris -> screening
# Sampling of optimised trajectories for and calculation of Morris Measures / Elementary Effects
from .morris_method import morris_sampling, elementary_effects
# Sample trajectories, run model and return Morris Elementary Effects
from .screening import screening, ee
# like unix tee
from .tee import tee


__all__ = ["__version__", "__author__",
           "const", "functions",
           "closest",
           "morris_sampling", "elementary_effects",
           "screening", "ee",
           "tee",
           ]
