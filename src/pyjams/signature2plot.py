#!/usr/bin/env python
"""
Write a copyright notice on a plot

This module was written by Matthias Cuntz while at Department of Computational
Hydrosystems, Helmholtz Centre for Environmental Research - UFZ, Leipzig,
Germany, and continued while at Institut National de Recherche pour
l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2014-2021 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   signature2plot

History
    * Written Jan 2014 by Matthias Cuntz (mc (at) macu (dot) de)
    * Make numpy docstring format, Nov 2020, Matthias Cuntz
    * Ported into pyjams, Nov 2021, Matthias Cuntz
    * dx, dy, and name mandatory parameters, Nov 2020, Matthias Cuntz

"""
import time as ptime
from .str2tex import str2tex


__all__ = ['signature2plot']


def signature2plot(handle, dx, dy, name,
                   small=False, medium=False, large=False,
                   bold=False, italic=False,
                   usetex=False, mathrm=False,
                   **kwargs):  # pragma: no cover
    """
    Write a copyright notice on a plot

    The notice is: '(C) *name* YYYY', where YYYY is the current 4-digit year.

    Parameter
    ---------
    dx : float
        % of xlim from min(xlim)
    dy : float
        % of ylim from min(ylim)
    name : str
        Name after (C)
    small : bool, optional
        True: fontsize='small'
    medium : bool, optional
        True: fontsize='medium' (default)
    large : bool, optional
        True: fontsize='large'
    bold : bool, optional
        True: fontweight='bold'

        False: fontsize='normal' (default)
    italic : bool, optional
        True:    fontstyle='italic'

        False:   fontstyle='normal' (default)
    usetex : bool, optional
        True: Embed into LaTeX math environment

        False: No LaTeX math mode
    mathrm : bool, optional
        True: Put signature into appropriate LaTeX mathrm/mathit/mathbf
        environment if *usetex==True* and *italic==True* or *bold==True*

        False: Use standard math font if *usetex==True* (default)
    **kwargs : dict, optional
        All additional parameters are passed passed to
        :meth:`matplotlib.axes.Axes.text()`

    Returns
    -------
    '(C) name YYYY' or '(C) YYYY' on plot, where YYYY is the 4-digit year.

    Examples
    --------
    fig = plt.figure()
    ax = fig.subplot(111)
    signature2plot(ax, 0., 0.05, 'M Cuntz, INRAE',
                   small=True, italic=True,
                   usetex=usetex, mathrm=True)

    """

    # Check input
    ifont = small + medium + large
    assert ifont <= 1, ('only one of small, medium or large'
                        ' font size can be chosen.')
    if ifont == 0:
        medium = True
    if usetex and mathrm:
        assert (bold+italic) <= 1, ('if usetex and mathrm: then bold and'
                                    ' italic are mutually exclusive.')

    # default dx/dy
    xmin, xmax = handle.get_xlim()
    ymin, ymax = handle.get_ylim()
    idx = xmin + dx * (xmax - xmin)
    if 'transform' in kwargs:
        if kwargs['transform'] is handle.transAxes:
            idx = dx
    idy = ymin + dy * (ymax - ymin)
    if 'transform' in kwargs:
        if kwargs['transform'] is handle.transAxes:
            idy = dy

    # name
    year = str(ptime.localtime().tm_year)
    s1 = str2tex(r'$\copyright$ ' + name.strip() + r' ' + year,
                 usetex=usetex)

    if 'horizontalalignment' not in kwargs:
        kwargs['horizontalalignment'] = 'right'

    if usetex:
        if mathrm:
            if bold:
                s1 = s1.replace('mathrm', 'mathbf')
            elif italic:
                s1 = s1.replace('mathrm', 'mathit')

    # Size
    if small:
        fs = 'small'
    if medium:
        fs = 'medium'
    if large:
        fs = 'large'

    # Weight
    if bold:
        fw = 'bold'
    else:
        fw = 'normal'

    # Style
    if italic:
        fst = 'italic'
    else:
        fst = 'normal'

    print(s1)
    label = handle.text(idx, idy, s1,
                        fontsize=fs, fontweight=fw, fontstyle=fst,
                        **kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # # outtype = ''
    # outtype = 'pdf'
    # pdffile = 'signature2plot.pdf'
    # usetex  = True
    # textsize = 18

    # import matplotlib as mpl
    # if (outtype == 'pdf'):
    #     mpl.use('PDF')  # set directly after import matplotlib
    #     import matplotlib.pyplot as plt
    #     from matplotlib.backends.backend_pdf import PdfPages
    #     # Customize: http://matplotlib.sourceforge.net/users/customizing.html
    #     mpl.rc('ps', papersize='a4', usedistiller='xpdf')  # ps2pdf
    #     mpl.rc('figure', figsize=(8.27, 11.69))  # a4 portrait
    #     if usetex:
    #         mpl.rc('text', usetex=True)
    # else:
    #     import matplotlib.pyplot as plt
    #     mpl.rc('figure', figsize=(4./5.*8.27, 4./5.*11.69))  # a4 portrait
    #     mpl.rc('path', simplify=False)  # do not remove

    # if (outtype == 'pdf'):
    #     print('Plot PDF ', pdffile)
    #     pdf_pages = PdfPages(pdffile)
    # else:
    #     print('Plot X')
    # figsize = mpl.rcParams['figure.figsize']

    # fig = plt.figure()
    # sub = fig.add_axes([0.05, 0.05, 0.4, 0.4])
    # mulx = 1.
    # muly = 1.
    # m = plt.plot(mulx*np.arange(100)/99., muly*np.arange(100)/99., 'k:')
    # signature2plot(sub, mulx*0.5, muly*0.5, 'Test1', usetex=usetex)
    # signature2plot(sub, mulx*0.6, muly*0.6, 'MC1', small=True,
    #                usetex=usetex)  # -
    # signature2plot(sub, mulx*0.7, muly*0.7, 'Test2', large=True,
    #                usetex=usetex, italic=True)
    # signature2plot(sub, mulx*0.8, muly*0.8, 'MC2', bold=True, usetex=usetex,
    #                ha='left', mathrm=True)
    # signature2plot(sub, mulx*0.8, muly*0.8, 'MC2', bold=True)
    # signature2plot(sub, mulx*0.9, muly*0.9, 'Test3', large=True,
    #                usetex=usetex, italic=True, mathrm=True)
    # signature2plot(sub, mulx*1.0, muly*1.0, 'MC3', usetex=usetex, bold=True,
    #                horizontalalignment='left')
    # signature2plot(sub, 0.9, 0.1, 'MM', transform=sub.transAxes,
    #                usetex=usetex, bold=True, horizontalalignment='center')

    # if (outtype == 'pdf'):
    #     pdf_pages.savefig(fig)
    #     plt.close()

    # if (outtype == 'pdf'):
    #     pdf_pages.close()
    # else:
    #     plt.show()
