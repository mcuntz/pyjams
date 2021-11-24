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
        assert str2tex(strin, usetex=True) == out
        assert str2tex(strin, bold=True, usetex=True) == (
            out.replace('rm', 'bf'))
        assert str2tex(strin, italic=True, usetex=True) == (
            out.replace('rm', 'it'))
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True,
                          usetex=True)
        assert str2tex(strin, space2linebreak=True, usetex=True) == out
        assert str2tex(strin, usetex=False) == strin
        assert str2tex(strin, usetex=False, space2linebreak=True) == strin

        # list and -
        strin = ['One-', 'One-Two']
        out = [r'$\mathrm{One}$$\textrm{-}$',
               r'$\mathrm{One}$$\textrm{-}$$\mathrm{Two}$']
        self.assertEqual(str2tex(strin, usetex=True), out)
        outbf = [ i.replace('rm', 'bf') for i in out ]
        self.assertEqual(str2tex(strin, bold=True, usetex=True), outbf)
        outit = [ i.replace('rm', 'it') for i in out ]
        self.assertEqual(str2tex(strin, italic=True, usetex=True), outit)
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True,
                          usetex=True)
        self.assertEqual(str2tex(strin, space2linebreak=True, usetex=True),
                         out)
        self.assertEqual(str2tex(strin, usetex=False), strin)
        self.assertEqual(str2tex(strin, usetex=False, space2linebreak=True),
                         strin)

        # tuple, space and linebreak
        strin = ('One Two', r'One\nTwo')
        out = (r'$\mathrm{One\ Two}$',
               r'$\mathrm{One}$\newline$\mathrm{Two}$')
        self.assertEqual(str2tex(strin, usetex=True), out)
        outbf = tuple([ i.replace('rm', 'bf') for i in out ])
        self.assertEqual(str2tex(strin, bold=True, usetex=True), outbf)
        outit = tuple([ i.replace('rm', 'it') for i in out ])
        self.assertEqual(str2tex(strin, italic=True, usetex=True), outit)
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True,
                          usetex=True)
        outsp = tuple([ out[1] for i in out ])
        self.assertEqual(str2tex(strin, space2linebreak=True, usetex=True),
                         outsp)
        outn = tuple([ i.replace(r'\n', ''+'\n'+'') for i in strin ])
        self.assertEqual(str2tex(strin, usetex=False), outn)
        strinsp = tuple([ i.replace(' ', ''+'\n'+'') for i in outn ])
        self.assertEqual(str2tex(strin, usetex=False, space2linebreak=True),
                         strinsp)

        # ndarray incl. LaTeX
        strin = np.array([r'A $S_{Ti}$ is great\nbut use-less-'])
        out = np.array([r'$\mathrm{A\ }$$S_{Ti}$$\mathrm{\ is\ great}$\newline'
                        r'$\mathrm{but\ use}$$\textrm{-}$$\mathrm{less}$'
                        r'$\textrm{-}$'])
        self.assertEqual(str2tex(strin, usetex=True), out)
        outbf = np.array([ i.replace('rm', 'bf') for i in out ])
        self.assertEqual(str2tex(strin, bold=True, usetex=True), outbf)
        outit = np.array([ i.replace('rm', 'it') for i in out ])
        self.assertEqual(str2tex(strin, italic=True, usetex=True), outit)
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True,
                          usetex=True)
        outsp = np.array([r'$\mathrm{A}$\newline$S_{Ti}$\newline$\mathrm{is}$'
                          r'\newline$\mathrm{great}$\newline$\mathrm{but}$'
                          r'\newline$\mathrm{use}$$\textrm{-}$$\mathrm{less}$'
                          r'$\textrm{-}$'])
        self.assertEqual(str2tex(strin, space2linebreak=True, usetex=True),
                         outsp)
        outn = tuple([ i.replace(r'\n', ''+'\n'+'') for i in strin ])
        self.assertEqual(str2tex(strin, usetex=False), outn)
        strinsp = tuple([ i.replace(' ', ''+'\n'+'') for i in outn ])
        self.assertEqual(str2tex(strin, usetex=False, space2linebreak=True),
                         strinsp)

        # complex string incl. LaTeX but use \n
        strin = r'$\alpha$Com_plex-str^ing\n(% of #string m$^{-2}$)$\alpha$'
        out = (r'$\alpha$$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
               r'\newline$\mathrm{(\%\ of\ \#string\ m}$$^{-2}$$\mathrm{)}$'
               r'$\alpha$')
        assert str2tex(strin, usetex=True) == out
        assert str2tex(strin, bold=True, usetex=True) == (
            out.replace('rm', 'bf'))
        assert str2tex(strin, italic=True, usetex=True) == (
            out.replace('rm', 'it'))
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True,
                          usetex=True)
        outsp = (r'$\alpha$$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
                 r'\newline$\mathrm{(\%}$\newline$\mathrm{of}$\newline'
                 r'$\mathrm{\#string}$\newline$\mathrm{m}$$^{-2}$$\mathrm{)}$'
                 r'$\alpha$')
        assert str2tex(strin, space2linebreak=True, usetex=True) == outsp
        strinu = strin.replace(r'\n', ''+'\n'+'').replace('%', r'\%')
        self.assertEqual(str2tex(strin, usetex=False), strinu)
        strinsp = strinu.replace(' ', ''+'\n'+'')
        self.assertEqual(str2tex(strin, usetex=False, space2linebreak=True),
                         strinsp)

        # complex string incl. LaTeX
        strin = r'$\alpha$Com_plex-str^ing\newline(% of #string m$^{-2}$)$\alpha$'
        out = (r'$\alpha$$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
               r'\newline$\mathrm{(\%\ of\ \#string\ m}$$^{-2}$$\mathrm{)}$'
               r'$\alpha$')
        assert str2tex(strin, usetex=True) == out
        assert str2tex(strin, bold=True, usetex=True) == (
            out.replace('rm', 'bf'))
        assert str2tex(strin, italic=True, usetex=True) == (
            out.replace('rm', 'it'))
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True,
                          usetex=True)
        outsp = (r'$\alpha$$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
                 r'\newline$\mathrm{(\%}$\newline$\mathrm{of}$\newline'
                 r'$\mathrm{\#string}$\newline$\mathrm{m}$$^{-2}$$\mathrm{)}$'
                 r'$\alpha$')
        assert str2tex(strin, space2linebreak=True, usetex=True) == outsp
        strinu = strin.replace(r'\newline', ''+'\n'+'').replace('%', r'\%')
        self.assertEqual(str2tex(strin, usetex=False), strinu)
        strinsp = strinu.replace(' ', ''+'\n'+'')
        self.assertEqual(str2tex(strin, usetex=False, space2linebreak=True),
                         strinsp)

        # complex string no LaTeX no raw string
        strin = 'Com_plex-str^ing (% of #string m)'
        out = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing'
               r'\ (\%\ of\ \#string\ m)}$')
        assert str2tex(strin, usetex=True) == out
        assert str2tex(strin, bold=True, usetex=True) == (
            out.replace('rm', 'bf'))
        assert str2tex(strin, italic=True, usetex=True) == (
            out.replace('rm', 'it'))
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True,
                          usetex=True)
        outsp = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
                 r'\newline$\mathrm{(\%}$\newline$\mathrm{of}$\newline$\mathrm{\#string}$'
                 r'\newline$\mathrm{m)}$')
        assert str2tex(strin, space2linebreak=True, usetex=True) == outsp
        strinu = strin.replace(r'\n', ''+'\n'+'').replace('%', r'\%')
        assert str2tex(strin, usetex=False) == strinu
        strinsp = strinu.replace(' ', ''+'\n'+'')
        assert str2tex(strin, usetex=False, space2linebreak=True) == strinsp

        # complex string no LaTeX using \n
        strin = r'Com_plex-str^ing\n(% of #string m)-'
        out = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
               r'\newline$\mathrm{(\%\ of\ \#string\ m)}$$\textrm{-}$')
        assert str2tex(strin, usetex=True) == out
        assert str2tex(strin, bold=True, usetex=True) == (
            out.replace('rm', 'bf'))
        assert str2tex(strin, italic=True, usetex=True) == (
            out.replace('rm', 'it'))
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True,
                          usetex=True)
        outsp = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
                 r'\newline$\mathrm{(\%}$\newline$\mathrm{of}$\newline'
                 r'$\mathrm{\#string}$\newline$\mathrm{m)}$$\textrm{-}$')
        assert str2tex(strin, space2linebreak=True, usetex=True) == outsp
        strinu = strin.replace(r'\n', ''+'\n'+'').replace('%', r'\%')
        assert str2tex(strin, usetex=False) == strinu
        strinsp = strinu.replace(' ', ''+'\n'+'')
        assert str2tex(strin, usetex=False, space2linebreak=True) == strinsp

        # complex string no LaTeX using \newline
        strin = r'Com_plex-str^ing\newline(% of #string m)-'
        out = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
               r'\newline$\mathrm{(\%\ of\ \#string\ m)}$$\textrm{-}$')
        assert str2tex(strin, usetex=True) == out
        assert str2tex(strin, bold=True, usetex=True) == (
            out.replace('rm', 'bf'))
        assert str2tex(strin, italic=True, usetex=True) == (
            out.replace('rm', 'it'))
        self.assertRaises(ValueError, str2tex, strin, bold=True, italic=True,
                          usetex=True)
        outsp = (r'$\mathrm{Com\_plex}$$\textrm{-}$$\mathrm{str\^ing}$'
                 r'\newline$\mathrm{(\%}$\newline$\mathrm{of}$\newline'
                 r'$\mathrm{\#string}$\newline$\mathrm{m)}$$\textrm{-}$')
        assert str2tex(strin, space2linebreak=True, usetex=True) == outsp
        strinu = strin.replace(r'\newline', ''+'\n'+'').replace('%', r'\%')
        assert str2tex(strin, usetex=False) == strinu
        strinsp = strinu.replace(' ', ''+'\n'+'')
        assert str2tex(strin, usetex=False, space2linebreak=True) == strinsp


if __name__ == "__main__":
    unittest.main()
