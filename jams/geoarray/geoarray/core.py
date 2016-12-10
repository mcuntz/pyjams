#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author
------
David Schaefer

Purpose
-------
This module provides a numpy.ma.MaskedArray as a wrapper around gdal raster functionality 

"""

import os
import warnings
import copy
import numpy as np
from numpy.ma import MaskedArray
from math import floor, ceil
from gdalfuncs import _toFile, _Projection, _Transformer, _warp, _warpTo

# to avoid rounding errors when dealing with coordinates
MAXPRECISION = 10

# Possible positions of the grid origin
ORIGINS = (
    "ul",    #     "ul" -> upper left
    "ur",    #     "ur" -> upper right
    "ll",    #     "ll" -> lower left
    "lr",    #     "lr" -> lower right
)

_METHODS = (
    "__add__",
)

def _checkProjection(func):
    def inner(*args):
        tmp = set()
        for a in args:
            try:
                tmp.add(a.proj)
            except AttributeError:
                pass
        if len(tmp) > 1:
            warnings.warn("Incompatible map projections!", RuntimeWarning)
        return func(*args)
    return inner
   
def _basicMatch(self, grid):
    """
    Arguments
    ---------
    grid : GeoArray

    Returns
    -------
    bool

    Purpose
    -------
    Check if two grids are broadcastable.
    """
    
    return (
        (self.proj == grid.proj) and
        (self.getOrigin() == grid.getOrigin(self.origin)) and
        (self.cellsize == grid.cellsize)
    )

def _dtypeInfo(dtype):
    try:
        tinfo = np.finfo(dtype)
    except ValueError:
        tinfo = np.iinfo(dtype)

    return {"min": tinfo.min, "max": tinfo.max}

def _broadcastTo(array, shape, dims):
    """
    array, shape: see numpy.broadcast_to
    dims: tuple, the dimensions the array dimensions should end up in the output array
    """
    assert len(array.shape) == len(dims)
    assert len(set(dims)) == len(dims) # no duplicates
    # handle negative indices
    dims = [d if d >= 0 else d+len(shape) for d in dims]
    # bring array to the desired dimensionality
    slc = [slice(None, None, None) if i in dims else None for i in range(len(shape))]
    return np.broadcast_to(array[slc], shape)


class GeoArrayMeta(object):
    def __new__(cls, name, bases, attrs):
        for key in _METHODS:
            attrs[key] = _checkProjection(getattr(MaskedArray, key))
        return type(name, bases, attrs)

class GeoArray(MaskedArray):
    """
    Arguments
    ----------
    data         : np.ndarray/list/tuple
    yorigin      : scalar                # y-coordinate of origin
    xorigin      : scalar                # x-coordinate of origin
    origin       : {"ul","ur","ll","lr"} # position of the grid origin
    fill_value   : scalar
    cellsize     : (scalar, scalar)
    fobj         : return object from gdal.Open or None
    proj         : _Projection           # Projection Instance holding projection information
    mode         : string
    
    Purpose
    -------
    This numpy.ndarray subclass adds geographic context to data.
    A (hopfully growing) number of operations on the data I/O to/from
    different file formats (see the variable gdalfuncs._DRIVER_DICT) is supported.

    Restrictions
    ------------
    Adding the geographic information to the data does (at the moment) not imply
    any additional logic. If the shapes of two grids allow the succesful execution
    of a certain operator/function your program will continue. It is within the responsability
    of the user to check whether a given operation makes sense within a geographic context
    (e.g. grids cover the same spatial domain, share a common projection, etc.) or not.
    Overriding the operators could fix this.
    """

    # __metaclass__ = GeoArrayMeta
    
    def __new__(
            cls, data, yorigin, xorigin, origin, cellsize,
            proj=None, fill_value=None, fobj=None, mode=None, # mask=None,
            *args, **kwargs
    ):
        # if mask is None:
        # The mask will always be calculated, even if its already present or not needed at all...
        mask = np.zeros_like(data, np.bool) if fill_value is None else data == fill_value
        
        
        if origin not in ORIGINS:
            raise TypeError("Argument 'origin' must be one of '{:}'".format(ORIGINS))
        try:
            # Does this work for grids crossing the equator??
            origin = "".join(
                ("l" if cellsize[0] > 0 else "u",
                 "l" if cellsize[1] > 0 else "r")
            )
        # iterable of len < 2, numeric value
        except (IndexError, TypeError):
            cs = abs(cellsize)
            cellsize = (
                cs if origin[0] == "l" else -cs,
                cs if origin[1] == "l" else -cs
            )
            
        obj = MaskedArray.__new__(cls, data, fill_value=fill_value, mask=mask, *args, **kwargs)

        obj._optinfo["yorigin"]    = yorigin
        obj._optinfo["xorigin"]    = xorigin
        obj._optinfo["origin"]     = origin
        obj._optinfo["cellsize"]   = cellsize
        obj._optinfo["_proj"]      = _Projection(proj)
        obj._optinfo["fill_value"] = fill_value if fill_value is not None else _dtypeInfo(obj.dtype)["min"]
        obj._optinfo["mode"]       = mode
        obj._optinfo["_fobj"]      = fobj
        
        return obj

    @property
    def header(self):
        """
        Arguments
        ---------
        None

        Returns
        -------
        dict

        Purpose
        -------
        Return the basic definition of the grid. Together
        with a numpy.ndarray this information
        can be passed to any of the factory functions.
        """

        return {
            "yorigin"     : self.yorigin,
            "xorigin"     : self.xorigin,
            "origin"      : self.origin,
            "fill_value"  : self.fill_value,
            "cellsize"    : self.cellsize,
            "proj"        : self.proj,
            "mode"        : self.mode,
        }

    @property
    def bbox(self):
        """
        Arguments
        ---------
        None

        Returns
        -------
        dict

        Purpose
        -------
        Return the grid's bounding box.
        """
        
        yvals = (self.yorigin, self.yorigin + self.nrows*self.cellsize[0])
        xvals = (self.xorigin, self.xorigin + self.ncols*self.cellsize[1])

        return {
            "ymin": min(yvals), "ymax": max(yvals),
            "xmin": min(xvals), "xmax": max(xvals),
        }

    @property
    def nbands(self):
        """
        Arguments
        ---------
        None

        Returns
        -------
        int

        Purpose
        -------
        Return the number of bands in the dataset, i.e. the third last element
        in the shape tuple.
        """

        try:
            return self.shape[-3]
        except IndexError:
            return 1

    @property
    def nrows(self):
        """
        Arguments
        ---------
        None

        Returns
        -------
        int

        Purpose
        -------
        Return the number of rows in the dataset, i.e. the second last element
        in the shape tuple.
        """

        try:
            return self.shape[-2]
        except IndexError:
            return 0

    @property
    def ncols(self):
        """
        Arguments
        ---------
        None

        Returns
        -------
        int

        Purpose
        -------
        Return the number of columns in the dataset, i.e. the last element
        in the shape tuple.
        """

        try:
            return self.shape[-1]
        except IndexError:
            return 0

    @property
    def proj(self):
        return self._proj.get()

    @proj.setter
    def proj(self, value):
        self._proj.set(value)
        
    @property
    def fill_value(self):
        return self._optinfo["fill_value"]
        
    @fill_value.setter
    def fill_value(self, value):
        # change fill_value and update mask
        self._optinfo["fill_value"] = value
        self.mask = self == value

    def getOrigin(self, origin=None):
        """
        Arguments
        ---------
        origin : str/None

        Returns
        -------
        (scalar, scalar)

        Purpose
        -------
        Return the grid's corner coordinates. Defaults to the origin
        corner. Any other corner may be specifed with the 'origin' argument,
        which should be one of: 'ul','ur','ll','lr'.
        """

        if not origin:
            origin = self.origin

        bbox = self.bbox
        return (
            bbox["ymax"] if origin[0] == "u" else bbox["ymin"],
            bbox["xmax"] if origin[1] == "r" else bbox["xmin"],
        )

    def coordinatesOf(self, y_idx, x_idx):
        """
        Arguments
        ---------
        y_idx, x_idx :  int

        Returns
        -------
        (scalar, scalar)

        Purpose
        -------
        Return the coordinates of the grid cell definied by the given row and column
        index values. The cell corner to which the returned values belong is definied
        by the attribute origin:
            "ll": lower-left corner
            "lr": lower-right corner
            "ul": upper-left corner
            "ur": upper-right corner
        """

        if (y_idx < 0 or x_idx < 0) or (y_idx >= self.nrows or x_idx >= self.ncols):
            raise ValueError("Index out of bounds !")

        yorigin, xorigin = self.getOrigin("ul")
        return (
            yorigin - y_idx * abs(self.cellsize[0]),
            xorigin + x_idx * abs(self.cellsize[1]),
        )
        
    def indexOf(self, ycoor, xcoor):
        """
        Arguments
        ---------
        ycoor, xcoor : scalar

        Returns
        -------
        (int, int)

        Purpose
        -------
        Find the grid cell into which the given coordinates
        fall and return its row/column index values.
        """

        yorigin, xorigin = self.getOrigin("ul")
        cellsize = np.abs(self.cellsize)
        yidx = int(floor((yorigin - ycoor)/float(cellsize[0])))
        xidx = int(floor((xcoor - xorigin )/float(cellsize[1])))
        
        if yidx < 0 or yidx >= self.nrows or xidx < 0 or xidx >= self.ncols:
            raise ValueError("Given Coordinates not within the grid domain!")

        return yidx, xidx

    def fill(self, fill_value):
        """
        works similar to MaskedArray.filled(value) but also changes the fill_value
        and returns an GeoArray instance
        """
        return GeoArray(
            data       = self.filled(fill_value),
            yorigin    = self.yorigin,
            xorigin    = self.xorigin,
            origin     = self.origin,
            cellsize   = self.cellsize,
            proj       = self.proj,
            fill_value = fill_value,
            mode       = self.mode
        )

    def trim(self):
        """
        Arguments
        ---------
        None

        Returns
        -------
        GeoArray

        Purpose
        -------
        Removes rows and columns from the margins of the
        grid if they contain only fill values.
        """

        try:
            y_idx, x_idx = np.where(self.data != self.fill_value)
            return self.removeCells(
                top  = min(y_idx), bottom = self.nrows-max(y_idx)-1,
                left = min(x_idx), right  = self.ncols-max(x_idx)-1
            )
        except ValueError:
            return self

    def removeCells(self, top=0, left=0, bottom=0, right=0):
        """
        Arguments
        ---------
        top, left, bottom, right : int

        Returns
        -------
        GeoArray

        Purpose
        -------
        Remove the number of given cells from the respective margin of the grid.
        """

        top    = int(max(top,0))
        left   = int(max(left,0))
        bottom = self.nrows - int(max(bottom,0))
        right  = self.ncols - int(max(right,0))

        return self[...,top:bottom,left:right]

    def shrink(self, ymin=None, ymax=None, xmin=None, xmax=None):
        """
        Arguments
        ---------
        ymin, ymax, xmin, xmax : scalar

        Returns
        -------
        GeoArray

        Purpose
        -------
        Shrinks the grid in a way that the given bbox is still within the grid domain.
        """
        bbox = {
            "ymin": ymin if ymin is not None else self.bbox["ymin"],
            "ymax": ymax if ymax is not None else self.bbox["ymax"],
            "xmin": xmin if xmin is not None else self.bbox["xmin"],
            "xmax": xmax if xmax is not None else self.bbox["xmax"],
            }

        cellsize = map(lambda x : float(abs(x)), self.cellsize)
        top    = floor((self.bbox["ymax"] - bbox["ymax"])/cellsize[0])
        left   = floor((bbox["xmin"] - self.bbox["xmin"])/cellsize[1])
        bottom = floor((bbox["ymin"] - self.bbox["ymin"])/cellsize[0])
        right  = floor((self.bbox["xmax"] - bbox["xmax"])/cellsize[1])
        
        return self.removeCells(max(top,0),max(left,0),max(bottom,0),max(right,0))

    def addCells(self, top=0, left=0, bottom=0, right=0):
        """
        Arguments
        ---------
        top, left, bottom, right : int

        Returns
        -------
        GeoArray

        Purpose
        -------
        Add the number of given cells to the respective margin of the grid.
        """
        
        top    = int(max(top,0))
        left   = int(max(left,0))
        bottom = int(max(bottom,0))
        right  = int(max(right,0))

        shape = list(self.shape)
        shape[-2:] = self.nrows + top  + bottom, self.ncols + left + right
        yorigin, xorigin = self.getOrigin("ul")

        out = GeoArray(
            data        = np.full(shape, self.fill_value, self.dtype),
            dtype       = self.dtype,
            yorigin     = yorigin + top*abs(self.cellsize[0]),
            xorigin     = xorigin - left*abs(self.cellsize[1]),
            origin      = "ul",
            fill_value  = self.fill_value,
            cellsize    = (abs(self.cellsize[0])*-1, abs(self.cellsize[1])),
            proj        = self.proj,
            mode        = self.mode,
        )
        
        # the Ellipsis ensures that the function works
        # for arrays with more than two dimensions
        out[..., top:top+self.nrows, left:left+self.ncols] = self
        return out

    def enlarge(self, ymin=None, ymax=None, xmin=None, xmax=None):
        """
        Arguments
        ---------
        ymin, ymax, xmin, xmax : scalar

        Returns
        -------
        None

        Purpose
        -------
        Enlarge the grid in a way that the given coordinates will
        be part of the grid domain. Added rows/cols are filled with
        the grid's fill value.
        """

        bbox = {
            "ymin": ymin if ymin is not None else self.bbox["ymin"],
            "ymax": ymax if ymax is not None else self.bbox["ymax"],
            "xmin": xmin if xmin is not None else self.bbox["xmin"],
            "xmax": xmax if xmax is not None else self.bbox["xmax"],
            }

        cellsize = map(lambda x : float(abs(x)), self.cellsize)

        top    = ceil((bbox["ymax"] - self.bbox["ymax"])/cellsize[0])
        left   = ceil((self.bbox["xmin"] - bbox["xmin"])/cellsize[1])
        bottom = ceil((self.bbox["ymin"] - bbox["ymin"])/cellsize[0])
        right  = ceil((bbox["xmax"] - self.bbox["xmax"])/cellsize[1])
        
        return self.addCells(max(top,0),max(left,0),max(bottom,0),max(right,0))

    # def snap(self,target):
    #     """
    #     Arguments
    #     ---------
    #     target : GeoArray

    #     Returns
    #     -------
    #     None

    #     Purpose
    #     -------
    #     Shift the grid origin that it matches the nearest cell origin in target.

    #     Restrictions
    #     ------------
    #     The shift will only alter the grid coordinates. No changes to the
    #     data will be done. In case of large shifts the physical integrety
    #     of the data might be disturbed!

    #     diff = np.array(self.getOrigin()) - np.array(target.getOrigin(self.origin))
    #     dy, dx = abs(diff)%target.cellsize * np.sign(diff)

    #     if abs(dy) > self.cellsize[0]/2.:
    #         dy += self.cellsize[0]

    #     if abs(dx) > self.cellsize[1]/2.:
    #         dx += self.cellsize[1]

    #     self.xorigin -= dx
    #     self.yorigin -= dy

    def __repr__(self):
        return super(self.__class__, self).__repr__()

    def __str__(self):
        out = super(self.__class__, self).__str__()
        name = self.__class__.__name__
        pad = " "*(len(name)+1)
        return "{:}({:})".format(
            name, os.linesep.join(["{:}{:}".format(pad,l) for l in out.split(os.linesep)]).strip()
        )

    def __getattr__(self, name):
        try:
            return self._optinfo[name]
        except KeyError:
            raise AttributeError(
                "'{:}' object has no attribute {:}".format (self.__class__.__name__, name)
            )

    def __deepcopy__(self, memo):
        return GeoArray(
            data       = self.data.copy(),
            yorigin    = self.yorigin,
            xorigin    = self.xorigin,
            origin     = self.origin,
            cellsize   = self.cellsize,
            proj       = copy.deepcopy(self.proj),
            fill_value = self.fill_value,
            mode       = self.mode,
        )

    @property
    def coordinates(self):
        """
        Returns the coordinates of the instance
        """

        def _arange(start, step, count):
            return tuple(start + step * i for i in xrange(count))

        cellsize = self.cellsize
        yorigin, xorigin = self.getOrigin()
        
        return (
            _arange(yorigin, cellsize[0], self.nrows),
            _arange(xorigin, cellsize[1], self.ncols)
        )

    def __getitem__(self, slc):

        data = super(GeoArray, self).__getitem__(slc)

        # empty array
        if data.size == 0:
            return data

        x, y = np.meshgrid(*self.coordinates[::-1])

        bbox = []
        for arr, idx in zip((y, x), (-2, -1)):
            arr = np.array(
                _broadcastTo(arr, self.shape, (-2, -1))[slc],
                copy=False, ndmin=abs(idx)
            )
            s = [0] * arr.ndim
            s[idx] = slice(None, None, None)
            bbox.append((arr[s][0], arr[s][-1]))

        try:
            # scalar
            ystart, ystop = sorted(bbox[0], reverse=data.origin[0]=="u")
            xstart, xstop = sorted(bbox[1], reverse=data.origin[1]=="r")
        except AttributeError:
            return data

        nrows, ncols = ((1, 1) + data.shape)[-2:]
        cellsize = (
            float(ystop-ystart)/(nrows-1) if nrows > 1 else self.cellsize[-2],
            float(xstop-xstart)/(ncols-1) if ncols > 1 else self.cellsize[-1],
        )

        return GeoArray(
            data       = data.data,
            yorigin    = ystart,
            xorigin    = xstart,
            origin     = self.origin,
            cellsize   = cellsize,
            proj       = self.proj,
            fill_value = self.fill_value,
            mode       = self.mode
        )
        
    def warp(self, proj, max_error=0.125):
        """
        Arguments
        ---------
        proj       : dict   -> proj4 parameters of the target coordinate system
        max_error  : float  -> Maximum error (in pixels) allowed in transformation
                               approximation (default: value of gdalwarp)

        Return
        ------
        GeoArray

        Todo
        ----
        - Make the resampling strategy an optional argument
        """

        target = GeoArray(**_warp(self, proj, max_error))
        return self.warpTo(target, max_error)

    def warpTo(self, target, max_error=0.125):
        """
        Arguments
        ---------
        grid: GeoArray
        
        Return
        ------
        GeoArray
        
        Purpose
        -------
        Interpolates self to the target grid, including
        coordinate transformations if necessary.
        """

        return GeoArray(**_warpTo(self, target, max_error))
 
    tofile = _toFile
    
