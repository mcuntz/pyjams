#!/usr/bin/env python
"""
Get, show, print color palettes

This module was written by Matthias Cuntz while at Institut National de
Recherche pour l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy,
France.

:copyright: Copyright 2021-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   get_color
   print_colors
   get_cmap
   print_palettes
   show_palettes

History
    * Written Nov 2021, Matthias Cuntz
    * Change order of color maps, Dec 2021, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz
    * Added 'order' keyword, Feb 2022, Matthias Cuntz
    * 'get_color', Mar 2022, Matthias Cuntz
    * 'cname' can be list of names in 'get_color', Apr 2022, Matthias Cuntz
    * Register ufz colors only once, Apr 2022, Matthias Cuntz
    * Added print_colors, Apr 2022, Matthias Cuntz
    * Use matplotlib.colormaps.get_cmap instead of deprecated
      matplotlib.cm.get_cmap, Dec 2022, Matthias Cuntz
    * Use matplotlib.colormaps[name] instead of
      matplotlib.colormaps.get_cmap(name) to work with matplotlib < v3.6,
      Jan 2023, Matthias Cuntz
    * Do not set_bad() for sron palettes, Jan 2023, Matthias Cuntz
    * Allow ncol=1 in get_cmap, Jun 2023, Matthias Cuntz

"""

__all__ = ['get_color', 'print_colors',
           'get_cmap', 'print_palettes', 'show_palettes']


def _rgb2rgb(col):
    """
    Transform RGB tuple with values 0-255 to tuple with values 0-1

    Parameters
    ----------
    col : iterable
        RGB tuple with values from 0-255

    Returns
    -------
    tuple
        RGB tuple with values from 0-1

    Examples
    --------
    col = (0, 126, 255)
    col = _rgb2rgb(col)

    """
    return tuple([ i / 255. for i in col ])


def _to_grey(col):
    """
    Transform RGB tuple to grey values

    Parameters
    ----------
    col : iterable
        RGB tuple

    Returns
    -------
    tuple
        RGB tuple with corresponding grey values

    Examples
    --------
    col = (0, 0.5, 1)
    col = _to_grey(col)

    """
    isgrey = 0.2125 * col[0] + 0.7154 * col[1] + 0.072 * col[2]
    return (isgrey, isgrey, isgrey)


def get_color(cname=''):
    """
    Register new named colors with Matplotlib and return named color(s)

    Registers the named colors given in ufz_palettes.
    Optionally returns the value(s) of the named color(s),
    which can be any color name known to Matplotlib.

    Parameters
    ----------
    cname : str or iterable of str, optional
        Colour name(s)

    Examples
    --------
    .. code-block:: python

       col1 = get_color('ufz:blue')
       col2 = get_color('xkcd:blue')
       cols = get_color(['blue', 'red'])

    """
    from collections.abc import Iterable
    import matplotlib.pyplot as plt
    import pyjams.color

    mapping = plt.cm.colors.get_named_colors_mapping
    # register ufz colors if not yet done
    if 'ufz:blue' not in mapping().keys():
        ufz_colors = [ i for i in dir(pyjams.color)
                       if i.startswith('ufz_')
                       and not i.endswith('_palettes') ]
        # ufz has only 1 list with colors
        ufz_colors = eval('pyjams.color.' + ufz_colors[0])
        mapping().update(ufz_colors)

    if cname:
        if isinstance(cname, Iterable) and (not isinstance(cname, str)):
            out = [ mapping()[i] for i in cname ]
            return out
        else:
            return mapping()[cname]


