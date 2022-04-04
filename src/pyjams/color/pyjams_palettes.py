#!/usr/bin/env python
"""
pyjams own color palettes

.. moduleauthor:: Matthias Cuntz

History
    * Written Apr 2022, Matthias Cuntz,
      added pyjams_amwg

"""

__all__ = ['pyjams_cmaps']


# Toned down version of ncl_amwg w/o pink and rose,
# from Cernusak et al. (New Phyt 2022)
# This is the change from the New Phytology editorial office
# to our plots made with ncl_amwg.
# Must be some kind of conversion between RGB, sRGB or Adobe RGB.
pyjams_amwg = [
    (145, 45, 50),
    (213, 75, 40),
    (229, 153, 42),
    (244, 208, 43),
    (206, 172, 130),
    (239, 220, 182),
    (14, 132, 88),
    (141, 185, 66),
    (0, 152, 163),
    (155, 204, 213),
    (93, 136, 185),
    (36, 91, 153),
    (36, 33, 104),
    (124, 104, 157),
    (0, 0, 0),
    (255, 255, 255) ]
pyjams_amwg = [ (c[0]/255, c[1]/255, c[2]/255) for c in pyjams_amwg ][::-1]

# pyjams color maps
pyjams_cmaps = {
    'pyjams_amwg': pyjams_amwg,
}


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
