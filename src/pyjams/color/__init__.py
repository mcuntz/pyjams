"""
Collection of color palettes and continuous color maps

:copyright: Copyright 2021- Matthias Cuntz, see AUTHORS.md for details.
:license: MIT License, see LICENSE for details.

Subpackages
===========
.. autosummary::
   brewer_palettes
   mathematica_palettes
   ncl_palettes
   oregon_palettes
   sron2012_palettes
   sron_palettes
   color

"""
# colour palettes
from .brewer_palettes import brewer_sequential, brewer_diverging
from .brewer_palettes import brewer_qualitative
from .mathematica_palettes import mathematica_rainbow
from .ncl_palettes import ncl_large, ncl_small, ncl_meteo_swiss
from .oregon_palettes import oregon_sequential, oregon_diverging
from .oregon_palettes import oregon_qualitative
from .sron2012_palettes import sron2012_colors, sron2012_functions
from .sron_palettes import sron_colors, sron_colormaps, sron_functions
# get, show, print color palettes
from .color import get_cmap, print_palettes, show_palettes


__all__ = ['brewer_sequential', 'brewer_diverging', 'brewer_qualitative',
           'mathematica_rainbow',
           'ncl_large', 'ncl_small', 'ncl_meteo_swiss',
           'oregon_sequential', 'oregon_diverging', 'oregon_qualitative',
           'sron2012_colors', 'sron2012_functions',
           'sron_colors', 'sron_colormaps', 'sron_functions',
           'get_cmap', 'print_palettes', 'show_palettes',
           ]