def print_colors(collection=''):
    """
    Print the known named colors

    Parameters
    ----------
    collection : str or list of strings, optional
        Name(s) of color collection(s).
        Known collections are 'base', 'tableau', 'ufz', 'css',
        and 'xkcd'.

    Returns
    -------
    None
        Prints list of known named colors to console.

    Examples
    --------
    .. code-block:: python

       print_colors()

    """
    import matplotlib.pyplot as plt
    import pyjams.color

    if collection:
        if isinstance(collection, str):
            collections = [collection.lower()]
        else:
            collections = [ i.lower for i in collection ]
    else:
        collections = ['base', 'tableau', 'ufz', 'css', 'xkcd']

    # register ufz colors if needed
    get_color()
    mapping = plt.cm.colors.get_named_colors_mapping
    colors = mapping().keys()

    if 'base' in collections:
        print('base')
        ll = [ cc for cc in colors if len(cc) == 1 ]
        print('       ', list(ll))

    if 'tableau' in collections:
        print('tableau')
        ll = [ cc for cc in colors if cc.startswith('tab:') ]
        print('       ', list(ll))

    if 'ufz' in collections:
        print('ufz')
        ll = [ cc for cc in colors if cc.startswith('ufz:') ]
        print('       ', list(ll))

    if 'css' in collections:
        print('css')
        ll = [ cc for cc in colors if (':' not in cc) and (len(cc) > 1) ]
        print('       ', list(ll))

    if 'xkcd' in collections:
        print('xkcd')
        ll = [ cc for cc in colors if cc.startswith('xkcd:') ]
        print('       ', list(ll))


