pyjams
======
..
  pandoc -f rst -o README.html -t html README.rst

A general Python package with a wide variety of miscellaneous utility functions.

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


About pyjams
------------

``pyjams`` is a general Python package offering a wide variety of miscellaneous
functions in different categories, such as reading different file formats, date
conversion routines, or calculating Elementary Effects. It has several
subpackages offering constants, special functions, or objective functions to be
used with scipy.optimize.

The package modernises and makes available routines of the `JAMS Python
library`_, which was created 2009 by Matthias Cuntz while at the Department of
Computational Hydrosystems, Helmholtz Centre for Environmental Research - UFZ,
Leipzig, Germany, and continued while at Institut National de Recherche pour
l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy, France.

The complete documentation of ``pyjams`` is available at:

   https://mcuntz.github.io/pyjams/


Installation
------------

The easiest way to install is via `pip`:

.. code-block:: bash

   pip install pyjams

or via `conda`:

.. code-block:: bash

   conda install -c conda-forge pyjams

Requirements
    * numpy_
    * scipy_
    * matplotlib_
    * cftime_
    * netCDF4_
    * openpyxl_
    * schwimmbad_


Content
-------

Modules and functions are currently provided in the following categories:
    * `Array Manipulation`_
    * `Ascii Files`_
    * `Data Processing`_
    * `Date and Time`_
    * `Grids and Polygons`_
    * Isotopes_
    * Math_
    * Meteorology_
    * Miscellaneous_
    * Plotting_
    * `Special Files`_

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
     - Wrapper for numpy.argmax, numpy.ma.argmax, and max for Python iterables
   * - argmin
     - Wrapper for numpy.argmin, numpy.ma.argmin, and min for Python iterables
   * - argsort
     - Wrapper for numpy.argsort, numpy.ma.argsort, and sorted for Python
       iterables
   * - closest
     - Index in array which entry is closest to a given number
   * - color
     - Collection of color palettes and continuous color maps
   * - const
     - Physical, mathematical, computational, isotope, and material constants
   * - date2date
     - Convert date representations between different regional variants
   * - date2dec
     - Return numeric time values given datetime objects or strings,
       same as `date2num`
   * - date2en
     - Convert dates to English date format YYYY-MM-DD hh:mm:ss
   * - date2fr
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss
   * - date2num
     - Return numeric time values given datetime objects or strings
   * - date2us
     - Convert dates to American date format MM/DD/YYYY hh:mm:ss
   * - datetime
     - Class as cftime.datetime for non-CF-conform calendars
   * - dec2date
     - Return datetime objects given numeric time values, same as `num2date`
   * - directories_from_gui
     - Open dialog to select one directory
   * - directory_from_gui
     - Open dialog to select several directories
   * - division
     - Divide two arrays, return 'otherwise' if division by 0
   * - div
     - Divide two arrays, return 'otherwise' if division by 0,
       same as `division`
   * - eair2mrair
     - Mixing ratio from partial pressure of water vapour and total pressure
   * - eair2rhair
     - Relative humidity from partial pressure of water vapour and temperature
   * - eair2shair
     - Specific humidity from partial pressure of water vapour and total pressure
   * - eair2vpd
     - Air vapour pressure deficit from partial pressure and temperature
   * - ee
     - Parameter screening using Morris' method of Elementary Effects,
       same as `screening`
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
   * - gridcellarea
     - Area of grid cells on Earth
   * - infonetcdf
     - Extract information from netCDF file, same as `ncinfo`
   * - int2roman
     - Integer to Roman numeral conversion
   * - kernel_regression
     - Multi-dimensional non-parametric kernel regression
   * - kernel_regression_h
     - Determination of bandwidth for kernel regression
   * - mad
     - Median absolute deviation test
   * - mcPlot
     - Matthias Cuntz' standard plotting class
   * - means
     - Calculate daily, monthly, yearly, etc. means of data
   * - morris_sampling
     - Sampling of optimised trajectories for Morris measures / Elementary
       Effects
   * - mrair2eair
     - Partial pressure of water vapour from mixing ratio and total pressure
   * - ncinfo
     - Extract information from netCDF file
   * - ncio
     - netCDF4 functions to copy a netcdf file while doing some
       transformations on variables and dimensions
   * - ncread
     - Read variables from netCDF file
   * - num2date
     - Return datetime objects given numeric time values
   * - pack
     - Pack array with mask like Fortran intrinsic pack
   * - position
     - Position arrays of subplots to be used with add_axes
   * - readnetcdf
     - Read variables from netCDF file, same as `ncread`
   * - rhair2eair
     - Partial pressure of water vapour from relative humidity and temperature
   * - rhair2vpd
     - Air vapour pressure deficit from relative humidity and temperature
   * - roman2int
     - Roman numeral to integer conversion
   * - sce
     - Shuffled-Complex-Evolution algorithm for function min(max)imisation
   * - screening
     - Parameter screening using Morris' method of Elementary Effects
   * - shair2eair
     - Partial pressure of water vapour from specific humidity and total pressure
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
   * - unpack
     - Unpack array using mask like Fortran intrinsic unpack
   * - updatez
     - Update arrays in uncompressed numpy .npz format
   * - updatez_compressed
     - Update arrays in compressed numpy .npz format
   * - us2date
     - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
   * - us2en
     - Convert dates to English date format YYYY-MM-DD hh:mm:ss
   * - us2fr
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss
   * - vpd2eair
     - Partial pressure of water vapour from air vapour pressure deficit and temperature
   * - vpd2rhair
     - Relative humidity from air vapour pressure deficit and temperature
   * - xlsread
     - Read numbers and strings from Excel file into 2D float and string arrays,
       same as `xread`
   * - xlsxread
     - Read numbers and strings from Excel file into 2D float and string arrays,
       same as `xread`
   * - xread
     - Read numbers and strings from Excel file into 2D float and string arrays

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
         - Wrapper for numpy.argmax, numpy.ma.argmax, and max for Python
           iterables.
       * - argmin
         - Wrapper for numpy.argmin, numpy.ma.argmin, and min for Python
           iterables.
       * - argsort
         - Wrapper for numpy.argsort, numpy.ma.argsort, and sorted for
           Python iterables.
       * - closest
         - Index in array which entry is closest to a given number.
       * - pack
         - Pack array with mask like Fortran intrinsic pack
       * - unpack
         - Unpack array using mask like Fortran intrinsic unpack

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

