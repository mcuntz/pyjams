#!/usr/bin/env python
"""
Colors from the guidelines of the Helmholtz Centre for Environmental Research -
UFZ, Leipzig, Germany from 18.01.2007

.. moduleauthor:: Matthias Cuntz

History
    * Written Mar 2022, Matthias Cuntz

"""


__all__ = ['ufz_colors']


ufz_colors = {
    'ufz:darkblue': (0./255., 62./255., 110./255.),
    'ufz:blue': (0./255., 88./255., 156./255.),
    'ufz:lightblue': (0./255., 162./255., 224./255.),
    'ufz:red': (212./255., 45./255., 18./255.),
    'ufz:orange': (207./255., 104./255., 0./255.),
    'ufz:yellow': (230./255., 175./255., 17./255.),
    'ufz:darkgreen': (20./255., 77./255., 40./255.),
    'ufz:green': (169./255., 181./255., 9./255.),
    'ufz:lightgreen': (169./255., 181./255., 9./255.),
    'ufz:gray1': (81./255., 81./255., 81./255.),
    'ufz:gray2': (156./255., 156./255., 156./255.),
    'ufz:gray3': (185./255., 185./255., 185./255.),
    'ufz:grey1': (81./255., 81./255., 81./255.),
    'ufz:grey2': (156./255., 156./255., 156./255.),
    'ufz:grey3': (185./255., 185./255., 185./255.),
    'ufz:darkgray': (81./255., 81./255., 81./255.),
    'ufz:gray': (156./255., 156./255., 156./255.),
    'ufz:lightgray': (185./255., 185./255., 185./255.),
    'ufz:darkgrey': (81./255., 81./255., 81./255.),
    'ufz:grey': (156./255., 156./255., 156./255.),
    'ufz:lightgrey': (185./255., 185./255., 185./255.),
    'ufz:black': (0./255., 0./255., 0./255.),
    'ufz:white': (255./255., 255./255., 255./255.),
}


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
