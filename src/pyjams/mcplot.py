#!/usr/bin/env python
"""
Standard plotting class of Matthias Cuntz.

It has the same functionality as the old mc_template.py by Matthias Cuntz but
uses the object-oriented approach of st_template.py of Stephan Thober.

It allows plotting on screen, into PDF and PNG files, as well as in HTML
files as a wrapper for PNG images or in D3 format (and plotly currently only
with older Matplotlib versions).

It is optimised for publication ready plots, either on white or black
background.


The simplest way to use mcPlot is to extend the class:

.. code-block:: python

   import numpy as np
   from pyjams import mcPlot

   class PlotIt(mcPlot):
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           # change e.g. colors
           self.lcol1 = 'cyan'
           # reset global values after colour changes, etc.
           self.set_matplotlib_rcparams()

       def read_data(self):
           # do something
           self.dat = np.arange(10)

       def plot_fig_1(self):
           import matplotlib.pyplot as plt

           self.ifig += 1
           fig = plt.figure(self.ifig)

           sub = fig.add_axes([0.125, 0.667, 0.3375, 0.233])

           larr = sub.plot(self.dat)
           plt.setp(larr[-1], linestyle='-', linewidth=self.lwidth,
                    marker='', color=self.lcol1)

           self.plot_save(fig)

       def plot_fig_2(self):
           import matplotlib.pyplot as plt

           self.ifig += 1
           fig = plt.figure(self.ifig)

           sub = fig.add_axes([0.125, 0.667, 0.3375, 0.233])

           larr = sub.plot(2*self.dat)
           plt.setp(larr[-1], linestyle='-', linewidth=self.lwidth,
                    marker='', color=self.lcols[-1])

           self.plot_save(fig)

   if __name__ == '__main__':
       iplot = PlotIt(desc='Test mcPlot',
                      argstr='No argument wanted')
       iplot.read_data()
       iplot.plot_fig_1()
       iplot.plot_fig_2()
       iplot.close()

Then call the script with -h to see the command line options.


This module was written by Matthias Cuntz while at Institut National de
Recherche pour l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy,
France.

:copyright: Copyright 2020-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following classes are provided:

.. autosummary::
   mcPlot

History
    * Written Sep 2020 by Matthias Cuntz (mc (at) macu (dot) de)
    * Write standard output file into current folder, Nov 2021, Matthias Cuntz
    * Change from NCL amwg color palette to pyjams amwg,
      May 2021, Matthias Cuntz
    * Add **kwargs to plot_save, May 2022, Matthias Cuntz
    * Add self.transparent to pdf output in plot_save, May 2022, Matthias Cuntz
    * Add --transparent as a standard option, May 2022, Matthias Cuntz
    * Add left, bottom, top to standard layout options,
      Jul 2022, Matthias Cuntz

"""
import numpy as np


__all__ = ['mcPlot']


# -------------------------------------------------------------------------
# Helper functions
#


def _filebase(f):
    f1 = f
    if f.startswith('..'):
        f1 = f[2:]
    elif f.startswith('.'):
        f1 = f[1:]
    else:
        f1 = f
    if '.' in f1:
        return f[0:f.rfind(".")]
    else:
        return f


# -------------------------------------------------------------------------
# Class mcPlot
#