.. _Data Processing:

**Data Processing**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - kernel_regression
         - Multi-dimensional non-parametric kernel regression
       * - kernel_regression_h
         - Determination of bandwidth for kernel regression
       * - mad
         - Median absolute deviation test
       * - means
         - Calculate daily, monthly, yearly, etc. means of data

.. _Date and Time:

**Date and Time**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - date2date
         - Convert date representations between different regional variants
       * - date2dec
         - Return numeric time values given datetime objects or strings,
           same as `date2num`
       * - date2en
         - Convert dates to English date format YYYY-MM-DD hh:mm:ss
       * - date2fr
         - Convert dates to French date format DD/MM/YYYY hh:mm:ss
       * - date2num
         - Return numeric time values given datetime objects or strings
       * - date2us
         - Convert dates to American date format MM/DD/YYYY hh:mm:ss
       * - datetime
         - Class as cftime.datetime for non-CF-conform calendars
       * - dec2date
         - Return datetime objects given numeric time values,
           same as `num2date`
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
       * - num2date
         - Return datetime objects given numeric time values
       * - us2date
         - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
       * - us2en
         - Convert dates to English date format YYYY-MM-DD hh:mm:ss
       * - us2fr
         - Convert dates to French date format DD/MM/YYYY hh:mm:ss

.. _Grids and Polygons:

**Grids and Polygons**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - gridcellarea
         - Area of grid cells on Earth

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
         - Divide two arrays, return 'otherwise' if division by 0,
           same as `division`
       * - ee
         - Parameter screening using Morris' method of Elementary Effects,
           same as `screening`
       * - elementary_effects
         - Morris measures mu, stddev and mu* 
       * - functions
         - Special functions for testing optimisations, sensitivity analysis,
           several forms of the logistic function and its derivatives, and other
           functions to be used with scipy.optimize
       * - morris_sampling
         - Sampling of optimised trajectories for Morris measures / Elementary
           Effects
       * - sce
         - Shuffled-Complex-Evolution algorithm for function min(max)imisation
       * - screening
         - Parameter screening using Morris' method of Elementary Effects

.. _Meteorology:

**Meteorology**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - eair2mrair
         - Mixing ratio from partial pressure of water vapour and total pressure
       * - eair2rhair
         - Relative humidity from partial pressure of water vapour and temperature
       * - eair2shair
         - Specific humidity from partial pressure of water vapour and total pressure
       * - eair2vpd
         - Air vapour pressure deficit from partial pressure and temperature
       * - esat
         - Saturation vapour pressure over water and ice
       * - mrair2eair
         - Partial pressure of water vapour from mixing ratio and total pressure
       * - rhair2eair
         - Partial pressure of water vapour from relative humidity and temperature
       * - rhair2vpd
         - Air vapour pressure deficit from relative humidity and temperature
       * - shair2eair
         - Partial pressure of water vapour from specific humidity and total pressure
       * - vpd2eair
         - Partial pressure of water vapour from air vapour pressure deficit and temperature
       * - vpd2rhair
         - Relative humidity from air vapour pressure deficit and temperature

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

.. _Special Files:

**Special Files**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - infonetcdf
         - Extract information from netCDF file, same as `ncinfo`
       * - ncinfo
         - Extract information from netCDF file
       * - ncio
         - netCDF4 functions to copy a netcdf file while doing some
           transformations on variables and dimensions
       * - ncread
         - Read variables from netCDF file
       * - readnetcdf
         - Read variables from netCDF file, same as `ncread`
       * - updatez
         - Update arrays in uncompressed numpy .npz format
       * - updatez_compressed
         - Update arrays in compressed numpy .npz format
       * - xlsread
         - Read numbers and strings from Excel file into 2D float and string arrays,
           same as `xread`
       * - xlsxread
         - Read numbers and strings from Excel file into 2D float and string arrays,
           same as `xread`
       * - xread
         - Read numbers and strings from Excel file into 2D float and string arrays


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
.. _cftime: https://github.com/Unidata/cftime
.. _matplotlib: https://matplotlib.org/
.. _netCDF4: https://github.com/Unidata/netcdf4-python
.. _numpy: https://numpy.org/
.. _openpyxl: https://foss.heptapod.net/openpyxl/openpyxl
.. _schwimmbad: https://github.com/adrn/schwimmbad/
.. _scipy: https://scipy.org/
.. _welltestpy: https://github.com/GeoStat-Framework/welltestpy/
