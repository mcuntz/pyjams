"""
Provides physical, mathematical, computational, isotope, and material
constants, such as `Pi = 3.141592653589793238462643383279502884197`.

:copyright: Copyright 2012-2021 Matthias Cuntz, see AUTHORS.md for details.
:license: MIT License, see LICENSE for details.

Subpackages
===========
.. autosummary::
   const
"""
from .const import Pi, Pi2, Pi3, TwoPi, pi, pi2, pi3, Twopi, Sqrt2
from .const import Gravity, T0, P0, T25, sigma, R, R_air, R_H2O
from .const import Na, REarth, mmol_co2, mmol_h2o, mmol_air
from .const import density_quartz, cheat_quartz, cheat_water, cheat_air
from .const import latentheat_vaporization
from .const import R13VPDB, R18VSMOW, R2VSMOW
from .const import tiny, huge, eps


__all__ = [
    'Pi', 'Pi2', 'Pi3', 'TwoPi', 'pi', 'pi2', 'pi3', 'Twopi', 'Sqrt2',
    'Gravity', 'T0', 'P0', 'T25', 'sigma', 'R', 'R_air', 'R_H2O',
    'Na', 'REarth', 'mmol_co2', 'mmol_h2o', 'mmol_air',
    'density_quartz', 'cheat_quartz', 'cheat_water', 'cheat_air',
    'latentheat_vaporization',
    'R13VPDB', 'R18VSMOW', 'R2VSMOW',
    'tiny', 'huge', 'eps']
