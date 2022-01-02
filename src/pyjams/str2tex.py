#!/usr/bin/env python
"""
Convert strings to LaTeX strings in math environment used by matplotlib's
usetex

This module was written by Matthias Cuntz while at Department of Computational
Hydrosystems, Helmholtz Centre for Environmental Research - UFZ, Leipzig,
Germany, and continued while at Institut National de Recherche pour
l'Agriculture, l'Alimentation et l'Environnement (INRAE), Nancy, France.

:copyright: Copyright 2015-2022 Matthias Cuntz, see AUTHORS.rst for details.
:license: MIT License, see LICENSE for details.

.. moduleauthor:: Matthias Cuntz

The following functions are provided:

.. autosummary::
   str2tex

History
    * Written Oct 2015 by Matthias Cuntz (mc (at) macu (dot) de)
    * Use raw strings for escaped characters, Nov 2021, Matthias Cuntz
    * Bug in space2linebreak in complex strings with spaces;
      do space2linebreak first, Nov 2021, Matthias Cuntz
    * Bug in escaping %, Nov 2021, Matthias Cuntz
    * Remove trailing $\\mathrm{}$, Nov 2021, Matthias Cuntz
    * Ported into pyjams, Nov 2021, Matthias Cuntz
    * Better handling of linebreaks in Matplotlib and LaTeX mode,
      Nov 2021, Matthias Cuntz
    * More consistent docstrings, Jan 2022, Matthias Cuntz

"""
import numpy as np


__all__ = ['str2tex']


