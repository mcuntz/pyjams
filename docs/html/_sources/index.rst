Quickstart
==========

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
used with mod:`scipy.optimize`.

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
   * - :func:`~pyjams.text2plot.abc2plot`
     - Write a, B, iii), ... on a plot
   * - :func:`~pyjams.alpha_equ_h2o.alpha_equ_h2o`
     - Equilibrium fractionation between liquid water and vapour
   * - :func:`~pyjams.alpha_kin_h2o.alpha_kin_h2o`
     - Kinetic fractionation of molecular diffusion of water vapour
   * - :func:`~pyjams.argsort.argmax`
     - Wrapper for numpy.argmax, numpy.ma.argmax, and max for Python
       iterables
   * - :func:`~pyjams.argsort.argmin`
     - Wrapper for numpy.argmin, numpy.ma.argmin, and min for Python
       iterables
   * - :func:`~pyjams.argsort.argsort`
     - Wrapper for numpy.argsort, numpy.ma.argsort, and sorted for Python
       iterables
   * - :func:`~pyjams.closest.closest`
     - Index in array which entry is closest to a given number
   * - :mod:`~pyjams.color`
     - Collection of color palettes and continuous color maps
   * - :mod:`~pyjams.const`
     - Physical, mathematical, computational, isotope, and material constants
   * - :func:`~pyjams.date2date.date2date`
     - Convert date representations between different regional variants
   * - :func:`~pyjams.class_datetime.date2dec`
     - Return numeric time values given datetime objects or strings,
       same as `date2num`
   * - :func:`~pyjams.date2date.date2en`
     - Convert dates to English date format YYYY-MM-DD hh:mm:ss
   * - :func:`~pyjams.date2date.date2fr`
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss
   * - :func:`~pyjams.class_datetime.date2num`
     - Return numeric time values given datetime objects or strings
   * - :func:`~pyjams.date2date.date2us`
     - Convert dates to American date format MM/DD/YYYY hh:mm:ss
   * - :func:`~pyjams.class_datetime.datetime`
     - Class as cftime.datetime for non-CF-conform calendars
   * - :func:`~pyjams.class_datetime.dec2date`
     - Return datetime objects given numeric time values, same as `num2date`
   * - :func:`~pyjams.fgui.directories_from_gui`
     - Open dialog to select one directory
   * - :func:`~pyjams.fgui.directory_from_gui`
     - Open dialog to select several directories
   * - :func:`~pyjams.division.division`
     - Divide two arrays, return 'otherwise' if division by 0
   * - :func:`~pyjams.division.div`
     - Divide two arrays, return 'otherwise' if division by 0,
       same as `division`
   * - :func:`~pyjams.air_humidity.eair2mrair`
     - Mixing ratio from partial pressure of water vapour and total pressure
   * - :func:`~pyjams.air_humidity.eair2rhair`
     - Relative humidity from partial pressure of water vapour and temperature
   * - :func:`~pyjams.air_humidity.eair2shair`
     - Specific humidity from partial pressure of water vapour and total pressure
   * - :func:`~pyjams.air_humidity.eair2vpd`
     - Air vapour pressure deficit from partial pressure and temperature
   * - :func:`~pyjams.screening.ee`
     - Parameter screening using Morris' method of Elementary Effects,
       same as `screening`
   * - :func:`~pyjams.morris_method.elementary_effects`
     - Morris measures mu, stddev and mu*
   * - :func:`~pyjams.date2date.en2date`
     - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
   * - :func:`~pyjams.date2date.en2fr`
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss
   * - :func:`~pyjams.date2date.en2us`
     - Convert dates to American date format MM/DD/YYYY hh:mm:ss
   * - :func:`~pyjams.air_humidity.esat`
     - Saturation vapour pressure over water and ice
   * - :func:`~pyjams.date2date.fr2date`
     - Convert French dates to standard date format DD.MM.YYYY hh:mm:ss
   * - :func:`~pyjams.date2date.fr2en`
     - Convert French dates to English date format YYYY-MM-DD hh:mm:ss
   * - :func:`~pyjams.date2date.fr2us`
     - Convert French dates to American date format MM/DD/YYYY hh:mm:ss
   * - :func:`~pyjams.fgui.file_from_gui`
     - Open dialog to select one file
   * - :func:`~pyjams.fgui.files_from_gui`
     - Open dialog to select one or several files
   * - :func:`~pyjams.fsread.fread`
     - Read numbers from a file into 2D float array
   * - :func:`~pyjams.fsread.fsread`
     - Read numbers and strings from a file into 2D float and string arrays
   * - :mod:`~pyjams.functions`
     - Special functions for testing optimisations, sensitivity analysis,
       several forms of the logistic function and its derivatives, and other
       functions to be used with :mod:`scipy.optimize`
   * - :func:`~pyjams.gridcellarea.gridcellarea`
     - Area of grid cells on Earth
   * - :func:`~pyjams.ncinfo.infonetcdf`
     - Extract information from netCDF file, same as :func:`ncinfo`
   * - :func:`~pyjams.romanliterals.int2roman`
     - Integer to Roman numeral conversion
   * - :func:`~pyjams.kernel_regression.kernel_regression`
     - Multi-dimensional non-parametric kernel regression
   * - :func:`~pyjams.kernel_regression.kernel_regression_h`
     - Determination of bandwidth for kernel regression
   * - :func:`~pyjams.mad.mad`
     - Median absolute deviation test
   * - :class:`~pyjams.mcplot.mcPlot`
     - Matthias Cuntz' standard plotting class
   * - :func:`~pyjams.means.means`
     - Calculate daily, monthly, yearly, etc. means of data
   * - :func:`~pyjams.morris_method.morris_sampling`
     - Sampling of optimised trajectories for Morris measures / Elementary
       Effects
   * - :func:`~pyjams.air_humidity.mrair2eair`
     - Partial pressure of water vapour from mixing ratio and total pressure
   * - :func:`~pyjams.ncinfo.ncinfo`
     - Extract information from netCDF file
   * - :mod:`~pyjams.ncio`
     - netCDF4 functions to copy a netcdf file while doing some
       transformations on variables and dimensions
   * - :func:`~pyjams.ncread.ncread`
     - Read variables from netCDF file
   * - :func:`~pyjams.class_datetime.num2date`
     - Return datetime objects given numeric time values
   * - :func:`~pyjams.pack.pack`
     - Pack array with mask like Fortran intrinsic pack
   * - :func:`~pyjams.position.position`
     - Position arrays of subplots to be used with add_axes
   * - :func:`~pyjams.ncread.readnetcdf`
     - Read variables from netCDF file, same as `ncread`
   * - :func:`~pyjams.air_humidity.rhair2eair`
     - Partial pressure of water vapour from relative humidity and temperature
   * - :func:`~pyjams.air_humidity.rhair2vpd`
     - Air vapour pressure deficit from relative humidity and temperature
   * - :func:`~pyjams.romanliterals.roman2int`
     - Roman numeral to integer conversion
   * - :func:`~pyjams.sce.sce`
     - Shuffled-Complex-Evolution algorithm for function min(max)imisation
   * - :func:`~pyjams.screening.screening`
     - Parameter screening using Morris' method of Elementary Effects
   * - :func:`~pyjams.air_humidity.shair2eair`
     - Partial pressure of water vapour from specific humidity and total pressure
   * - :func:`~pyjams.text2plot.signature2plot`
     - Write a copyright notice on a plot
   * - :func:`~pyjams.fsread.sread`
     - Read strings from a file into 2D string array
   * - :func:`~pyjams.str2tex.str2tex`
     - Convert strings to LaTeX strings in math environment used by matplotlib's
       usetex
   * - :func:`~pyjams.tee.tee`
     - Prints arguments on screen and in file, like Unix/Linux tee utility
   * - :func:`~pyjams.text2plot.text2plot`
     - Write text on a plot
   * - :func:`~pyjams.pack.unpack`
     - Unpack array using mask like Fortran intrinsic unpack
   * - :func:`~pyjams.npyio.updatez`
     - Update arrays in uncompressed numpy .npz format
   * - :func:`~pyjams.npyio.updatez_compressed`
     - Update arrays in compressed numpy .npz format
   * - :func:`~pyjams.date2date.us2date`
     - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
   * - :func:`~pyjams.date2date.us2en`
     - Convert dates to English date format YYYY-MM-DD hh:mm:ss
   * - :func:`~pyjams.date2date.us2fr`
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss
   * - :func:`~pyjams.air_humidity.vpd2eair`
     - Partial pressure of water vapour from air vapour pressure deficit and temperature
   * - :func:`~pyjams.air_humidity.vpd2rhair`
     - Relative humidity from air vapour pressure deficit and temperature
   * - :func:`~pyjams.fsread.xlsread`
     - Read numbers and strings from Excel file into 2D float and string arrays,
       same as `xread`
   * - :func:`~pyjams.fsread.xlsxread`
     - Read numbers and strings from Excel file into 2D float and string arrays,
       same as `xread`
   * - :func:`~pyjams.fsread.xread`
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
       * - :func:`~pyjams.argsort.argmax`
         - Wrapper for numpy.argmax, numpy.ma.argmax, and  max for Python
           iterables
       * - :func:`~pyjams.argsort.argmin`
         - Wrapper for numpy.argmin, numpy.ma.argmin, and min for Python
           iterables
       * - :func:`~pyjams.argsort.argsort`
         - Wrapper for numpy.argsort, numpy.ma.argsort, and sorted for
           Python iterables
       * - :func:`~pyjams.closest.closest`
         - Index in array which entry is closest to a given number
       * - :func:`~pyjams.pack.pack`
         - Pack array with mask like Fortran intrinsic pack
       * - :func:`~pyjams.pack.unpack`
         - Unpack array using mask like Fortran intrinsic unpack

