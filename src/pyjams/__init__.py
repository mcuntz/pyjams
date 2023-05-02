#!/usr/bin/env python
"""
pyjams is a general Python package with a wide variety of miscellaneous utility
functions. It is offering miscellaneous functions in different categories, such
as reading different file formats, date conversion routines, or meteorological
functions. It has several subpackages offering constants, special functions as
well as objective functions to be used with scipy.optimize.fmin or
scipy.optimize.curvefit, and much more.

The package has evolved from its predecessor the JAMS Python package
https://github.com/mcuntz/jams_python

:copyright: Copyright 2021-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

Subpackages
===========
.. autosummary::
   air_humidity
   alpha_equ_h2o
   alpha_kin_h2o
   argsort
   gridcellarea
   closest
   color
   const
   date2date
   class_datetime
   division
   fgui
   fsread
   functions
   kernel_regression
   mad
   mcplot
   means
   morris_method
   ncio
   npyio
   position
   readnetcdf
   romanliterals
   sce
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
    * v1.15, added esat, Jan 2022, Matthias Cuntz
    * v1.16, added mad, Jan 2022, Matthias Cuntz
    * v1.17, added xread, xlsread, and xlsxread, Jan 2022, Matthias Cuntz
    * v1.18, helper module to preserve input types, Mar 2022, Matthias Cuntz
    * v1.19, added readnetcdf, Mar 2022, Matthias Cuntz
    * v1.20, added gridcellarea and kernel_regression, Apr 2022, Matthias Cuntz
    * v1.21, enhancements in color and kernel_regression,
      Apr 2022, Matthias Cuntz
    * v1.22, added ncio, May 2022, Matthias Cuntz
    * v1.23, added datetime module, Jun 2022, Matthias Cuntz
    * v1.24, moved docu to Github Pages, Jun 2022, Matthias Cuntz
    * v1.25, Microseconds and negative years in date2date and datetime,
      Jun 2022, Matthias Cuntz
    * v1.26, added means, Jul 2022, Matthias Cuntz
    * v1.27, added sce, Dec 2022, Matthias Cuntz
    * v1.28, added updatez, Jan 2023, Matthias Cuntz
    * v1.29, added functions for converting humidity in air,
      Jan 2023, Matthias Cuntz
    * v1.30, hvplot in mcplot, May 2023, Matthias Cuntz

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
# netCDF4 functions to copy netcdf file while doing some transformations on
# variables and dimensions.
from . import ncio

# air humidity calculations
from .air_humidity import esat, eair2rhair, rhair2eair
from .air_humidity import eair2vpd, vpd2eair, rhair2vpd, vpd2rhair
from .air_humidity import eair2shair, shair2eair, eair2mrair, mrair2eair
# isotopic fractionation factors during liquid-water vapour equilibration
from .alpha_equ_h2o import alpha_equ_h2o
# kinetic fractionation of molecular diffusion of water vapour
from .alpha_kin_h2o import alpha_kin_h2o
# argmax, argmin and argsort for array_like and Python iterables
from .argsort import argmax, argmin, argsort
# Area of grid cells on Earth
from .gridcellarea import gridcellarea
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
# cftime extension
from .class_datetime import date2dec, date2num, dec2date, num2date, datetime
# GUI dialogs to choose files and directories using Tkinter
from .fgui import directory_from_gui, directories_from_gui
from .fgui import file_from_gui, files_from_gui
# read numbers and strings from a file into 2D float and string arrays
from .fsread import fsread, fread, sread
from .fsread import xread, xlsread, xlsxread
# multi-dimensional non-parametric kernel regression
from .kernel_regression import kernel_regression_h, kernel_regression
# median absolute deviation test
from .mad import mad
# Matthias Cuntz' standard plotting class.
from .mcplot import mcPlot
# daily, monthly, yearly, etc. means
from .means import means
# has to be ordered for import: morris -> screening
# Sampling of optimised trajectories for and calculation of Morris Measures /
# Elementary Effects
from .morris_method import morris_sampling, elementary_effects
# update arrays in a single file in numpy's npz format
from .npyio import updatez, updatez_compressed
# positions of subplots, used with add_axes
from .position import position
# get variables from or print information of a netcdf file
from .readnetcdf import infonetcdf, ncinfo, readnetcdf, ncread
# Convert integer to and from Roman numerals
from .romanliterals import int2roman, roman2int
# Shuffled-Complex-Evolution (SCE) algorithm for function minimization
from .sce import sce
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
           'esat',
           'eair2rhair', 'rhair2eair',
           'eair2vpd', 'vpd2eair',
           'rhair2vpd', 'vpd2rhair',
           'eair2shair', 'shair2eair',
           'eair2mrair', 'mrair2eair',
           'alpha_equ_h2o', 'alpha_kin_h2o',
           'argmax', 'argmin', 'argsort',
           'gridcellarea',
           'closest',
           'date2date',
           'date2en', 'date2fr', 'date2us',
           'en2date', 'en2fr', 'en2us',
           'fr2date', 'fr2en', 'fr2us',
           'us2date', 'us2en', 'us2fr',
           'division', 'div',
           'date2dec', 'date2num', 'dec2date', 'num2date', 'datetime',
           'directory_from_gui', 'directories_from_gui',
           'file_from_gui', 'files_from_gui',
           'fsread', 'fread', 'sread',
           'xread', 'xlsread', 'xlsxread',
           'kernel_regression_h', 'kernel_regression'
           'mad',
           'mcPlot',
           'means',
           'morris_sampling', 'elementary_effects',
           'updatez', 'updatez_compressed',
           'position',
           'infonetcdf', 'ncinfo', 'readnetcdf', 'ncread',
           'int2roman', 'roman2int',
           'sce',
           'screening', 'ee',
           'str2tex',
           'tee',
           'text2plot', 'abc2plot', 'signature2plot',
           ]
