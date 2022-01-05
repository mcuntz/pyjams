Changelog
---------

v1.15 (Jan 2022)
    * Added `esat`, giving saturation vapour pressure over water and ice.
    * Bug in `alpha_equ_h2o` in return type if list or tuple and undef.

v1.14 (Jan 2022)
    * Added `directory_from_gui`, `directories_from_gui`, `file_from_gui`, and
      `files_from_gui`, GUI dialogs to choose directories and files using
      Tkinter.
    * Organize API reference documentation by categories.
    * More consistent docstrings across routines.
    * Bug in `alpha_equ_h2o` for scalar in/out.

v1.13 (Dec 2021)
    * Added `fsread`, `fread`, and `sread`, reading numbers and strings from a
      file into 2D float and string arrays.
    * Changed order of color maps in printing and plotting.
    * Edited docstrings of color module to follow closer numpydoc.

v1.12 (Dec 2021)
    * Added `date2date`, which converts date representations between different
      regional variants.
    * Change documentation to Alabaster theme with custom CSS file.

v1.11 (Nov 2021)
    * Use `text2plot` in `abc2plot` and `signature2plot`.
    * Better handling of linebreaks in Matplotlib and LaTeX mode in `str2tex`.
    * Added `text2plot`, adding text onto a plot.
    * Added `int2roman` and `roman2int`, converting integer to and from
      Roman literals.
    * Combine `abc2plot` and `signature2plot` in one file `text2plot.py`.
    * Added `abc2plot`, adding a, B, iii), etc. onto a plot.
    * Added `signature2plot`, adding a copyright notice onto a plot.
    * Added 'pyjams_color.pdf' as reference to available colormaps.

v1.10 (Nov 2021)
    * Added tests for `color`.
    * Added 'pragma: no cover' to plot and MPI sections of codes so that they
      are not included in coverage report.
    * Cleaned mcPlot docstrings.
    * Cleaned formats in all docstrings.
    * Added current colors of Paul Tol, i.e. sron color palettes.

v1.9 (Nov 2021)
    * Add `position`, which positions arrays of subplots to be used with
      Matplotlib's add_axes.

v1.8 (Nov 2021)
    * Write standard output file of mcPlot into current folder.
    * Add `str2tex`, converting strings to LaTeX strings
    * Bug in masked array input to `alpha_equ_h2o`, needed to check masked array
      before ndarray because the former is also the latter.
    * Enhanced tests of `alpha_equ_h2o`, `alpha_kin_h2o`, `fit_functions`,
      `argsort` so that have 100% coverage.
    * Added `color`, a collection of color palettes and continuous color maps.

v1.7 (Nov 2021)
    * Add `mcPlot`, the standard plotting class of Matthias Cuntz.
        - It currently assumes that MyriadPro is installed for LaTeX if one
          wants to typeset with latex (-u, --usetex). For installing MyriadPro
          on macOS see https://github.com/mcuntz/setup_mac#myriad-pro This
          should be similar on Linux.
        - There are no tests for mcPlot yet.

v1.6 (Nov 2021)
    * Avoid overflow warnings in `alpha_equ_h2o`.
    * Added `alpha_kin_h2o`, kinetic fractionation factors for molecular
      diffusion of water isotopologues.

v1.5 (Oct 2021)
    * Added `alpha_equ_h2o`, isotopic fractionation between liquid water and
      vapour.
    * Added `pyjams` to conda-forge.

v1.4 (Oct 2021)
    * Added `division`, divides arrays dealing with zero in denominator.

v1.3 (Oct 2021)
    * Added `argmax`, `argmin` and `argsort` for array_like and Python
      iterables.

v1.2 (Oct 2021)
    * Added `closest`, which searches the closest element in an array.

v1.1.x (Oct 2021)
    * Minor updates fixing JSON format of Zenodo defaults file `.zenodo.json`,
      using a combination of the successful metadata of Zenodo of v1.0, which
      itself does not work as a template ;-( and the information given on
      https://developers.zenodo.org/.

v1.1 (Oct 2021)
    * Use automatic versioning with setuptools_scm. Delete
      `src/pyjams/version.py`.
    * Edited zenodo defaults for new releases.
    * Updated DOI in all documentation.
    * Use __all__ in all __init__.py.

v1.0 (Oct 2021)
    * Initial release on Github, PyPI, and Zenodo.
    * Copied routines from JAMS package https://github.com/mcuntz/jams_python,
      formatted docstrings in numpydoc format, made the code flake8 compatible,
      and added extensive tests. Routines in JAMS get DeprecationWarning.
    * Provide basic documentation.
    * Added `tee`, which mimics the Unix/Linux tee utility, i.e. prints
      arguments on screen and in a file.
    * Added module `const`, which provides physical, mathematical,
      computational, isotope, and material constants, such as `Pi =
      3.141592653589793238462643383279502884197`.
    * Added module `functions`, which provides a variety of special functions,
      including common test functions for parameter estimations such as
      Rosenbrock and Griewank, test functions for parameter sensitivity analysis
      such as the Ishigami and Homma function, several forms of the logistic
      function and its first and second derivatives, and a variety of other
      functions together with robust and square cost functions to use with the
      scipy.optimize package.
    * Added `morris_method.py` for Morris' Method with functions
      `morris_sampling` and `elementary_effects` to sample trajectories in
      parameter space and to calculate Elementary Effects from model output on
      trajectories.
    * Added `screening.py` for applying Morris' Method on arbitrary functions,
      providing the function `screening` that samples trajectories with
      `morris_sampling` of `morris_method.py`, applies a function on these
      trajectories, and calculates Elementary Effects with function
      `elementary_effects` of `morris_method.py`.
      It also provides a wrapper function `ee` for `screening`.
