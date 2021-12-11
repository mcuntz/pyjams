Quickstart
----------

A general Python package with miscellaneous utility functions used in several other packages.

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5574388.svg
   :target: https://doi.org/10.5281/zenodo.5574388
   :alt: Zenodo DOI

.. image:: https://badge.fury.io/py/pyjams.svg
   :target: https://badge.fury.io/py/pyjams
   :alt: PyPI version

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
mod:`scipy.optimize`.

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
    * `Date and Time`_
    * Isotopes_
    * Math_
    * Miscellaneous_
    * Plotting_

Functions and modules (alphabetical)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - Function/module
     - Short description
   * - :func:`~pyjams.text2plot.abc2plot`
     - Write a, B, iii), ... on a plot
   * - :func:`~pyjams.alpha_equ_h2o`
     - Equilibrium fractionation between liquid water and vapour
   * - :func:`~pyjams.alpha_kin_h2o`
     - Kinetic fractionation of molecular diffusion of water vapour
   * - :func:`~pyjams.argmax`
     - Wrapper for numpy.argmax, numpy.ma.argmax, and using max for Python
       iterables
   * - :func:`~pyjams.argmin`
     - Wrapper for numpy.argmin, numpy.ma.argmin, and using min for Python
       iterables
   * - :func:`~pyjams.argsort`
     - Wrapper for numpy.argsort, numpy.ma.argsort, and using sorted for Python
       iterables
   * - :func:`~pyjams.closest`
     - Index in array which entry is closest to a given number
   * - :mod:`~pyjams.color`
     - Collection of color palettes and continuous color maps
   * - :mod:`~pyjams.const`
     - Physical, mathematical, computational, isotope, and material constants
   * - :func:`~pyjams.date2date.date2date`
     - Convert date representations between different regional variants
   * - :func:`~pyjams.date2date.date2en`
     - Convert dates to English date format YYYY-MM-DD hh:mm:ss
   * - :func:`~pyjams.date2date.date2fr`
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss
   * - :func:`~pyjams.date2date.date2us`
     - Convert dates to American date format MM/DD/YYYY hh:mm:ss
   * - :func:`~pyjams.division.division`
     - Divide two arrays, return 'otherwise' if division by 0
   * - :func:`~pyjams.division.div`
     - Alias for division
   * - :func:`~pyjams.screening.ee`
     - Alias for screening
   * - :func:`~pyjams.morris_method.elementary_effects`
     - Morris measures mu, stddev and mu* 
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
   * - :mod:`~pyjams.functions`
     - Special functions for testing optimisations, sensitivity analysis,
       several forms of the logistic function and its derivatives, and other
       functions to be used with :mod:`scipy.optimize`
   * - :func:`~pyjams.romanliterals.int2roman`
     - Integer to Roman numeral conversion
   * - :class:`~pyjams.mcPlot`
     - Matthias Cuntz' standard plotting class
   * - :func:`~pyjams.morris_method.morris_sampling`
     - Sampling of optimised trajectories for Morris measures / Elementary
       Effects
   * - :func:`~pyjams.position`
     - Position arrays of subplots to be used with add_axes
   * - :func:`~pyjams.romanliterals.roman2int`
     - Roman numeral to integer conversion
   * - :func:`~pyjams.screening.screening`
     - Parameter screening using Morris' method of Elementary Effects
   * - :func:`~pyjams.text2plot.signature2plot`
     - Write a copyright notice on a plot
   * - :func:`~pyjams.str2tex`
     - Convert strings to LaTeX strings in math environment used by matplotlib's
       usetex
   * - :func:`~pyjams.tee`
     - Prints arguments on screen and in file, like Unix/Linux tee utility
   * - :func:`~pyjams.text2plot.text2plot`
     - Write text on a plot
   * - :func:`~pyjams.date2date.us2date`
     - Convert dates to standard date format DD.MM.YYYY hh:mm:ss
   * - :func:`~pyjams.date2date.us2en`
     - Convert dates to English date format YYYY-MM-DD hh:mm:ss
   * - :func:`~pyjams.date2date.us2fr`
     - Convert dates to French date format DD/MM/YYYY hh:mm:ss

