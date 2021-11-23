#!/usr/bin/env python
"""
This is the unittest for romanliterals module.

python -m unittest -v tests/test_romanliterals.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_romanliterals.py

"""
from __future__ import division, absolute_import, print_function
import unittest


class TestRomanliterals(unittest.TestCase):
    """
    Tests for romanliterals.py
    """

    def test_int2roman(self):
        from pyjams import int2roman

        assert int2roman(1) == 'I'
        assert int2roman(19) == 'XIX'
        assert int2roman(159) == 'CLIX'
        assert int2roman(159, lower=True) == 'clix'

    def test_roman2int(self):
        from pyjams import roman2int

        assert roman2int('I') == 1
        assert roman2int('i') == 1
        assert roman2int('iv') == 4
        assert roman2int('MCCCLIV') == 1354


if __name__ == "__main__":
    unittest.main()
