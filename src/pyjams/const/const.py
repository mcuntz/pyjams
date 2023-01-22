#!/usr/bin/env python
"""
Physical, mathematical, computational, isotope, and material constants.

Defines the following constants:
    Mathematical
        Pi, Pi2, Pi3, TwoPi, Sqrt2, pi, pi2, pi3, Twopi

    Physical
        Gravity, T0, P0, T25, sigma, R, R_air, R_H2O, Na, REarth

    Isotope
        R13VPDB, R18VSMOW, R2VSMOW

    Computational
        tiny, huge, eps

    Material
        mmol_co2, mmol_h2o, mmol_air,
        density_quartz, cheat_quartz, cheat_water, cheat_air,
        latentheat_vaporization

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2012-2021 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

Constants:

.. autosummary::
   Pi
   Pi2
   Pi3
   TwoPi
   pi
   pi2
   pi3
   Twopi
   Sqrt2
   sqrt2
   gravity
   T0
   P0
   T25
   sigma
   R
   Rair
   Rh2o
   Na
   kB
   REarth
   mmol_co2
   molmass_co2
   mmol_h2o
   molmass_h2o
   mmol_air
   molmass_air
   density_quartz
   cheat_quartz
   cheat_water
   cheat_air
   latentheat_vaporization
   R13VPDB
   R18VSMOW
   R2VSMOW
   tiny
   huge
   eps

History
    * Written Jan 2012 by Matthias Cuntz (mc (at) macu (dot) de)
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Added dielectric constant for water, Mar 2014, Arndt Piayda
    * Added heat capacities for air, water and quartz as well as density of
      quartz, Sep 2014, Arndt Piayda
    * Added Pi3=pi/3, R13VPDB, R18VSMOW, R2VSMOW, Mar 2015, Matthias Cuntz
    * Renamed heat capacities, molar masses, density of quartz,
      Mar 2015, Matthias Cuntz
    * Moved calculation of dielectric constant of water to own routine,
      Mar 2015, Matthias Cuntz
    * Added computational constants such as tiny=np.finfo(np.float).tiny,
      Nov 2016, Matthias Cuntz
    * Added gas constants for dry air and water, May 2017, RL
    * Using numpy docstring format, May 2020, Matthias Cuntz
    * Added lowercase version of pi constants, May 2020, Matthias Cuntz
    * Updated all constants related to gases for redefinition of
      SI units of 2019, Jan 2023, Matthias Cuntz
    * Renamed some constant for greater consistency, Jan 2023, Matthias Cuntz

"""
from __future__ import division, absolute_import, print_function
import numpy as np


__all__ = [
    'Pi', 'Pi2', 'Pi3', 'TwoPi', 'pi', 'pi2', 'pi3', 'Twopi', 'Sqrt2', 'sqrt2',
    'gravity', 'T0', 'P0', 'T25', 'sigma', 'R', 'Rair', 'Rh2o',
    'Na', 'REarth', 'mmol_co2', 'molmass_co2', 'mmol_h2o', 'molmass_h2o',
    'mmol_air', 'molmass_air',
    'density_quartz', 'cheat_quartz', 'cheat_water', 'cheat_air',
    'latentheat_vaporization',
    'R13VPDB', 'R18VSMOW', 'R2VSMOW',
    'tiny', 'huge', 'eps']


# Mathematical
Pi = 3.141592653589793238462643383279502884197
r"""
Mathematical constant :math:`\pi`
"""
pi = 3.141592653589793238462643383279502884197
r"""
Mathematical constant :math:`\pi`
"""
Pi2 = 1.57079632679489661923132169163975144209858
r"""
Mathematical constant :math:`\pi/2`
"""
pi2   = 1.57079632679489661923132169163975144209858
r"""
Mathematical constant :math:`\pi/2`
"""
Pi3   = 1.0471975511965977461542144610931676280656
r"""
Mathematical constant :math:`\pi/3`
"""
pi3   = 1.0471975511965977461542144610931676280656
r"""
Mathematical constant :math:`\pi/3`
"""
TwoPi = 6.283185307179586476925286766559005768394
r"""
Mathematical constant :math:`2\pi`
"""
Twopi = 6.283185307179586476925286766559005768394
r"""
Mathematical constant :math:`2\pi`
"""
Sqrt2 = 1.41421356237309504880168872420969807856967
r"""
Mathematical constant :math:`\sqrt{2}`
"""
sqrt2 = 1.41421356237309504880168872420969807856967
r"""
Mathematical constant :math:`\sqrt{2}`
"""

