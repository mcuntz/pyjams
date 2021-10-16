Changelog
---------

All notable changes after its initial submission in October 2021 (v1.0)
are documented in this file.

v1.0 (Oct 2021)
    * Initial release on Github, PyPI, and Zenodo.
    * Provide basic documentation.
    * Added module `functions`, which provides a variety of special functions,
      including common test functions for parameter estimations such as
      Rosenbrock and Griewank, test functions for parameter sensitivity analysis
      such as the Ishigami and Homma function, several forms of the logistic
      function and its first and second derivatives, and a variety of other
      functions together with robust and square cost functions to use with the
      scipy.optimize package.
    * Added module `const`, which provides physical, mathematical,
      computational, isotope, and material constants, such as `Pi =
      3.141592653589793238462643383279502884197`.
    * Added `tee`, which mimics the Unix/Linux tee utility, i.e. prints
      arguments on screen and in a file.
    * Added `screening.py` for applying Morris' Method on arbitrary functions,
      providing the function `screening` that samples trajectories with
      `morris_sampling` of `morris_method.py`, applies a function on these
      trajectories, and calculates Elementary Effects with function
      `elementary_effects` of `morris_method.py`.
      It also provides a wrapper function `ee` for `screening`.
    * Added `morris_method.py` for Morris' Method with functions
      `morris_sampling` and `elementary_effects` to sample trajectories in
      parameter space and to calculate Elementary Effects from model output on
      trajectories.
    * Copied routines from JAMS package https://github.com/mcuntz/jams_python,
      formatted docstrings in numpydoc format, made the code flake8 compatible,
      and added extensive tests. Routines in JAMS get DeprecationWarning.
