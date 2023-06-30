#!/usr/bin/env python


__all__ = ['lat_fmt', 'lon_fmt']


def lat_fmt(lat):
    r"""
    Set lat label string (called by Basemap.drawparallels) if LaTeX package
    clash.


    Definition
    ----------
    def lat_fmt(lat):


    Input
    -----
    latitude -90-90


    Output
    ------
    formatted string


    Examples
    --------
    >>> import matplotlib as mpl
    >>> mpl.rcParams['text.usetex'] = False
    >>> lat = [-90, -45, 0, 45, 90]
    >>> for l in lat: print(lat_fmt(l))
    90$^{\circ}$S
    45$^{\circ}$S
    0$^{\circ}$N
    45$^{\circ}$N
    90$^{\circ}$N

    >>> mpl.rcParams['text.usetex'] = True
    >>> for l in lat: print(lat_fmt(l))
    90$\/^{\circ}\/\mathrm{S}$
    45$\/^{\circ}\/\mathrm{S}$
    0$\/^{\circ}\/\mathrm{N}$
    45$\/^{\circ}\/\mathrm{N}$
    90$\/^{\circ}\/\mathrm{N}$

    History
    -------
    Written,  MC, Oct 2015
    """
    from matplotlib import rcParams
    if rcParams['text.usetex']:
        if lat < 0:
            return str(abs(int(lat))) + r'$\/^{\circ}\/\mathrm{S}$'
        else:
            return str(int(lat)) + r'$\/^{\circ}\/\mathrm{N}$'
    else:
        if lat < 0:
            return str(abs(int(lat))) + r'$^{\circ}$S'
        else:
            return str(int(lat)) + r'$^{\circ}$N'


def lon_fmt(lon):
    r"""
    Set lon label string (called by Basemap.drawmeridians) if LaTeX package
    clash.


    Definition
    ----------
    def lon_fmt(lon):


    Input
    -----
    longitude 0-360


    Output
    ------
    formatted string


    Examples
    --------
    >>> import matplotlib as mpl
    >>> mpl.rcParams['text.usetex'] = False
    >>> lon = [0, 90, 180, 270, 360]
    >>> for l in lon: print(lon_fmt(l))
    0$^{\circ}$E
    90$^{\circ}$E
    180$^{\circ}$E
    90$^{\circ}$W
    0$^{\circ}$E

    >>> mpl.rcParams['text.usetex'] = True
    >>> for l in lon: print(lon_fmt(l))
    0$\/^{\circ}\/\mathrm{E}$
    90$\/^{\circ}\/\mathrm{E}$
    180$\/^{\circ}\/\mathrm{E}$
    90$\/^{\circ}\/\mathrm{W}$
    0$\/^{\circ}\/\mathrm{E}$

    History
    -------
    Written,  MC, Oct 2015
    """
    from matplotlib import rcParams
    if lon > 180:
        ilon = lon - 360
    else:
        ilon = lon
    if rcParams['text.usetex']:
        if ilon < 0:
            return str(abs(int(ilon))) + r'$\/^{\circ}\/\mathrm{W}$'
        else:
            return str(int(ilon)) + r'$\/^{\circ}\/\mathrm{E}$'
    else:
        if ilon < 0:
            return str(abs(int(ilon))) + r'$^{\circ}$W'
        else:
            return str(int(ilon)) + r'$^{\circ}$E'


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # lon = [0, 90, 180, 270, 360]
    # for l in lon: print(lon_fmt(l))
    # # 0$^{\circ}$E
    # # 90$^{\circ}$E
    # # 180$^{\circ}$E
    # # 90$^{\circ}$W
    # # 0$^{\circ}$E

    # lat = [-90, -45, 0, 45, 90]
    # for l in lat: print(lat_fmt(l))
    # # 90$^{\circ}$S
    # # 45$^{\circ}$S
    # # 0$^{\circ}$N
    # # 45$^{\circ}$N
    # # 90$^{\circ}$N

    # import matplotlib as mpl
    # mpl.rcParams['text.usetex'] = True

    # for l in lon: print(lon_fmt(l))
    # # 0$\/^{\circ}\/\mathrm{E}$
    # # 90$\/^{\circ}\/\mathrm{E}$
    # # 180$\/^{\circ}\/\mathrm{E}$
    # # 90$\/^{\circ}\/\mathrm{W}$
    # # 0$\/^{\circ}\/\mathrm{E}$

    # for l in lat: print(lat_fmt(l))
    # # 90$\/^{\circ}\/\mathrm{S}$
    # # 45$\/^{\circ}\/\mathrm{S}$
    # # 0$\/^{\circ}\/\mathrm{N}$
    # # 45$\/^{\circ}\/\mathrm{N}$
    # # 90$\/^{\circ}\/\mathrm{N}$
