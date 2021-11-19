#!/usr/bin/env python
"""
This is the unittest for str2tex module.

python -m unittest -v tests/test_str2tex.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_str2tex.py

"""
from __future__ import division, absolute_import, print_function
import unittest


class TestStr2Tex(unittest.TestCase):
    """
    Tests for str2tex.py
    """

    def test_str2tex(self):
        import numpy as np
        from pyjams import str2tex

        # string
        strin = 'One'
        out = r'$\mathrm{One}$'
        assert str2tex(strin) == out
        assert str2tex(strin, bold=True) == out.replace('rm', 'bf')
        assert str2tex(strin, italic=True) == out.replace('rm', 'it')
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True)
        assert str2tex(strin, space2linebreak=True) == out
        assert str2tex(strin, usetex=False) == strin
        assert str2tex(strin, usetex=False, space2linebreak=True) == strin

        # list and -
        strin = ['One-', 'One-Two']
        out = [r'$\mathrm{One}$$\textrm{-}$',
               r'$\mathrm{One}$$\textrm{-}$$\mathrm{Two}$']
        self.assertEqual(str2tex(strin), out)
        outbf = [ i.replace('rm', 'bf') for i in out ]
        self.assertEqual(str2tex(strin, bold=True), outbf)
        outit = [ i.replace('rm', 'it') for i in out ]
        self.assertEqual(str2tex(strin, italic=True), outit)
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True)
        self.assertEqual(str2tex(strin, space2linebreak=True), out)
        self.assertEqual(str2tex(strin, usetex=False), strin)
        self.assertEqual(str2tex(strin, usetex=False, space2linebreak=True),
                         strin)

        # tuple, space and linebreak
        strin = ('One Two', r'One\nTwo')
        out = (r'$\mathrm{One\ Two}$',
               r'$\mathrm{One}$ \n $\mathrm{Two}$')
        self.assertEqual(str2tex(strin), out)
        outbf = tuple([ i.replace('rm', 'bf') for i in out ])
        self.assertEqual(str2tex(strin, bold=True), outbf)
        outit = tuple([ i.replace('rm', 'it') for i in out ])
        self.assertEqual(str2tex(strin, italic=True), outit)
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True)
        outsp = tuple([ out[1] for i in out ])
        self.assertEqual(str2tex(strin, space2linebreak=True), outsp)
        self.assertEqual(str2tex(strin, usetex=False), strin)
        strinsp = tuple([ i.replace(' ', r'\n') for i in strin ])
        self.assertEqual(str2tex(strin, usetex=False, space2linebreak=True),
                         strinsp)

        # ndarray incl. LaTeX
        strin = np.array([r'A $S_{Ti}$ is great\nbut use-less-'])
        out = np.array([r'$\mathrm{A\ }$$S_{Ti}$$\mathrm{\ is\ great}$ \n '
                        r'$\mathrm{but\ use}$$\textrm{-}$$\mathrm{less}$'
                        r'$\textrm{-}$'])
        self.assertEqual(str2tex(strin), out)
        outbf = np.array([ i.replace('rm', 'bf') for i in out ])
        self.assertEqual(str2tex(strin, bold=True), outbf)
        outit = np.array([ i.replace('rm', 'it') for i in out ])
        self.assertEqual(str2tex(strin, italic=True), outit)
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True)
        outsp = np.array([r'$\mathrm{A}$ \n $S_{Ti}$ \n $\mathrm{is}$ \n '
                          r'$\mathrm{great}$ \n $\mathrm{but}$ \n '
                          r'$\mathrm{use}$$\textrm{-}$$\mathrm{less}$'
                          r'$\textrm{-}$'])
        self.assertEqual(str2tex(strin, space2linebreak=True), outsp)
        self.assertEqual(str2tex(strin, usetex=False), strin)
        strinsp = np.array([ i.replace(' ', r'\n') for i in strin ])
        self.assertEqual(str2tex(strin, usetex=False, space2linebreak=True),
                         strinsp)

        # complex string incl. LaTeX
        strin = r'$\alpha$Com_plex-str^ing\n(% of #string m$^{-2}$)$\alpha$'
        out = (r'$\alpha$$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
               r' \n $\mathrm{(\%\ of\ \#string\ m}$$^{-2}$$\mathrm{)}$'
               r'$\alpha$')
        assert str2tex(strin) == out
        assert str2tex(strin, bold=True) == out.replace('rm', 'bf')
        assert str2tex(strin, italic=True) == out.replace('rm', 'it')
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True)
        outsp = (r'$\alpha$$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
                 r' \n $\mathrm{(\%}$ \n $\mathrm{of}$ \n $\mathrm{\#string}$'
                 r' \n $\mathrm{m}$$^{-2}$$\mathrm{)}$$\alpha$')
        assert str2tex(strin, space2linebreak=True) == outsp
        strinu = strin.replace('%', r'\%')
        assert str2tex(strin, usetex=False) == strinu
        strinsp = strin.replace(' ', r'\n').replace('%', r'\%')
        assert str2tex(strin, usetex=False, space2linebreak=True) == strinsp

        # complex string no LaTeX no raw string
        strin = 'Com_plex-str^ing (% of #string m)'
        out = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing'
               r'\ (\%\ of\ \#string\ m)}$')
        assert str2tex(strin) == out
        assert str2tex(strin, bold=True) == out.replace('rm', 'bf')
        assert str2tex(strin, italic=True) == out.replace('rm', 'it')
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True)
        outsp = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
                 r' \n $\mathrm{(\%}$ \n $\mathrm{of}$ \n $\mathrm{\#string}$'
                 r' \n $\mathrm{m)}$')
        assert str2tex(strin, space2linebreak=True) == outsp
        strinu = strin.replace('%', r'\%')
        assert str2tex(strin, usetex=False) == strinu
        strinsp = strin.replace(' ', r'\n').replace('%', r'\%')
        assert str2tex(strin, usetex=False, space2linebreak=True) == strinsp

        # complex string no LaTeX
        strin = r'Com_plex-str^ing\n(% of #string m)-'
        out = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
               r' \n $\mathrm{(\%\ of\ \#string\ m)}$$\textrm{-}$')
        assert str2tex(strin) == out
        assert str2tex(strin, bold=True) == out.replace('rm', 'bf')
        assert str2tex(strin, italic=True) == out.replace('rm', 'it')
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True)
        outsp = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
                 r' \n $\mathrm{(\%}$ \n $\mathrm{of}$ \n $\mathrm{\#string}$'
                 r' \n $\mathrm{m)}$$\textrm{-}$')
        assert str2tex(strin, space2linebreak=True) == outsp
        strinu = strin.replace('%', r'\%')
        assert str2tex(strin, usetex=False) == strinu
        strinsp = strin.replace(' ', r'\n').replace('%', r'\%')
        assert str2tex(strin, usetex=False, space2linebreak=True) == strinsp


if __name__ == "__main__":
    unittest.main()