def str2tex(strin, space2linebreak=False,
            bold=False, italic=False, usetex=False):
    """
    Convert strings to LaTeX strings in math environment used by matplotlib's
    usetex

    Strings are embedded into '$\\mathrm{strin}$' by default but can be
    embedded into '\\mathbf' and '\\mathit'.
    Spaces are escaped but can be replaced by linebreaks.

    Parameters
    ----------
    strin : str or array-like of str
        string (array)
    space2linebreak : bool, optional
        Replace space (' ') by linebreak ('\\n') if True (default: False)
    bold : bool, optional
        Use '\\mathbf' instead of '\\mathrm' if True (default: False)
    italic : bool, optional
        Use '\\mathit' instead of '\\mathrm' if True (default: False)
    usetex : bool, optional
        Treat only linebreaks and comments if False (default)

    Returns
    -------
    string : str
        string (array) that can be used in matplotlib independent of usetex.

    Examples
    --------
    .. code-block:: python

       fig = plt.figure()
       tit = str2tex('A $S_{Ti}$ is great\\nbut use-less', usetex=usetex)
       fig.suptitle(tit)

    """
    import matplotlib.pyplot as plt

    # Input type and shape
    if isinstance(strin, list):
        from copy import copy
        istrin = copy(strin)
    elif isinstance(strin, tuple):
        istrin = list(strin)
    elif isinstance(strin, np.ndarray):
        istrin = list(strin.flatten())
    else:
        istrin = [strin]
    # nstrin = len(istrin)

    # font style
    if (bold+italic) > 1:
        raise ValueError('bold and italic are mutually exclusive.')
    else:
        if bold:
            mtex = r'$\mathbf{'
            ttex = r'$\textbf{'
            empty = r'$\mathbf{}$'
        elif italic:
            mtex = r'$\mathit{'
            ttex = r'$\textit{'
            empty = r'$\mathit{}$'
        else:
            mtex = r'$\mathrm{'
            ttex = r'$\textrm{'
            empty = r'$\mathrm{}$'

    # helpers
    a0 = chr(0)  # ascii 0
    # string replacements
    if usetex:
        # no '\n' in LaTeX, use '\newline'
        rep_n       = lambda s: s.replace(r'\n', '}$' + a0 + r'\newline'
                                          + a0 + mtex)
        rep_newline = lambda s: s.replace(r'\newline', '}$' + a0 + r'\newline'
                                          + a0 + mtex)
    else:
        # '\n' has to be unicode string and not raw string in Matplotlib
        rep_n       = lambda s: s.replace(r'\n', '' + a0 + '\n'
                                          + a0 + '')
        rep_newline = lambda s: s.replace(r'\newline', '' + a0 + '\n'
                                          + a0 + '')
    rep_down     = lambda s: s.replace('_', r'\_')
    rep_up       = lambda s: s.replace('^', r'\^')
    rep_hash     = lambda s: s.replace('#', r'\#')
    rep_percent  = lambda s: s.replace('%', r'\%')
    rep_space    = lambda s: s.replace(' ', r'\ ')
    rep_minus    = lambda s: s.replace('-', '}$' + ttex + '-}$' + mtex)
    rep_a02empty = lambda s: s.replace(a0, '')
    if usetex or (plt.get_backend() == 'pdf'):
        rep_space2n = lambda s: s.replace(' ', '}$' + a0 + r'\newline'
                                          + a0 + mtex)
    else:
        rep_space2n = lambda s: s.replace(' ', ''+'\n'+'')
    rep_empty = lambda s: s.replace(empty, '')

    if usetex:
        for j, s in enumerate(istrin):
            if '$' in s:
                cleanempty = empty not in s
                ss = s.split('$')
                # outside $...$
                # -, _, ^ only escaped if not between $
                for ii in range(0, len(ss), 2):
                    ss[ii] = mtex + ss[ii] + '}$'
                    # - not minus sign
                    if '-' in ss[ii]:
                        ss[ii] = rep_minus(ss[ii])
                        if ss[ii].endswith('{}$'):
                            ss[ii] = ss[ii][:-11]  # rm trailing $\mathrm{}$
                    # \n not in tex mode but normal matplotlib
                    if (r'\n' in ss[ii]) and not (r'\newline' in ss[ii]):
                        ss[ii] = rep_n(ss[ii])
                    elif (r'\newline' in ss[ii]):
                        ss[ii] = rep_newline(ss[ii])
                    # escape _
                    if '_' in ss[ii]:
                        ss[ii] = rep_down(ss[ii])
                    # escape ^
                    if '^' in ss[ii]:
                        ss[ii] = rep_up(ss[ii])
                    # escape #
                    if '#' in ss[ii]:
                        ss[ii] = rep_hash(ss[ii])
                    # escape %
                    if ('%' in ss[ii]) and not (r'\%' in ss[ii]):
                        ss[ii] = rep_percent(ss[ii])
                    if space2linebreak:
                        if ' ' in ss[ii]:
                            ss[ii] = rep_space2n(ss[ii])

                # reassemble string
                istrin[j] = '$'.join(ss)

                if s[0] == '$':
                    # rm leading $\mathrm{}$ if string started with $
                    istrin[j] = istrin[j][11:]
            else:
                cleanempty = True
                istrin[j] = mtex + s + '}$'
                # - not minus sign
                if '-' in istrin[j]:
                    istrin[j] = rep_minus(istrin[j])
                    if istrin[j].endswith('{}$'):
                        istrin[j] = istrin[j][:-11]  # rm trailing $\mathrm{}$
                # \n not in tex mode but normal matplotlib
                if (r'\n' in istrin[j]) and not (r'\newline' in istrin[j]):
                    istrin[j] = rep_n(istrin[j])
                elif (r'\newline' in istrin[j]):
                    istrin[j] = rep_newline(istrin[j])
                # escape _
                if '_' in istrin[j]:
                    istrin[j] = rep_down(istrin[j])
                # escape ^
                if '^' in istrin[j]:
                    istrin[j] = rep_up(istrin[j])
                # escape #
                if '#' in istrin[j]:
                    istrin[j] = rep_hash(istrin[j])
                # escape %
                if ('%' in istrin[j]) and not (r'\%' in istrin[j]):
                    istrin[j] = rep_percent(istrin[j])
                if space2linebreak:
                    if ' ' in istrin[j]:
                        istrin[j] = rep_space2n(istrin[j])

            # rm $\mathrm{}$
            if cleanempty:
                istrin[j] = rep_empty(istrin[j])

            # escape space
            if ' ' in istrin[j]:
                istrin[j] = rep_space(istrin[j])

            # rm ascii character 0 around linebreaks introduced above
            if a0 in istrin[j]:
                istrin[j] = rep_a02empty(istrin[j])
    else:
        # escape %
        istrin = [ rep_percent(i) if ('%' in i) and not (r'\%' in i) else i
                   for i in istrin ]
        # '\n' is Matplotlib but nor LaTeX
        for j, s in enumerate(istrin):
            if (r'\n' in istrin[j]) and not (r'\newline' in istrin[j]):
                istrin[j] = rep_n(istrin[j])
            elif (r'\newline' in istrin[j]):
                istrin[j] = rep_newline(istrin[j])
            if a0 in istrin[j]:
                istrin[j] = rep_a02empty(istrin[j])
            if space2linebreak:
                if ' ' in istrin[j]:
                    istrin[j] = rep_space2n(istrin[j])
        if (plt.get_backend() == 'pdf'):  # pragma: no cover
            # pdf backend uses LaTeX
            istrin = [ i.replace(r'\n', r'\newline')
                       if (r'\n' in i) and not (r'\newline' in i) else i
                       for i in istrin ]

    # Return right type
    if isinstance(strin, list):
        return istrin
    elif isinstance(strin, tuple):
        return tuple(istrin)
    elif isinstance(strin, np.ndarray):
        return np.array(istrin).reshape(strin.shape)
    else:
        return istrin[0]


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # strin = ['One', 'One-', 'One-Two', 'One Two', 'One\nTwo', 'A $S_{Ti}$ is great\nbut use-less']
    # print(str2tex(strin))
    # # ['$\\mathrm{One}$', '$\\mathrm{One}$$\\textrm{-}$', '$\\mathrm{One}$$\\textrm{-}$$\\mathrm{Two}$', '$\\mathrm{One\\ Two}$', '$\\mathrm{One}$ \n $\\mathrm{Two}$', '$\\mathrm{A\\ }$$S_{Ti}$$\\mathrm{\\ is\\ great}$ \n $\\mathrm{but\\ use}$$\\textrm{-}$$\\mathrm{less}$']
    # print(str2tex(strin, bold=True))
    # # ['$\\mathbf{One}$', '$\\mathbf{One}$$\\textbf{-}$', '$\\mathbf{One}$$\\textbf{-}$$\\mathbf{Two}$', '$\\mathbf{One\\ Two}$', '$\\mathbf{One}$ \n $\\mathbf{Two}$', '$\\mathbf{A\\ }$$S_{Ti}$$\\mathbf{\\ is\\ great}$ \n $\\mathbf{but\\ use}$$\\textbf{-}$$\\mathbf{less}$']
    # print(str2tex(strin, italic=True))
    # # ['$\\mathit{One}$', '$\\mathit{One}$$\\textit{-}$', '$\\mathit{One}$$\\textit{-}$$\\mathit{Two}$', '$\\mathit{One\\ Two}$', '$\\mathit{One}$ \n $\\mathit{Two}$', '$\\mathit{A\\ }$$S_{Ti}$$\\mathit{\\ is\\ great}$ \n $\\mathit{but\\ use}$$\\textit{-}$$\\mathit{less}$']
    # print(str2tex(strin, space2linebreak=True))
    # # ['$\\mathrm{One}$', '$\\mathrm{One}$$\\textrm{-}$', '$\\mathrm{One}$$\\textrm{-}$$\\mathrm{Two}$', '$\\mathrm{One}$ \n $\\mathrm{Two}$', '$\\mathrm{One}$ \n $\\mathrm{Two}$', '$\\mathrm{A}$ \n $\\mathrm{}$$S_{Ti}$$\\mathrm{ \n $\\mathrm{is \n $\\mathrm{great}$ \n $\\mathrm{but \n $\\mathrm{use}$$\\textrm{-}$$\\mathrm{less}$']
    # print(str2tex(strin, space2linebreak=True, bold=True))
    # # ['$\\mathbf{One}$', '$\\mathbf{One}$$\\textbf{-}$', '$\\mathbf{One}$$\\textbf{-}$$\\mathbf{Two}$', '$\\mathbf{One}$ \n $\\mathbf{Two}$', '$\\mathbf{One}$ \n $\\mathbf{Two}$', '$\\mathbf{A}$ \n $\\mathbf{}$$S_{Ti}$$\\mathbf{ \n $\\mathbf{is \n $\\mathbf{great}$ \n $\\mathbf{but \n $\\mathbf{use}$$\\textbf{-}$$\\mathbf{less}$']
    # print(str2tex(strin, usetex=False))
    # # ['One', 'One-', 'One-Two', 'One Two', 'One\nTwo', 'A $S_{Ti}$ is great\nbut use-less']
    # print(str2tex(strin, space2linebreak=True, usetex=False))
    # # ['One', 'One-', 'One-Two', 'One\nTwo', 'One\nTwo', 'A\n$S_{Ti}$\nis\ngreat\nbut\nuse-less']

    # strin = [r'A $S_{Ti}$ is great\nbut use-less-']
    # outsp = [r'A\n$S_{Ti}$\nis\ngreat\nbut\nuse-less-']
    # outsp = [ s.replace(r'\n', '' + '\n' + '') for s in outsp ]
    # print(outsp)
    # print(str2tex(strin, space2linebreak=True))

    # strin = [r'A $S_{Ti}$ is great\nbut use-less-']
    # outsp = [r'$\mathrm{A}$\newline$S_{Ti}$\newline$\mathrm{is}$'
    #          r'\newline$\mathrm{great}$\newline$\mathrm{but}$'
    #          r'\newline$\mathrm{use}$$\textrm{-}$$\mathrm{less}$'
    #          r'$\textrm{-}$']
    # print(outsp)
    # print(str2tex(strin, space2linebreak=True, usetex=True))