.. _Ascii Files:

**Ascii Files**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.fsread.fread`
         - Read numbers from a file into 2D float array
       * - :func:`~pyjams.fsread.fsread`
         - Read numbers and strings from a file into 2D float and string arrays
       * - :func:`~pyjams.fsread.sread`
         - Read strings from a file into 2D string array

.. _Data Processing:

**Data Processing**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.kernel_regression.kernel_regression`
         - Multi-dimensional non-parametric kernel regression
       * - :func:`~pyjams.kernel_regression.kernel_regression_h`
         - Determination of bandwidth for kernel regression
       * - :func:`~pyjams.mad.mad`
         - Median absolute deviation test
       * - :func:`~pyjams.means.means`
         - Calculate daily, monthly, yearly, etc. means of data

.. _Date and Time:

**Date and Time**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.date2date.date2date`
         - Convert date representations between different regional variants
       * - :func:`~pyjams.class_datetime.date2dec`
         - Return numeric time values given datetime objects or strings,
           same as `date2num`
       * - :func:`~pyjams.date2date.date2en`
         - Convert dates to English date format YYYY-MM-DD hh:mm:ss
       * - :func:`~pyjams.date2date.date2fr`
         - Convert dates to French date format DD/MM/YYYY hh:mm:ss
       * - :func:`~pyjams.class_datetime.date2num`
         - Return numeric time values given datetime objects or strings
       * - :func:`~pyjams.date2date.date2us`
         - Convert dates to American date format MM/DD/YYYY hh:mm:ss
       * - :func:`~pyjams.class_datetime.datetime`
         - Class as cftime.datetime for non-CF-conform calendars
       * - :func:`~pyjams.class_datetime.dec2date`
         - Return datetime objects given numeric time values,
           same as `num2date`
       * - :func:`~pyjams.date2date.en2date`
         - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
       * - :func:`~pyjams.date2date.en2fr`
         - Convert dates to French date format DD/MM/YYYY hh:mm:ss
       * - :func:`~pyjams.date2date.en2us`
         - Convert dates to American date format MM/DD/YYYY hh:mm:ss
       * - :func:`~pyjams.date2date.fr2date`
         - Convert French dates to standard date format DD.MM.YYYY hh:mm:ss
       * - :func:`~pyjams.date2date.fr2en`
         - Convert French dates to English date format YYYY-MM-DD hh:mm:ss
       * - :func:`~pyjams.date2date.fr2us`
         - Convert French dates to American date format MM/DD/YYYY hh:mm:ss
       * - :func:`~pyjams.date2date.us2date`
         - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
       * - :func:`~pyjams.date2date.us2en`
         - Convert dates to English date format YYYY-MM-DD hh:mm:ss
       * - :func:`~pyjams.date2date.us2fr`
         - Convert dates to French date format DD/MM/YYYY hh:mm:ss
       * - :func:`~pyjams.class_datetime.num2date`
         - Return datetime objects given numeric time values

.. _Grids and Polygons:

**Grids and Polygons**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.gridcellarea.gridcellarea`
         - Area of grid cells on Earth

