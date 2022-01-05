pyjams
======
..
  pandoc -f rst -o README.html -t html README.rst

A general Python package with miscellaneous utility functions used in several other packages.

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5574388.svg
   :target: https://doi.org/10.5281/zenodo.5574388
   :alt: Zenodo DOI

.. image:: https://badge.fury.io/py/pyjams.svg
   :target: https://badge.fury.io/py/pyjams
   :alt: PyPI version

.. image:: https://img.shields.io/conda/vn/conda-forge/pyjams.svg
   :target: https://anaconda.org/conda-forge/pyjams
   :alt: Conda version

.. image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/mcuntz/pyjams/blob/master/LICENSE
   :alt: License

.. image:: https://github.com/mcuntz/pyjams/workflows/Continuous%20Integration/badge.svg?branch=main
   :target: https://github.com/mcuntz/pyjams/actions
   :alt: Build status

.. image:: https://coveralls.io/repos/github/mcuntz/pyjams/badge.svg?branch=main
   :target: https://coveralls.io/github/mcuntz/pyjams?branch=main
   :alt: Coverage status

.. image:: https://readthedocs.org/projects/pyjams/badge/?version=latest
   :target: https://pyjams.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status


About pyjams
------------

``pyjams`` is a general Python package offering miscellaneous functions in
different categories, such as reading different file formats, Julian date
routines, or calculating Elementary Effects. It has several subpackages offering
constants or special functions, or objective functions to be used with
scipy.optimize.

The package modernises and makes available routines of the `JAMS Python
library`_, which was created 2009 by Matthias Cuntz while at the Department of
Computational Hydrosystems, Helmholtz Centre for Environmental Research - UFZ,
Leipzig, Germany, and continued while at Institut National de Recherche pour
l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy, France.

The complete documentation of ``pyjams`` is available at:

   http://pyjams.readthedocs.org/en/latest/


Installation
------------

The easiest way to install is via `pip`:

.. code-block:: bash

   pip install pyjams

Requirements
    * numpy_
    * scipy_
    * matplotlib_
    * schwimmbad_


Content
-------

Modules and functions are currently provided in the following categories:
    * `Array Manipulation`_
    * `Ascii Files`_
    * `Date and Time`_
    * Isotopes_
    * Math_
    * Meteorology_
    * Miscellaneous_
    * Plotting_

Functions and modules (alphabetical)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - Function/module
     - Short description
   * - abc2plot
     - Write a, B, iii), ... on a plot
   * - alpha_equ_h2o
     - Equilibrium fractionation between liquid water and vapour
   * - alpha_kin_h2o
     - Kinetic fractionation of molecular diffusion of water vapour
   * - argmax
     - Wrapper for numpy.argmax, numpy.ma.argmax, and using max for Python
       iterables
   * - argmin
     - Wrapper for numpy.argmin, numpy.ma.argmin, and using min for Python
       iterables
   * - argsort
     - Wrapper for numpy.argsort, numpy.ma.argsort, and using sorted for Python
       iterables
   * - closest
     - Index in array which entry is closest to a given number
   * - color
     - Collection of color palettes and continuous color maps
   * - const
     - Physical, mathematical, computational, isotope, and material constants
   * - date2date
     - Convert date representations between different regional variants
   * - date2en
     - Convert dates to English date format YYYY-MM-DD hh:mm:ss
   * - date2fr
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss
   * - date2us
     - Convert dates to American date format MM/DD/YYYY hh:mm:ss
   * - directories_from_gui
     - Open dialog to select one directory
   * - directory_from_gui
     - Open dialog to select several directories
   * - division
     - Divide two arrays, return 'otherwise' if division by 0
   * - div
     - Wrapper for division
   * - elementary_effects
     - Morris measures mu, stddev and mu*
   * - en2date
     - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
   * - en2fr
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss
   * - en2us
     - Convert dates to American date format MM/DD/YYYY hh:mm:ss
   * - esat
     - Saturation vapour pressure over water and ice
   * - file_from_gui
     - Open dialog to select one file
   * - files_from_gui
     - Open dialog to select one or several files
   * - fr2date
     - Convert French dates to standard date format DD.MM.YYYY hh:mm:ss
   * - fr2en
     - Convert French dates to English date format YYYY-MM-DD hh:mm:ss
   * - fr2us
     - Convert French dates to American date format MM/DD/YYYY hh:mm:ss
   * - fread
     - Read numbers from a file into 2D float array
   * - fsread
     - Read numbers and strings from a file into 2D float and string arrays
   * - functions
     - Special functions for testing optimisations, sensitivity analysis,
       several forms of the logistic function and its derivatives, and other
       functions to be used with scipy.optimize
   * - int2roman
     - Integer to Roman numeral conversion
   * - mcPlot
     - Matthias Cuntz' standard plotting class
   * - morris_sampling
     - Sampling of optimised trajectories for Morris measures / Elementary
       Effects
   * - position
     - Position arrays of subplots to be used with add_axes
   * - roman2int
     - Roman numeral to integer conversion
   * - screening
     - Parameter screening using Morris' method of Elementary Effects
   * - signature2plot
     - Write a copyright notice on a plot
   * - sread
     - Read strings from a file into 2D string array
   * - str2tex
     - Convert strings to LaTeX strings in math environment used by matplotlib's
       usetex
   * - tee
     - Prints arguments on screen and in file, like Unix/Linux tee utility
   * - text2plot
     - Write text on a plot
   * - us2date
     - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
   * - us2en
     - Convert dates to English date format YYYY-MM-DD hh:mm:ss
   * - us2fr
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss

