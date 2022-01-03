#!/usr/bin/env python
"""
pyjams is a general Python package with miscellaneous utility functions used in
several other packages. It is offering miscellaneous functions in different
categories, such as reading different file formats, julian date routines, or
meteorological functions. It has several subpackages offering constants or
special functions as well as objective functions to be used with
scipy.optimize.fmin or scipy.optimize.curvefit, and much more.

The package has evolved from its predecessor the JAMS Python package
https://github.com/mcuntz/jams_python

:copyright: Copyright 2021-2022 Matthias Cuntz, see AUTHORS.md for details.
:license: MIT License, see LICENSE for details.

Subpackages
===========
.. autosummary::
   alpha_equ_h2o
   alpha_kin_h2o
   argsort
   closest
   color
   const
   date2date
   division
   fgui
   fsread
   functions
   mcplot
   morris_method
   position
   romanliterals
   screening
   str2tex
   tee
   text2plot

History
    * Written Oct 2021 by Matthias Cuntz (mc (at) macu (dot) de)
    * v1.0, initial Github, PyPI, Zenodo commit, Oct 2021, Matthias Cuntz
    * v1.1, automatic versioning, zenodo defaults, Oct 2021, Matthias Cuntz
    * v1.2, added closest, Oct 2021, Matthias Cuntz
    * v1.3, added argsort, Oct 2021, Matthias Cuntz
    * v1.4, added division, Oct 2021, Matthias Cuntz
    * v1.5, added alpha_equ_h2o, Oct 2021, Matthias Cuntz
    * v1.6, added alpha_kin_h2o, Nov 2021, Matthias Cuntz
    * v1.7, added mcPlot, Nov 2021, Matthias Cuntz
    * v1.8, added str2tex and color, Nov 2021, Matthias Cuntz
    * v1.9, added position, Nov 2021, Matthias Cuntz
    * v1.10, added sron colors, Nov 2021, Matthias Cuntz
    * v1.11, added text2plot, abc2plot, signature2plot,
      Nov 2021, Matthias Cuntz
    * v1.12, added date2dec and all its wrappers, Dec 2021, Matthias Cuntz
    * v1.13, added fsread, fread, sread, Dec 2021, Matthias Cuntz
    * v1.14, added GUI dialogs to choose files and directories using Tkinter,
      Jan 2022, Matthias Cuntz

"""
# version, author
try:  # pragma: no cover
    from ._version import __version__
except ImportError:  # pragma: no cover
    # package is not installed
    __version__ = "0.0.0.dev0"
__author__  = "Matthias Cuntz, Juliane Mai, Stephan Thober, Arndt Piayda"

# sub-packages without dependencies to rest of pyjams
# color palettes and continuous color maps
from . import color
# physical, mathematical, computational, isotope, and material constants
from . import const
# variety of specialised functions
from . import functions

# isotopic fractionation factors during liquid-water vapour equilibration
from .alpha_equ_h2o import alpha_equ_h2o
# kinetic fractionation of molecular diffusion of water vapour
from .alpha_kin_h2o import alpha_kin_h2o
# argmax, argmin and argsort for array_like and Python iterables
from .argsort import argmax, argmin, argsort
# (index of) closest element in an array
from .closest import closest
# convert date representations between different regional variants
from .date2date import date2date
from .date2date import date2en, date2fr, date2us
from .date2date import en2date, en2fr, en2us
from .date2date import fr2date, fr2en, fr2us
from .date2date import us2date, us2en, us2fr
# catch division by zero
from .division import division, div
# GUI dialogs to choose files and directories using Tkinter
from .fgui import directory_from_gui, directories_from_gui
from .fgui import file_from_gui, files_from_gui
# read numbers and strings from a file into 2D float and string arrays
from .fsread import fsread, fread, sread
# Matthias Cuntz' standard plotting class.
from .mcplot import mcPlot
# has to be ordered for import: morris -> screening
# Sampling of optimised trajectories for and calculation of Morris Measures / Elementary Effects
from .morris_method import morris_sampling, elementary_effects
# positions of subplots, used with add_axes
from .position import position
# Convert integer to and from Roman numerals
from .romanliterals import int2roman, roman2int
# Sample trajectories, run model and return Morris Elementary Effects
from .screening import screening, ee
# Convert strings to LaTeX strings
from .str2tex import str2tex
# like unix tee
from .tee import tee
# put text on plot (import after str2tex)
from .text2plot import text2plot, abc2plot, signature2plot


__all__ = ['__version__', '__author__',
           'color', 'const', 'functions',
           'alpha_equ_h2o', 'alpha_kin_h2o',
           'argmax', 'argmin', 'argsort',
           'closest',
           'date2date',
           'date2en', 'date2fr', 'date2us',
           'en2date', 'en2fr', 'en2us',
           'fr2date', 'fr2en', 'fr2us',
           'us2date', 'us2en', 'us2fr',
           'division', 'div',
           'directory_from_gui', 'directories_from_gui',
           'file_from_gui', 'files_from_gui',
           'fsread', 'fread', 'sread',
           'mcPlot',
           'morris_sampling', 'elementary_effects',
           'position',
           'int2roman', 'roman2int',
           'screening', 'ee',
           'str2tex',
           'tee',
           'text2plot', 'abc2plot', 'signature2plot',
           ]