.. _Isotopes:

**Isotopes**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.alpha_equ_h2o.alpha_equ_h2o`
         - Equilibrium fractionation between liquid water and vapour
       * - :func:`~pyjams.alpha_kin_h2o.alpha_kin_h2o`
         - Kinetic fractionation of molecular diffusion of water vapour

.. _Math:

**Math**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.division.division`
         - Divide two arrays, return 'otherwise' if division by 0
       * - :func:`~pyjams.division.div`
         - Divide two arrays, return 'otherwise' if division by 0,
           same as `division`
       * - :func:`~pyjams.screening.ee`
         - Parameter screening using Morris' method of Elementary Effects,
           same as `screening`
       * - :func:`~pyjams.morris_method.elementary_effects`
         - Morris measures mu, stddev and mu*
       * - :mod:`~pyjams.functions`
         - Special functions for testing optimisations, sensitivity analysis,
           several forms of the logistic function and its derivatives, and other
           functions to be used with :mod:`scipy.optimize`
       * - :func:`~pyjams.morris_method.morris_sampling`
         - Sampling of optimised trajectories for Morris measures / Elementary
           Effects
       * - :func:`~pyjams.sce.sce`
         - Shuffled-Complex-Evolution algorithm for function min(max)imisation
       * - :func:`~pyjams.screening.screening`
         - Parameter screening using Morris' method of Elementary Effects

