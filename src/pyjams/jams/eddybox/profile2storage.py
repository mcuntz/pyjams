#!/usr/bin/env python
import numpy as np
from pyjams.jams.date2dec import date2dec
from pyjams.const import mmol_co2, mmol_h2o, mmol_air, cheat_air, latentheat_vaporization, T0
from scipy.interpolate import splrep, splint
from pyjams.air_humidity import esat


def profile2storage(fluxfile, fluxfile2, profilefile, outdir, heights, CO2=None,
                    H2O=None, T=None, rH=None, delimiter=[',',',',','],
                    skiprows=[1,1,1], format=['ascii','ascii','ascii'],
                    undef=-9999, plot=False):
    '''
    Calculates storage fluxes for changes in CO2, H2O, air temperature and air
    moisture from profile data or meteorological data to correct Eddy
    Covariance fluxes. FLux files from EddySoft and from fluxflag are needed as
    well as a file with the profile or meteo data. Fluxes will be updated with
    the respective storage fluxes and saved in a new file. Multiple application
    of this routine with different profile or meteo files are possible to
    correct e.g. the CO2, H2O and latent heat fluxes with profile data of CO2
    and H2O concentrations and afterwards the H flux with temperature data from
    another file.


    Definition
    ----------
    profile2storage(fluxfile, fluxfile2, profilefile, outdir, heights, CO2=None,
                    H2O=None, T=None, rH=None, delimiter=[',',',',','],
                    skiprows=[1,1,1], format=['ascii','ascii','ascii'],
                    undef=-9999, plot=False):


    Input
    -----
    fluxfile    str, path and file name of fluxflag output file containing
                fluxes and flags. These fluxes will be updated by the storage
                fluxes and saved as a new file
    fluxfile2   str, path and file name of EddyFlux output file (timestep
                checked) containing original fluxes
    profilefile str, path and file name of the profile file or meteorology file
                containing CO2, H2O, T or rH values to compute the profile
                storage from
    outdir      str, path of the output folder
    heights     list of floats, observation heights of the profile [m],
                increasing e.g. [0.5,1.0,10.0,20.0].
    CO2         list of int, column numbers of CO2 concentrations for the
                different heights (in the same order) [mumol/mol] in profilefile,
                column number starts with 0 which is first data column.
    H2O         list of int, column numbers of H2O concentrations for the
                different heights (in the same order) [mmol/mol] in profilefile,
                column number starts with 0 which is first data column.
    T           list of int, column numbers of air temperatures for the
                different heights (in the same order) [degC] in profilefile,
                column number starts with 0 which is first data column.
    rH          list of int, column numbers of relative humidity for the
                different heights (in the same order) [%] in profilefile,
                column number starts with 0 which is first data column. The
                calculation of air vapour energy storage change within the
                profile works only when T is given as well.


    Optional Input
    --------------
    delimiter   list of str, delimiters of fluxfile, fluxfile and profilefile
                (default: [',',',',','])
    skiprows    list of int, lines to skip at the beginning of fluxfile,
                fluxfile and profilefile, e.g. header lines (default: [1,1,1])
    format      list of str, time formats of fluxfile, fluxfile and profilefile,
                'ascii' and 'eng' possible (default: ['ascii','ascii','ascii'])
    undef       int/float, missing value of fluxfile, fluxfile and profilefile
                (default: -9999, np.nan is not possible)
    plot        bool, if True performs plotting (default: False)


    Output
    ------
    flux+stor.csv file containing fluxes and flags where storage fluxes are
                  added in an additional column and storage fluxes are appended
                  to the end of the file


    Restrictions
    ------------
    Works only with half hourly time steps, all files in sync


    License
    -------
    This file is part of the JAMS Python package, distributed under the MIT
    License. The JAMS Python package originates from the former UFZ Python library,
    Department of Computational Hydrosystems, Helmholtz Centre for Environmental
    Research - UFZ, Leipzig, Germany.

    Copyright (c) 2014 Arndt Piayda

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.


    History
    -------
    Written,  AP, Sep 2014
    '''
    ###########################################################################
    # time interval
    int = 30.
    dt  = int*60.

    if plot:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import matplotlib.backends.backend_pdf as pdf

    ###########################################################################
    # reading input files
    # fluxes to correct for storage changes
    d1 = np.loadtxt(fluxfile, dtype='|S100', delimiter=delimiter[0])
    # original flux file from EddyFlux containing air density rho_a
    d2 = np.loadtxt(fluxfile2, dtype='|S100', delimiter=delimiter[1])
    # file containing profile data (can be meteo file if no profile available)
    d3 = np.loadtxt(profilefile, dtype='|S100', delimiter=delimiter[2])

    assert (d1.shape[1]==11) | (d1.shape[1]==19), 'profile2storage: fluxfile must be from fluxflag or profiletostorage and have 11 or 19 cols'
    assert d2.shape[1]==68, 'profile2storage: fluxfile2 must be from EddyFlux and have 68 cols'
    assert d1.shape[0]==d2.shape[0], 'profile2storage: fluxfile and fluxfile2 must be in sync'
    assert d1.shape[0]==d3.shape[0], 'profile2storage: fluxfile and profilefile must be in sync'
    assert (((H2O==None) & (rH==None)) ^ ((H2O!=None) ^ (rH!=None))), 'profile2storage: give either H2O or rH, both would be double correction'

    if format[0]=='ascii':
        datev   = date2dec(ascii=d1[skiprows[0]:,0])
    elif format[0]=='eng':
        datev   = date2dec(eng=d1[skiprows[0]:,0])
    else:
        raise ValueError('profile2storage: unknown format')
    if format[2]=='ascii':
        datem   = date2dec(ascii=d2[skiprows[2]:,0])
    elif format[2]=='eng':
        datem   = date2dec(eng=d2[skiprows[2]:,0])
    else:
        raise ValueError('profile2storage: unknown format')

    flux1 = np.where(d1[skiprows[0]:,1:]=='', str(undef), d1[skiprows[0]:,1:]).astype(np.float)
    flux2 = np.where(d2[skiprows[1]:,1:]=='', str(undef), d2[skiprows[1]:,1:]).astype(np.float)
    prof  = np.where(d3[skiprows[2]:,1:]=='', str(undef), d3[skiprows[2]:,1:]).astype(np.float)

    flux1 = np.ma.array(flux1, mask=flux1==undef, hard_mask=True)
    flux2 = np.ma.array(flux2, mask=flux2==undef)
    prof  = np.ma.array(prof,  mask=prof==undef)

    ###########################################################################
    # assign variables
    if d1.shape[1]==11:
        H, Hflag   = flux1[:,0], flux1[:,1]
        Le, Leflag = flux1[:,2], flux1[:,3]
        E, Eflag   = flux1[:,4], flux1[:,5]
        C, Cflag   = flux1[:,6], flux1[:,7]
    else:
        H, Hflag   = flux1[:,0], flux1[:,2]
        Le, Leflag = flux1[:,3], flux1[:,5]
        E, Eflag   = flux1[:,6], flux1[:,8]
        C, Cflag   = flux1[:,9], flux1[:,11]
    p          = flux2[:,58] # [hPa]
    rho        = flux2[:,62] # [kg/m3]

    ###########################################################################
    # prepare output array
    d4 = np.copy(d1)
    if d1.shape[1]==11:
        temp = np.empty((d1.shape[0],4), dtype='|S100')
        temp[:] = ' '*(11-len(str(undef)))+str(undef)
        temp[0,:] = ['       H+sT','     LE+sLE','       E+sE','       C+sC']
        d4 = np.insert(d4, [2,4,6,8], temp, axis=1)

        temp[0,:] = ['         sT','        sLE','         sE','         sC']
        d4 = np.append(d4, temp, axis=1)

    ###########################################################################
    # calls
    if CO2:
        CO2 = prof[:,CO2]
        assert CO2.shape[1]==len(heights), 'profile2storage: number of CO2 cols must equal heights'
        # calculate storage flux and storage flux flag
        sfCO2     = stor2flux(CO2, rho, heights, dt, 'CO2')
        sfCO2flag = sfCO2.mask.astype(np.int)
        # add to eddy flux
        newC      = C + np.ma.filled(sfCO2, 0)
        # format and write into output array
        newC_str  = np.array(['%11.5f'%x for x in np.ma.filled(newC, undef)])
        newC_str  = np.where(newC_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), newC_str)
        sfCO2_str = np.array(['%11.5f'%x for x in np.ma.filled(sfCO2, undef)])
        sfCO2_str = np.where(sfCO2_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), sfCO2_str)
        d4[skiprows[0]:,11] = newC_str
        d4[skiprows[0]:,18] = sfCO2_str

        if plot:
            storplot(CO2, datev, heights, C, sfCO2, newC, 'storageCO2.pdf', pdf, plt, mpl, outdir)

    if H2O:
        H2O = prof[:,H2O]
        assert H2O.shape[1]==len(heights), 'profile2storage: number of H2O cols must equal heights'
        # calculate storage flux and storage flux flag
        sfH2O     = stor2flux(H2O, rho, heights, dt, 'H2O')
        sfH2O_Wm2 = sfH2O * mmol_h2o * latentheat_vaporization /1.e6
        sfH2Oflag = sfH2O.mask.astype(np.int)
        # add to eddy flux
        newE      = E + np.ma.filled(sfH2O, 0)
        newLe     = Le + np.ma.filled(sfH2O_Wm2, 0)
        # format and write into output array
        newE_str      = np.array(['%11.5f'%x for x in np.ma.filled(newE, undef)])
        newLe_str     = np.array(['%11.5f'%x for x in np.ma.filled(newLe, undef)])
        sfH2O_str     = np.array(['%11.5f'%x for x in np.ma.filled(sfH2O, undef)])
        sfH2O_Wm2_str = np.array(['%11.5f'%x for x in np.ma.filled(sfH2O_Wm2, undef)])
        newE_str      = np.where(newE_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), newE_str)
        newLe_str     = np.where(newLe_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), newLe_str)
        sfH2O_str     = np.where(sfH2O_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), sfH2O_str)
        sfH2O_Wm2_str = np.where(sfH2O_Wm2_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), sfH2O_Wm2_str)
        d4[skiprows[0]:,8]  = newE_str
        d4[skiprows[0]:,17] = sfH2O_str
        d4[skiprows[0]:,5]  = newLe_str
        d4[skiprows[0]:,16] = sfH2O_Wm2_str

        if plot:
            storplot(H2O, datev, heights, E, sfH2O, newE, 'storageH2O.pdf', pdf, plt, mpl, outdir)

    if T:
        T   = prof[:,T]
        assert T.shape[1]==len(heights), 'profile2storage: number of T cols must equal heights'
        # calculate storage flux and storage flux flag
        sfT       = stor2flux(T, rho, heights, dt, 'T')
        sfTflag   = sfT.mask.astype(np.int)
        # add to eddy flux
        newH      = H + np.ma.filled(sfT, 0)
        # format and write into output array
        newH_str  = np.array(['%11.5f'%x for x in np.ma.filled(newH, undef)])
        newH_str  = np.where(newH_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), newH_str)
        sfT_str   = np.array(['%11.5f'%x for x in np.ma.filled(sfT, undef)])
        sfT_str   = np.where(sfT_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), sfT_str)
        d4[skiprows[0]:,2]  = newH_str
        d4[skiprows[0]:,15] = sfT_str

        if plot:
            storplot(T, datev, heights, H, sfT, newH, 'storageT.pdf', pdf, plt, mpl, outdir)

    if rH:
        rH  = prof[:,rH]
        assert rH.shape[1]==len(heights), 'profile2storage: number of rH cols must equal heights'
        # calculate specific humidity
        vapourpressure = esat(T+T0)*(rH/100.)/100. #[hPa]
        specifichumidity = (mmol_h2o/mmol_air*vapourpressure) / (p-(1.-mmol_h2o/mmol_air)*vapourpressure)
        # calculate storage flux and storage flux flag
        sfrH_Wm2  = stor2flux(specifichumidity, rho, heights, dt, 'rH')
        sfrH      = sfrH_Wm2 * 1.e6 / (mmol_h2o * latentheat_vaporization)
        sfrHflag  = sfrH.mask.astype(np.int)
        # add to eddy flux
        newE      = E + np.ma.filled(sfrH, 0)
        newLe     = Le + np.ma.filled(sfrH_Wm2, 0)
        # format and write into output array
        newE_str     = np.array(['%11.5f'%x for x in np.ma.filled(newE, undef)])
        newLe_str    = np.array(['%11.5f'%x for x in np.ma.filled(newLe, undef)])
        sfrH_str     = np.array(['%11.5f'%x for x in np.ma.filled(sfrH, undef)])
        sfrH_Wm2_str = np.array(['%11.5f'%x for x in np.ma.filled(sfrH_Wm2, undef)])
        newE_str     = np.where(newE_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), newE_str)
        newLe_str    = np.where(newLe_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), newLe_str)
        sfrH_str     = np.where(sfrH_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), sfrH_str)
        sfrH_Wm2_str = np.where(sfrH_Wm2_str=='%11.5f'%undef, ' '*(11-len(str(undef)))+str(undef), sfrH_Wm2_str)
        d4[skiprows[0]:,8]  = newE_str
        d4[skiprows[0]:,17] = sfrH_str
        d4[skiprows[0]:,5]  = newLe_str
        d4[skiprows[0]:,16] = sfrH_Wm2_str

        if plot:
            storplot(rH, datev, heights, E, sfH2O, newE, 'storagerH.pdf', pdf, plt, mpl, outdir)

    ###########################################################################
    # write output
    np.savetxt('%s/flux+stor.csv'%outdir, d4, '%s', delimiter=',')

