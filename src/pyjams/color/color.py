#!/usr/bin/env python
"""
Get, show, print color palettes

This module was written by Matthias Cuntz while at Institut National de
Recherche pour l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy,
France.

:copyright: Copyright 2021- Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   get_cmap
   print_palettes
   show_palettes

History
    * Written Nov 2021, Matthias Cuntz

"""


__all__ = ['get_cmap', 'print_palettes', 'show_palettes']


def _rgb2rgb(col):
    """
    Transform RGB tuple with values 0-255 to tuple with values 0-1

    Parameters
    ----------
    col : iterable
        RGB tuple with values from 0-255

    Returns
    -------
    RGB tuple with values from 0-1

    Examples
    --------
    col = (0, 126, 255)
    col = _rgb2rgb(col)

    """
    return tuple([ i / 255. for i in col ])


def get_cmap(palette, ncol=0, offset=0, upper=1, as_cmap=False,
             reverse=False, grey=False):
    """
    Get colors of defined palettes or continuous color maps

    Parameters
    ----------
    palette : str
        Name of color palette or continuous color map
    ncol : int, optional
        Number of desired colors

        If 0, all colors defined by the specific palette will be returned.
        256 colors will be chosen for continuous color maps.

        If > 0, existing color palettes will be subsampled to *ncol* colors.
        *ncol* colors will be produced from continuous color maps.
    offset : float (0-1), optional
        Bottom fraction to exclude for subsample or continuous color maps
    upper : float (0-1), optional
        Upper most fraction to include for subsample or continuous color maps
    reverse : bool, optional
        If True, reverse color map. This can also be achieved by adding '_r' to
        the palette name. Palettes that end with '_r' will not be reversed.
    grey : bool, optional
        If True, return grey equivalent colors.

    Returns
    -------
    list of RGB tuples or :class:`matplotlib.colors.Colormap`

    Examples
    --------
    cols = get_cmap('mathematica_dark_rainbow_256', 15)

    """
    import matplotlib as mpl
    import pyjams.color

    # _r at end of palette is same as reverse=True
    if palette.endswith('_r'):
        palette = palette[:-2]
        reverse = True

    brewer_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('brewer_')
                           and not i.endswith('_palettes') ]
    mathematica_collections = [ i for i in dir(pyjams.color)
                                if i.startswith('mathematica_')
                                and not i.endswith('_palettes') ]
    ncl_collections = [ i for i in dir(pyjams.color)
                        if i.startswith('ncl_')
                        and not i.endswith('_palettes') ]
    oregon_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('oregon_')
                           and not i.endswith('_palettes') ]
    sron2012_collections = [ i for i in dir(pyjams.color)
                             if i.startswith('sron2012_')
                             and not i.endswith('_palettes') ]

    found_palette = False
    nosubsample = False
    for bb in brewer_collections:
        dd = eval('pyjams.color.' + bb)
        if palette in dd:
            found_palette = True
            colors = [ _rgb2rgb(i) for i in dd[palette] ]

    if not found_palette:
        for bb in mathematica_collections:
            dd = eval('pyjams.color.' + bb)
            if palette in dd:
                found_palette = True
                colors = dd[palette]

    if not found_palette:
        for bb in ncl_collections:
            dd = eval('pyjams.color.' + bb)
            if palette in dd:
                found_palette = True
                colors = dd[palette]

    if not found_palette:
        for bb in oregon_collections:
            dd = eval('pyjams.color.' + bb)
            if palette in dd:
                found_palette = True
                colors = [ _rgb2rgb(i) for i in dd[palette] ]

    if not found_palette:
        for bb in sron2012_collections:
            dd = eval('pyjams.color.' + bb)
            if palette in dd:
                found_palette = True
                if bb == 'sron2012_colors':
                    colors = [ mpl.colors.colorConverter.to_rgb(i)
                               for i in dd[palette] ]
                elif bb == 'sron2012_functions':
                    nosubsample = True
                    colors = []
                    if ncol == 0:
                        ncol1 = 256
                    else:
                        ncol1 = ncol
                    for i in range(ncol1):
                        x = offset + float(i)/float(ncol1-1) * (upper-offset)
                        colors.append(tuple(dd[palette](x)))
                else:
                    raise ValueError('Unknown sron2012 palette. Coding Error.')

    if not found_palette:
        amplmaps = mpl.pyplot.colormaps()
        mplmaps = [ i for i in amplmaps if not i.endswith('_r') ]
        if palette in mplmaps:
            found_palette = True
            cmap = mpl.cm.get_cmap(palette)
            try:
                # mpl.colors.ListedColormap
                colors = cmap.colors
            except AttributeError:
                # mpl.colors.LinearSegmentedColormap
                colors = [ cmap(i) for i in range(cmap.N) ]
        else:
            lmplmaps = [ i.lower() for i in mplmaps ]
            if palette.lower() in lmplmaps:
                found_palette = True
                ipalette = lmplmaps.index(palette.lower())
                cmap = mpl.cm.get_cmap(mplmaps[ipalette])
                try:
                    # mpl.colors.ListedColormap
                    colors = cmap.colors
                except AttributeError:
                    # mpl.colors.LinearSegmentedColormap
                    colors = [ cmap(i) for i in range(cmap.N) ]

    if not found_palette:
        raise ValueError(palette+' color palette not found.')

    if reverse:
        colors = colors[::-1]

    if grey:
        for ii, cc in enumerate(colors):
            isgrey = 0.2125 * cc[0] + 0.7154 * cc[1] + 0.072 * cc[2]
            colors[ii] = (isgrey, isgrey, isgrey)

    # subsample
    if (ncol > 0) and not nosubsample:
        ncolors = len(colors)
        ocolors = ['']*ncol
        for i in range(ncol):
            x = offset + float(i)/float(ncol-1) * (upper-offset)  # [0-1]
            iicol = round(x * (ncolors-1))  # [0-ncolor-1]
            ocolors[i] = colors[iicol]
        colors = ocolors

    if as_cmap:
        colors = mpl.colors.ListedColormap(colors)

    return colors


