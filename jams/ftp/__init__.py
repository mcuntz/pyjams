#!/usr/bin/env python
"""
    Functions for interacting with an open FTP connection.


    Provided functions
    ------------------
    get_binary                  - Get a binary file from an ftp connection
    get_check_binary            - Get a binary file from an ftp connection
                                  True if all bytes transfered
                                  False if local bytes differ after transfer
    get_unix_ascii              - Get a Unix/Linux ascii file from an ftp connection
    get_check_unix_ascii        - Get a Unix/Linux ascii file from an ftp connection
                                  True if all bytes transfered
                                  False if local bytes differ after transfer
    get_windows_ascii           - Get a Windows ascii file from an ftp connection
    get_check_windows_ascii     - Get a Windows ascii file from an ftp connection
                                  True if all bytes transfered
                                  False if local bytes differ after transfer
    get_names                   - Get file names in current directory on ftp connection
    get_names_dates             - Get file names and dates in current directory on ftp connection
    get_names_sizes             - Get file names and sizes in current directory on ftp connection
    get_names_times             - Wrapper for get_names_dates
    get_names_dates_sizes       - Get file names, dates and sizes in current directory on ftp connection
    get_names_times_sizes       - Wrapper for get_names_dates_sizes
    get_size                    - Get the size of a file on an ftp connection
    get_sizes                   - Get file sizes in current directory on ftp connection
    set_mtime(ftp, fname)       - Set access and modification time of local file from date information on ftp connection
    put_binary                  - Put a binary file to an ftp connection
    put_check_binary            - Put a binary file to an ftp connection
                                  True if all bytes transfered
                                  False if remote bytes differ after transfer


    Example
    -------
    # Transfer files from FTP connection if they are larger than existing local files
    import ftplib
    import os
    # open ftp connection
    ftp = ftplib.FTP("ftp.server.de")
    ftp.login("user", "password")
    fisdir = ftp.pwd()
    # go to directory
    ftp.cwd(choose/directory)
    # get all dat files with filesizes
    flsdat, flsdatsize = get_names_sizes(ftp, '*.dat')
    # if you want to get more than one file ending, e.g. .zip and .tar.gz
    fls, flssize = get_names_sizes(ftp)
    flszip     = [ i for i in fls if i.endswith('.zip') ]
    flszipsize = [ flssize[ii] for ii, i in enumerate(fls) if i.endswith('.zip') ]
    flstar     = [ i for i in fls if i.endswith('.tar.gz') ]
    flstarsize = [ flssize[ii] for ii, i in enumerate(fls) if i.endswith('.tar.gz') ]
    # local dat file names and sizes
    llsdat     = os.listdir('*.dat')
    llsdatsize = [ int(os.stat(n).st_size) for n in llsdat ]
    ldict = dict(zip(llsdat, llsdatsize))
    fdict = dict(zip(flsdat, fldatsize))
    def local_lt_ftp(name, local_dict, ftp_dict):
        if name not in local_dict:
            return True
        else:
            if local_dict[name] < ftp_dict[name]:
                return True
            else:
                return False
    for i in flsdat:
        if local_lt_ftp(i, ldict, fdict):
            if not get_check_binary(ftp, i):
                if not get_check_binary(ftp, i):
                    print('Transfer of ', i, ' failed twice.')
                    if os.path.exists(i):
                        os.remove(i)
    ftp.quit()


    License
    -------
    This file is part of the JAMS Python package.

    The JAMS Python package is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The JAMS Python package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with the JAMS Python package (cf. gpl.txt and lgpl.txt).
    If not, see <http://www.gnu.org/licenses/>.

    Copyright 2014-2016 Matthias Cuntz


    History
    -------
    Written,  MC, Jun-Dec 2014
    Modified, MC, Jan 2016
"""
from .ftp import *

# Information
__author__   = "Matthias Cuntz"
__version__  = '1.1'
__revision__ = "Revision: 2468"
__date__     = 'Date: 06.01.2016'
