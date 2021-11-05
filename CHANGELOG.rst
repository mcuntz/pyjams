Changelog
---------

v1.7 (Nov 2021)
    * Add `mcPlot`, the standard plotting class of Matthias Cuntz.
      - It currently assumes that MyriadPro is installed for LaTeX if one wants
        to typeset with latex (-u, --usetex). For installing MyriadPro on macOS
        see https://github.com/mcuntz/setup_mac#myriad-pro This should be
        similar on Linux.
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