def print_palettes(collection=''):
    """
    Print the known color palettes and continuous color maps

    Parameters
    ----------
    collection : str or list of strings, optional
        Name(s) of color palette collection(s).
        Known collections are 'brewer', 'mathematica', 'ncl',
        'oregon', 'sron2012', and 'matplotlib'.

    Returns
    -------
    Prints list of known color palettes and continuous color maps.

    Examples
    --------
    print_palettes()

    """
    import matplotlib as mpl
    import pyjams.color

    brewer_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('brewer_')
                           and not i.endswith('_palettes') ]
    mathematica_collections = [ i for i in dir(pyjams.color)
                                if i.startswith('mathematica_')
                                and not i.endswith('_palettes') ]
    ncl_collections = [ i for i in dir(pyjams.color)
                        if i.startswith('ncl_')
                        and not i.endswith('_palettes') ]
    oregon_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('oregon_')
                           and not i.endswith('_palettes') ]
    sron2012_collections = [ i for i in dir(pyjams.color)
                             if i.startswith('sron2012_')
                             and not i.endswith('_palettes') ]

    if collection:
        if isinstance(collection, str):
            collections = [collection.lower()]
        else:
            collections = [ i.lower for i in collection ]
    else:
        collections = ['brewer', 'mathematica', 'ncl', 'oregon',
                       'sron2012', 'matplotlib']

    if 'brewer' in collections:
        print('brewer')
        for cc in brewer_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'mathematica' in collections:
        print('mathematica')
        for cc in mathematica_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'ncl' in collections:
        print('ncl')
        for cc in ncl_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'oregon' in collections:
        print('oregon')
        for cc in oregon_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'sron2012' in collections:
        print('sron2012')
        for cc in sron2012_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'matplotlib' in collections:
        print('matplotlib')
        acmaps = mpl.pyplot.colormaps()
        cmaps  = [ i for i in acmaps if not i.endswith('_r') ]
        cmaps.sort()
        print('   ', cmaps)


def _newfig(ifig, ititle):
    """ Helper function for show_palettes """
    import matplotlib.pyplot as plt
    fig = plt.figure(ifig)
    fig.suptitle(ititle)
    plt.subplots_adjust(left=0.3, bottom=0.1,
                        right=0.95, top=0.95,
                        wspace=0.05, hspace=0.2)
    return fig


def _newsubplot(nrow, ncol, iplot, iname):
    """ Helper function for show_palettes """
    import numpy as np
    import matplotlib.pyplot as plt
    ax = plt.subplot(nrow, ncol, iplot)
    ax.axis('off')
    cmap = get_cmap(iname, as_cmap=True)
    # ax.pcolormesh(np.outer(np.ones(cmap.N), np.arange(cmap.N)),
    #               cmap=cmap)
    ax.imshow(np.outer(np.ones(cmap.N), np.arange(cmap.N)),
              aspect='auto', cmap=cmap, origin="lower")
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    dx = -0.01
    dy = 0.5
    ax.text(xmin+dx*(xmax-xmin), ymin+dy*(ymax-ymin), iname,
            ha='right', va='center')
    # return ax


def _savefig(fig, ifig, outtype, outfile, pdf_pages):
    """ Helper function for show_palettes """
    import matplotlib.pyplot as plt
    if (outtype == 'pdf'):
        pdf_pages.savefig(fig)
        plt.close(fig)
    elif not (outtype == 'X'):
        ofile = (outfile[:outfile.rfind('.')] + '_' + '{:04d}'.format(ifig)
                 + '.' + outtype)
        fig.savefig(ofile)
        plt.close(fig)
    else:
        pass


