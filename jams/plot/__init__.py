#!/usr/bin/env python
from __future__ import division, absolute_import, print_function
"""
    Code snippets for plotting.


    Snippets
    --------
    set_outtype   


    Example
    -------
    >>> import numpy as np
    >>> from autostring import astr
    >>> print(astr(np.array(jams.color.ufzdarkblue), 4))
    ['0.0000' '0.2431' '0.4314']

    >>> print(colours('ufzdarkblue', rgb256=True))
    (0, 62, 110)

    >>> print(colours(names=True)[0:3])
    ['ufzdarkblue', 'ufzblue', 'ufzlightblue']

    >>> print(astr(np.array(jams.color.colours('JAMSDARKBLUE')), 4))
    ['0.0000' '0.2431' '0.4314']

    >>> print(astr(np.array(jams.color.colours('DarkBlue')), 4))
    ['0.0000' '0.2431' '0.4314']

    >>> print(jams.color.colours(['orange','ufzdarkblue'], rgb256=True))
    [(207, 104, 0), (0, 62, 110)]


    # Print
    # jams.color.print_brewer('diverging')

    # Plot
    # jams.color.plot_brewer('brew_')

    # Get Names
    # names = jams.color.get_brewer(names='sequential')

    # Register colour map and get colour map handle
    # cc = jams.color.get_brewer('RdYlBu11')
    # plt.pcolormesh(np.outer(np.arange(cc.N), np.ones(cc.N)), cmap=cc)

    # Get RGB colours of colour map
    # cc = jams.color.get_brewer('blues4', rgb=True)
    # mark1 = sub.plot(x, y)
    # plt.setp(mark1, linestyle='None', marker='o', markeredgecolor=cc[0], markerfacecolor='None')

    # Register and use colour map
    # from scipy import misc
    # lena = misc.lena()
    # plt.imshow(l, cmap=mpl.cm.rainbow)
    # jams.color.register_brewer('ncl_meteo_swiss')
    # plt.imshow(l, cmap=mpl.cm.get_cmap('hotcold_18lev'))
    # plt.imshow(l, cmap=jams.get_brewer('hotcold_18lev'))


    >>> print(jams.color.brewer_sequential['blues4'])
    [(239, 243, 255), (189, 215, 231), (107, 174, 214), (33, 113, 181)]

    >>> jams.color.print_brewer('qualitative')[0:7]
    ['set33', 'set34', 'set35', 'set36', 'set37', 'set38', 'set39']

    >>> print(astr(np.array(jams.color.get_brewer('blues4', rgb=True)[0]), 4))
    ['0.9373' '0.9529' '1.0000']

    >>> print(jams.color.get_brewer('Blues4', rgb256=True)[0])
    (239, 243, 255)

    >>> cc = jams.color.get_brewer('bLuEs4', rgb256=True, reverse=True)
    >>> print(cc[-1])
    (239, 243, 255)
    >>> print(cc[0])
    (33, 113, 181)

    >>> print(astr(np.array(jams.color.get_brewer('blues4', rgb256=True, grey=True)[0]), 4))
    ['242.9897' '242.9897' '242.9897']


    >>> r = (1.0,0.0,0.0)
    >>> b = (0.0,0.0,1.0)
    >>> print(jams.color.rgb_blend(r,b,0.0), jams.color.rgb_blend(r,b,0.5), jams.color.rgb_blend(r,b,1.0))
    (1.0, 0.0, 0.0) (0.5, 0.0, 0.5) (0.0, 0.0, 1.0)

    >>> print(jams.color.rgb_range(r,b,3))
    [(1.0, 0.0, 0.0), (0.5, 0.0, 0.5), (0.0, 0.0, 1.0)]

    >>> print(jams.color.rgb_range(r,b,3,pow=2))
    [(1.0, 0.0, 0.0), (0.75, 0.0, 0.25), (0.0, 0.0, 1.0)]

    >>> print(jams.color.rgb_gradient([r,b],[0.0,1.0],3))
    [(1.0, 0.0, 0.0), (0.5, 0.0, 0.5), (0.0, 0.0, 1.0)]

    >>> print(jams.color.rgb_gradient([r,r,b,b],[0.0,0.25,0.75,1.0],5, cmap='MyGradient'))
    [(1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.5, 0.0, 0.5), (0.0, 0.0, 1.0), (0.0, 0.0, 1.0)]


    >>> print(jams.color.chroma_brewer['OrRd'])
    ['#fff7ec', '#fee8c8', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548', '#d7301f', '#b30000', '#7f0000']

    >>> print(jams.color.chroma_x11['indigo'])
    #4b0082

    >>> print(jams.color.rgb2hex(1, 101, 201))
    #0165c9


    >>> print(jams.color.limit(-1))
    0

    >>> print(jams.color.limit(2))
    1

    >>> print(jams.color.limit(267, mini=0, maxi=255))
    255

    >>> print(jams.color.luminance(*(0,0,0)))
    0.0

    >>> print(jams.color.luminance(*(255,255,255)))
    1.0

    >>> print(jams.color.luminance(*(255,0,0)))
    0.2126


    >>> print(jams.color.hex2rgb(jams.color.rgb2hex(1, 101, 201)))
    (1, 101, 201)

    >>> print(jams.color.hsi2rgb(*jams.color.rgb2hsi(1, 101, 201)))
    (1, 101, 201)

    >>> print(jams.color.hsl2rgb(*jams.color.rgb2hsl(1, 101, 201)))
    (1, 101, 201)

    >>> print(jams.color.hsv2rgb(*jams.color.rgb2hsv(1, 101, 201)))
    (1, 101, 201)

    >>> print(jams.color.lab2rgb(*jams.color.rgb2lab(1, 101, 201)))
    (1, 101, 201)

    >>> print(jams.color.lch2rgb(*jams.color.rgb2lch(1, 101, 201)))
    (1, 101, 201)


    import numpy as np
    from jams.color import chroma_brewer, hex2rgb01

    import matplotlib as mpl
    from matplotlib.pylab import *

    fig = figure(figsize=(8,6))
    ax1 = fig.add_axes([0.05, 0.90, 0.9, 0.10])
    ax2 = fig.add_axes([0.05, 0.75, 0.9, 0.10])
    ax3 = fig.add_axes([0.05, 0.60, 0.9, 0.10])
    ax4 = fig.add_axes([0.05, 0.45, 0.9, 0.10])
    ax5 = fig.add_axes([0.05, 0.30, 0.9, 0.10])
    ax6 = fig.add_axes([0.05, 0.15, 0.9, 0.10])
    ax7 = fig.add_axes([0.05, 0.00, 0.9, 0.10])

    # 7 sequential colours of increasing luminance
    nn     = 7
    cc     = jams.color.bezier(['black', 'red', 'yellow', 'white'], nn)
    cmap   = mpl.colors.ListedColormap(cc)
    norm   = mpl.colors.BoundaryNorm(np.arange(cmap.N+1), cmap.N)
    cb     = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='horizontal')

    # 255 sequential colours of decreasing luminance
    cc     = jams.color.bezier(['white', 'yellow', 'red', 'black'], reverse=True)
    cmap   = mpl.colors.ListedColormap(cc)
    norm   = mpl.colors.BoundaryNorm(np.arange(cmap.N+1), cmap.N)
    cb     = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal')

    # 9 diverging colours from 5 given colours, first increasing then decreasing luminance
    nn     = 9
    cc     = jams.color.bezier(['darkred', 'deeppink', 'lightyellow', 'lightgreen', 'teal'], nn)
    cmap   = mpl.colors.ListedColormap(cc)
    norm   = mpl.colors.BoundaryNorm(np.arange(cmap.N+1), cmap.N)
    cb     = mpl.colorbar.ColorbarBase(ax3, cmap=cmap, norm=norm, orientation='horizontal')

    # 9 sequential colours of decreasing luminance
    nn     = 9
    cc     = jams.color.bezier([ jams.color.hex2rgb01(i) for i in jams.color.chroma_brewer['Oranges'][::3] ], nn)
    cmap   = mpl.colors.ListedColormap(cc)
    norm   = mpl.colors.BoundaryNorm(np.arange(cmap.N+1), cmap.N)
    cb     = mpl.colorbar.ColorbarBase(ax4, cmap=cmap, norm=norm, orientation='horizontal')

    # 5 sequential colours of decreasing luminance registered as MyBrewer colour map with matplotlib
    nn     = 5
    cc     = jams.color.bezier([ jams.color.rgb2rgb01(*i) for i in [(255,255,178), (253,141,60), (189,0,38)] ], nn, cmap='MyBrewer')
    norm   = mpl.colors.BoundaryNorm(np.arange(nn+1), nn)
    cb     = mpl.colorbar.ColorbarBase(ax5, cmap=mpl.cm.get_cmap('MyBrewer'), norm=norm, orientation='horizontal')

    # 9 diverging colours from 3 given colours, first increasing then decreasing luminance
    nn     = 9
    cc     = jams.color.bezier(['darkred', 'lightyellow', 'teal'], nn)
    cmap   = mpl.colors.ListedColormap(cc)
    norm   = mpl.colors.BoundaryNorm(np.arange(cmap.N+1), cmap.N)
    cb     = mpl.colorbar.ColorbarBase(ax6, cmap=cmap, norm=norm, orientation='horizontal')

    # 9 diverging colours from 3 given colours, first increasing then decreasing luminance
    # but interpolated in L*C*h space instead of L*a*b
    nn     = 9
    cc     = jams.color.bezier(['darkred', 'lightyellow', 'teal'], nn, lch=True)
    cmap   = mpl.colors.ListedColormap(cc)
    norm   = mpl.colors.BoundaryNorm(np.arange(cmap.N+1), cmap.N)
    cb     = mpl.colorbar.ColorbarBase(ax7, cmap=cmap, norm=norm, orientation='horizontal')

    show()


    License
    -------
    This file is part of the JAMS Python package.

    Copyright (c) 2018 Matthias Cuntz - mc (at) macu (dot) de

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.


    History
    -------
    Written,  MC, Jul 2018
"""

# UFZ colours
from .mc_plot_snippets import mc_set_outtype, mc_set_matplotlib
from .mc_plot_snippets import mc_plot_begin, mc_plot_start, mc_plot_save, mc_plot_end, mc_plot_stop

# Information
__author__   = "Matthias Cuntz"
__version__  = '1.0'
__revision__ = "Revision: 2419"
__date__     = 'Date: 25.07.2018'
