#!/usr/bin/env python
"""
Color palettes of 2012 of Paul Tol at SRON - Netherlands Institute for Space
Research

These are the color maps of the 2012 version of:
    https://personal.sron.nl/~pault/data/colourschemes.pdf

.. moduleauthor:: Matthias Cuntz

History
    * Written Nov 2021 from code of May 2016, Matthias Cuntz
    * Ported to pyjams, Nov 2021, Matthias Cuntz
    * flake8 compatible, Nov 2021, Matthias Cuntz

"""
from math import erf


__all__ = ['sron2012_colors', 'sron2012_functions']


sron2012_colors = {
    # All references to sron_colourschemes.pdf of 2012
    # Fig.2 - regular pattern of hue
    # Fig. 2 upper row
    'sron2012_light': ['#77AADD', '#77CCCC', '#88CCAA', '#DDDD77',
                       '#DDAA77', '#DD7788', '#CC99BB'],
    # Fig. 2 middle row
    'sron2012_medium': ['#4477AA', '#44AAAA', '#44AA77', '#AAAA44',
                        '#AA7744', '#AA4455', '#AA4488'],
    # Fig. 2 lower row
    'sron2012_dark': ['#114477', '#117777', '#117744', '#777711',
                      '#774411', '#771122', '#771155'],
    # Fig. 3 - qualitative data
    'sron2012_1': ['#4477AA'],
    'sron2012_2': ['#4477AA', '#CC6677'],
    'sron2012_3': ['#4477AA', '#DDCC77', '#CC6677'],
    'sron2012_4': ['#4477AA', '#117733', '#DDCC77', '#CC6677'],
    'sron2012_5': ['#332288', '#88CCEE', '#117733', '#DDCC77', '#CC6677'],
    'sron2012_6': ['#332288', '#88CCEE', '#117733', '#DDCC77', '#CC6677',
                   '#AA4499'],
    'sron2012_7': ['#332288', '#88CCEE', '#44AA99', '#117733', '#DDCC77',
                   '#CC6677', '#AA4499'],
    'sron2012_8': ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933',
                   '#DDCC77', '#CC6677', '#AA4499'],
    'sron2012_9': ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933',
                   '#DDCC77', '#CC6677', '#882255', '#AA4499'],
    'sron2012_10': ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933',
                    '#DDCC77', '#661100', '#CC6677', '#882255', '#AA4499'],
    'sron2012_11': ['#332288', '#6699CC', '#88CCEE', '#44AA99', '#117733',
                    '#999933', '#DDCC77', '#661100', '#CC6677', '#882255',
                    '#AA4499'],
    'sron2012_12': ['#332288', '#6699CC', '#88CCEE', '#44AA99', '#117733',
                    '#999933', '#DDCC77', '#661100', '#CC6677', '#AA4466',
                    '#882255', '#AA4499'],
    # Fig. 4 - print black&white on paper
    'sron2012_greysafe': ['#809BC8', '#FF6666', '#FFCC66', '#64C204'],
    # Fig. 7 - sequential data yellow-orange-brown
    'sron2012_ylorbr_3': ['#FFF7BC', '#FEC44F', '#D95F0E'],
    'sron2012_ylorbr_4': ['#FFFBD5', '#FED98E', '#FB9A29', '#CC4C02'],
    'sron2012_ylorbr_5': ['#FFFBD5', '#FED98E', '#FB9A29', '#D95F0E',
                          '#993404'],
    'sron2012_ylorbr_6': ['#FFFBD5', '#FEE391', '#FEC44F', '#FB9A29',
                          '#D95F0E', '#993404'],
    'sron2012_ylorbr_7': ['#FFFBD5', '#FEE391', '#FEC44F', '#FB9A29',
                          '#EC7014', '#CC4C02', '#8C2D04'],
    'sron2012_ylorbr_8': ['#FFFFE5', '#FFF7BC', '#FEE391', '#FEC44F',
                          '#FB9A29', '#EC7014', '#CC4C02', '#8C2D04'],
    'sron2012_ylorbr_9': ['#FFFFE5', '#FFF7BC', '#FEE391', '#FEC44F',
                          '#FB9A29', '#EC7014', '#CC4C02', '#993404',
                          '#662506'],
    # Fig. 8 - diverging data blue-yellow-red
    'sron2012_buylrd_3': ['#99C7EC', '#FFFAD2', '#F5A275'],
    'sron2012_buylrd_4': ['#008BCE', '#B4DDF7', '#F9BD7E', '#D03232'],
    'sron2012_buylrd_5': ['#008BCE', '#B4DDF7', '#FFFAD2', '#F9BD7E',
                          '#D03232'],
    'sron2012_buylrd_6': ['#3A89C9', '#99C7EC', '#E6F5FE', '#FFE3AA',
                          '#F5A275', '#D24D3E'],
    'sron2012_buylrd_7': ['#3A89C9', '#99C7EC', '#E6F5FE', '#FFFAD2',
                          '#FFE3AA', '#F5A275', '#D24D3E'],
    'sron2012_buylrd_8': ['#3A89C9', '#77B7E5', '#B4DDF7', '#E6F5FE',
                          '#FFE3AA', '#F9BD7E', '#ED875E', '#D24D3E'],
    'sron2012_buylrd_9': ['#3A89C9', '#77B7E5', '#B4DDF7', '#E6F5FE',
                          '#FFFAD2', '#FFE3AA', '#F9BD7E', '#ED875E',
                          '#D24D3E'],
    'sron2012_buylrd_10': ['#3D52A1', '#3A89C9', '#77B7E5', '#B4DDF7',
                           '#E6F5FE', '#FFE3AA', '#F9BD7E', '#ED875E',
                           '#D24D3E', '#AE1C3E'],
    'sron2012_buylrd_11': ['#3D52A1', '#3A89C9', '#77B7E5', '#B4DDF7',
                           '#E6F5FE', '#FFFAD2', '#FFE3AA', '#F9BD7E',
                           '#ED875E', '#D24D3E', '#AE1C3E'],
    # Fig. 13 - rainbow scheme
    'sron2012_rainbow_4': ['#404096', '#57A3AD', '#DEA73A', '#D92120'],
    'sron2012_rainbow_5': ['#404096', '#529DB7', '#7DB874', '#E39C37',
                           '#D92120'],
    'sron2012_rainbow_6': ['#404096', '#498CC2', '#63AD99', '#BEBC48',
                           '#E68B33', '#D92120'],
    'sron2012_rainbow_7': ['#781C81', '#3F60AE', '#539EB6', '#6DB388',
                           '#CAB843', '#E78532', '#D92120'],
    'sron2012_rainbow_8': ['#781C81', '#3F56A7', '#4B91C0', '#5FAA9F',
                           '#91BD61', '#D8AF3D', '#E77C30', '#D92120'],
    'sron2012_rainbow_9': ['#781C81', '#3F4EA1', '#4683C1', '#57A3AD',
                           '#6DB388', '#B1BE4E', '#DFA53A', '#E7742F',
                           '#D92120'],
    'sron2012_rainbow_10': ['#781C81', '#3F479B', '#4277BD', '#529DB7',
                            '#62AC9B', '#86BB6A', '#C7B944', '#E39C37',
                            '#E76D2E', '#D92120'],
    'sron2012_rainbow_11': ['#781C81', '#404096', '#416CB7', '#4D95BE',
                            '#5BA7A7', '#6EB387', '#A1BE56', '#D3B33F',
                            '#E59435', '#E6682D', '#D92120'],
    'sron2012_rainbow_12': ['#781C81', '#413B93', '#4065B1', '#488BC2',
                            '#55A1B1', '#63AD99', '#7FB972', '#B5BD4C',
                            '#D9AD3C', '#E68E34', '#E6642C', '#D92120'],
    # Fig. 14 - banded rainbow
    'sron2012_rainbow_band_14': ['#882E72', '#B178A6', '#D6C1DE', '#1965B0',
                                 '#5289C7', '#7BAFDE', '#4EB265', '#90C987',
                                 '#CAE0AB', '#F7EE55', '#F6C141', '#F1932D',
                                 '#E8601C', '#DC050C'],
    'sron2012_rainbow_band_15': ['#114477', '#4477AA', '#77AADD', '#117755',
                                 '#44AA88', '#99CCBB', '#777711', '#AAAA44',
                                 '#DDDD77', '#771111', '#AA4444', '#DD7777',
                                 '#771144', '#AA4477', '#DD77AA'],
    'sron2012_rainbow_band_18': ['#771155', '#AA4488', '#CC99BB', '#114477',
                                 '#4477AA', '#77AADD', '#117777', '#44AAAA',
                                 '#77CCCC', '#777711', '#AAAA44', '#DDDD77',
                                 '#774411', '#AA7744', '#DDAA77', '#771122',
                                 '#AA4455', '#DD7788'],
    'sron2012_rainbow_band_21': ['#771155', '#AA4488', '#CC99BB', '#114477',
                                 '#4477AA', '#77AADD', '#117777', '#44AAAA',
                                 '#77CCCC', '#117744', '#44AA77', '#88CCAA',
                                 '#777711', '#AAAA44', '#DDDD77', '#774411',
                                 '#AA7744', '#DDAA77', '#771122', '#AA4455',
                                 '#DD7788'],
}