.. _Meteorology:

**Meteorology**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.air_humidity.eair2mrair`
         - Mixing ratio from partial pressure of water vapour and total pressure
       * - :func:`~pyjams.air_humidity.eair2rhair`
         - Relative humidity from partial pressure of water vapour and temperature
       * - :func:`~pyjams.air_humidity.eair2shair`
         - Specific humidity from partial pressure of water vapour and total pressure
       * - :func:`~pyjams.air_humidity.eair2vpd`
         - Air vapour pressure deficit from partial pressure and temperature
       * - :func:`~pyjams.air_humidity.esat`
         - Saturation vapour pressure over water and ice
       * - :func:`~pyjams.air_humidity.mrair2eair`
         - Partial pressure of water vapour from mixing ratio and total pressure
       * - :func:`~pyjams.air_humidity.rhair2eair`
         - Partial pressure of water vapour from relative humidity and temperature
       * - :func:`~pyjams.air_humidity.rhair2vpd`
         - Air vapour pressure deficit from relative humidity and temperature
       * - :func:`~pyjams.air_humidity.shair2eair`
         - Partial pressure of water vapour from specific humidity and total pressure
       * - :func:`~pyjams.air_humidity.vpd2eair`
         - Partial pressure of water vapour from air vapour pressure deficit and temperature
       * - :func:`~pyjams.air_humidity.vpd2rhair`
         - Relative humidity from air vapour pressure deficit and temperature

.. _Miscellaneous:

**Miscellaneous**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :mod:`~pyjams.const`
         - Physical, mathematical, computational, isotope, and material
           constants
       * - :func:`~pyjams.fgui.directories_from_gui`
         - Open dialog to select one directory
       * - :func:`~pyjams.fgui.directory_from_gui`
         - Open dialog to select several directories
       * - :func:`~pyjams.fgui.file_from_gui`
         - Open dialog to select one file
       * - :func:`~pyjams.fgui.files_from_gui`
         - Open dialog to select one or several files
       * - :func:`~pyjams.romanliterals.int2roman`
         - Integer to Roman numeral conversion
       * - :func:`~pyjams.romanliterals.roman2int`
         - Roman numeral to integer conversion
       * - :func:`~pyjams.tee.tee`
         - Prints arguments on screen and in file, like Unix/Linux tee utility

.. _Plotting:

**Plotting**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.text2plot.abc2plot`
         - Write a, B, iii), ... on a plot
       * - :mod:`~pyjams.color`
         - Collection of color palettes and continuous color maps
       * - :func:`~pyjams.romanliterals.int2roman`
         - Integer to Roman numeral conversion
       * - :class:`~pyjams.mcplot.mcPlot`
         - Matthias Cuntz' standard plotting class
       * - :func:`~pyjams.position.position`
         - Position arrays of subplots to be used with add_axes
       * - :func:`~pyjams.romanliterals.roman2int`
         - Roman numeral to integer conversion
       * - :func:`~pyjams.text2plot.signature2plot`
         - Write a copyright notice on a plot
       * - :func:`~pyjams.str2tex.str2tex`
         - Convert strings to LaTeX strings in math environment used by
           matplotlib's usetex
       * - :func:`~pyjams.text2plot.text2plot`
         - Write text on a plot

.. _Special Files:

**Special Files**
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.ncinfo.infonetcdf`
         - Extract information from netCDF file, same as `ncinfo`
       * - :func:`~pyjams.ncinfo.ncinfo`
         - Extract information from netCDF file
       * - :mod:`~pyjams.ncio`
         - netCDF4 functions to copy a netcdf file while doing some
           transformations on variables and dimensions
       * - :func:`~pyjams.ncread.ncread`
         - Read variables from netCDF file
       * - :func:`~pyjams.ncread.readnetcdf`
         - Read variables from netCDF file, same as `ncread`
       * - :func:`~pyjams.npyio.updatez`
         - Update arrays in uncompressed numpy .npz format
       * - :func:`~pyjams.npyio.updatez_compressed`
         - Update arrays in compressed numpy .npz format
       * - :func:`~pyjams.fsread.xlsread`
         - Read numbers and strings from Excel file into 2D float and string arrays,
           same as `xread`
       * - :func:`~pyjams.fsread.xlsxread`
         - Read numbers and strings from Excel file into 2D float and string arrays,
           same as `xread`
       * - :func:`~pyjams.fsread.xread`
         - Read numbers and strings from Excel file into 2D float and string arrays


License
-------

``pyjams`` is distributed under the MIT License. See the LICENSE_ file for
details.

Copyright (c) 2012-2023 Matthias Cuntz, Juliane Mai, Stephan Thober, and Arndt
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
