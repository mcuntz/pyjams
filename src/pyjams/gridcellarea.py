#!/usr/bin/env python
"""
Area of grid cells on Earth

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2009-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   gridcellarea

History
    * Written Jul 2009 by Matthias Cuntz - mc (at) macu (dot) de
    * Ported to Python 3, Feb 2013, Matthias Cuntz
    * Assert correct input, Apr 2014, Matthias Cuntz
    * Clip lat because -90 and 90 give negative area, Oct 2018, Matthias Cuntz
    * Corrected bug in checking ascending or descending lats,
      Apr 2022, Matthias Cuntz
    * Removed assertion of nlat/nlon > 2, Apr 2022, Matthias Cuntz
    * Keyword radius of Earth and changed default from 6371000 to 6371009
      as in the rest of pyjams, Apr 2022, Matthias Cuntz
    * Rename cellarea to gridcellarea, Apr 2022, Matthias Cuntz

"""
import numpy as np


__all__ = ['gridcellarea']


def gridcellarea(lat, lon, globe=False, rearth=6371009.):
    """
    Area of grid cells on a spherical Earth in square metre

    Parameters
    ----------
    lat : array_like
        Latitudes of grid cell centres in degrees N
    lon : array_like
        Longitudes of grid cell centres in degrees E
    globe : bool, optional
        Assumes that latitudes span the globe if True,
        i.e. they are bounded by 90 and -90 degrees latitude
    rearth : float, optional
        Radius of the spherical Earth (default: 6371009.)

    Returns
    -------
    numpy array with area in m^2


    Notes
    -----
    This is a rather rough routine with lots of possible improvements,
    notably allowing irregular grids, grid boundaries, etc.


    Examples
    --------

    Gaussian latitudes

    >>> lat = np.array([ 12.98898858, 9.27785325, 5.56671363])
    >>> lon = np.array([ 0., 3.75, 7.5])

    >>> print(gridcellarea(lat, lon)[0,:])
    [1.67639557e+11 1.67639557e+11 1.67639557e+11]

    >>> print(gridcellarea(lat, lon)[1,:])
    [1.69790907e+11 1.69790907e+11 1.69790907e+11]

    >>> print(gridcellarea(lat, lon)[2,:])
    [1.71230373e+11 1.71230373e+11 1.71230373e+11]

    """
    # assert numpy
    lati = np.array(lat)
    loni = np.array(lon)
    nlat = lati.size
    nlon = loni.size

    # assert -90 < lat < 90
    assert np.abs(lat).max() <= 90., (
        'probably swapped lat and lon in call:'
        ' def gridcellarea(lat, lon, globe=False):')

    # lat size in degrees
    # still + or -
    dlat = lati - np.roll(lati, 1)
    if globe:
        if dlat[0] > 0:  # descending lats
            l0 = 90.
        else:            # ascending lats
            l0 = -90.
        dlat[0]  = (lati[0] - l0) + 0.5 * (lati[1] - lati[0])
        dlat[-1] = (-l0 - lati[-1]) - 0.5*(lati[-2] - lati[-1])
    else:
        dlat[0]  = lati[1] - lati[0]
        dlat[-1] = lati[-1] - lati[-2]

    # lon size in degrees
    # check if meridian in lon range -> shift to -180,180
    # e.g. 358 359 0 1
    if np.any(np.abs(np.diff(loni)) > 360. / nlon):
        loni = np.where(loni > 180., loni - 360., loni)
    # check if -180,180 longitude in lon range -> shift to 0,360
    # e.g. 179 180 -179 -178
    if np.any(np.abs(np.diff(loni)) > 360. / nlon):
        loni = np.where(loni < 0., loni + 360., loni)
    dlon = np.abs(loni - np.roll(loni, 1))
    dlon[0] = np.abs(loni[1] - loni[0])

    # Northern latitudes of grid cell edges
    n_lat = lati[0] + dlat[0]/2. + np.cumsum(dlat)

    # Area of grid cells in m^2 with lat/lon in degree
    d2r = np.pi / 180.  # degree to radian

    area = np.empty([nlat, nlon])
    dlat = np.abs(dlat[:])
    # -90, 90 give negative np.cos(lat*d2r)
    lati = np.clip(lati, -89.99999, 89.99999)
    for i in range(nlon):
        area[:, i] = (2. * d2r * rearth**2 * dlon[i] *
                      np.sin(0.5 * dlat * d2r) * np.cos(lati * d2r))

    return area


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
