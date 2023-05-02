Changelog
---------

v1.30 (May 2023)
    * Replace plotly with hvplot in `mcPlot`.
    * Add unicode symbol degree \u00B0, which gets replaced by ^\circ
      if usetex==True in str2tex.
    * Do not escape % if not usetex in str2tex.
    * Make `get_variable_definition` public in ncio.
    * Correct docstring of strip keyword in fsread and xread.
    * Added `filebase` to helpers.
    * Exchanged functions and wrapper functions in readnetcdf.

v1.29 (Jan 2023)
    * Added functions `eair2rhair`, `rhair2eair`, `eair2vpd`, `vpd2eair`,
      `rhair2vpd`, `vpd2rhair`, `eair2shair`, `shair2eair`, `eair2mrair`,
      `mrair2eair`, for conversions between partial pressure, relative humidity,
      and specific humidity of water vapour in air.
    * Renamed module `esat` to `air_humidity`.
    * Correct treating of undef if two arrays given in `array2input` helper
      function.
    * Updated all constants related to gases in `const` module for redefinition
      of SI units of 2019.
    * Renamed some constants in `const` for greater consistency.
    * Keyword only_use_pyjams_datetimes in `num2date` to be able to use all
      implemented methods of `datetime` class.
    * Allow also CF-calendars in `datetime` class.
    * Updated tests for `sce`.

v1.28 (Jan 2023)
    * Add `updatez` and `updatez_compressed` to update arrays in a single file
      in numpy's npz format.
    * Do not set color for missing data; only existed for sron palettes.
    * Add --dpi as a standard option in `mcPlot`.
    * Use mpl.colormaps[name] instead of mpl.colormaps.get_cmap(name)
      to replace mpl.cm.get_cmap(name) to work with matplotlib < v3.6.

v1.27 (Dec 2022)
    * Assure 4-digit years and catch %04Y format errors on Windows in
      `date2date` and in datetime class.
    * Use assert_almost_equal for fractional days with microseconds in tests of
      datetime class
    * Changed matplotlib.cm.get_cmap to matplotlib.colormaps.get_cmap in
      color module and tests.
    * Skip test for float128 on Windows in `ncio`.
    * Python 3.6 might not be fully supported anymore.
    * Remove dependency to ``partialwrap`` for tests.
    * Remove dependency to ``partialwrap`` for tests.
    * Adding `sce` the Shuffled-Complex-Evolution algorithm for function
      minimization.
    * Adding 'a wide variety of' to ``pyjams`` key phrase.
    * NA to NaN, i.e. R to Python convention in `fsread`.

v1.26 (Jul 2022)
    * round_microseconds method for `datetime` class if dates are from
      non-microsecond precise origin.
    * Added return_arrays keyword in `date2num`.
    * calendar keyword takes precedence on calendar attribute of
      datetime objects in `date2num`.
    * Add left, bottom, top to standard layout options in `mcPlot`.
    * Documented as_cmap keyword of `get_cmap`.
    * Added `means` to calculate daily, monthly, yearly, etc. means.
    * Allow scalar input in `num2date`.
    * Renamed `datetime.py` to `class_datetime.py`.

v1.25 (Jun 2022)
    * Allow negative dates in `date2date`.
    * Support of microseconds in `date2date`.
    * Assure that `input2array` gives no 0d-array.
    * More `datetime` tests and bug fixes for microseconds and has_year_zero.
    * Delete unnecessary HDF5 filters in variable definition in `netcdfio`
      for compatibility with netcdf4 > 1.6.0.
    * Reduce precision to 14 digits for tests of `logistic2_offset`.
    * Remove Python version 3.7 from CI but leave version 3.6 because of
      problems with netcdf4 for 3.7 on Windows.

v1.24 (Jun 2022)
    * Removed documentation from `Read the Docs` and moved to Github Pages:
      https://mcuntz.github.io/pyjams/
    * More `datetime` tests and bug fixes.

v1.23 (Jun 2022)
    * Added module `datetime` with class `datetime` that mimics cftime.datetime
      but for non-CF-conform calendars. It also adds the functions `date2num`
      and `num2date` for conversion between datetime objects or string
      representations and numerical times. It adds the convenience wrappers
      `date2dec` and `dec2date` for easier portability of older code using
      JAMS.
    * Allows more usage of helper functions `input2array` and `array2input`
      by allowing undef=None in and making it the default.
    * Make netCDF4 an requirement of ``pyjams``.
    * Use I/O type helpers in `str2tex`.
    * Use I/O type helpers in `date2date`.
    * Allow strings and string arrays in `array2input` and `input2array`.
    * Add kwargs mechanism to `plot_save` in `mcPlot` to pass arguments
      to save_file.
    * Add --transparent as a standard option in `mcPlot`.

v1.22 (May 2022)
    * Added module `ncio` with netCDF4 functions to copy netcdf files while
      doing some transformations on variables and dimensions.
    * Added shape keyword to `infonetcdf`.
    * Assert that at least one of nc, snc, cname, or sname is given in call to
      `xread`.
    * Change from NCL amwg to pyjams amwg as the default color palette in
      `mcPlot`.

v1.21 (Apr 2022)
    * Added `pyjams_amwg` color map.
    * Bandwidth h output of `kernel_regression_h` is scalar if one-dimensional.
    * undef=np.nan is default in helper functions `array2input` and
      `input2array`.
    * Array masked or set to undef only if shapes of array and input agree in
      `array2input`.
    * Output of `kernel_regression` now has the type of `y` and not `x` or
      `xout`.
    * `get_color` can get list of colors and not only single colors.
    * Register ufz colors only once with `get_color`.
    * Add `print_colors` to print known named colors to console.

v1.20 (Apr 2022)
    * Add `gridcellarea` to calculate the area of grid cells on Earth in
      square metre.
    * Add `kernel_regression` and `kernel_regression_h` for multi-dimensional
      non-parametric kernel regression.

v1.19 (Mar 2022)
    * Add `infonetcdf` and `readnetcdf` to get variables from or print
      information of a netcdf file.
    * Add `get_color` to get value of named colors known to Matplotlib.
    * Added named colors of the guidelines of the Helmholtz Centre for
      Environmental Research - UFZ, Leipzig, Germany.

v1.18 (Mar 2022)
    * Use `array2input` and `input2array` in `division`, correcting bug with
      scalar input and getting rid of numpy geterr and seterr.
    * Enhanced `array2input` to take second input variable.
    * Added functions `isundef` in `helper` module to deal with NaN and Inf.
    * Added 'order' keyword to `get_cmap`.
    * Added functions `array2input` and `input2array` in new `helper` module to
      assure same input and output types. Use them in `esat` and
      `alpha_equ_h2o`. The `helper` module is not in `__init__.py` nor in the
      documentation (yet?).
    * Return numpy array if type(input)(output) fails for unknown iterable
      types in `esat` and `alpha_equ_h2o`.

v1.17 (Jan 2022)
    * Always close open files in module `fsread`.
    * Set default fill_value to NaN for floats in module `fsread`.
    * Remove read_only mode for openpyxl in `xread` because closing is disabled
      in this case.
    * Change handling of return type to allow more (unspecific) iterable types
      such as pandas time series in `esat` and `alpha_equ_h2o`.
    * Added `xread`, `xlsread`, and `xlsxread`, reading numbers and strings
      from an Excel file into 2D float and string arrays.

v1.16 (Jan 2022)
    * Added `mad`, median absolute deviation test.

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
