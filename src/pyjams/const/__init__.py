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
from .const import Pi, Pi2, Pi3, TwoPi, pi, pi2, pi3, Twopi, Sqrt2, sqrt2
from .const import gravity, T0, P0, T25, sigma, R, Rair, Rh2o
from .const import Na, kB, REarth
from .const import mmol_co2, molmass_co2, mmol_h2o, molmass_h2o
from .const import mmol_air, molmass_air
from .const import density_quartz, cheat_quartz, cheat_water, cheat_air
from .const import latentheat_vaporization
from .const import R13VPDB, R18VSMOW, R2VSMOW
from .const import tiny, huge, eps


__all__ = [
    'Pi', 'Pi2', 'Pi3', 'TwoPi', 'pi', 'pi2', 'pi3', 'Twopi', 'Sqrt2', 'sqrt2',
    'gravity', 'T0', 'P0', 'T25', 'sigma', 'R', 'Rair', 'Rh2o',
    'Na', 'kB', 'REarth', 'mmol_co2', 'molmass_co2', 'mmol_h2o', 'molmass_h2o',
    'mmol_air', 'molmass_air',
    'density_quartz', 'cheat_quartz', 'cheat_water', 'cheat_air',
    'latentheat_vaporization',
    'R13VPDB', 'R18VSMOW', 'R2VSMOW',
    'tiny', 'huge', 'eps']
