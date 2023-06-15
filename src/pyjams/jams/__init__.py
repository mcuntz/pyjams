#!/usr/bin/env python
"""
JAMS Python Utilities

Package offers miscellaneous functions and sub-modules in different categories.

Get help on each function by typing
>>> import pyjams
>>> help(pyjams.jams.function)

Subpackages
===========
.. autosummary::
   encrypt
   qa
   apply_undef
   area_poly
   around
   autostring
   baseflow
   climate_index_knoben
   clockplot
   convex_hull
   correlate
   cuntz_gleixner
   date2dec
   dec2date
   delta_isogsm2
   dewpoint
   dielectric_water
   ellipse_area
   errormeasures
   fftngo
   fill_nonfinite
   find_in_path
   fwrite
   gap2lai
   get_angle
   get_era5
   get_isogsm2
   get_nearest
   grid_mid2edge
   head
   heaviside
   homo_sampling
   in_poly
   interpol
   intersection
   jab
   jconfigparser
   kriging
   lagcorr
   latlon_fmt
   lhs
   lif
   line_dev_mask
   lowess
   maskgroup
   mat2nc
   netcdf4
   outlier
   pareto_metrics
   pawn_index
   pca
   pet_oudin
   pi
   pritay
   pso
   readhdf
   readhdf5
   river_network
   rolling
   saltelli
   samevalue
   sap_app
   savitzky_golay
   semivariogram
   sendmail
   sigma_filter
   smooth_minmax
   sobol_index
   srrasa
   tail
   tcherkez
   timestepcheck
   tsym
   volume_poly
   writenetcdf
   xkcd
   yrange
   zacharias
   distributions
   eddybox
   files
   ftp
   leafmodel
   level1

Provided functions and modules (alphabetic)
-------------------------------------------
apply_undef            Use a function on masked arguments.
area_poly              Area of a polygon.
around                 Round to the passed power of ten.
astr                   Wrapper for autostring.
autostring             Format number (array) with given decimal precision.
baseflow               Calculate baseflow from discharge timeseries
climate_index_knoben   Determines continuous climate indexes based on Knoben et al. (2018).
clockplot              The clockplot of mHM.
convex_hull            Calculate subset of points that make a convex hull around a set of 2D points.
correlate              Computes the cross-correlation function of two series x and y.
cuntz_gleixner         Cuntz-Gleixner model of 13C discrimination.
dielectric_water       Dielectric constant of liquid water.
delta_isogsm2          Calculate delta values from downloaded IsoGSM2 data.
dewpoint               Calculates the dew point from ambient humidity.
dfgui                  A minimalistic GUI for analyzing Pandas DataFrames based on wxPython.
distributions          Module for pdfs of additional distributions.
dumpnetcdf             Convenience function for writenetcdf
eddybox                Module containing Eddy Covaraince utilities, see eddysuite.py for details
eddysuite              Example file for processing Eddy data with eddybox and EddySoft
ellipse_area           Area of ellipse (or circle)
encrypt                Module to encrypt and decrypt text using a key system as well as a cipher.
errormeasures          Definition of different error measures.
fftngo                 Fast fourier transformation for dummies (like me)
files                  Module with file list function.
fill_nonfinite         Fill missing values by interpolation.
find_in_path           Look for file in system path.
ftp                    Module with functions for interacting with an open FTP connection.
fwrite                 Writes an array to ascii file
gap2lai                Calculation of leaf area index from gap probability observations.
get_angle              Returns the angle in radiant from each point in xy1 to each point in xy2.
get_era5               Download ERA5 data suitable to produce MuSICA input data.
get_isogsm2            Get IsoGSM2 output.
get_nearest            Returns a value z for each point in xy near to the xyz field.
grid_mid2edge          Longitude and latitude grid edges from grid midpoints.
hdfread                Wrapper for readhdf.
hdf5read               Wrapper for readhdf5.
head                   Return list with first n lines of file.
heaviside              Heaviside (or unit step) operator.
homo_sampling          Generation of homogeneous, randomly distributed points in a given rectangular area.
in_poly                Determines whether a 2D point falls in a polygon.
inpoly                 Wrapper for in_poly.
interpol               One-dimensional linear interpolation on first dimension.
intersection           Intersection of two curves from x,y coordinates.
jab                    Jackknife-after-Bootstrap error.
jConfigParser          Extended Python ConfigParser.
kriging                Krig a surface from a set of 2D points.
lagcorr                Calculate time lag of maximum or minimum correlation of two arrays.
lat_fmt                Set lat label string (called by Basemap.drawparallels) if LaTeX package clash.
leafmodel              Model to compute photosynthesis and stomatal conductance of canopies.
leafprojection         Calculation of leaf projection from leaf angle observations.
level1                 Module with functions dealing with CHS level1 data files, data and flags.
lhs                    Latin Hypercube Sampling of any distribution without correlations.
lif                    Count number of lines in file.
line_dev_mask          Maskes elements of an array deviating from a line fit.
lon_fmt                Set lon label string (called by Basemap.drawmeridians) if LaTeX package clash.
lowess                 Locally linear regression in n dimensions.
mat2nc                 Converts Matlab file *.mat into NetCDF *.nc.
netcdf4                Convenience layer around netCDF4
outlier                Rossner''s extreme standardized deviate outlier test.
pareto_metrics         Performance metrics to compare Pareto fronts.
pca                    Principal component analysis (PCA) upon the first dimension of an 2D-array.
pet_oudin              Daily potential evapotranspiration following the Oudin formula.
pi                     Parameter importance index PI or alternatively B index calculation.
pritay                 Daily reference evapotranspiration after Priestley & Taylor.
pso                    Particle swarm optimization
qa                     Module of quality (error) measures.
readhdf                Reads variables or information from hdf4 and hdf5 files.
readhdf5               Reads variables or information from hdf5 file.
river_network          a class for creating a river network from a DEM including flow direction, flow accumulation and channel order
rolling                Reshape an array in a "rolling window" style.
rossner                Wrapper for outlier.
t2sap                  Conversion of temperature difference to sap flux density.
savitzky_golay         Smooth (and optionally differentiate) 1D data with a Savitzky-Golay filter.
savitzky_golay2d       Smooth (and optionally differentiate) 2D data with a Savitzky-Golay filter.
saltelli               Parameter sampling for Sobol indices calculation.
semivariogram          Calculates semivariogram from spatial data.
sendmail               Send an e-mail.
sg                     Wrapper savitzky_golay.
sg2d                   Wrapper savitzky_golay2d.
sigma_filter           Mask values deviating more than z standard deviations from a given function.
tail                   Return list with last n lines of file.
maskgroup              Masks elements in a 1d array gathered in small groups.
samevalue              Checks if abs. differences of array values within a certain window are smaller than threshold.
smax                   Calculating smooth maximum of two numbers
smin                   Calculating smooth minimum of two numbers
sobol_index            Calculates the first-order and total variance-based sensitivity indices.
srrasa                 Generates stratified random 2D points within a given rectangular area.
srrasa_trans           Generates stratified random 2D transects within a given rectangular area.
tcherkez               Calculates the Tcherkez model of 13C-discrimiantion in the Calvin cycle.
timestepcheck          Fills missing time steps in ascii data files
tsym                   Raw unicodes for common symbols.
volume_poly            Volume of function above a polygon
writenetcdf            Write netCDF4 file.
xkcd                   Make plot look handdrawn.
yrange                 Calculates plot range from input array.
zacharias              Soil water content with van Genuchten and Zacharias et al. (2007).
zacharias_check        Checks validity of parameter set for Zacharias et al. (2007).


Provided functions and modules per category
-------------------------------------------
    Array manipulation
    Ascii files
    Data processing
    Grids / Polygons
    Hydrology
    Isotopes
    Math
    Meteorology
    Miscellaneous
    Models
    Plotting
    Special files
-------------------------------------------

Array manipulation
------------------
samevalue              Checks if abs. differences of array values within a certain window are smaller than threshold.
maskgroup              Masks elements in a 1d array gathered in small groups.
rolling                Reshape an array in a "rolling window" style.
smax                   Calculating smooth maximum of two numbers
smin                   Calculating smooth minimum of two numbers


Ascii files
-----------
fwrite                 Writes an array to ascii file
head                   Return list with first n lines of file.
lif                    Count number of lines in file.
tail                   Return list with last n lines of file.


Data processing
---------------
convex_hull            Calculate subset of points that make a convex hull around a set of 2D points.
eddybox                Module containing Eddy Covaraince utilities, see eddybox folder for details
eddysuite              Example file for processing Eddy data with eddybox and EddySoft
fill_nonfinite         Fill missing values by interpolation.
gap2lai                Calculation of leaf projection and leaf area index from gap probability observations.
interpol               One-dimensional linear interpolation on first dimension.
kriging                Krig a surface from a set of 2D points.
leafprojection         Calculation of leaf projection from leaf angle observations.
level1                 Module with functions dealing with CHS level1 data files, data and flags.
line_dev_mask          Mask elements of an array deviating from a line fit.
lowess                 Locally linear regression in n dimensions.
outlier                Rossner''s extreme standardized deviate outlier test.
pca                    Principal component analysis (PCA) upon the first dimension of an 2D-array.
rossner                Wrapper for outlier.
t2sap                  Conversion of temperature difference to sap flux density.
savitzky_golay         Smooth (and optionally differentiate) 1D data with a Savitzky-Golay filter.
savitzky_golay2d       Smooth (and optionally differentiate) 2D data with a Savitzky-Golay filter.
semivariogram          Calculates semivariogram from spatial data.
sg                     Wrapper savitzky_golay.
sg2d                   Wrapper savitzky_golay2d.
sigma_filter           Mask values deviating more than z standard deviations from a given function.
srrasa                 Generates stratified random 2D points within a given rectangular area.
srrasa_trans           Generates stratified random 2D transects within a given rectangular area.
timestepcheck          Fills missing time steps in ascii data files


Grids / Polygons
----------------
area_poly              Area of a polygon
grid_mid2edge          Longitude and latitude grid edges from grid midpoints.
homo_sampling          Generation of homogeneous, randomly distributed points in a given rectangular area.
in_poly                Determines whether a 2D point falls in a polygon.
inpoly                 Wrapper for in_poly.
volume_poly            Volume of function above a polygon
get_angle              Returns the angle in radiant from each point in xy1 to each point in xy2.
get_nearest            Returns a value z for each point in xy near to the xyz field.


Hydrology
---------
baseflow               Calculate baseflow from discharge timeseries
river_network          a class for creating a river network from a DEM including flow direction, flow accumulation and channel order


Isotopes
--------
cuntz_gleixner         Cuntz-Gleixner model of 13C discrimination.
delta_isogsm2          Calculate delta values from downloaded IsoGSM2 data.
get_isogsm2            Get IsoGSM2 output.
tcherkez               Calculates the Tcherkez model of 13C-discrimiantion in the Calvin cycle.


Math
----
around                 Round to the passed power of ten.
correlate              Computes the cross-correlation function of two series x and y.
distributions          Module for pdfs of additional distributions.
ellipse_area           Area of ellipse (or circle)
errormeasures          Definition of different error measures.
fftngo                 Fast fourier transformation for dummies (like me)
heaviside              Heaviside (or unit step) operator.
intersection           Intersection of two curves from x,y coordinates.
jab                    Jackknife-after-Bootstrap error.
lagcorr                Calculate time lag of maximum or minimum correlation of two arrays.
lhs                    Latin Hypercube Sampling of any distribution without correlations.
pareto_metrics         Performance metrics to compare Pareto fronts.
pi                     Parameter importance index PI or alternatively B index calculation.
pso                    Particle swarm optimization
qa                     Module of quality assessment (error) measures.
saltelli               Parameter sampling for Sobol indices calculation.
sobol                  Generates Sobol sequences
sobol_index            Calculates the first-order and total variance-based sensitivity indices.


Meteorology
-----------
climate_index_knoben   Determines continuous climate indexes based on Knoben et al. (2018).
dewpoint               Calculates the dew point from ambient humidity.
dielectric_water       Dielectric constant of liquid water.
get_era5               Download ERA5 data suitable to produce MuSICA input data.
pet_oudin              Daily potential evapotranspiration following the Oudin formula.
pritay                 Daily reference evapotranspiration after Priestley & Taylor


Miscellaneous
-------------
apply_undef            Use a function on masked arguments.
astr                   Wrapper for autostring.
autostring             Format number (array) with given decimal precision.
encrypt                Module to encrypt and decrypt text using a key system as well as a cipher.
files                  Module with file list function.
find_in_path           Look for file in system path.
ftp                    Module with functions for interacting with an open FTP connection.
sendmail               Send an e-mail.
zacharias              Soil water content with van Genuchten and Zacharias et al. (2007).
zacharias_check        Checks validity of parameter set for Zacharias et al. (2007).


Models
------
leafmodel              Model to compute photosynthesis and stomatal conductance of canopies


Plotting
--------
clockplot              The clockplot of mHM.
dfgui                  A minimalistic GUI for analyzing Pandas DataFrames based on wxPython.
lat_fmt                Set lat label string (called by Basemap.drawparallels) if LaTeX package clash.
lon_fmt                Set lon label string (called by Basemap.drawmeridians) if LaTeX package clash.
tsym                   Raw unicodes for common symbols.
xkcd                   Make plot look handdrawn.
yrange                 Calculates plot range from input array.


Special files
-------------
dumpnetcdf             Convenience function for writenetcdf
hdfread                Wrapper for readhdf.
hdf5read               Wrapper for readhdf5.
jConfigParser          Extended Python ConfigParser.
mat2nc                 Converts Matlab file *.mat into NetCDF *.nc.
netcdf4                Convenience layer around netCDF4
readhdf                Reads variables or information from hdf4 and hdf5 files.
readhdf5               Reads variables or information from hdf5 file.
writenetcdf            Write netCDF4 file.


History
-------
Written,  Matthias Cuntz, Jul 2009
Modified, Matthias Cuntz, Jul 2009
              - lif, fread, sread, readnetcdf, cellarea, pack, unpack
          Matthias Cuntz, Aug 2009 - position
          Maren Goehler, Jul 2010  - outlier
          Arndt Piayda, Jan 2011   - date2dec, dec2date
          Arndt Piayda, Feb 2011   - semivariogram
          Tino Rau, May 2011       - gap_filling
          Tino Rau, May 2011       - calcvpd
          Matthias Cuntz, Jun 2011
              - /usr/bin/python to /usr/bin/env python
              - tsym, around
          Matthias Cuntz, Nov 2011 - mad
          Matthias Cuntz, Nov 2011 - try netcdf and stats routines
          Matthias Cuntz, Nov 2011 - autostring
          Matthias Cuntz, Jan 2012
              - esat, closest, dewpoint, division, heaviside, tcherkez, yrange,
              - const, cuntz_gleixner
              - calcvpd obsolete
          Matthias Cuntz, Mar 2012 - gapfill, nee2gpp
          Matthias Cuntz, May 2012
              - astr, div, sobol_index, pi, roman, zacharias, saltelli
          Matthias Zink, Jun 2012  - writenetcdf
          Matthias Cuntz, Jun 2012 - roman -> romanliterals, interpol
          Matthias Zink, Jun 2012  - readhdf5
          Matthias Cuntz, Jun 2012 - readhdf4, readhdf
          Matthias Cuntz, Sep 2012 - brewer
          Matthias Cuntz, Oct 2012 - savitzky_golay
          Matthias Cuntz, Nov 2012
              - added netcdftime but no import so that available w/o netcdf
          Arndt Piayda, Nov 2012
              - convex_hull, in_poly, kriging, semivariogram update
              - srrasa, srrasa_trans
          Matthias Cuntz, Nov 2012
              - nee2gpp, nee2gpp_falge, nee2gpp_lasslop, nee2gpp_reichstein
          Matthias Cuntz, Dec 2012
              - functions
              - gap_filling obsolete
          Matthias Cuntz, Feb 2013 - area_poly
          Matthias Cuntz & Juliane Mai, Feb 2013 - volume_poly
          Matthias Cuntz, Feb 2013 - ported to Python 3
          Matthias Cuntz, Mar 2013 - find_in_path, xkcd
          Matthias Cuntz, Apr 2013 - rgb
          Matthias Cuntz, Jun 2013 - colours
          Matthias Cuntz, Jul 2013 - fill_nonfinite, means
          Matthias Cuntz, Oct 2013
              - morris, sce, inpoly, rossner, netcdfread, ncread, readnc
              - hdfread, hdf4read, hdf5read
          Arndt Piayda, Feb 2014
              - maskgroup
              - line_dev_mask
          Matthias Cuntz, Feb 2014
              - removed all import *
              - sigma_filter
          Arndt Piayda, Mar 2014   - lagcorr
          Matthias Cuntz, Apr 2014 - correlate
          Matthias Cuntz, May 2014
              - signature2plot
              - adapted new CHS license scheme
          Arndt Piayda, May 2014   - get_nearest
          Arndt Piayda, Jun 2014   - get_angle
          Andreas Wiedemann, Jun 2014 - t2sap
          Arndt Piayda, Jul 2014
              - errormeasures, homo_sampling, sltclean, meteo4slt
              - eddycorr, eddyspec
          Arndt Piayda, Aug 2014
              - planarfit, timestepcheck, fluxplot, itc, spikeflag, ustarflag
              - fluxflag, fluxfill
          Arndt Piayda, Sep 2014   - energyclosure, fluxpart
          Stephan Thober, Sep 2014 - dumpnetcdf
          Matthias Cuntz, Sep 2014 - alpha_equ_h2o, alpha_kin_h2o
          Arndt Piayda, Sep 2014
              - leafmodel
              - profile2storage
              - eddybox -> moved eddycorr, eddyspec, energyclosure,
                                 fluxfill, fluxflag, fluxpart,
                                 fluxplot, gapfill, itc, meteo4slt,
                                 nee2gpp, nee2gpp_falge,
                                 nee2gpp_lasslop, nee2gpp_reichstein,
                                 planarfit, profile2storage,
                                 sltclean, spikeflag, ustarflag
                           into eddybox module
          Arndt Piayda, Sep 2014   - eddysuite
          Matthias Cuntz, Oct 2014
              - ufz module -> ufz package
              - clockplot, ellipse_area, savez, savez_compressed
              - grid_mid2edge, tee
          Matthias Cuntz, Nov 2014 - pca, head
          Arndt Piayda, Nov 2014   - gap2lai, leafprojection
          Matthias Cuntz, Dec 2014
              - directory_from_gui, file_from_gui, files_from_gui
              - logtools,
              - sendmail, argsort, tail
              - ftp
              - file
              - encrypt
          Matthias Cuntz, Feb 2015
              - fsread
              - ascii2ascii, ascii2eng, eng2ascii
          Matthias Cuntz, Mar 2015
              - module level1 with get_flag, set_flag, read_data, write_data
              - rename file to files
              - dielectric_water
              - color
              - redone all __init__.py
          David Schaefer, Sep 2015 - hollickLyneFilter
          Arndt Piayda, Sep 2015   - confidence intervals to errormeasures
          Andreas Wiedemann, Sep 2015 - samevalue
          Matthias Cuntz, Oct 2015 - str2tex, lat_fmt, lon_fmt
          Matthias Cuntz, Oct 2015 - directories_from_gui
          Stephan Thober, Nov 2015 - kge
          Stephan Thober, Dec 2015 - river_network
          Stephan Thober, Feb 2016
              - function for writing 2d arrays to ascii file
          Juliane Mai, Feb 2016    - pareto_metrics
          Stephan Thober, Mar 2016 - smax, smin
          David Schaefer, Mar 2016 - netcdf4
          Matthias Cuntz, May 2016 - qa
          Matthias Cuntz, May 2016 - distributions
          Matthias Cuntz, Oct 2016 - rm colours and rgb from main directory
          Arndt Piayda, Oct 2016   - fftngo
          Juliane Mai, Oct 2016    - mat2nc
          Juliane Mai, Oct 2016    - dag
          Arndt Piayda, Oct 2016   - pritay
          David Schaefer, Oct 2016 - added geoarray
          Matthias Cuntz, Nov 2016 - ported to Python 3
          Matthias Cuntz, Nov 2016 - pso
          Arndt Piayda, Dec 2016   - rolling
          Stephan Thober, Aug 2017 - added fwrite
          Matthias Cuntz, Nov 2017 - xread
          Juliane Mai, Dec 2017    - pawn_index
          Matthias Cuntz, Dec 2017 - screening
          Matthias Cuntz, Jan 2018 - lowess
          Matthias Cuntz, Jan 2018 - apply_undef
          Matthias Cuntz, Mar 2018
              - ascii2en, en2ascii, ascii2fr, fr2ascii, ascii2us, us2ascii
          Matthias Cuntz, Jul 2018 - plot
          Matthias Cuntz, Nov 2018 - intersection, jConfigParser
          Matthias Cuntz, Jan 2019
              - dfgui, delta_isogsm2, get_era5, get_era_interim, get_isogsm2
          Matthias Cuntz, Feb 2019 - xlsread, xlsxread
          Matthias Cuntz, Apr 2019 - nc2nc
          Matthias Cuntz, Jul 2019 - argmax, argmin
          Juliane Mai, Feb 2020    - pet_oudin
          Juliane Mai, Feb 2020    - climate_index_knoben
          Matthias Cuntz, Dec 2020 - mcPlot
          Matthias Cuntz, Oct 2021 - started deprecation
          Matthias Cuntz, Jun 2023
              - moved jams to pyjams
              - cleaning deprecated and unsupported routines

"""
# sub-packages without dependencies to rest of jams
from . import encrypt
from . import qa