def get_cmap(palette, ncol=0, offset=0, upper=1,
             reverse=False, grey=False, order=None, as_cmap=False):
    """
    Get colors of defined palettes or continuous colormaps

    Parameters
    ----------
    palette : str
        Name of color palette or continuous colormap
    ncol : int, optional
        Number of desired colors.
        If 0, all colors defined by the specific palette will be returned.
        256 colors will be chosen for continuous colormaps.
        If > 0, existing color palettes will be subsampled to *ncol* colors.
        *ncol* colors will be produced from continuous colormaps.
    offset : float (0-1), optional
        Bottom fraction to exclude for subsample or continuous colormaps
    upper : float (0-1), optional
        Upper most fraction to include for subsample or continuous colormaps
    reverse : bool, optional
        Reverse colormap if True (default: False). This can also be achieved by
        adding '_r' to the palette name. Palettes that end with '_r' will not
        be reversed.
    grey : bool, optional
        Return grey equivalent colors if True (default: False).
    order : str, optional
        Order colors by 'hue', 'saturation', or 'value'.
        This is done before *reverse* and *grey*
        (default: order from color sources).
    as_cmap : bool, optional
        If True, returns matplotlib.colors.Colormap
        instead of list of RGB tuples

    Returns
    -------
    list or matplotlib.colors.Colormap
        List of RGB tuples or :class:`matplotlib.colors.Colormap`

    Notes
    -----
    `get_cmap` always returns a list of RGB tuples or a Matplotlib
    ListedColormap. You can use the *ncol*, *offset*, and *upper* keywords to
    subsample colormaps. To get smoothly-varying colormaps, you can use the
    method :meth:`matplotlib.colors.LinearSegmentedColormap.from_list`

       cols = get_cmap('sron_ylorbr')

       cmap = matplotlib.colors.LinearSegmentedColormap.from_list(cols)

    You can get the color tuples from a LinearSegmentedColormap like this

       colors = [ cmap(i) for i in range(cmap.N) ]

    Examples
    --------
    .. code-block:: python

       cols = get_cmap('mathematica_dark_rainbow_256', 15)

    """
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import pyjams.color
    from pyjams import argsort

    # _r at end of palette is same as reverse=True
    if palette.endswith('_r'):
        palette = palette[:-2]
        reverse = True

    pyjams_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('pyjams_')
                           and not i.endswith('_palettes') ]
    sron_collections = [ i for i in dir(pyjams.color)
                         if i.startswith('sron_')
                         and not i.endswith('_palettes') ]
    sron2012_collections = [ i for i in dir(pyjams.color)
                             if i.startswith('sron2012_')
                             and not i.endswith('_palettes') ]
    mathematica_collections = [ i for i in dir(pyjams.color)
                                if i.startswith('mathematica_')
                                and not i.endswith('_palettes') ]
    oregon_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('oregon_')
                           and not i.endswith('_palettes') ]
    ncl_collections = [ i for i in dir(pyjams.color)
                        if i.startswith('ncl_')
                        and not i.endswith('_palettes') ]
    brewer_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('brewer_')
                           and not i.endswith('_palettes') ]

    found_palette = False
    nosubsample = False
    # miss = None

    if not found_palette:
        for bb in pyjams_collections:
            dd = eval('pyjams.color.' + bb)
            if palette in dd:
                found_palette = True
                colors = dd[palette]

    if not found_palette:
        for bb in sron_collections:
            dd = eval('pyjams.color.' + bb)
            if palette in dd:
                found_palette = True
                if bb == 'sron_colors':
                    colors = [ mpl.colors.colorConverter.to_rgb(i)
                               for i in dd[palette] ]
                elif bb == 'sron_colormaps':
                    colors = [ mpl.colors.colorConverter.to_rgb(i)
                               for i in dd[palette][0] ]
                    # miss = mpl.colors.colorConverter.to_rgb(dd[palette][1])
                elif bb == 'sron_functions':
                    nosubsample = True
                    if ncol == 0:
                        ncol1 = 23
                    else:
                        ncol1 = ncol
                    cols = dd[palette](ncol1)
                    colors = [ mpl.colors.colorConverter.to_rgb(i)
                               for i in cols[0] ]
                    # miss = mpl.colors.colorConverter.to_rgb(cols[1])

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
                        if ncol1 == 1:
                            x = offset
                        else:
                            x = (offset + float(i) / float(ncol1 - 1) *
                                 (upper - offset))
                        colors.append(tuple(dd[palette](x)))

    if not found_palette:
        for bb in mathematica_collections:
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
        for bb in ncl_collections:
            dd = eval('pyjams.color.' + bb)
            if palette in dd:
                found_palette = True
                colors = dd[palette]

    if not found_palette:
        # try:
        #     amplmaps = plt.colormaps()
        #     mplmaps = [ i for i in amplmaps if not i.endswith('_r') ]
        # except AttributeError:
        #     mplmaps = sorted(mpl.cm.datad.keys())
        amplmaps = plt.colormaps()
        mplmaps = [ i for i in amplmaps if not i.endswith('_r') ]
        if palette in mplmaps:
            found_palette = True
            # cmap = mpl.cm.get_cmap(palette)
            # cmap = mpl.colormaps.get_cmap(palette)
            cmap = mpl.colormaps[palette]
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
                # cmap = mpl.cm.get_cmap(mplmaps[ipalette])
                # cmap = mpl.colormaps.get_cmap(mplmaps[ipalette])
                cmap = mpl.colormaps[mplmaps[ipalette]]
                try:
                    # mpl.colors.ListedColormap
                    colors = cmap.colors
                except AttributeError:
                    # mpl.colors.LinearSegmentedColormap
                    colors = [ cmap(i) for i in range(cmap.N) ]

    if not found_palette:
        for bb in brewer_collections:
            dd = eval('pyjams.color.' + bb)
            if palette in dd:
                found_palette = True
                colors = [ _rgb2rgb(i) for i in dd[palette] ]

    if not found_palette:
        raise ValueError(palette + ' color palette not found.')

    if order is not None:
        hsv = ['hue', 'saturation', 'value']
        if order.lower() in hsv:
            oo = hsv.index(order.lower())
        else:
            raise ValueError('Sort order not known: ' + order)
        ii = argsort([ mpl.colors.rgb_to_hsv(cc)[oo]
                       for cc in colors ])
        colors = [ colors[i] for i in ii ]

    if reverse:
        colors = colors[::-1]

    if grey:
        colors = [ _to_grey(i) for i in colors ]

    # subsample
    if (ncol > 0) and not nosubsample:
        ncolors = len(colors)
        ocolors = [''] * ncol
        for i in range(ncol):
            if ncol == 1:
                x = offset
            else:
                # [0-1]
                x = offset + float(i) / float(ncol - 1) * (upper - offset)
            iicol = round(x * (ncolors - 1))  # [0-ncolor-1]
            ocolors[i] = colors[iicol]
        colors = ocolors

    if as_cmap:
        colors = mpl.colors.ListedColormap(colors)
        # if mpl.__version__ > '3.4.0':
        #     if miss is not None:
        #         colors.set_bad(miss)

    return colors