def stor2flux(concentrations, rho, heights, dt, constituent='CO2'):
    '''
    '''
    xb = 0.0                # bottom height of interpolation
    xe = np.amax(heights)   # top height of interpolation

    if constituent=='CO2':
        # mole volume [m3/mol] = mmol_co2[g/mol]/(rho[kg/m3]*1000.)
        m = mmol_co2/(rho*1000.)
    elif constituent=='H2O':
        # mole volume [m3/mol] = mmol_h2o[g/mol]/(rho[kg/m3]*1000.)
        m = mmol_h2o/(rho*1000.)
    elif constituent=='T':
        # 1/energy content of the air [1/(J/m3 K)] = 1/ (rho[kg/m3]*heat capacity of air [J/kg K])
        m = 1./(rho*cheat_air)
    elif constituent=='rH':
        # 1/energy content of vapor [1/(J/m3)] = 1/ (rho[kg/m3] * specific heat of vaporization of water [J/kg])
        m = 1./(rho * latentheat_vaporization)
    else:
        raise ValueError('stor2flux: unknown constituent')

    ###########################################################################
    # calculate storage for every time step
    storage, sf = np.ma.masked_all_like(rho), np.ma.masked_all_like(rho)
    for i,item in enumerate(concentrations):
        if not item.mask.any():
            # if only one height given, take box approach (splrep does not work)
            if len(heights)==1:
                storage[i] = item*heights
            # else interpolate nicely :-)
            else:
                tck        = splrep(heights,item,xb=xb,xe=xe,k=1)
                storage[i] = splint(xb,xe,tck)

    ###########################################################################
    # calculate storage flux
    # storage flux per time step
    # for CO2: [mumol/m*2] = [mumol/mol*m]/[m3/mol]
    # for H2O: [mmol/m*2] = [mmol/mol*m]/[m3/mol]
    # for T:   [J/m*2] = [K*m]/[1/(J/m3 K)]
    # for rH:  [J/m*2] = [m]/[1/(J/m3)]
    sf[1:] = storage[:-1]/m[:-1] - storage[1:]/m[1:]
    sf[0]  = sf[1]
    # storage flux per second
    # for CO2: [mumol/(m2*s)]
    # for H2O: [mmol/(m2*s)]
    # for T:   [J/(m2*s)]=[W/m*2]
    # for rH:  [J/(m2*s)]=[W/m*2]
    sf     = sf/dt

    return sf