# Routines
from .apply_undef          import apply_undef
from .area_poly            import area_poly
from .around               import around
from .autostring           import autostring, astr
from .baseflow             import hollickLyneFilter
from .climate_index_knoben import climate_index_knoben
from .clockplot            import clockplot
from .convex_hull          import convex_hull
from .correlate            import correlate
from .cuntz_gleixner       import cuntz_gleixner
from .date2dec             import date2dec
from .dec2date             import dec2date
from .delta_isogsm2        import delta_isogsm2
from .dewpoint             import dewpoint
try:
    import dfgui
except:
    pass  # PyQT not installed
from .dielectric_water     import dielectric_water
from .ellipse_area         import ellipse_area
from .errormeasures        import bias, mae, mse, rmse, nse, kge, pear2
from .fftngo               import fftngo
from .fill_nonfinite       import fill_nonfinite
from .find_in_path         import find_in_path
from .fwrite               import fwrite
from .gap2lai              import gap2lai, leafprojection
from .get_angle            import get_angle
from .get_era5             import get_era5
try:
    from .get_isogsm2      import get_isogsm2
except                     ImportError:
    pass
from .get_nearest          import get_nearest
from .grid_mid2edge        import grid_mid2edge
from .head                 import head
from .heaviside            import heaviside
from .homo_sampling        import homo_sampling
from .in_poly              import in_poly, inpoly
from .interpol             import interpol
from .intersection         import intersection
from .jab                  import jab
from .jconfigparser        import jConfigParser
from .kriging              import kriging
from .lagcorr              import lagcorr
from .latlon_fmt           import lat_fmt, lon_fmt
from .lhs                  import lhs
from .lif                  import lif
from .line_dev_mask        import line_dev_mask
from .lowess               import lowess
from .maskgroup            import maskgroup
from .mat2nc               import mat2nc
from .netcdf4              import netcdf4
try:
    from .outlier          import outlier, rossner
