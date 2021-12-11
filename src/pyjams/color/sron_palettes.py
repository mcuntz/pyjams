#!/usr/bin/env python
"""
Color palettes of Paul Tol at SRON - Netherlands Institute for Space
Research

These are the color maps of:
    https://personal.sron.nl/~pault/data/colourschemes.pdf

For details see:
    https://personal.sron.nl/~pault

The color maps are published under the licence: Standard 3-clause BSD

.. moduleauthor:: Matthias Cuntz

History
    * Written Nov 2021 from code *tol_colors.py*
      of Paul Tol, Matthias Cuntz

"""


__all__ = ['sron_colors', 'sron_colormaps', 'sron_functions']


sron_colors = {
    # All references to sron_colourschemes.pdf
    # Fig. 1
    'sron_bright': ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE',
                    '#AA3377', '#BBBBBB', '#000000'],
    # Fig. 2
    'sron_high-contrast': ['#004488', '#DDAA33', '#BB5566', '#000000'],
    # Fig. 3
    'sron_vibrant': ['#EE7733', '#0077BB', '#33BBEE', '#EE3377', '#CC3311',
                     '#009988', '#BBBBBB', '#000000'],
    # Fig. 4
    'sron_muted': ['#CC6677', '#332288', '#DDCC77', '#117733', '#88CCEE',
                   '#882255', '#44AA99', '#999933', '#AA4499', '#DDDDDD',
                   '#000000'],
    # Fig. 5
    'sron_medium-contrast': ['#6699CC', '#004488', '#EECC66', '#994455',
                             '#997700', '#EE99AA', '#000000'],
    # Fig. 7
    'sron_light': ['#77AADD', '#EE8866', '#EEDD88', '#FFAABB', '#99DDFF',
                   '#44BB99', '#BBCC33', '#AAAA00', '#DDDDDD', '#000000'],
}


sron_colormaps = {
    # All references to sron_colourschemes.pdf
    # tuple([colors], missing value)
    # Fig. 12
    'sron_sunset': (['#364B9A', '#4A7BB7', '#6EA6CD', '#98CAE1', '#C2E4EF',
                     '#EAECCC', '#FEDA8B', '#FDB366', '#F67E4B', '#DD3D2D',
                     '#A50026'], '#FFFFFF'),
    # Fig. 13
    'sron_burd': (['#2166AC', '#4393C3', '#92C5DE', '#D1E5F0', '#F7F7F7',
                   '#FDDBC7', '#F4A582', '#D6604D', '#B2182B'], '#FFEE99'),
    # Fig. 14
    'sron_prgn': (['#762A83', '#9970AB', '#C2A5CF', '#E7D4E8', '#F7F7F7',
                   '#D9F0D3', '#ACD39E', '#5AAE61', '#1B7837'], '#FFEE99'),
    # Fig. 17
    'sron_ylorbr': (['#FFFFE5', '#FFF7BC', '#FEE391', '#FEC44F', '#FB9A29',
                     '#EC7014', '#CC4C02', '#993404', '#662506'], '#888888'),
    # Fig. 17 variant
    'sron_whorbr': (['#FFFFFF', '#FFF7BC', '#FEE391', '#FEC44F', '#FB9A29',
                     '#EC7014', '#CC4C02', '#993404', '#662506'], '#888888'),
    # Fig. 18
    'sron_iridescent': (['#FEFBE9', '#FCF7D5', '#F5F3C1', '#EAF0B5', '#DDECBF',
                         '#D0E7CA', '#C2E3D2', '#B5DDD8', '#A8D8DC', '#9BD2E1',
                         '#8DCBE4', '#81C4E7', '#7BBCE7', '#7EB2E4', '#88A5DD',
                         '#9398D2', '#9B8AC4', '#9D7DB2', '#9A709E', '#906388',
                         '#805770', '#684957', '#46353A'], '#999999'),
    # Fig. 19 top
    'sron_rainbow_purd': (['#6F4C9B', '#6059A9', '#5568B8', '#4E79C5',
                           '#4D8AC6', '#4E96BC', '#549EB3', '#59A5A9',
                           '#60AB9E', '#69B190', '#77B77D', '#8CBC68',
                           '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C',
                           '#E49C39', '#E78C35', '#E67932', '#E4632D',
                           '#DF4828', '#DA2222'], '#FFFFFF'),
    # Fig. 19 bottom
    'sron_rainbow_pubr': (['#6F4C9B', '#6059A9', '#5568B8', '#4E79C5',
                           '#4D8AC6', '#4E96BC', '#549EB3', '#59A5A9',
                           '#60AB9E', '#69B190', '#77B77D', '#8CBC68',
                           '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C',
                           '#E49C39', '#E78C35', '#E67932', '#E4632D',
                           '#DF4828', '#DA2222', '#B8221E', '#95211B',
                           '#721E17', '#521A13'], '#FFFFFF'),
    # Fig. 20 variant 1
    'sron_rainbow_whrd': (['#E8ECFB', '#DDD8EF', '#D1C1E1', '#C3A8D1',
                           '#B58FC2', '#A778B4', '#9B62A7', '#8C4E99',
                           '#6F4C9B', '#6059A9', '#5568B8', '#4E79C5',
                           '#4D8AC6', '#4E96BC', '#549EB3', '#59A5A9',
                           '#60AB9E', '#69B190', '#77B77D', '#8CBC68',
                           '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C',
                           '#E49C39', '#E78C35', '#E67932', '#E4632D',
                           '#DF4828', '#DA2222'], '#666666'),
    # Fig. 20 variant 2
    'sron_rainbow_whbr': (['#E8ECFB', '#DDD8EF', '#D1C1E1', '#C3A8D1',
                           '#B58FC2', '#A778B4', '#9B62A7', '#8C4E99',
                           '#6F4C9B', '#6059A9', '#5568B8', '#4E79C5',
                           '#4D8AC6', '#4E96BC', '#549EB3', '#59A5A9',
                           '#60AB9E', '#69B190', '#77B77D', '#8CBC68',
                           '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C',
                           '#E49C39', '#E78C35', '#E67932', '#E4632D',
                           '#DF4828', '#DA2222', '#B8221E', '#95211B',
                           '#721E17', '#521A13'], '#666666'),
}


