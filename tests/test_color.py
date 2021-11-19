#!/usr/bin/env python
"""
This is the unittest for color module.

python -m unittest -v tests/test_color.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_color.py

"""
from __future__ import division, absolute_import, print_function
import unittest


def _rgb2rgb(col):
    """
    Transform RGB tuple with values 0-255 to tuple with values 0-1
    """
    return tuple([ i / 255. for i in col ])


def _to_grey(col):
    """
    Transform RGB tuple to grey values
    """
    isgrey = 0.2125 * col[0] + 0.7154 * col[1] + 0.072 * col[2]
    return (isgrey, isgrey, isgrey)


class TestColor(unittest.TestCase):
    """
    Tests for color.py
    """

    def test_get_cmap(self):
        import matplotlib as mpl
        mpl.use('Agg')
        import matplotlib.pyplot as plt  # needed to work
        from pyjams.color import get_cmap
        from pyjams.color import brewer_sequential
        from pyjams.color import mathematica_rainbow
        from pyjams.color import ncl_small
        from pyjams.color import oregon_sequential
        from pyjams.color import sron2012_colors, sron2012_functions
        from pyjams.color import sron_colors, sron_colormaps, sron_functions

        # brewer
        brewer_ylgn3 = brewer_sequential['brewer_ylgn3']
        brewer_ylgn3 = [ _rgb2rgb(i) for i in brewer_ylgn3 ]

        # mathematica
        mathematica_dark_rainbow_8 = (
            mathematica_rainbow['mathematica_dark_rainbow_8'])

        # ncl
        ncl_amwg = ncl_small['ncl_amwg']

        # oregon
        osu_bu7 = oregon_sequential['osu_bu7']
        osu_bu7 = [ _rgb2rgb(i) for i in osu_bu7 ]

        # sron2012
        sron2012_light = sron2012_colors['sron2012_light']
        sron2012_light = [ mpl.colors.colorConverter.to_rgb(i)
                           for i in sron2012_light ]

        sron2012_ylorbr_3 = [ sron2012_functions['sron2012_ylorbr'](i/2.)
                              for i in range(3) ]
        sron2012_buylrd_3 = [ sron2012_functions['sron2012_buylrd'](i/2.)
                              for i in range(3) ]
        sron2012_rainbow_3 = [ sron2012_functions['sron2012_rainbow'](i/2.)
                               for i in range(3) ]

        # sron
        sron_vibrant = sron_colors['sron_vibrant']
        sron_vibrant = [ mpl.colors.colorConverter.to_rgb(i)
                         for i in sron_vibrant ]

        sron_iridescent = sron_colormaps['sron_iridescent']
        sron_iridescent_miss = mpl.colors.colorConverter.to_rgba(
            sron_iridescent[1])
        sron_iridescent = [ mpl.colors.colorConverter.to_rgb(i)
                            for i in sron_iridescent[0] ]

        sron_rainbow_discrete = sron_functions['sron_rainbow_discrete']

        sron_rainbow_discrete_3 = sron_rainbow_discrete(3)
        sron_rainbow_discrete_3_miss = mpl.colors.colorConverter.to_rgba(
            sron_rainbow_discrete_3[1])
        sron_rainbow_discrete_3 = [ mpl.colors.colorConverter.to_rgb(i)
                                    for i in sron_rainbow_discrete_3[0] ]

        sron_rainbow_discrete_23 = sron_rainbow_discrete()
        sron_rainbow_discrete_23_miss = mpl.colors.colorConverter.to_rgba(
            sron_rainbow_discrete_23[1])
        sron_rainbow_discrete_23 = [ mpl.colors.colorConverter.to_rgb(i)
                                     for i in sron_rainbow_discrete_23[0] ]

        # brewer
        cmap = get_cmap('brewer_ylgn3')
        target = brewer_ylgn3
        self.assertEqual(cmap, target)

        # resample
        cmap = get_cmap('brewer_ylgn3', ncol=2)
        target = [brewer_ylgn3[0], brewer_ylgn3[2]]
        self.assertEqual(cmap, target)

        # color map
        cmap = get_cmap('brewer_ylgn3', as_cmap=True)
        assert isinstance(cmap, mpl.colors.ListedColormap)

        # reverse
        cmap = get_cmap('brewer_ylgn3', reverse=True)
        target = brewer_ylgn3[::-1]
        self.assertEqual(cmap, target)

        cmap = get_cmap('brewer_ylgn3_r')
        target = brewer_ylgn3[::-1]
        self.assertEqual(cmap, target)

        # grey
        cmap = get_cmap('brewer_ylgn3', grey=True)
        target = [ _to_grey(i) for i in brewer_ylgn3 ]
        self.assertEqual(cmap, target)

        # mathematica
        cmap = get_cmap('mathematica_dark_rainbow_8')
        target = mathematica_dark_rainbow_8
        self.assertEqual(cmap, target)

        # ncl
        cmap = get_cmap('ncl_amwg')
        target = ncl_amwg
        self.assertEqual(cmap, target)

        # oregon
        cmap = get_cmap('osu_bu7')
        target = osu_bu7
        self.assertEqual(cmap, target)

        # sron2012_colors
        cmap = get_cmap('sron2012_light')
        target = sron2012_light
        self.assertEqual(cmap, target)

        # sron2012_functions
        cmap = get_cmap('sron2012_ylorbr', ncol=3)
        target = sron2012_ylorbr_3
        self.assertEqual(cmap, target)

        # sron2012_functions
        cmap = get_cmap('sron2012_buylrd', ncol=3)
        target = sron2012_buylrd_3
        self.assertEqual(cmap, target)

        # sron2012_functions
        cmap = get_cmap('sron2012_rainbow', 3)
        target = sron2012_rainbow_3
        self.assertEqual(cmap, target)

        # sron2012_functions - ncol=0
        cmap = get_cmap('sron2012_rainbow')
        target = [ sron2012_functions['sron2012_rainbow'](i/255.)
                   for i in range(256) ]
        self.assertEqual(cmap, target)

        # sron2012_functions - offset, upper
        cmap = get_cmap('sron2012_rainbow', ncol=3, offset=0.2, upper=0.9)
        target = [ sron2012_functions['sron2012_rainbow'](0.2+i*0.7/2.)
                   for i in range(3) ]
        self.assertEqual(cmap, target)

        # sron_colors
        cmap = get_cmap('sron_vibrant')
        target = sron_vibrant
        self.assertEqual(cmap, target)

        # sron_colormaps
        cmap = get_cmap('sron_iridescent')
        target = sron_iridescent
        self.assertEqual(cmap, target)

        # sron_colormaps - as_cmap, miss
        cmap = get_cmap('sron_iridescent', as_cmap=True)
        cols = cmap.colors
        target = sron_iridescent
        self.assertEqual(cols, target)
        if mpl.__version__ > '3.4.0':
            miss = tuple(cmap.get_bad())
            target = sron_iridescent_miss
            self.assertEqual(miss, target)

        # sron_functions
        cmap = get_cmap('sron_rainbow_discrete', 3)
        target = sron_rainbow_discrete_3
        self.assertEqual(cmap, target)
        cmap = get_cmap('sron_rainbow_discrete', 23)
        target = sron_rainbow_discrete_23
        self.assertEqual(cmap, target)

        # sron_functions - as_cmap, miss
        cmap = get_cmap('sron_rainbow_discrete', ncol=3, as_cmap=True)
        cols = cmap.colors
        target = sron_rainbow_discrete_3
        self.assertEqual(cols, target)
        if mpl.__version__ > '3.4.0':
            miss = tuple(cmap.get_bad())
            target = sron_rainbow_discrete_3_miss
            self.assertEqual(miss, target)
        cmap = get_cmap('sron_rainbow_discrete', as_cmap=True)
        cols = cmap.colors
        target = sron_rainbow_discrete_23
        self.assertEqual(cols, target)
        if mpl.__version__ > '3.4.0':
            miss = tuple(cmap.get_bad())
            target = sron_rainbow_discrete_23_miss
            self.assertEqual(miss, target)

        # matplotlib - ListedColormap
        cmap = get_cmap('viridis')
        target = mpl.cm.get_cmap('viridis').colors
        self.assertEqual(cmap, target)

        # matplotlib - LinearSegmentedColormap
        cmap = get_cmap('Blues')
        target = mpl.cm.get_cmap('Blues')
        target = [ target(i) for i in range(target.N) ]
        self.assertEqual(cmap, target)

        # matplotlib - ListedColormap - upper-/lowercase
        cmap = get_cmap('Viridis')
        target = mpl.cm.get_cmap('viridis').colors
        self.assertEqual(cmap, target)

        # matplotlib - LinearSegmentedColormap - upper-/lowercase
        cmap = get_cmap('blues')
        target = mpl.cm.get_cmap('Blues')
        target = [ target(i) for i in range(target.N) ]
        self.assertEqual(cmap, target)

        # nonsense name
        self.assertRaises(ValueError, get_cmap, 'NonSense')

    def test_print_palettes(self):
        from pyjams.color import print_palettes

        assert print_palettes('mathetamica') is None
        assert print_palettes(['mathetamica', 'matplotlib']) is None
        assert print_palettes() is None


if __name__ == "__main__":
    unittest.main()