def print_palettes(collection=''):
    """
    Print the known color palettes and continuous colormaps

    Parameters
    ----------
    collection : str or list of strings, optional
        Name(s) of color palette collection(s).
        Known collections are 'pyjams', 'sron', 'sron2012', 'mathematica',
        'oregon', 'ncl', 'matplotlib', and 'brewer'.

    Returns
    -------
    None
        Prints list of known color palettes and continuous colormaps to
        console.

    Examples
    --------
    .. code-block:: python

       print_palettes()

    """
    # import matplotlib as mpl
    import matplotlib.pyplot as plt
    import pyjams.color

    pyjams_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('pyjams_')
                           and not i.endswith('_palettes') ]
    sron_collections = [ i for i in dir(pyjams.color)
                         if i.startswith('sron_')
                         and not i.endswith('_palettes') ]
    sron2012_collections = [ i for i in dir(pyjams.color)
                             if i.startswith('sron2012_')
                             and not i.endswith('_palettes') ]
    mathematica_collections = [ i for i in dir(pyjams.color)
                                if i.startswith('mathematica_')
                                and not i.endswith('_palettes') ]
    oregon_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('oregon_')
                           and not i.endswith('_palettes') ]
    ncl_collections = [ i for i in dir(pyjams.color)
                        if i.startswith('ncl_')
                        and not i.endswith('_palettes') ]
    brewer_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('brewer_')
                           and not i.endswith('_palettes') ]

    if collection:
        if isinstance(collection, str):
            collections = [collection.lower()]
        else:
            collections = [ i.lower for i in collection ]
    else:
        collections = ['pyjams', 'sron', 'sron2012', 'mathematica',
                       'oregon', 'ncl', 'matplotlib', 'brewer']

    if 'pyjams' in collections:
        print('pyjams')
        for cc in pyjams_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'sron' in collections:
        print('sron')
        for cc in sron_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'sron2012' in collections:
        print('sron2012')
        for cc in sron2012_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'mathematica' in collections:
        print('mathematica')
        for cc in mathematica_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'oregon' in collections:
        print('oregon')
        for cc in oregon_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'ncl' in collections:
        print('ncl')
        for cc in ncl_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))

    if 'matplotlib' in collections:
        print('matplotlib')
        # try:
        #     acmaps = plt.colormaps()
        #     cmaps  = [ i for i in acmaps if not i.endswith('_r') ]
        #     cmaps.sort()
        # except AttributeError:
        #     cmaps = sorted(mpl.colorbar.cm.datad.keys())
        acmaps = plt.colormaps()
        cmaps  = [ i for i in acmaps if not i.endswith('_r') ]
        cmaps.sort()
        print('   ', cmaps)

    if 'brewer' in collections:
        print('brewer')
        for cc in brewer_collections:
            print('   ', cc)
            ll = eval('pyjams.color.' + cc + '.keys()')
            print('       ', list(ll))


def _newfig(ifig, ititle):  # pragma: no cover
    """ Helper function for show_palettes """
    import matplotlib.pyplot as plt
    fig = plt.figure(ifig)
    fig.suptitle(ititle)
    plt.subplots_adjust(left=0.3, bottom=0.1,
                        right=0.95, top=0.95,
                        wspace=0.05, hspace=0.5)
    return fig


def _newsubplot(nrow, ncol, iplot, iname, ncolors=0):  # pragma: no cover
    """ Helper function for show_palettes """
    import numpy as np
    import matplotlib.pyplot as plt
    ax = plt.subplot(nrow, ncol, iplot)
    ax.axis('off')
    cmap = get_cmap(iname, ncolors, as_cmap=True)
    # ax.pcolormesh(np.outer(np.ones(cmap.N), np.arange(cmap.N)),
    #               cmap=cmap)
    ax.imshow(np.outer(np.ones(cmap.N), np.arange(cmap.N)),
              aspect='auto', cmap=cmap, origin="lower")
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    dx = -0.01
    dy = 0.5
    if ncolors:
        iiname = iname + '(' + str(ncolors) + ')'
    else:
        iiname = iname
    ax.text(xmin + dx * (xmax - xmin), ymin + dy * (ymax - ymin), iiname,
            ha='right', va='center')
    # return ax