def _rainbow_discrete(n=23):
    """ Function __rainbow_discrete of tol_colors.py """
    assert n <= 23
    colors = ['#E8ECFB', '#D9CCE3', '#D1BBD7', '#CAACCB', '#BA8DB4',
              '#AE76A3', '#AA6F9E', '#994F88', '#882E72', '#1965B0',
              '#437DBF', '#5289C7', '#6195CF', '#7BAFDE', '#4EB265',
              '#90C987', '#CAE0AB', '#F7F056', '#F7CB45', '#F6C141',
              '#F4A736', '#F1932D', '#EE8026', '#E8601C', '#E65518',
              '#DC050C', '#A5170E', '#72190E', '#42150A']
    indexes = [[9],
               [9, 25],
               [9, 17, 25],
               [9, 14, 17, 25],
               [9, 13, 14, 17, 25],
               [9, 13, 14, 16, 17, 25],
               [8, 9, 13, 14, 16, 17, 25],
               [8, 9, 13, 14, 16, 17, 22, 25],
               [8, 9, 13, 14, 16, 17, 22, 25, 27],
               [8, 9, 13, 14, 16, 17, 20, 23, 25, 27],
               [8, 9, 11, 13, 14, 16, 17, 20, 23, 25, 27],
               [2, 5, 8, 9, 11, 13, 14, 16, 17, 20, 23, 25],
               [2, 5, 8, 9, 11, 13, 14, 15, 16, 17, 20, 23, 25],
               [2, 5, 8, 9, 11, 13, 14, 15, 16, 17, 19, 21, 23, 25],
               [2, 5, 8, 9, 11, 13, 14, 15, 16, 17, 19, 21, 23, 25, 27],
               [2, 4, 6, 8, 9, 11, 13, 14, 15, 16, 17, 19, 21, 23, 25, 27],
               [2, 4, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17, 19, 21, 23, 25, 27],
               [2, 4, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17, 19, 21, 23, 25, 26,
                27],
               [1, 3, 4, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17, 19, 21, 23, 25,
                26, 27],
               [1, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 21, 23,
                25, 26, 27],
               [1, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 22,
                24, 25, 26, 27],
               [1, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 22,
                24, 25, 26, 27, 28],
               [0, 1, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 22,
                24, 25, 26, 27, 28]]
    cols = [ colors[i] for i in indexes[n-1] ]
    if n == 23:
        return (cols, '#777777')
    else:
        return (cols, '#FFFFFF')


sron_functions = {
    # Fig. 22
    'sron_rainbow_discrete': _rainbow_discrete,
}


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
