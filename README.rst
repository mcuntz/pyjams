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
    * `Array manipulation`_
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
   * - mcPlot
     - Matthias Cuntz' standard plotting class
   * - morris_sampling
     - Sampling of optimised trajectories for Morris measures / Elementary
       Effects
   * - position
     - Position arrays of subplots to be used with add_axes
   * - screening
     - Parameter screening using Morris' method of Elementary Effects
   * - str2tex
     - Convert strings to LaTeX strings in math environment used by matplotlib's
       usetex
   * - tee
     - Prints arguments on screen and in file, like Unix/Linux tee utility

Functions and modules per category
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Array manipulation:

Array manipulation
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

.. _Isotopes:

Isotopes
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

Math
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

.. _Miscellaneous:

Miscellaneous
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - const
         - Physical, mathematical, computational, isotope, and material
           constants
       * - tee
         - Prints arguments on screen and in file, like Unix/Linux tee utility

.. _Plotting:

Plotting
    .. list-table::
       :widths: 10 25
       :header-rows: 1

       * - Function/module
         - Short description
       * - color
         - Collection of color palettes and continuous color maps
       * - mcPlot
         - Matthias Cuntz' standard plotting class
       * - position
         - Position arrays of subplots to be used with add_axes
       * - str2tex
         - Convert strings to LaTeX strings in math environment used by
           matplotlib's usetex


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
.. _matplotlib: https://matplotlib.org/
.. _numpy: https://numpy.org/
.. _scipy: https://scipy.org/
.. _schwimmbad: https://github.com/adrn/schwimmbad/
.. _welltestpy: https://github.com/GeoStat-Framework/welltestpy/
