#!/usr/bin/env python
import numpy as np
from pyjams.jams.date2dec import date2dec


def fluxplot(infile, outfile, numheader=1, lineofvar=1, novalue=-9999,
             delimiter=',', format='ascii', format_str='%d-%m-%Y %H:%M',
             units=False, plot=False):
    '''
    Plotting routine for Eddy Covariance data generated by EddyFlux (and
    basically any other ascii data file) with first column containing time steps
    in either 'asci' or 'eng' time format. Loads the file and plots each column
    in a separate page of a pdf file. Missing values are plotted in red.


    Definition
    ----------
    fluxplot(infile, outfile, numheader=1, lineofvar=1, novalue=-9999,
             format='ascii', format_str_x='%d-%m-%Y %H:%M', units=False,
             plot=False):


    Input
    -----
    infile      str, path and name of the input file
    outfile     str, path and name of the output pdf


    Optional Input
    --------------
    numhead     int, number of header lines in the input files (default: 1)
    lineofvar   int, line in input file containing variable names (default: 1)
    novalue     int/float, missing value in input file (default: -9999)
    delimiter   str, delimiter of the input file
    format      str, format of time stamps in input files. 'ascii' or 'eng' is
                possible (default: 'ascii')
    format_str  str, format string for plot date formatting
                (default: '%d-%m-%Y %H:%M')
    units       bool, if True, all units of a standard EddyFlux output file
                are added to each plot. Needs to be set False if other files
                are plotted (default: False)
    plot        bool, only if True, the plot is performed (default: False)


    Output
    ------
    outfile     pdf with each page containing a plot of one column of the input
                file


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
    Written,  AP, Aug 2014
    '''

    if plot:
        import matplotlib
        matplotlib.use('PDF')
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        from matplotlib.backends.backend_pdf import PdfPages
        from matplotlib import rcParams
    else:
        raise ValueError('fluxplot: plot must be True')

    ############################################################################
    # set parameters for matplotlib
    rcParams['ps.papersize']        = 'a4'
    rcParams['savefig.orientation'] = 'landscape'
    rcParams['lines.linewidth']     = 0.75
    rcParams['axes.linewidth']      = 1
    rcParams['axes.titlesize']      = 12
    rcParams['axes.labelsize']      = 8
    rcParams['xtick.labelsize']     = 8
    rcParams['ytick.labelsize']     = 8
    rcParams['legend.fontsize']     = 8
    rcParams['path.simplify']       = False

    ############################################################################
    # reading input file
    d       = np.loadtxt(infile, dtype='|S100', delimiter=delimiter)
    header  = d[lineofvar-1,1:]
    date    = d[numheader:,0]
    value   = d[numheader:,1:]
    value[value==''] = str(novalue)
    value   = value.astype(np.float)
    missing = np.where(value == novalue, 0, np.NaN)
    value   = np.where(value == novalue, np.NaN, value)
    length  = len(date)
    if units:
        units = ['W m-2', 'W m-2', 'mmol m-2 s-1', 'mumol m-2 s-1', 'm s-1',
                 'kg m-1 s-2', 'm2 s-2', 'm2 s-2', 'm2 s-2', 'K2', 'mmol2 m-6',
                 'mmol2 m-6', 'm s-1', 'm s-1', 'm s-1', ' deg C', 'mmol m-3',
                 'mmol m-3', 'm s-1', 'deg', 'deg', 'deg', 'deg', 'samples',
                 'samples', 'm', '-', 'deg C', 'W m-2', 'W m-2', 'mmol m-2 s-1',
                 'mumol m-2 s-1', 'm', 'm', 'm', '-', '-', '-', '-', '-', '-',
                 'm2 s-2', 'm2 s-2', 'm2 s-2', '-', 'samples', 'samples',
                 'samples', 'samples', 'samples', 'samples', 'samples',
                 'samples', 'samples', 'samples', 'samples', 'samples',
                 'samples', 'hPa', 'deg C', '%', 'hPa', 'kg m-3', 'samples',
                 'samples', 'm', 'm']
    else:
        units = ['']*length
    ############################################################################
    # convert input date in JD and array format
    date01 = date2dec(yr=1, mo=1, dy=2, hr=0, mi=0, sc=0)
    if format=='ascii':
        jdarr = date2dec(ascii=date) - date01
    elif format=='eng':
        jdarr = date2dec(eng=date) - date01
    else:
        raise ValueError('fluxplot: format unknown')

    ############################################################################
    # plot
    majticks = matplotlib.dates.MonthLocator(bymonthday=1)
    pdf_pages = PdfPages(outfile)

    ############################################################################
    for i in xrange(len(header)):#len(header)

        fig = plt.figure(i)
        ax = fig.add_subplot(111)
        ax.plot(jdarr, value[:,i], 'b-')
        ylim = ax.get_ylim()
        if (ylim[0] < 0) and (ylim[1] > 0):
            ax.axhline(y=0, linewidth=0.75, color='k')
            ax.plot(jdarr, missing[:,i], 'r-', lw=2)
        else:
            ax.plot(jdarr, np.where(missing[:,i] == 0, ylim[0], np.NaN), 'r-', lw=2)

        ax.set_xlabel('Date [DD-MM-YYYY]')
        ylabel = '%s \n %s' %(header[i], units[i])
        ax.set_ylabel(ylabel)

        ax.set_xlim(jdarr[0],jdarr[-1])
        ax.xaxis.set_major_locator(majticks)
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(format_str))
        fig.autofmt_xdate()

        pdf_pages.savefig(fig)
        plt.close()
    pdf_pages.close()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