def _savefig(fig, ifig, outtype, outfile, pdf_pages):  # pragma: no cover
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


def show_palettes(outfile='', collection=''):  # pragma: no cover
    """
    Show the known color palettes and continuous colormaps

    Parameters
    ----------
    outfile : str, optional
        Output file name. Output type will be determined from file suffix.
    collection : str or list of strings, optional
        Name(s) of color palette collection(s).
        All palettes will be shown if collection is empty or 'all'.
        Known collections are: 'pyjams', 'sron', 'sron2012', 'mathematica',
        'oregon', 'ncl', 'matplotlib', and 'brewer'.

    Returns
    -------
    None
        Plots known color palettes and continuous colormaps in file or on
        plotting window.

    Examples
    --------
    .. code-block:: python

       show_palettes(outfile='pyjams_cmaps.pdf',
                     collection=['mathematica', 'matplotlib'])

    """
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import pyjams.color
    # outtype
    if '.' in outfile:
        outtype = outfile[outfile.rfind('.') + 1:]
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

    # which collections to include
    collections = ['pyjams', 'sron', 'sron2012', 'mathematica', 'oregon',
                   'ncl', 'matplotlib', 'brewer']
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
        mpl.rc('figure', figsize=(8.27 * 0.75, 11.69 * 0.75))
    # figsize = mpl.rcParams['figure.figsize']
    mpl.rc('font', size=textsize)
    nrow = 35

    # get collections
    pyjams_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('pyjams_')
                           and not i.endswith('_palettes') ]
    sron_collections = [ i for i in dir(pyjams.color)
                         if i.startswith('sron_')
                         and not i.endswith('_palettes') ]
    sron2012_collections = [ i for i in dir(pyjams.color)
                             if i.startswith('sron2012_')
                             and not i.endswith('_palettes') ]
    mathematica_collections = [ i for i in dir(pyjams.color)
                                if i.startswith('mathematica_')
                                and not i.endswith('_palettes') ]
    oregon_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('oregon_')
                           and not i.endswith('_palettes') ]
    ncl_collections = [ i for i in dir(pyjams.color)
                        if i.startswith('ncl_')
                        and not i.endswith('_palettes') ]
    brewer_collections = [ i for i in dir(pyjams.color)
                           if i.startswith('brewer_')
                           and not i.endswith('_palettes') ]

    all_collections = []
    if 'pyjams' in collections:
        for cc in pyjams_collections:
            all_collections.append(cc)
    if 'sron' in collections:
        for cc in sron_collections:
            all_collections.append(cc)
    if 'sron2012' in collections:
        for cc in sron2012_collections:
            all_collections.append(cc)
    if 'mathematica' in collections:
        for cc in mathematica_collections:
            all_collections.append(cc)
    if 'oregon' in collections:
        for cc in oregon_collections:
            all_collections.append(cc)
    if 'ncl' in collections:
        for cc in ncl_collections:
            all_collections.append(cc)
    if 'matplotlib' in collections:
        # try:
        #     acmaps = plt.colormaps()
        #     cmaps  = [ i for i in acmaps if not i.endswith('_r') ]
        #     cmaps.sort()
        # except AttributeError:
        #     cmaps = sorted(mpl.colorbar.cm.datad.keys())
        acmaps = plt.colormaps()
        cmaps  = [ i for i in acmaps if not i.endswith('_r') ]
        cmaps.sort()
        all_collections.extend(cmaps)
    if 'brewer' in collections:
        for cc in brewer_collections:
            all_collections.append(cc)

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
            if collname == 'sron_functions':
                for ncolors in range(1, 24):
                    ipanel += 1
                    _newsubplot(nrow, 1, ipanel, iname, ncolors)
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