Functions and modules per category
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Array Manipulation:

Array Manipulation
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.argmax`
         - Wrapper for numpy.argmax, numpy.ma.argmax, and using max for Python
           iterables
       * - :func:`~pyjams.argmin`
         - Wrapper for numpy.argmin, numpy.ma.argmin, and using min for Python
           iterables
       * - :func:`~pyjams.argsort`
         - Wrapper for numpy.argsort, numpy.ma.argsort, and using sorted for
           Python iterables
       * - :func:`~pyjams.closest`
         - Index in array which entry is closest to a given number

.. _Date and Time:

Date and Time
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.date2date.date2date`
         - Convert date representations between different regional variants
       * - :func:`~pyjams.date2date.date2en`
         - Convert dates to English date format YYYY-MM-DD hh:mm:ss
       * - :func:`~pyjams.date2date.date2fr`
         - Convert dates to French date format DD/MM/YYYY hh:mm:ss
       * - :func:`~pyjams.date2date.date2us`
         - Convert dates to American date format MM/DD/YYYY hh:mm:ss
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

.. _Isotopes:

Isotopes
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.alpha_equ_h2o`
         - Equilibrium fractionation between liquid water and vapour
       * - :func:`~pyjams.alpha_kin_h2o`
         - Kinetic fractionation of molecular diffusion of water vapour

.. _Math:

Math
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.division.division`
         - Divide two arrays, return 'otherwise' if division by 0
       * - :func:`~pyjams.division.div`
         - Alias for division
       * - :func:`~pyjams.screening.ee`
         - Alias for screening
       * - :func:`~pyjams.morris_method.elementary_effects`
         - Morris measures mu, stddev and mu* 
       * - :mod:`~pyjams.functions`
         - Special functions for testing optimisations, sensitivity analysis,
           several forms of the logistic function and its derivatives, and other
           functions to be used with :mod:`scipy.optimize`
       * - :func:`~pyjams.morris_method.morris_sampling`
         - Sampling of optimised trajectories for Morris measures / Elementary
           Effects
       * - :func:`~pyjams.screening.screening`
         - Parameter screening using Morris' method of Elementary Effects

.. _Miscellaneous:

Miscellaneous
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :mod:`~pyjams.const`
         - Physical, mathematical, computational, isotope, and material
           constants
       * - :func:`~pyjams.romanliterals.int2roman`
         - Integer to Roman numeral conversion
       * - :func:`~pyjams.romanliterals.roman2int`
         - Roman numeral to integer conversion
       * - :func:`~pyjams.tee`
         - Prints arguments on screen and in file, like Unix/Linux tee utility

.. _Plotting:

Plotting
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - :func:`~pyjams.text2plot.abc2plot`
         - Write a, B, iii), ... on a plot
       * - :mod:`~pyjams.color`
         - Collection of color palettes and continuous color maps
       * - :class:`~pyjams.mcPlot`
         - Matthias Cuntz' standard plotting class
       * - :func:`~pyjams.position`
         - Position arrays of subplots to be used with add_axes
       * - :func:`~pyjams.text2plot.signature2plot`
         - Write a copyright notice on a plot
       * - :func:`~pyjams.str2tex`
         - Convert strings to LaTeX strings in math environment used by
           matplotlib's usetex
       * - :func:`~pyjams.text2plot.text2plot`
         - Write text on a plot


License
-------

``pyjams`` is distributed under the MIT License. See the LICENSE_ file for
details.

Copyright (c) 2012-2021 Matthias Cuntz, Juliane Mai, Stephan Thober, and Arndt
Piayda

The project structure of ``pyjams`` has borrowed heavily from welltestpy_
by `Sebastian Müller`_.

.. _JAMS Python library: https://github.com/mcuntz/jams_python
.. _LICENSE: https://github.com/mcuntz/pyjams/blob/main/LICENSE
.. _Sebastian Müller: https://github.com/MuellerSeb
.. _numpy: https://numpy.org/
.. _scipy: https://scipy.org/
.. _schwimmbad: https://github.com/adrn/schwimmbad/
.. _welltestpy: https://github.com/GeoStat-Framework/welltestpy/
.. _matplotlib: https://matplotlib.org/
