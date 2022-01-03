#!/usr/bin/env python
"""
GUI dialogs to choose files and directories using Tkinter

This module was written by Matthias Cuntz while at Department of
Computational Hydrosystems, Helmholtz Centre for Environmental
Research - UFZ, Leipzig, Germany, and continued while at Institut
National de Recherche pour l'Agriculture, l'Alimentation et
l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2015-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided

.. autosummary::
   directory_from_gui
   directories_from_gui
   file_from_gui
   files_from_gui

History
    * Written Jun 2014 by Matthias Cuntz (mc (at) macu (dot) de)
    * Added directories_from_gui, Oct 2015, Matthias Cuntz
    * Using numpy docstring format, May 2020, Matthias Cuntz
    * Port to pyjams, Jan 2022, Matthias Cuntz

"""


__all__ = ['directory_from_gui', 'directories_from_gui',
           'file_from_gui', 'files_from_gui']


# -------------------------------------------------------------------------
# Choose one directory in GUI
#

def directory_from_gui(
        initialdir='.',
        title='Choose directory'):  # pragma: no cover
    """
    Opens dialog to one select directory

    Parameters
    ----------
    initialdir : str, optional
        Initial directory, in which opens GUI (default: '.')
    title : str, optional
        Title of GUI (default: 'Choose directory')

    Returns
    ------
    str
        Selected directory

    Examples
    --------
    .. code-block:: python

       if not idir:
           idir = directory_from_gui()
           if not idir:
               raise ValueError('Error: no directory given.')

    """
    import tkinter as Tkinter
    import tkinter.filedialog as tkFileDialog

    root = Tkinter.Tk()
    root.withdraw()  # hide root window, i.e. white square

    # always on top
    # focus on (hidden) window so that child is on top
    root.tk.call('wm', 'attributes', '.', '-topmost', 1)

    direcs = tkFileDialog.askdirectory(
        parent=root, title=title, initialdir=initialdir)

    root.destroy()

    return direcs


# -------------------------------------------------------------------------
# Choose directories in GUI
#

def directories_from_gui(
        initialdir='.',
        title='Choose one or several directories'):  # pragma: no cover
    """
    Open dialog to select several directories

    Parameters
    ----------
    initialdir : str, optional
        Initial directory, in which opens GUI (default: '.')
    title : str, optional
        Title of GUI (default: 'Choose one or several directories')

    Returns
    ------
    list
        Selected directories

    Examples
    --------
    .. code-block:: python

       if not direcs:
           direcs = directories_from_gui()
           if not direcs:
               raise ValueError('Error: no directories given.')

    """
    import tkinter as Tkinter
    import tkinter.filedialog as tkFileDialog

    root = Tkinter.Tk()
    root.withdraw()  # hide root window, i.e. white square

    # always on top
    # focus on (hidden) window so that child is on top
    root.tk.call('wm', 'attributes', '.', '-topmost', 1)

    idir = initialdir
    alldirecs = []
    while True:
        direcs = tkFileDialog.askdirectory(
            parent=root, title=title, initialdir=idir)
        if not direcs:
            break
        alldirecs.append(direcs)
        idir = direcs

    root.destroy()

    return alldirecs


# -------------------------------------------------------------------------
# Choose one file in GUI
#

def file_from_gui(initialdir='.', title='Choose file',
                  multiple=False):  # pragma: no cover
    """
    Wrapper for :func:`files_from_gui` with multiple=False, i.e.
    open dialog to select one file

    Examples
    --------
    .. code-block:: python

       if not file:
           file = file_from_gui()
           if not file:
               raise ValueError('Error: no input file given.')

    """
    return files_from_gui(initialdir=initialdir,
                          title=title,
                          multiple=multiple)


# -------------------------------------------------------------------------
# Choose files in GUI
#

def files_from_gui(initialdir='.', title='Choose file(s)',
                   multiple=True):  # pragma: no cover
    """
    Open dialog to select one or several files

    Parameters
    ----------
    initialdir : str, optional
        Initial directory, in which opens GUI (default: '.')
    title : str, optional
        Title of GUI (default: 'Choose file(s)')
    multiple : bool, optional
        Allow selection of multiple files if True (default),
        else it is only possible to select one single file.

    Returns
    ------
    list
        Selected file(s)

    Note
    ----
    It always returns a list even with `multiple=False`.

    Examples
    --------
    .. code-block:: python

       if not files:
           files = files_from_gui()
           if not files:
               raise ValueError('Error: no input file(s) given.')

    """
    import tkinter as Tkinter
    import tkinter.filedialog as tkFileDialog
    root = Tkinter.Tk()
    root.withdraw()  # hide root window, i.e. white square

    # always on top
    # focus on (hidden) window so that child is on top
    root.tk.call('wm', 'attributes', '.', '-topmost', 1)

    files = tkFileDialog.askopenfilename(
        parent=root, title=title, multiple=multiple, initialdir=initialdir)
    files = list(root.tk.splitlist(files))

    root.destroy()

    return files


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