class mcPlot(object):
    """
    Standard plotting class of Matthias Cuntz

    Upon initialisation,
    the command line arguments are gathered (get_command_line_arguments),
    the output type is set (set_output_type),
    standard layout options are added to self (set_layout_options),
    global rcParams are set for Matplotlib (set_matplotlib_rcparams), and
    the output plotting file is opened (plot_begin).

    Attributes
    ----------
    desc : string, optional
        Description for command line parser, which will be shown when
        called with -h.
    argstr : string, optional
        String given as description for the positional arguments.

    Methods
    -------
    get_command_line_arguments(desc=None, argstr=None)
        Standard command line parser with the default arguments
        such as plot type, filename, etc. If extra arguments are needed,
        one should copy this routine into the extending class and adapt
        it to its needs, keeping the existing optional arguments.
    plot_end() or plot_stop() or plot_close() or end() or stop()
        Finish, closing opened output files.
    plot_save(fig, **kwargs)
        Save, close or show `figure`.
    set_layout_options()
        Sets the colours and styles that can be used in plots.
        One can either copy this routine into the extending class and adapt it,
        or add a new method that resets some of the layout options and call it
        in the initialisation of the extending class, or simply set layout
        options in the initialisation of the extending class.

    Notes
    -----
    Several more methods are defined, which should probably not be changed.

    plot_begin() or plot_start()
        Open output file and similar at the beginning.

    plot_test()
        A simple plot as an example.

    set_matplotlib_rcparams()
        Set rcParams of Matplotlib depending on output type, and chosen layout.
        rcParams can also be re-set in the initialisation of the extending
        class.

    set_output_type()
        Set the format of the output such as pdf or png.

    Examples
    --------
    The simplest way to use `mcPlot` is to extend the class:

    .. code-block:: python

       import numpy as np
       from pyjams import mcPlot

       class PlotIt(mcPlot):
           def __init__(self, *args, **kwargs):
               super().__init__(*args, **kwargs)
               # change e.g. colors
               self.lcol1 = 'cyan'

           def read_data(self):
               # do something
               self.dat = np.arange(10)

           def plot_fig_1(self):
               import matplotlib.pyplot as plt

               self.ifig += 1
               fig = plt.figure(self.ifig)

               sub = fig.add_axes([0.125, 0.667, 0.3375, 0.233])

               larr = sub.plot(self.dat)
               plt.setp(larr[-1], linestyle='-', linewidth=self.lwidth,
                        marker='', color=self.lcol1)

               self.plot_save(fig)

           def plot_fig_2(self):
               import matplotlib.pyplot as plt

               self.ifig += 1
               fig = plt.figure(self.ifig)

               sub = fig.add_axes([0.125, 0.667, 0.3375, 0.233])

               larr = sub.plot(2*self.dat)
               plt.setp(larr[-1], linestyle='-', linewidth=self.lwidth,
                        marker='', color=self.lcols[-1])

               self.plot_save(fig)

       if __name__ == '__main__':
           iplot = PlotIt(desc='Test mcPlot')
           iplot.read_data()
           iplot.plot_fig_1()
           iplot.plot_fig_2()
           iplot.close()

    Then call the script with -h to see the command line options.

    """

    # -------------------------------------------------------------------------
    # init
    #
    def __init__(self, desc=None, argstr=None):
        """
        Initialise the class mcPlot.

        It does the following steps:
            the command line arguments are gathered,
            the output type is set,
            standard layout options are added to self,
            global rcParams are set for Matplotlib, and
            the output plotting file is opened.

        Examples
        --------
        An extending class should initialise with something similar to

        .. code-block:: python
           class UsemcPlot(mcPlot):
               def __init__(self, *args, **kwargs):
                   super().__init__(*args, **kwargs)`

        """
        # get options
        self.get_command_line_arguments(desc=desc, argstr=argstr)
        # pdf, png, ...
        self.set_output_type()
        # nrow, ncol, colours, etc.
        self.set_layout_options()
        # mpl.use and rcParams
        self.set_matplotlib_rcparams()
        # begin plot
        self.plot_begin()

    # -------------------------------------------------------------------------
    # command line arguments
    #
    def get_command_line_arguments(self, desc=None, argstr=None):
        """
        Standard command line parser with default arguments
        such as plot type, filename, etc.

        If extra arguments are needed, one should copy this routine
        into an extending class and adapt it to its needs,
        keeping the existing optional arguments.

        Parameters
        ----------
        desc : string, optional
            Description for command line parser, which will be shown when
            called with -h.
        argstr : string, optional
            String given as description for the positional arguments.

        Notes
        -----
        Standard command line arguments are:

        .. code-block:: bash

           positional arguments:
             args                  Text will be replaced by `argstr`.

           optional arguments:
             -h, --help            show this help message and exit
             -p plotname, --plotname plotname
                                   Name of plot output file for types pdf,
                                   html, d3, or plotly, and name basis for type
                                   png (default: calling_filename without
                                   extension).
             -s, --serif           Use serif font; default sans serif.
             -t outtype, --type outtype
                                   Output type is pdf, png, html, d3, or plotly
                                   (default: open screen windows).
             --transparent         Transparent figure background
                                   (default: black or white).
             -u, --usetex          Use LaTeX to render text in pdf, png and
                                   html.
             -w, --white           White lines on transparent or black
                                   background; default: black lines on
                                   transparent or white background.

        Examples
        --------
        .. code-block:: python

           iplot = mcPlot(desc="Test Matthias' plotting class.",
                          argstr="directory file")

        """
        import argparse
        import os

        if desc is None:
            idesc = "Matthias Cuntz' standard plotting class."
        else:
            idesc = desc
        if argstr is None:
            iargstr = 'Command line arguments.'
        else:
            iargstr = argstr

        plotname = ''
        serif    = False
        outtype  = ''
        transparent = False
        usetex   = False
        dowhite  = False
        parser   = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=idesc)
        default = _filebase(os.path.basename(__file__))
        hstr = (f'Name of plot output file for types pdf, html, d3, or'
                f' plotly, and name basis for type png (default:'
                f' {default}).')
        parser.add_argument('-p', '--plotname', action='store',
                            default=plotname, dest='plotname',
                            metavar='plotname', help=hstr)
        hstr = 'Use serif font; default sans serif.'
        parser.add_argument('-s', '--serif', action='store_true',
                            default=serif, dest='serif', help=hstr)
        hstr = ('Output type is pdf, png, html, d3, or plotly'
                ' (default: open screen windows).')
        parser.add_argument('-t', '--type', action='store', default=outtype,
                            dest='outtype', metavar='outtype', help=hstr)
        hstr = ('Transparent figure background (default: black or white).')
        parser.add_argument('--transparent', action='store_true',
                            default=transparent, dest='transparent', help=hstr)
        hstr = 'Use LaTeX to render text in pdf, png and html.'
        parser.add_argument('-u', '--usetex', action='store_true',
                            default=usetex, dest='usetex', help=hstr)
        hstr = ('White lines on transparent or black background;'
                ' default: black lines on transparent or white background.')
        parser.add_argument('-w', '--white', action='store_true',
                            default=dowhite, dest='dowhite', help=hstr)
        parser.add_argument('cargs', nargs='*', default=None,
                            metavar='args', help=iargstr)

        args = parser.parse_args()

        self.args        = args.cargs
        self.plotname    = args.plotname
        self.serif       = args.serif
        self.outtype     = args.outtype
        self.transparent = args.transparent
        self.usetex      = args.usetex
        self.dowhite     = args.dowhite

        del parser, args

    # -------------------------------------------------------------------------
    # current layout options
    #
    def set_layout_options(self):
        """
        Standard layout options that can be used in plotting methods

        One can either copy this routine into an extending class and adapt it,
        or add a new method that resets some of the layout options and call it
        in the initialisation of an extending class, or simply set layout
        options in the initialisation of an extending class.

        Current layout options are:

        .. list-table::
           :widths: 15 50
           :header-rows: 1

           * - Option
             - Description
           * - self.nrow
             - number of rows of subplots per figure
           * - self.ncol
             - number of columns of subplots per figure
           * - self.left
             - left space on page
           * - self.right
             - right space on page
           * - self.bottom
             - lower bottom space on page
           * - self.top
             - upper top space on page
           * - self.hspace
             - (horizontal) x-space between subplots
           * - self.vspace
             - (vertical) y-space between subplots
           * - self.textsize
             - standard text size
           * - self.dxabc
             - % of (max-min) shift to the right of left y-axis for a,b,c,...
               labels
           * - self.dyabc
             - % of (max-min) shift up from lower x-axis for a,b,c,... labels
           * - self.lwidth
             - line width
           * - self.elwidth
             - errorbar line width
           * - self.alwidth
             - axis line width
           * - self.msize
             - marker size
           * - self.mwidth
             - marker edge width
           * - self.fgcolor
             - foreground colour
           * - self.bgcolor
             - background colour
           * - self.mcols
             - list of marker colours
           * - self.mcol1
             - marker colour 1
           * - self.mcol2
             - marker colour 2
           * - self.mcol3
             - marker colour 3
           * - self.mcol4
             - marker colour 4
           * - self.mcol5
             - marker colour 5
           * - self.lcol1
             - list of line colours
           * - self.lcol2
             - line colour 1
           * - self.lcol3
             - line colour 2
           * - self.lcol4
             - line colour 3
           * - self.lcol5
             - line colour 4
           * - self.lcols
             - line colour 5
           * - self.ldashes
             - list of line styles
           * - self.llxbbox
             - x-anchor legend bounding box
           * - self.llybbox
             - y-anchor legend bounding box
           * - self.llrspace
             - spacing between rows in legend
           * - self.llcspace
             - spacing between columns in legend
           * - self.llhtextpad
             - pad between the legend handle and text
           * - self.llhlength
             - length of the legend handles
           * - self.frameon
             - if True: draw a frame around the legend.
               If None: use rc
           * - self.dpi
             - DPI of non-vector figure output
           * - self.transparent
             - True for transparent background in figure
           * - self.bbox_inches
             - Bbox in inches. If 'tight', try to figure out the tight bbox of the
               figure
           * - self.pad_inches
             - Amount of padding when bbox_inches is 'tight'

        Examples
        --------
        Setting layout options in initialisation

        .. code-block:: python

           class UsemcPlot(mcPlot):
               def __init__(self, *args, **kwargs):
                   super().__init__(*args, **kwargs)
                   self.lcol1     = 'black'
                   self.mynewcol = 'red'
                   # reset global values after colour changes, etc.
                   self.set_matplotlib_rcparams()

        """
        # layout and spaces
        self.nrow     = 3     # # of rows of subplots per figure
        self.ncol     = 2     # # of columns of subplots per figure
        self.left     = 0.125  # left space on page
        self.right    = 0.9   # right space on page
        self.bottom   = 0.1   # lower space on page
        self.top      = 0.9   # upper space on page
        self.hspace   = 0.1   # x-space between subplots
        self.vspace   = 0.1   # y-space between subplots
        self.textsize = 12    # standard text size
        self.dxabc    = 0.90  # % of (max-min) shift to the right
                              # of left y-axis for a,b,c,... labels
        self.dyabc    = 0.05  # % of (max-min) shift up from lower x-axis
                              # for a,b,c,... labels
        # lines, markers and colours
        self.lwidth  = 1.5  # linewidth
        self.elwidth = 1.0  # errorbar line width
        self.alwidth = 1.0  # axis line width
        self.msize   = 1.5  # marker size
        self.mwidth  = 1.0  # marker edge width
        if self.dowhite:
            self.fgcolor = 'white'
            self.bgcolor = 'black'
        else:
            self.fgcolor = 'black'
            self.bgcolor = 'white'
        # pyjams' amwg color map without the first three colours
        # white, black and purple
        amwg = [(0.141, 0.129, 0.408),  # dark blue
                (0.141, 0.357, 0.6),    # medium blue
                (0.365, 0.533, 0.725),  # light blue
                (0.608, 0.8, 0.835),    # cyan
                (0.0, 0.596, 0.639),    # turquoise
                (0.553, 0.725, 0.259),  # light green
                (0.055, 0.518, 0.345),  # dark green
                (0.937, 0.863, 0.714),  # sand
                (0.808, 0.675, 0.51),   # beige
                (0.957, 0.816, 0.169),  # yellow
                (0.898, 0.6, 0.165),    # orange
                (0.835, 0.294, 0.157),  # light red
                (0.568, 0.176, 0.196)]  # dark red
        self.mcols = amwg
        self.mcol1 = self.mcols[0]   # dark blue
        self.mcol2 = self.mcols[12]  # dark red
        self.mcol3 = self.mcols[2]   # light blue
        self.mcol4 = self.mcols[10]  # orange
        self.mcol5 = self.mcols[6]   # dark green
        self.lcol1 = self.mcol1
        self.lcol2 = self.mcol2
        self.lcol3 = self.mcol3
        self.lcol4 = self.mcol4
        self.lcol5 = self.mcol5
        self.lcols = self.mcols
        # ldashes     = [(5, 2, 2, 2, 2, 2, 2, 2), (2, 2), (10, 3), (5, 3),
        #                (3, 5), (5, 0)]
        self.ldashes = [(5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                        (5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
                        (5, 0),
                        (5, 2),
                        (5, 2, 2, 2),
                        (5, 2, 2, 2, 2, 2),
                        (5, 2, 2, 2, 2, 2, 2, 2),
                        (5, 2, 2, 2, 2, 2, 2, 2, 2, 2)]
        # legend
        self.llxbbox    = 1.0    # x-anchor legend bounding box
        self.llybbox    = 1.0    # y-anchor legend bounding box
        self.llrspace   = 0.     # spacing between rows in legend
        self.llcspace   = 1.0    # spacing between columns in legend
        self.llhtextpad = 0.4    # pad between the legend handle and text
        self.llhlength  = 1.5    # length of the legend handles
        self.frameon    = False  # if True, draw a frame around the legend.
                                 # If None, use rc
        # png
        self.dpi         = 300
        self.bbox_inches = 'tight'
        self.pad_inches  = 0.035

    # -------------------------------------------------------------------------
    # test figure
    #
    def plot_test(self):
        """
        A simple test plot

        """
        import matplotlib.pyplot as plt

        self.ifig += 1
        iplot  = 0
        print('    Plot - Fig ', self.ifig)
        fig = plt.figure(self.ifig)

        nn = 100
        xx = np.arange(nn) / float(nn) * 4.*np.pi
        yy1 = np.sin(xx)
        yy2 = np.cos(xx)

        xlab = r'4 $\pi$'
        ylab = 'sine and cosine function'
        xlim = None
        ylim = None

        iplot += 1

        sub = fig.add_axes([0.125, 0.667, 0.3375, 0.233], label=str(iplot))

        tarr = ['sin']
        larr = sub.plot(xx, yy1)
        plt.setp(larr[-1], linestyle='-', linewidth=self.lwidth, marker='',
                 color=self.lcols[0])

        tarr += ['cos']
        larr += sub.plot(xx, yy2)
        plt.setp(larr[-1], linestyle='-', linewidth=self.lwidth, marker='',
                 color=self.lcols[-3])

        if xlab != '':
            plt.setp(sub, xlabel=xlab)
        if ylab != '':
            plt.setp(sub, ylabel=ylab)
        sub.grid(False)

        sub.spines['right'].set_color('none')
        sub.spines['top'].set_color('none')

        if xlim is not None:
            plt.setp(sub, xlim=xlim)
        if ylim is not None:
            plt.setp(sub, ylim=ylim)

        ll = sub.legend(larr, tarr, frameon=self.frameon, ncol=1,
                        labelspacing=self.llrspace,
                        handletextpad=self.llhtextpad,
                        handlelength=self.llhlength,
                        loc='upper left',
                        bbox_to_anchor=(self.llxbbox, self.llybbox),
                        scatterpoints=1, numpoints=1)
        plt.setp(ll.get_texts(), fontsize='small')

        # import pdb; pdb.set_trace()

        self.plot_save(fig)

    # -------------------------------------------------------------------------
    # output type
    #
    def set_output_type(self):
        """
        Set type of chosen output.

        Fall back to standard html mode if mlpd3 or plotly modules are not
        installed.

        """
        self.outtype  = self.outtype.lower()
        self.outtypes = ['', 'pdf', 'png', 'html', 'd3', 'plotly']
        if self.outtype not in self.outtypes:
            estr  = '\nOutput ' + self.outtype + ' type must be in:'
            raise IOError(estr, self.outtypes)

        if (self.outtype == 'd3'):
            try:
                import mpld3
            except ModuleNotFoundError:
                print("    No mpld3 found. Use output type html instead.")
                self.outtype = 'html'

        if (self.outtype == 'plotly'):
            try:
                import plotly.tools
                import plotly.offline
            except ModuleNotFoundError:
                print("    No plotly found. Use output type html instead.")
                outtype = 'html'
            if (self.outtype == 'plotly') and (self.plotname != ''):
                assert self.plotname.endswith('html'), (
                    'Plotly plotnames must end with .html')

    # -------------------------------------------------------------------------
    # Matplotlib defaults
    #
    def set_matplotlib_rcparams(self):
        """
        Set rcParams depending on output type and other options such as using
        LaTeX, serif fonts, etc.

        rcParams can be overwritten in the initialisation of an extending
        class.

        Current parameters set are:

        .. list-table::
           :widths: 15 50
           :header-rows: 1

           * - Parameter
             - Options
           * - ps
             - papersize, usedistiller
           * - figure
             - figsize, edgecolor, facecolor
           * - text
             - usetex, latex.preamble, color
           * - font
             - family, sans-serif, size
           * - savefig
             - dpi, format, edgecolor, facecolor
           * - axes
             - linewidth, edgecolor, facecolor, labelcolor, prop_cycle
           * - boxplot
             - boxprops.color, capprops.color, flierprops.color,
               flierprops.markeredgecolor, whiskerprops.color
           * - grid
             - color
           * - lines
             - linewidth, color
           * - patch
             - edgecolor
           * - path
             - simplify
           * - xtick
             - color
           * - ytick
             - color

        Examples
        --------
        Setting rcParams in initialisation

        .. code-block:: python

           class UsemcPlot(mcPlot):
               def __init__(self, *args, **kwargs):
                   import matplotlib as mpl
                   super().__init__(*args, **kwargs)
                   mpl.rc('grid', color='red')
                   mpl.rcParams['boxplot.boxprops.color'] = 'blue'

        """
        import matplotlib as mpl
        if (self.outtype == 'pdf'):
            mpl.use('PDF')  # set directly after import matplotlib
            from matplotlib.backends.backend_pdf import PdfPages
            self.PdfPages = PdfPages
            # Customize
            #     http://matplotlib.sourceforge.net/users/customizing.html
            mpl.rc('ps', papersize='a4', usedistiller='xpdf')  # ps2pdf
            mpl.rc('figure', figsize=(8.27, 11.69))  # a4 portrait
            if self.usetex:
                mpl.rc('text', usetex=True)
                if not self.serif:
                    #   r'\usepackage{helvet}',  # use Helvetica
                    mpl.rcParams['text.latex.preamble'] = '\n'.join([
                        # use MyriadPro font
                        r'\usepackage[math,lf,mathtabular,footnotefigures]{MyriadPro}',
                        # normal text font is sans serif
                        r'\renewcommand{\familydefault}{\sfdefault}',
                        r'\figureversion{lining,tabular}',
                        # for permil symbol (load after MyriadPro)
                        r'\usepackage{wasysym}',
                        # for degree symbol (load after MyriadPro)
                        r'\usepackage{gensymb}'])
                else:
                    mpl.rcParams['text.latex.preamble'] = '\n'.join([
                        r'\usepackage{wasysym}',  # for permil symbol
                        r'\usepackage{gensymb}'])  # for degree symbol
            else:
                if self.serif:
                    mpl.rcParams['font.family']     = 'serif'
                    mpl.rcParams['font.sans-serif'] = 'Times'
                else:
                    mpl.rcParams['font.family']     = 'sans-serif'
                    mpl.rcParams['font.sans-serif'] = 'Arial'  # Arial, Verdana
        elif ((self.outtype == 'png') or (self.outtype == 'html') or
              (self.outtype == 'd3') or (self.outtype == 'plotly')):
            mpl.use('Agg')  # set directly after import matplotlib
            mpl.rc('figure', figsize=(8.27, 11.69))  # a4 portrait
            if self.usetex:
                mpl.rc('text', usetex=True)
                if not self.serif:
                    #   r'\usepackage{helvet}',  # use Helvetica
                    mpl.rcParams['text.latex.preamble'] = '\n'.join([
                        # use MyriadPro font
                        r'\usepackage[math,lf,mathtabular,footnotefigures]{MyriadPro}',
                        # normal text font is sans serif
                        r'\renewcommand{\familydefault}{\sfdefault}',
                        r'\figureversion{lining,tabular}',
                        # for permil symbol (load after MyriadPro)
                        r'\usepackage{wasysym}',
                        # for degree symbol (load after MyriadPro)
                        r'\usepackage{gensymb}'])
                else:
                    mpl.rcParams['text.latex.preamble'] = '\n'.join([
                        r'\usepackage{wasysym}',   # for permil symbol
                        r'\usepackage{gensymb}'])  # for degree symbol
            else:
                if self.serif:
                    mpl.rcParams['font.family']     = 'serif'
                    mpl.rcParams['font.sans-serif'] = 'Times'
                else:
                    mpl.rcParams['font.family']     = 'sans-serif'
                    mpl.rcParams['font.sans-serif'] = 'Arial'  # Arial, Verdana
            mpl.rc('savefig', dpi=self.dpi, format='png')
        else:
            mpl.rc('figure', figsize=(4./5.*8.27, 4./5.*11.69))  # a4 portrait
        # print(mpl.rcParams)
        mpl.rc('axes', linewidth=self.alwidth, edgecolor=self.fgcolor,
               facecolor=self.bgcolor, labelcolor=self.fgcolor,
               prop_cycle=mpl.rcsetup.cycler('color',
                                             ['8dd3c7', 'feffb3', 'bfbbd9',
                                              'fa8174', '81b1d2', 'fdb462',
                                              'b3de69', 'bc82bd', 'ccebc4',
                                              'ffed6f']))
        mpl.rcParams['boxplot.boxprops.color'] = self.fgcolor
        mpl.rcParams['boxplot.capprops.color'] = self.fgcolor
        mpl.rcParams['boxplot.flierprops.color'] = self.fgcolor
        mpl.rcParams['boxplot.flierprops.markeredgecolor'] = self.fgcolor
        mpl.rcParams['boxplot.whiskerprops.color'] = self.fgcolor
        mpl.rc('figure', edgecolor=self.bgcolor, facecolor=self.bgcolor)
        mpl.rc('font', size=self.textsize)
        mpl.rc('grid', color=self.fgcolor)
        mpl.rc('lines', linewidth=self.lwidth, color=self.fgcolor)
        mpl.rc('patch', edgecolor=self.fgcolor)
        mpl.rc('path', simplify=False)  # do not remove
        mpl.rc('savefig', edgecolor=self.bgcolor, facecolor=self.bgcolor)
        mpl.rc('text', color=self.fgcolor)
        mpl.rc('xtick', color=self.fgcolor)
        mpl.rc('ytick', color=self.fgcolor)

    # -------------------------------------------------------------------------
    # plot begin
    #
    def plot_begin(self):
        import os.path
        """
        Last step of initialisation

        Set output filename depending on chosen output type. Opens output file
        if appropriate.

        """
        self.outtype_ends = ['', '.pdf', '_', '.html', '.html']
        if self.plotname == '':
            self.plotfile  = (_filebase(os.path.basename(__file__)) +
                              self.outtype_ends[
                                  self.outtypes.index(self.outtype)])
        else:
            self.plotfile = self.plotname
        if self.outtype == '':
            print('    Plot X')
        else:
            print('    Plot ', self.plotfile)

        if (self.outtype == 'pdf'):
            self.pdf_pages = self.PdfPages(self.plotfile)
        # figsize = mpl.rcParams['figure.figsize']

        if self.outtype in ['html', 'd3']:
            print('    Write html file ', self.plotfile)
            self.fhtml = open(self.plotfile, 'w')
            fstr  = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01'
            fstr += ' Transitional//EN">'
            print(fstr, file=self.fhtml)
            print("<html>", file=self.fhtml)
            print("<head>", file=self.fhtml)
            print("<title>"+self.plotfile+"</title>", file=self.fhtml)
            print("</head>", file=self.fhtml)
            print("<body>", file=self.fhtml)

        if (self.outtype == 'plotly'):
            self.htmlfiles = []

        self.ifig = 0

    def plot_start(self):
        """Alias for plot_begin()"""
        self.plot_begin()

    # -------------------------------------------------------------------------
    # plot save
    #
    def plot_save(self, fig, **kwargs):
        """
        Save figure into output file

        Parameters
        ----------
        fig : matplotlib.figure.Figure
            Matplotlib figure object.    argstr : string, optional
        kwargs : dict, optional
            Additional keywords will be passed to *savefig* for 'pdf',
            'png', and 'html'; to *fig_to_html* for 'd3', and to
            *offline.plot* for 'plotly'. This overwrites *self.transparent*,
            *self.bbox_inches*, *self.pad_inches* for 'pdf', 'png', and 'html',
            and *auto_open=False* for 'plotly'.

        """
        import matplotlib.pyplot as plt
        # save pages
        if (self.outtype == 'pdf'):
            if 'transparent' not in kwargs:
                kwargs.update({'transparent': self.transparent})
            self.pdf_pages.savefig(fig, **kwargs)
            plt.close(fig)
        elif (self.outtype == 'png'):
            pngfile = self.plotfile+"{0:04d}".format(self.ifig)+".png"
            if 'transparent' not in kwargs:
                kwargs.update({'transparent': self.transparent})
            if 'bbox_inches' not in kwargs:
                kwargs.update({'bbox_inches': self.bbox_inches})
            if 'pad_inches' not in kwargs:
                kwargs.update({'pad_inches': self.pad_inches})
            fig.savefig(pngfile, **kwargs)
            plt.close(fig)
        elif (self.outtype == 'html'):
            pngfile  = _filebase(self.plotfile) + "_"
            pngfile += "{0:04d}".format(self.ifig) + ".png"
            if 'transparent' not in kwargs:
                kwargs.update({'transparent': self.transparent})
            if 'bbox_inches' not in kwargs:
                kwargs.update({'bbox_inches': self.bbox_inches})
            if 'pad_inches' not in kwargs:
                kwargs.update({'pad_inches': self.pad_inches})
            fig.savefig(pngfile, **kwargs)
            print('<p><img src='+pngfile+'></p>', file=self.fhtml)
            plt.close(fig)
        elif (self.outtype == 'd3'):
            import mpld3
            # Does not work:
            #     mpld3.plugins.connect(fig, mpld3.plugins.LinkedBrush(line1))
            d3str = mpld3.fig_to_html(fig, **kwargs)
            print(d3str, file=self.fhtml)
            plt.close(fig)
        elif (self.outtype == 'plotly'):
            import plotly.tools
            import plotly.offline
            htmlfile = self.plotfile+"{0:04d}".format(self.ifig)+".html"
            plotly_fig = plotly.tools.mpl_to_plotly(fig)
            if 'auto_open' not in kwargs:
                kwargs.update({'auto_open': False})
            ff = plotly.offline.plot(plotly_fig, filename=htmlfile, **kwargs)
            self.htmlfiles.append(htmlfile)
            plt.close(fig)

    # -------------------------------------------------------------------------
    # plot end
    #
    def plot_end(self):
        """
        Finish plotting

        Close output file if appropriate or show interactive plots.

        """
        if (self.outtype == 'pdf'):
            self.pdf_pages.close()
        elif (self.outtype == 'png'):
            pass
        elif (self.outtype == 'html') or (self.outtype == 'd3'):
            print("</body>\n</html>", file=self.fhtml)
            self.fhtml.close()
        elif (self.outtype == 'plotly'):
            import os
            if self.ifig > 1:
                import fileinput
                htmlfile = self.plotfile
                with open(htmlfile, 'w') as fout:
                    fin = fileinput.input(self.htmlfiles)
                    for line in fin:
                        fout.write(line)
                    fin.close()
                for ff in self.htmlfiles:
                    os.remove(ff)
            else:
                os.rename(self.htmlfiles[0], self.plotfile)
        else:
            import matplotlib.pyplot as plt
            plt.show()

    def plot_stop(self):
        """Alias for plot_end()"""
        self.plot_end()

    def plot_close(self):
        """Alias for plot_end()"""
        self.plot_end()

    def close(self):
        """Alias for plot_end()"""
        self.plot_end()

    def end(self):
        """Alias for plot_end()"""
        self.plot_end()


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