Functions and modules per category
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Array Manipulation:

**Array Manipulation**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - argmax
         - Wrapper for numpy.argmax, numpy.ma.argmax, and using max for Python
           iterables.
       * - argmin
         - Wrapper for numpy.argmin, numpy.ma.argmin, and using min for Python
           iterables.
       * - argsort
         - Wrapper for numpy.argsort, numpy.ma.argsort, and using sorted for
           Python iterables.
       * - closest
         - Index in array which entry is closest to a given number.

.. _Ascii Files:

**Ascii Files**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - fread
         - Read numbers from a file into 2D float array
       * - fsread
         - Read numbers and strings from a file into 2D float and string arrays
       * - sread
         - Read strings from a file into 2D string array

.. _Date and Time:

**Date and Time**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - date2date
         - Convert date representations between different regional variants
       * - date2en
         - Convert dates to English date format YYYY-MM-DD hh:mm:ss
       * - date2fr
         - Convert dates to French date format DD/MM/YYYY hh:mm:ss
       * - date2us
         - Convert dates to American date format MM/DD/YYYY hh:mm:ss
       * - en2date
         - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
       * - en2fr
         - Convert dates to French date format DD/MM/YYYY hh:mm:ss
       * - en2us
         - Convert dates to American date format MM/DD/YYYY hh:mm:ss
       * - fr2date
         - Convert French dates to standard date format DD.MM.YYYY hh:mm:ss
       * - fr2en
         - Convert French dates to English date format YYYY-MM-DD hh:mm:ss
       * - fr2us
         - Convert French dates to American date format MM/DD/YYYY hh:mm:ss
       * - us2date
         - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
       * - us2en
         - Convert dates to English date format YYYY-MM-DD hh:mm:ss
       * - us2fr
         - Convert dates to French date format DD/MM/YYYY hh:mm:ss

.. _Isotopes:

**Isotopes**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - alpha_equ_h2o
         - Equilibrium fractionation between liquid water and vapour
       * - alpha_kin_h2o
         - Kinetic fractionation of molecular diffusion of water vapour

.. _Math:

**Math**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - division
         - Divide two arrays, return 'otherwise' if division by 0
       * - div
         - Wrapper for division
       * - elementary_effects
         - Morris measures mu, stddev and mu* 
       * - functions
         - Special functions for testing optimisations, sensitivity analysis,
           several forms of the logistic function and its derivatives, and other
           functions to be used with scipy.optimize
       * - morris_sampling
         - Sampling of optimised trajectories for Morris measures / Elementary
           Effects
       * - screening
         - Parameter screening using Morris' method of Elementary Effects

.. _Meteorology:

**Meteorology**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - esat
         - Saturation vapour pressure over water and ice

.. _Miscellaneous:

**Miscellaneous**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - const
         - Physical, mathematical, computational, isotope, and material
           constants
       * - directories_from_gui
         - Open dialog to select one directory
       * - directory_from_gui
         - Open dialog to select several directories
       * - file_from_gui
         - Open dialog to select one file
       * - files_from_gui
         - Open dialog to select one or several files
       * - int2roman
         - Integer to Roman numeral conversion
       * - roman2int
         - Roman numeral to integer conversion
       * - tee
         - Prints arguments on screen and in file, like Unix/Linux tee utility

.. _Plotting:

**Plotting**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - abc2plot
         - Write a, B, iii), ... on a plot
       * - color
         - Collection of color palettes and continuous color maps
       * - int2roman
         - Integer to Roman numeral conversion
       * - mcPlot
         - Matthias Cuntz' standard plotting class
       * - position
         - Position arrays of subplots to be used with add_axes
       * - roman2int
         - Roman numeral to integer conversion
       * - signature2plot
         - Write a copyright notice on a plot
       * - str2tex
         - Convert strings to LaTeX strings in math environment used by
           matplotlib's usetex
       * - text2plot
         - Write text on a plot


License
-------

``pyjams`` is distributed under the MIT License. See the LICENSE_ file for
details.

Copyright (c) 2012-2022 Matthias Cuntz, Juliane Mai, Stephan Thober, and Arndt
Piayda

The project structure of ``pyjams`` has borrowed heavily from welltestpy_
by `Sebastian Müller`_.

.. _JAMS Python library: https://github.com/mcuntz/jams_python
.. _LICENSE: https://github.com/mcuntz/pyjams/blob/main/LICENSE
.. _Sebastian Müller: https://github.com/MuellerSeb
.. _matplotlib: https://matplotlib.org/
.. _numpy: https://numpy.org/
.. _scipy: https://scipy.org/
.. _schwimmbad: https://github.com/adrn/schwimmbad/
.. _welltestpy: https://github.com/GeoStat-Framework/welltestpy/