except:
    pass  # No extra statistics in scipy and hence in JAMS
from .pareto_metrics       import sn, cz, hi, ef, aed, is_dominated, point_to_front
try:
    from .pawn_index       import pawn_index
except:
    pass  # No statsmodels installed.
from .pca                  import pca, check_pca
from .pet_oudin            import pet_oudin
from .pi                   import pi
from .pritay               import pritay
from .pso                  import pso
try:
    from .readhdf          import readhdf, hdfread
except ImportError:
    pass  # HDF5 not installed
from .readhdf5             import readhdf5, hdf5read
from .river_network        import river_network, upscale_fdir
from .rolling              import rolling
from .saltelli             import saltelli
from .samevalue            import samevalue
from .sap_app              import t2sap
from .savitzky_golay       import savitzky_golay, sg, savitzky_golay2d, sg2d
from .semivariogram        import semivariogram
from .sendmail             import sendmail
from .sigma_filter         import sigma_filter
from .smooth_minmax        import smin, smax
from .sobol_index          import sobol_index
from .srrasa               import srrasa, srrasa_trans
from .tail                 import tail
from .tcherkez             import tcherkez
from .timestepcheck        import timestepcheck
from .tsym                 import tsym
from .volume_poly          import volume_poly
from .writenetcdf          import writenetcdf, dumpnetcdf
from .xkcd                 import xkcd
from .yrange               import yrange
from .zacharias            import zacharias, zacharias_check

# sub-packages with dependencies to rest jams have to be loaded separately as in scipy
# ToDo: from here on redo __init__.py
from . import distributions
from . import eddybox
from . import files
from . import ftp
from . import leafmodel
from . import level1


# Information
__author__   = "Matthias Cuntz"
__version__  = 'v23.0'
__date__     = 'Date: 13.06.2023'

# Main
if __name__ == '__main__':
    print('\nJAMS Python Package.')
    print("Version {:s} from {:s}.".format(__version__, __date__))
    print('\nThis is the README file. See als the license file LICENSE.\n\n')
    f = open('README', 'r')
    for line in f:
        print(line, end='')
    f.close()