def storplot(conc, date, heights, oriflux, storflux, newflux, name, pdf, plt, mpl, outdir):
    '''
    '''
    majticks = mpl.dates.MonthLocator(bymonthday=1)
    format_str='%d %m %Y %H:%M'
    date01 = date2dec(yr=1, mo=1, dy=2, hr=0, mi=0, sc=0)

    conc = np.ma.copy(conc.transpose())
    date = np.ma.copy(date-date01)

    pp1 = pdf.PdfPages(outdir+'/'+name)
    fig1 = plt.figure(name)
    sub1 = fig1.add_subplot(211)
    for i, item in enumerate(conc):
        sub1.plot(date, item, label='%2.1f m'%(heights[i]))
    plt.legend(loc='best')

    sub2 = fig1.add_subplot(212)
    sub2.axhline(y=0, xmin=0, xmax=1, color='k')
    sub2.plot(date, oriflux, 'b-', label='original')
    sub2.plot(date, storflux, 'r-', label='storage')
    sub2.plot(date, newflux, 'g-', label='new')
    plt.legend(loc='best')

    sub1.set_xlim(date[0],date[-1])
    sub1.xaxis.set_major_locator(majticks)
    sub1.xaxis.set_major_formatter(mpl.dates.DateFormatter(format_str))
    sub2.set_xlim(date[0],date[-1])
    sub2.xaxis.set_major_locator(majticks)
    sub2.xaxis.set_major_formatter(mpl.dates.DateFormatter(format_str))
    fig1.autofmt_xdate()

    plt.show()
    fig1.savefig(pp1, format='pdf')
    pp1.close()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
