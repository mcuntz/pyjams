#!/usr/bin/env python
"""
Positions of subplots, used with add_axes

This module was written by Matthias Cuntz while at Department of Computational
Hydrosystems, Helmholtz Centre for Environmental Research - UFZ, Leipzig,
Germany, and continued while at Institut National de Recherche pour
l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2009-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   position

History
    * Written Aug 2009 by Matthias Cuntz (mc (at) macu (dot) de)
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Add vspace instead of wspace, Jul 2013, Matthias Cuntz
    * Use assert instead of raise Error, Apr 2014, Matthias Cuntz
    * Added height and width, Feb 2016, Stephan Thober
    * Ported to pyjams, Nov 2021, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz

"""


__all__ = ['position']


def position(row=1, col=1, num=1,
             left=0.125, right=0.9, bottom=0.1, top=0.9,
             hspace=0.1, vspace=0.1,
             width=None, height=None,
             sortcol=False,
             golden=False, inversegolden=False,
             figsize=(1., 1.)):
    """
    Gives positions of subplots, to be used with add_axes instead of subplot

    All dimensions are fractions of the figure width or height.
    Figure and subplot spaces are the same as for figure.subplot params
    except for hspace and vspace, which are halved.

    If the figsize keyword is given, a square section of the figure
    will be used.

    Parameters
    ----------
    row : int, optional
        Number of subplot rows (default: 1)
    col : int, optional
        Number of subplot columns (default: 1)
    num : int, optional
        Subplot number (default: 1)
    left : float, optional
        Left border of plot (default: 0.125)
    right : float, optional
        Right border of plot (default: 0.9)
    bottom : float, optional
        Bottom border of plot (default: 0.1)
    top : float, optional
        Top border of plot (default: 0.9)
    hspace : float, optional
        Horizontal space between columns (default: 0.1)
    vspace : float, optional
        Vertical space between rows (default: 0.1)
    width : float, optional
        Prescribe width of plots (default: calculated *col*, *left*, etc.)
    height : float, optional
        Prescribe height of plots (default: calculated *row*, *top*, etc.)
    sortcol : bool, optional
        Fill columns then rows if True (default: False)
    golden : bool, optional
        Ratio of width/height = (1+sqrt(5))/2 if True, i.e. the golden ratio
        (default: False)
    inversegolden : bool, optional
        Ratio of height/width = (1+sqrt(5))/2 if True, i.e. the golden ratio
        (default: False). The *golden* keyword takes precedence over
        *inversegolden*.
    figsize : tuple of 2 float, optional
        (width, height) of figure as given by e.g.
        matplotlib.rcParams['figure.figsize'].
        Scales everything to a square section (default: (1, 1))

    Returns
    -------
    list
        [left, bottom, width, height] to be used with Matplotlib's
        fig.add_axes.


    Examples
    --------
    Use, for example, as follows

    .. code-block:: python

       fig1 = figure(1)
       sub1 = fig1.add_axes(position(2, 2, 1))
       sub2 = fig1.add_axes(position(2, 2, 2))

    Give *figsize* and set same left and right margins if you want to have true
    squares

    .. code-block:: python

       figsize = matplotlib.rcParams['figure.figsize']
       sub = fig1.add_axes(position(1, 1, 1, figsize=figsize, left=0.1,
                                    right=0.9))

    If you want to have a true golden ratio

    .. code-block:: python

       sub = fig1.add_axes(position(1, 1, 1, golden=True))

    >>> import numpy as np
    >>> print(np.around(position(2, 2, 1), 3))
    [0.125 0.55  0.338 0.35 ]
    >>> print(np.around(position(2, 2, 1, sortcol=True), 3))
    [0.125 0.55  0.338 0.35 ]
    >>> print(np.around(position(2, 2, 1, golden=True), 3))
    [0.125 0.409 0.338 0.209]
    >>> print(np.around(position(2, 2, 1, inversegolden=True), 3))
    [0.125 0.55  0.216 0.35 ]
    >>> print(np.around(position(2, 2, 1, golden=True, sortcol=True), 3))
    [0.125 0.409 0.338 0.209]
    >>> print(np.around(position(2, 2, 1, top=1., bottom=0., left=0., right=1.,
    ...                          hspace=0., vspace=0.), 3))
    [0.  0.5 0.5 0.5]
    >>> print(np.around(position(2, 2, 2, top=1., bottom=0., left=0., right=1.,
    ...                          hspace=0., vspace=0.), 3))
    [0.5 0.5 0.5 0.5]
    >>> print(np.around(position(2, 2, 3, top=1., bottom=0., left=0., right=1.,
    ...                          hspace=0., vspace=0.), 3))
    [0.  0.  0.5 0.5]
    >>> print(np.around(position(2, 2, 4, top=1., bottom=0., left=0., right=1.,
    ...                          hspace=0., vspace=0.), 3))
    [0.5 0.  0.5 0.5]
    >>> print(np.around(position(2, 2, 1, top=1., bottom=0., left=0., right=1.,
    ...                          hspace=0., vspace=0., golden=True), 3))
    [0.    0.309 0.5   0.309]
    >>> print(np.around(position(2, 2, 2, top=1., bottom=0., left=0., right=1.,
    ...                          hspace=0., vspace=0., golden=True), 3))
    [0.5   0.309 0.5   0.309]
    >>> print(np.around(position(2, 2, 3, top=1., bottom=0., left=0., right=1.,
    ...                          hspace=0., vspace=0., golden=True), 3))
    [0.    0.    0.5   0.309]
    >>> print(np.around(position(2, 2, 4, top=1., bottom=0., left=0., right=1.,
    ...                          hspace=0., vspace=0., golden=True), 3))
    [0.5   0.    0.5   0.309]

    >>> figsize=[8, 11]
    >>> print(np.around(position(2, 2, 1, golden=True, sortcol=True,
    ...                          figsize=figsize), 3))
    [0.125 0.324 0.338 0.152]
    >>> print(np.around(position(2, 2, 1, figsize=figsize, left=0.1), 3))
    [0.1   0.427 0.35  0.255]
    >>> print(np.around(position(2, 2, 1, figsize=figsize, left=0.1,
    ...                          golden=True), 3))
    [0.1   0.33  0.35  0.157]

    """
    # Check
    nplots = row * col
    assert num <= nplots, ('num > number of plots: ' + str(num) + ' > '
                           + str(nplots))
    assert right-left > 0., 'right > left: ' + str(right) + ' > ' + str(left)
    assert top-bottom > 0., 'top < bottom: ' + str(top) + ' < ' + str(bottom)

    # Scaling to figsize
    scalex = figsize[1] / float(max(figsize))
    scaley = figsize[0] / float(max(figsize))

    # width, height
    if width is None:
        dx = (right - left - (col-1)*hspace) / col
    else:
        dx = width
    if height is None:
        dy = (top - bottom - (row-1)*vspace) / row
    else:
        dy = height

    # golden ratio
    ratio = (1. + 5**0.5) / 2.
    if golden:
        width  = dx
        height = dx / ratio
        checkheight = (top - bottom - row*height) - (row-1)*vspace
        if checkheight < 0.:
            height = dy
            width  = dy * ratio
            checkwidth = (right - left - col*width) - (col-1)*hspace
            if checkwidth < 0.:
                raise ValueError('golden ratio does not work. Have to recode.')
    elif inversegolden:
        height = dy
        width  = dy / ratio
        checkwidth = (right - left - col*width) - (col-1)*hspace
        if checkwidth < 0.:
            width  = dx
            height = dx * ratio
            checkheight = (top - bottom - row*height) - (row-1)*vspace
            if checkheight < 0.:
                raise ValueError('inverse golden ratio does not work.'
                                 ' Have to recode.')
    else:
        width  = dx
        height = dy

    # order row/colmn, column/row
    if sortcol:
        irow = (num-1) % row
        icol = (num-1) // row
    else:
        irow = (num-1) // col
        icol = (num-1) % col

    # position
    pos    = ['']*4
    pos[0] = left   + icol * (width+hspace)          * scalex
    pos[1] = bottom + (row-1-irow) * (height+vspace) * scaley
    pos[2] = width  * scalex
    pos[3] = height * scaley

    return pos


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
