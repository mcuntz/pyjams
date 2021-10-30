Contributing to pyjams
======================

``pyjams`` development is driven by user feedback, and your contributions help
to find bugs, add features, and improve performance. This is a small guide to
help those who wish to contribute.

We are happy about all contributions! :thumbsup:

Did you find a bug?
    * Ensure that the bug was not already reported under `GitHub
      issues`_.
    * If the bug was not already reported, open a `new issue`_ with a clear
      description of the problem and if possible with a `minimal working
      example`_.
    * Please add the version number to the issue:

      .. code-block:: python

         import pyjams
         print(pyjams.__version__)

Do you have suggestions for new features?
    * Open a `new issue`_ with your idea or suggestion and we'd love to discuss
      about it.

Do you want to enhance pyjams or fix something?
    * Fork the repo on GitHub_.
    * Fix a routine or add a new module in `src/pyjams`.
    * Import a new routine in `src/pyjams/__init__.py` and add it to `__all__`.
    * Add some tests either in an existing `tests/test_*.py` file or create a
      new test class in a new file under `tests/`.
    * Add a new module to the automatic documentation by creating a
      reStructuredText file in `docs/source/` as in the example given by
      `docs/source/tee.rst`.
    * Add the name of the reStructuredText file to `docs/source/api.rst`.
    * Add the functions with short descriptions to the alphabetical list and
      the list per category in `README.rst`. 
    * Do the same in `docs/source/index.rst` but using markup such as `:mod:`
      and `:func:`.
    * Add yourself to `AUTHORS.rst`, if you want to.
    * Push to your fork and submit a pull request.


.. _GitHub: https://github.com/mcuntz/pyjams
.. _GitHub issues: https://github.com/mcuntz/pyjams/issues
.. _new issue: https://github.com/mcuntz/pyjams/issues
.. _minimal working example: https://en.wikipedia.org/wiki/Minimal_working_example
