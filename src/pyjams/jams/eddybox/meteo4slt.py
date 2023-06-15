#!/usr/bin/env python
import numpy as np
from pyjams.jams.date2dec import date2dec  # jams
from pyjams.jams.dec2date import dec2date  # jams
import os as os
import re as re


def meteo4slt(sltdir, metfile, p_t_rh, outfile,
              pat='[a-zA-Z0-9]*.slt|[a-zA-Z0-9]*.SLT', delimiter=',',
              skiprows=1, format='ascii'):
    """
        To supply EddyFlux (Kolle & Rebmann, 2007) with meteorological
        data, it is necessary to extract for each available *.slt file the
        corresponding air pressure, air temperature and air relative humidity.
        The module looks in sltdir for available *.slt files and uses the metfile
        for syncronisation


        Definition
        ----------
        meteo4slt(sltdir, metfile, p_t_rh, outfile,
              pat='[a-zA-Z0-9]*.slt|[a-zA-Z0-9]*.SLT', delimiter=',',
              skiprows=1, format='ascii'):

        Input
        -----
        sltdir      str, path of the folder containing the *.slt files
        metfile     str, path of the meteo file
        p_t_rh      list, column number of Pressure, T, rH
        outfile     str, path of the output file


        Optional Input
        --------------
        pat         str, regular expression, describing the name pattern of
                    the *.slt files in the indir folder
        delimiter   str, column delimiter of the meteo file (default=',')
        skiprows    int, number of rows to skip at the beginning of the met file
                    e.g. header lines (default=1)
        format      str, time format of the meteo file (default='ascii')


        Output
        ------
        outfile     file, containing Pressure, T and rH values of the meteo
                    file for each *.slt file


        Restrictions
        ------------
        - assumes site name in slt fielname is only one character
          (e.g. W20133652300.slt AND NOT WULF20133652300.slt)
        - currently only supports format='ascii', nice would be 'eng'
        - does not work for data containning multiple years because of ugly
          doy calculation
        - works only for half hourly *.stl and half hourly meteo data


        License
        -------
        This file is part of the JAMS Python package, distributed under the MIT
        License. The JAMS Python package originates from the former UFZ Python library,
        Department of Computational Hydrosystems, Helmholtz Centre for Environmental
        Research - UFZ, Leipzig, Germany.

        Copyright (c) 2014 Arndt Piayda, Matthias Cuntz - mc (at) macu (dot) de

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
        Written,  AP, Jul 2014
        Modified, MC, Aug 2014 - clean up and Python 3
    """

    # half hour in jd
    halfhjd = 1800./86400.

    ###########################################################################
    # reading slt directory
    dirlist = os.listdir(sltdir)
    sltdates = np.array([])

    ###########################################################################
    # remove all files and folders from list which are not *.slt files and get size
    pat = re.compile(pat)
    for item in dirlist:
        if re.search(pat, item):
            sltdates = np.append(sltdates, item[1:-4])

    # replace time steps which dont fit in half hour interval
    mi = np.array([x[-2:] for x in sltdates])
    mi = np.where(mi.astype(int)<30, '00', '30')
    sltdates = np.array([sltdates[i][:-2]+mi[i] for i in range(mi.size)])

    ###########################################################################
    # load meteo data
    metdata = np.loadtxt(metfile, dtype='|S100', delimiter=delimiter,
                         skiprows=skiprows, usecols=[0]+p_t_rh)

    # get the metdate
    if format == 'ascii':
        # shift met dates one half hour back since slt time stamp marks half
        # hour start but meteo date mark half hour end
        jd = date2dec(ascii=metdata[:,0]) - halfhjd
        fulldate = dec2date(jd, fulldate=True)
        adate    = dec2date(jd, ascii=True)
        doy  = np.ceil(date2dec(ascii=adate)-
                       date2dec(yr=fulldate[0][0],
                                mo=1,dy=1,hr=0,mi=0, sc=0)).astype(int)
        doy = np.where((fulldate[3]==0) & (fulldate[4]==0), doy+1, doy)
        metdates = np.array(['%04i%03i%02i%02i'%(fulldate[0][i], doy[i],
                                                fulldate[3][i], fulldate[4][i])
                             for i in range(jd.size)])
    elif format == 'eng':
        # shift met dates one half hour back since slt time stamp marks half
        # hour start but meteo date mark half hour end
        jd = date2dec(eng=metdata[:,0]) - halfhjd
        fulldate = dec2date(jd, fulldate=True)
        adate    = dec2date(jd, ascii=True)
        doibegin = np.array([date2dec(yr=x, mo=1,dy=1,hr=0,mi=0, sc=0) for x in fulldate[0]])
        doy = np.ceil(date2dec(ascii=adate)-doibegin).astype(int)
        doy = np.where((fulldate[3]==0) & (fulldate[4]==0), doy+1, doy)
        metdates = np.array(['%04i%03i%02i%02i'%(fulldate[0][i], doy[i],
                                                fulldate[3][i], fulldate[4][i])
                             for i in range(jd.size)])
    else:
        raise ValueError('meteo4slt: unknown format!')

    ###########################################################################
    # sync both dates
    mask = np.in1d(metdates, sltdates)

    ###########################################################################
    # write output
    np.savetxt(outfile, metdata[mask,1:], '%s', ',')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