def show_palettes(outfile='', collection=''):
    """
    Show the known color palettes and continuous color maps

    Parameters
    ----------
    outfile : str, optional
        Output file name. Output type will be determined from file suffix.
    collection : str or list of strings, optional
        Name(s) of color palette collection(s).
        Known collections are 'brewer', 'mathematica', 'ncl',
        'oregon', 'sron2012', and 'matplotlib'.

        All palettes will be shown if collection is empty or 'all'.

    Returns
    -------
    Plots known color palettes and continuous color maps.

    Examples
    --------
    show_palettes(outfile='pyjams_cmaps.pdf', collection=['mathematica', 'matplotlib'])

    """
    import pyjams.color
    import matplotlib as mpl
    # outtype
    if '.' in outfile:
        outtype = outfile[outfile.rfind('.')+1:]
        if outtype == 'pdf':
            mpl.use('PDF')  # set directly after import matplotlib
            from matplotlib.backends.backend_pdf import PdfPages
            textsize = 10
        else:
            mpl.use('Agg')  # set directly after import matplotlib
            textsize = 10
    else:
        outtype = 'X'
        textsize = 8
    import matplotlib.pyplot as plt

    # which collections to include
    collections = ['brewer', 'mathematica', 'ncl', 'oregon',
                   'sron2012', 'matplotlib']
    if collection:
        if isinstance(collection, str):
            if collection.lower() != 'all':
                collections = [collection.lower()]
        else:
            collections = [ i.lower() for i in collection ]

    # plot setup
    if outfile:
        mpl.rc('figure', figsize=(8.27, 11.69))  # a4 portrait
        if not (outtype == 'pdf'):
            mpl.rc('savefig', dpi=300, format=outtype)
    else:
        mpl.rc('figure', figsize=(8.27*0.75, 11.69*0.75))
    figsize = mpl.rcParams['figure.figsize']
    mpl.rc('font', size=textsize)
    nrow = 35

    # get collections
    brewer_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('brewer_')
                           and not i.endswith('_palettes') ]
    mathematica_collections = [ i for i in dir(pyjams.color)
                                if i.startswith('mathematica_')
                                and not i.endswith('_palettes') ]
    ncl_collections = [ i for i in dir(pyjams.color)
                        if i.startswith('ncl_')
                        and not i.endswith('_palettes') ]
    oregon_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('oregon_')
                           and not i.endswith('_palettes') ]
    sron2012_collections = [ i for i in dir(pyjams.color)
                             if i.startswith('sron2012_')
                             and not i.endswith('_palettes') ]

    all_collections = []
    if 'brewer' in collections:
        for cc in brewer_collections:
            all_collections.append(cc)
    if 'mathematica' in collections:
        for cc in mathematica_collections:
            all_collections.append(cc)
    if 'ncl' in collections:
        for cc in ncl_collections:
            all_collections.append(cc)
    if 'oregon' in collections:
        for cc in oregon_collections:
            all_collections.append(cc)
    if 'sron2012' in collections:
        for cc in sron2012_collections:
            all_collections.append(cc)
    if 'matplotlib' in collections:
        acmaps = mpl.pyplot.colormaps()
        cmaps  = [ i for i in acmaps if not i.endswith('_r') ]
        cmaps.sort()
        all_collections.extend(cmaps)

    # plotting
    ifig = 0
    if (outtype == 'pdf'):
        pdf_pages = PdfPages(outfile)
    else:
        pdf_pages = None

    ipanel = 0
    for cc in all_collections:
        try:
            icoll = eval('pyjams.color.' + cc)
            newcoll = True
            collname = cc
        except AttributeError:
            # matplotlib name
            icoll = [cc]
            newcoll = False
            collname = 'matplotlib'
        for iname in icoll:
            # colors = icoll[iname]
            if ipanel == 0:
                ifig += 1
                fig = _newfig(ifig, collname)
            ipanel += 1
            # ax = _newsubplot(nrow, 1, ipanel, iname)
            _newsubplot(nrow, 1, ipanel, iname)
            if ipanel == nrow:
                _savefig(fig, ifig, outtype, outfile, pdf_pages)
                ipanel = 0
        if (ipanel != 0) and newcoll:
            _savefig(fig, ifig, outtype, outfile, pdf_pages)
            ipanel = 0
    if ipanel != 0:
        _savefig(fig, ifig, outtype, outfile, pdf_pages)

    if outtype == 'pdf':
        pdf_pages.close()
    elif outtype == 'X':
        plt.show()
    else:
        pass


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