def _ylorbr(x):
    """ Eq. 1 of sron_colourschemes.pdf """
    r = 1.0 - 0.392*(1.0 + erf((x - 0.869) / 0.255))
    g = 1.021 - 0.456*(1.0 + erf((x - 0.527) / 0.376))
    b = 1.0 - 0.493*(1.0 + erf((x - 0.272) / 0.309))
    return r, g, b


def _buylrd(x):
    """ Eq. 2 of sron_colourschemes.pdf """
    r = (0.237 - 2.13 * x + 26.92 * x**2 - 65.5 * x**3
         + 63.5 * x**4 - 22.36 * x**5)
    g = ( (0.572 + 1.524 * x - 1.811 * x**2)
          / (1.0 - 0.291 * x + 0.1574 * x**2) )**2
    b = 1.0 / (1.579 - 4.03 * x + 12.92 * x**2 - 31.4 * x**3
               + 48.6 * x**4 - 23.36 * x**5)
    return r, g, b


def _rainbow(x):
    """ Eq. 3 of sron_colourschemes.pdf """
    r = ((0.472 - 0.567 * x + 4.05 * x**2)
         / (1.0 + 8.72 * x - 19.17 * x**2 + 14.1 * x**3))
    g = (0.108932 - 1.22635 * x + 27.284 * x**2 - 98.577 * x**3
         + 163.3 * x**4 - 131.395 * x**5 + 40.634 * x**6)
    b = 1.0 / (1.97 + 3.54 * x - 68.5 * x**2 + 243. * x**3
               - 297. * x**4 + 125. * x**5)
    return r, g, b


sron2012_functions = {
    # Fig. 7 - sequential data yellow-orange-brown
    'sron2012_ylorbr': _ylorbr,
    # Fig. 8 - diverging data blue-yellow-red
    'sron2012_buylrd': _buylrd,
    # Fig. 13 - rainbow scheme
    'sron2012_rainbow': _rainbow,
}


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