# Physical
gravity = 9.80665
r"""
Standard average Earth's gravity (:math:`m^2 s^{-1}`)
"""
T0 = 273.15
"""
0 degree Celsius in Kelvin.
Conversion constant from Celsius to Kelvin.
"""
P0 = 101325.
"""
Standard pressure (Pa)
"""
T25 = 298.15
r"""
Standard ambient temperature of 25 :math:`^\circ C` in Kelvin [K]
"""
sigma = 5.67e-08
"""
Stefan-Boltzmann constant (:math:`W m^{-2} K^{-4}`)
"""
R = 8.31446261815324
r"""
Ideal gas constant R = Na*kB (:math:`J K^{-1} mol^{-1}`)
"""
Rair = 287.05799595894405
r"""
Specific gas constant of dry air Rair = R/molmass_air (:math:`J K^{-1} kg^{-1}`)
"""
Rh2o = 461.52280831345604
r"""
Gas constant of water vapour Rh2o = R/molmass_h2o (:math:`J K^{-1} kg^{-1}`)
"""
Na = 6.02214076e23
r"""
Avogadro number (:math:`mol^{-1}`)
"""
kB = 1.380649e-23
r"""
Boltzmann constant (:math:`J K^{-1}`)
"""
REarth = 6371009.
"""
Radius of the Earth (m)
"""

# Material
mmol_co2 = 44.009
r"""
Molar mass of :math:`CO_2` (:math:`g mol^{-1}`)
"""
molmass_co2 = 44.009e-3
r"""
Molar mass of :math:`CO_2` (:math:`kg mol^{-1}`)
"""
mmol_h2o = 18.01528
r"""
Molar mass of water (:math:`g mol^{-1}`)
"""
molmass_h2o = 18.01528e-3
r"""
Molar mass of water (:math:`kg mol^{-1}`)
"""
mmol_air = 28.9644
r"""
Molar mass of dry air of standard atmosphere (:math:`g mol^{-1}`)
"""
molmass_air = 28.9644e-3
r"""
Molar mass of dry air (:math:`kg mol^{-1}`)
"""
# from Cambell G (1985) Soil Physics with BASIC, Elsevier Science
density_quartz = 2.65
r"""
Density of quartz (:math:`g cm^{-3}`)
"""
cheat_quartz = 800.
r"""
Heat capacity of quartz (:math:`J kg^-1 K^-1`)
"""
cheat_water = 4180.
r"""
Heat capacity of water (:math:`J kg^{-1} K^{-1}`)
"""
cheat_air = 1010.
r"""
Heat capacity of air (:math:`J kg^{-1} K^{-1}`)
"""
latentheat_vaporization = 2.45e6
r"""
Latent heat of vaporization of water (:math:`J kg^{-1}`)
"""

# Isotope
R13VPDB = 0.0112372
r"""
:math:`^{13}C` isotope ratio of VPDB
"""
R18VSMOW = 2005.2e-6
r"""
:math:`^{18}O` isotope ratio of VSMOW
"""
R2VSMOW = 155.76e-6
r"""
Deuterium= :math:`^{2}H` isotope ratio of VSMOW
"""

# Computational
eps = np.finfo(float).eps
r"""
Numerical precision of floats.
The difference between 1.0 and the next smallest representable float larger
than 1.0. For example, for 64-bit binary floats in the IEEE-754 standard,
:math:`eps = 2^{-52}`, approximately 2.22e-16.
"""
huge = np.finfo(float).max
"""
The largest representable floating point number.
"""
tiny = np.finfo(float).tiny
"""
The smallest positive floating point number with full precision.
"""


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
