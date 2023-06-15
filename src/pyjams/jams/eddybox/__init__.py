#!/usr/bin/env python
'''
    JAMS Eddy Covariance utilities

    Get help on each function by typing
    >>> help()
    help> eddybox.function
    Or
    >>> from jams import eddybox
    >>> help(eddybox.function)


    Provided functions (alphabetic w/o obsolete)
    ------------------
    eddycorr               Calculate time lags between wind and concentrations for EddyFlux.
    eddyspec               Performs spectrum analysis with EddySpec and SpecMean and determines inductances.
    energyclosure          Computes energy closure and correction for Eddy covaraince data
    fluxfill               Wrapper function for gapfill with file management and plotting.
    fluxflag               Quality flag calculation for Eddy Covariance data
    fluxpart               Wrapper function for nee2gpp including file management and plotting
    fluxplot               Plotting routine for Eddy Covariance or other ascii data file
    gapfill                Gapfill Eddy flux data.
    itc                    Calculation of integral turbulence characteristics after Thomas & Foken (2002)
    meteo4slt              EddyFlux supply with meteorological data.
    nee2gpp                Photosynthesis and ecosystem respiration from NEE Eddy flux data.
    nee2gpp_falge          nee2gpp using one fit for whole time period
    nee2gpp_lasslop        nee2gpp using the daytime method of Lasslop et al. (2010)
    nee2gpp_reichstein     nee2gpp using several fits as in Reichstein et al. (2005)
    planarfit              Planar fit of Eddy Covariance wind components
    profile2storage        Calculate storage fluxes from profile data to correct eddy data
    sltclean               Moves *.slt files in a deleted folder to exclude from processing (EddySoft files).
    spikeflag              Spike detection for Eddy Covariance data (and basically all other data)
    ustarflag              Friction velocity flagging for Eddy Covariance data


    Example
    -------
    see eddysuite.py


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
    Written  AP, Sep 2014
'''
from .eddycorr          import eddycorr
from .eddyspec          import eddyspec
from .energyclosure     import energyclosure
from .fluxfill          import fluxfill
from .fluxflag          import fluxflag
from .fluxpart          import fluxpart
from .fluxplot          import fluxplot
from .gapfill           import gapfill
from .itc               import itc
from .meteo4slt         import meteo4slt
from .nee2gpp           import nee2gpp, nee2gpp_falge, nee2gpp_lasslop, nee2gpp_reichstein
from .planarfit         import planarfit
from .profile2storage   import profile2storage
from .sltclean          import sltclean
from .spikeflag         import spikeflag
from .ustarflag         import ustarflag

# Information
__author__   = "Arndt Piayda, Matthias Cuntz"
__version__  = '1.0'
__revision__ = "$Revision: 1796$"
__date__     = '$Date: 30.09.2014$'
