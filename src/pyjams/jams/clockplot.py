#!/usr/bin/env python
import numpy as np


__all__ = ['clockplot']


def clockplot(sub, si, sti=None, stierr=None,
              iplot       = None,           # plot number for abc2plot
              usetex      = False,
              dxabc       = 2,              # factor to half the plot size for a,b,c,... labels
              dyabc       = 0.5,            # factor to 0.1 time the plot height for a,b,c,... labels
              dxsig       = 1.23,           # factor to half the plot size for signature
              dysig       = -0.05,          # factor to 0.1 time the plot height for signature
              elwidth     = 1.0,            # errorbar line width
              alwidth     = 1.0,            # axis line width
              glwidth     = 0.5,            # grid line width
              acol        = 'black',        # axis colour
              mcol        = '0.4',          # grid colour
              ecol        = 'black',        # error bar colour
              mcols       = ['0.0', '0.4', '0.4', '0.7', '0.7', '1.0'],      # stack colors
              lcols       = ['None', 'None', 'None', 'None', 'None', '0.0'], # stack bourder colours
              hatches     = [None, None, None, None, None, '//'],            # stack hatching
              llxbbox     = 0.0,            # x-anchor legend bounding box
              llybbox     = 1.15,           # y-anchor legend bounding box
              ymax        = 0.8,            # maximum of y-axis
              ntextsize   = 'medium',       # normal textsize (relative to mpl.rcParams['font.size'])
              bmod        = 0.5,            # fraction of ymax from center to start module colours
              alphamod    = 0.7,            # alpha channel for modules
              fwm         = 0.05,           # module width to remove at sides
              ylabel1     = 1.15,           # position of module names
              ylabel2     = 1.35,           # position of class names
              mtextsize   = 'large',        # textsize of module labels (relative to mpl.rcParams['font.size'])
              bpar        = 0.4,            # fraction of ymax from center to start with parameter bars
              fwb         = [0.7,0.4,0.3],  # fractional width of bars
              plwidth     = 0.5,            # stack border line width
              bplabel     = 0.1,            # fractional distance of ymax of param numbers in centre from 0-line
              ptextsize   = 'medium',       # textsize of param numbers in centre (relative to mpl.rcParams['font.size'])
              space4yaxis = 2,              # space for y-axis (integer)
              ytextsize   = 'medium',       # textsize of y-axis (relative to mpl.rcParams['font.size'])
              dobw        = False,          # True: black & white
              docomp      = True,           # True: Print classification on top of modules
              dosig       = False,          # True: add signature to plot
              dolegend    = False,          # True: add legend to each subplot
              doabc       = False,          # True: add subpanel numbering
              modul         = ['Interception',    'Snow',             'Soil moisture', 'Soil moisture',
                             r'Direct\n runoff', r'Evapo-\n transp.', 'Interflow',     'Percolation',
                             'Routing',         'Geology'],      # module names
              modhalign    = None,          # Horizontal alignment of module names
              modvalign    = None,          # Vertical alignment of module names
              comp        = ['P',               'P',                'S',             'ET',
                             'Q',               'ET',               'S',             'S',
                             'Q',               'S'],            # class names
              pmod        = [ 1,                 8,                  9,               8,
                              1,                 3,                  5,               3,
                              5,                 9],             # # of parameters per class
              cmod        = 'mhm',                               # color scheme chosen ('mhm' or 'noah')
              cmap        = None,                                # Color for each module mod (if not given cmod determines colors)
              saname      = ['Sobol', 'weighted Sobol', 'RMSE'], # stack names
              indexname   = [r'$S_i$', r'$S_{Ti}-S_i$'],           # index legend name
              star        = None,                                # star symbols
              dystar      = 0.95,                                # % of ymax for stars
              scol        = '1.0',                               # star colour
              sfcol       = 'None',                              # star face colour
              ssize       = 3.0,                                 # star size
              swidth      = 1.0,                                 # star edge width
              ssym        = '*',                                 # star symbol
              sig         = 'J Mai & M Cuntz'):                  # signature
    r"""
    The clock plot with modules and up to three index stacks.

    The plot currently defaults to mHM but it can be customized for any model output.


    Definition
    ----------
    def clockplot(sub, si, sti=None, stierr=None,
                  usetex=False,
                  dxabc       = 2,
                  dyabc       = 0.5,
                  dxsig       = 1.23,
                  dysig       = -0.05,
                  elwidth     = 1.0,
                  alwidth     = 1.0,
                  glwidth     = 0.5,
                  acol        = 'black',
                  mcol        = '0.4',
                  ecol        = 'black',
                  mcols       = ['0.0', '0.4', '0.4', '0.7', '0.7', '1.0'],
                  lcols       = ['None', 'None', 'None', 'None', 'None', '0.0'],
                  hatches     = [None, None, None, None, None, '//'],
                  llxbbox     =  0.0,
                  llybbox     = 1.15,
                  ymax = 0.8,
                  ntextsize   = 'medium',
                  bmod        = 0.5,
                  alphamod    = 0.7,
                  fwm         = 0.05,
                  ylabel1     = 1.15,
                  ylabel2     = 1.35,
                  mtextsize   = 'large',
                  bpar        = 0.4,
                  fwb         = [0.7,0.4,0.3],
                  plwidth     = 0.5,
                  bplabel     = 0.1,
                  ptextsize   = 'medium',
                  space4yaxis = 2,
                  ytextsize   = 'medium',
                  dobw      = False,
                  docomp    = True,
                  dosig     = False,
                  dolegend  = False,
                  doabc     = False,
                  modul   = ['Interception',    'Snow',             'Soil moisture', 'Soil moisture',
                           'Direct\n runoff', 'Evapo-\n transp.', 'Interflow',     'Percolation',
                           'Routing',         'Geology'],
                  modhalign    = None,
                  modvalign    = None,
                  comp  = ['P',               'P',                'S',             'ET',
                           'Q',               'ET',               'S',             'S',
                           'Q',               'S'],
                  pmod  = [ 1,                 8,                  9,               8,
                            1,                 3,                  5,               3,
                            5,                 9],
                  cmod  = 'mhm',
                  cmap  = [['reds8',   1], ['reds8',   2], ['reds8',   3], ['reds8',   4],
                           ['blues8',  3], ['blues8',  4], ['blues8',  5], ['blues8',  6], 
                           ['reds8',   5], ['reds8',   6]],
                  saname = ['Sobol', 'weighted Sobol', 'RMSE'],
                  indexname = ['$S_i$', '$S_{Ti}-S_i$'],
                  star = None,
                  dystar = 0.95,
                  scol = '1.0',
                  sfcol = 'None',
                  ssize = 3.0,
                  swidth = 1.0,
                  ssym = '*',
                  sig = 'J Mai & M Cuntz'):


    Input
    -----
    sub                          axes handle from for example
                                 sub = fig.add_axes(jams.position(nrow,ncol,iplot), polar=True)
    si                           list, list of arrays, 1D-, or 2D-array si[nstacks, nparameters] of, e.g.,
                                 first-order Sobol' indexes or other indexes


    Optional Input
    --------------
    sti = None                   list, list of arrays, 1D-, or 2D-array sti[nstacks, nparameters] of, e.g.,
                                 total-order Sobol' indexes or upper stack values
    stierr = None                list, list of arrays, 1D-, or 2D-array si[nstacks, nparameters] of
                                 error bars of upper stack indexes
    usetex = False               True: use LaTeX rendering
    dxabc = 2                    % of (max-min) shift to the right from left y-axis for a,b,c,... labels
    dyabc = 0.5                  % of (max-min) shift up from lower x-axis for a,b,c,... labels
    dxsig = 1.23                 % of (max-min) shift to the right from left y-axis for signature
    dysig = -0.05                % of (max-min) shift up from lower x-axis for signature
    elwidth = 1.0                errorbar line width
    alwidth = 1.0                axis line width
    glwidth = 0.5                grid line width
    acol = 'black'               axis colour
    mcol = '0.4'                 grid colour
    ecol = 'black',              error bar colour
    mcols = ['0.0', '0.4', '0.4', '0.7', '0.7', '1.0']        stack colors
    lcols = ['None', 'None', 'None', 'None', 'None', '0.0']   stack border colours
    hatches = [None, None, None, None, None, '//']            stack hatching
    llxbbox =  0.0               x-anchor legend bounding box
    llybbox = 1.15,              y-anchor legend bounding box
    ymax = 0.8                   y-axis maximum
    ntextsize = 'medium'         normal textsize
    bmod = 0.5                   fraction of ymax to start module colours
    alphamod = 0.7               alpha channel for modules
    fwm = 0.05                   module width to remove at sides for space between modules
    ylabel1 = 1.15               fractional position of module names
    ylabel2 = 1.35               fractional position of class names
    mtextsize = 'large'          textsize of module labels
    bpar = 0.4                   fraction of ymax to start parameter bars
    fwb = [0.7,0.4,0.3]          fractional width of bars depending on number of index stacks
    plwidth = 0.5                stack border line width
    bplabel = 0.1                fractional distance of ymax of param numbers in centre from 0-line
    ptextsize = 'medium'         textsize of param numbers in centre
    space4yaxis = 2              space for y-axis top tickmark label (integer)
    ytextsize = 'medium'         textsize of y-axis tickmark labels
    dobw = False                 True: black & white; False: colour
    docomp = True                True: Print classification on top of modules
    dosig = False                True: add signature (sig) to plot
    dolegend = False             True: add legend to each subplot
    doabc = False                True: add subpanel numbering
    modul  = ['Interception',    'Snow',             'Soil moisture', 'Soil moisture',
            'Direct\n runoff', 'Evapo-\n transp.', 'Interflow',     'Percolation',
            'Routing',         'Geology'],                                           module names
    modhalign = None,             list of horizontal alignments of module names
    modvalign = None,             list of vertical alignments of module names
    comp = ['P',               'P',                'S',             'ET',
            'Q',               'ET',               'S',             'S',
            'Q',               'S'],                                                 class names
    pmod = [ 1,                 8,                  9,               8,
             1,                 3,                  5,               3,
             5,                 9],                                                  number of parameters per class
    cmod = 'mhm',                                                                    color scheme chose ('mhm' or 'noah')
    cmap = [['reds8',   1], ['reds8',   2], ['reds8',   3], ['reds8',   4],
             ['blues8',  3], ['blues8',  4], ['blues8',  5], ['blues8',  6], 
             ['reds8',   5], ['reds8',   6]],                                        colors for each class
    saname = ['Sobol', 'weighted Sobol', 'RMSE'],                                    stack names
    indexname = ['$S_i$', '$S_{Ti}-S_i$'],                                           index legend name
    star = None,                                                                     star symbols
    dystar = 0.95,                                                                   % of ymax for stars
    scol = '1.0',                                                                    star colour
    sfcol = 'None',                                                                  star face colour
    ssize = 3.0,                                                                     star size
    swidth = 1.0,                                                                    star edge width
    ssym = '*',                                                                      star symbol
    sig = 'J Mai & M Cuntz'                                                          signature


    Output
    ------
    clockplot on axes sub


    Restrictions
    ------------
    None


    Examples
    --------
    see below if __name__ == '__main__':


    History
    -------
    Written,  MC, JM, AP, Oct 2014

    """
    # Check si[nstacks, nparams]
    if sti is not None:
        assert np.shape(si) == np.shape(sti), 'Lower and upper stacks must have same dimensions.'
    if stierr is not None:
        assert np.shape(si) == np.shape(stierr), 'Error bars must have must have same dimensions as upper indexes.'
    si_shape = np.shape(si)
    if np.size(si_shape) == 1:
        nsi = 1
        isi  = np.array(si)
        isi  = isi[np.newaxis, :]
        if sti is not None:
            isti = np.array(sti)
            isti = isti[np.newaxis, :]
        if stierr is not None:
            istierr = np.array(stierr)
            istierr = istierr[np.newaxis, :]
    elif np.size(si_shape) == 2:
        nsi = si_shape[0]
        if nsi > 3:
            raise ValueError('first data dimension must be <= 3, i.e. at most 3 stacks per parameter supported.')
        isi  = np.array(si)
        if sti is not None:
            isti = np.array(sti)
        if stierr is not None:
            istierr = np.array(stierr)
    else:
        raise ValueError('input data must be 1D or 2D.')
    npar = isi.shape[1]
    if sti is not None:
        idsi = isti - isi

    # alignement of module names
    if modhalign is not None:
        if isinstance(modhalign, (list, tuple, np.ndarray)):
            assert len(modul) == len(modhalign), 'modhalign must be scalar or same size as modul.'
            imodhalign = modhalign
        else:
            imodhalign = [modhalign] * len(modul)
    else:
        imodhalign = ['center'] * len(modul)
    if modvalign is not None:
        if isinstance(modvalign, (list, tuple, np.ndarray)):
            assert len(modul) == len(modvalign), 'modvalign must be scalar or same size as modul.'
            imodvalign = modvalign
        else:
            imodvalign = [modvalign] * len(modul)
    else:
        imodvalign = ['center'] * len(modul)

    # Prepare annotations
    if type(saname) is list:
        isaname = saname[:]
    else:
        isaname = [saname]
    if type(modul) is list:
        ismod = modul[:]
    else:
        ismod = [modul]
    if usetex:
        imod = []
        for ii, i in enumerate(ismod):
            if r'\n' in i:
                ss = i.split(r'\n')
            else:
                ss = [i]
            ss = [ r'' + j.strip() for j in ss ]
            for j, s in enumerate(ss):
                ss[j] = r'$\mathrm{' + s + r'}$'
                if '-' in ss[j]:
                    ss[j] = ss[j].replace('-}$', '}$-')
                if ' ' in ss[j]:
                    ss[j] = ss[j].replace(' ', r'\ ')
                if "'" in isaname[j]:
                    ss[j] = ss[j].replace("'", r"}\\textrm{'}\mathrm{")
            imod.append(ss)
        ismod = imod
        comp = [ r'$\mathbf{' + i + r'}$' for i in comp ]
        for j in range(len(comp)):
            if "'" in comp[j]:
                comp[j] = comp[j].replace("'", r"}\\textrm{'}\mathbf{")
        for j, s in enumerate(isaname):
            isaname[j] = r'$\mathrm{' + s + r'}$'
            if '-' in isaname[j]:
                isaname[j] = isaname[j].replace('-}$', '}$-')
            if ' ' in isaname[j]:
                isaname[j] = isaname[j].replace(' ', r'\ ')
            if "'" in isaname[j]:
                isaname[j] = isaname[j].replace("'", r"}\\textrm{'}\mathrm{")
    else:
        imod = []
        for i in ismod:
            if '\n' in i:
                ss = i.split('\n')
            else:
                ss = [i]
            ss = [ r'' + j.strip() for j in ss ]
            imod.append(ss)
        ismod = imod

    # numbers
    nmod   = len(ismod)  # number modules
    nparam = sum(pmod)   # number of parameters
    param  = np.arange(nparam) + 1
    assert nparam == npar, 'si.shape[1] must be sum(pmod).'
    if star is not None:
        assert nparam == np.size(star), 'There must be the same number of star indications as parameters.'

    # colours
    if dobw:
        c = np.linspace(0.2, 0.85, nmod)
        c = np.ones(nmod) * 0.7
        c = [ str(i) for i in c ]
    else:
        from pyjams.jams.brewer import get_brewer
        if (cmod == 'mhm'):
            c = [get_brewer('rdylbu11', rgb=True)[0],  # interception
                 get_brewer('rdylbu11', rgb=True)[1],  # snow
                 get_brewer('rdylbu11', rgb=True)[2],  # soil moisture
                 get_brewer('rdylbu11', rgb=True)[2],  # soil moisture
                 get_brewer('rdylbu11', rgb=True)[3],  # direct runoff
                 get_brewer('rdylbu11', rgb=True)[4],  # Evapotranspiration
                 get_brewer('rdylbu11', rgb=True)[6],  # interflow
                 get_brewer('rdylbu11', rgb=True)[7],  # percolation
                 get_brewer('rdylbu11', rgb=True)[8],  # routing
                 get_brewer('rdylbu11', rgb=True)[9]]  # geology
        elif (cmod == 'noah'):
            c = [get_brewer('reds8', rgb=True)[3], #  Radiation
                 get_brewer('ylorbr4', rgb=True)[2], #  SoilPhysiology
                 get_brewer('ylorrd8', rgb=True)[2], #  Transfer
                 get_brewer('greens4', rgb=True)[2], #  VegetationStructure
                 get_brewer('bugn4', rgb=True)[2], #  Physiology
                 get_brewer('blues4', rgb=True)[2], #  SoilWater
                 get_brewer('blues6', rgb=True)[5], #  Runoff
                 get_brewer('greys8', rgb=True)[2], #  SnowEnergy
                 get_brewer('greys8', rgb=True)[4], #  SoilEnergy
                 get_brewer('greys8', rgb=True)[5], #  Carbon
                 get_brewer('rdpu5', rgb=True)[2], #  VOC
                 get_brewer('reds8', rgb=True)[5], #  Input*
                 get_brewer('reds8', rgb=True)[3], #  Radiation*
                 get_brewer('ylorbr4', rgb=True)[2], #  SoilPhysiology*
                 get_brewer('ylorrd8', rgb=True)[2], #  Transfer*
                 get_brewer('greens4', rgb=True)[2], #  VegetationStructure*
                 get_brewer('bugn4', rgb=True)[2], #  Physiology*
                 get_brewer('blues4', rgb=True)[2], #  SoilWater*
                 get_brewer('blues6', rgb=True)[5], #  Runoff*
                 get_brewer('blues4', rgb=True)[3], #  SnowWater*
                 get_brewer('greys8', rgb=True)[2], #  SnowEnergy*
                 get_brewer('greys8', rgb=True)[4], #  SoilEnergy*
                 get_brewer('greys8', rgb=True)[5], #  Carbon*
                 get_brewer('greys9', rgb=True)[6]] #  ????
        else:
            if cmap is None:
                raise ValueError("cmod can be only 'mhm' or 'noah', otherwise cmap has to be given.")

    if cmap is not None:
        c = cmap

    # conversion factor from parameter number to radian
    n2rad = 2. * np.pi / (nparam + space4yaxis)

    # -------------------------------------------------------------------------
    # Plot
    #

    # Axes have to be defined externally
    # sub = fig.add_axes(jams.position(nrow,ncol,iplot,hspace=hspace,vspace=vspace), polar=True)
    sub.set_theta_zero_location('N') # 0 is North
    sub.set_theta_direction(-1)      # clockwise

    xlim = [0, 2. * np.pi]
    ylim = [-bpar * ymax, ymax]

    # coloured modules
    mleft   = (space4yaxis + np.cumsum([0] + pmod[:-1]) + fwm) * n2rad  # left start at space4yaxis
    mheight = np.ones(nmod) * ymax * (1.-bmod)                     # height from bmod*ymax to ymax
    mwidth  = (np.array(pmod) - 2. * fwm) * n2rad                    # width is number of params per module
    iidx = np.where(np.array(pmod) > 0)
    bar1    = sub.bar(mleft[iidx], mheight[iidx], mwidth[iidx], bottom=bmod*ymax,
                      color=np.array(c)[iidx], alpha=alphamod,
                      linewidth=0)

    # module and class labels
    xm = mleft + 0.5 * mwidth
    for i in range(nmod):
        if (pmod[i] > 0):
            # module
            nm = len(ismod[i])
            for j, m in enumerate(ismod[i]):
                mlabel12 = (ylabel2 - ylabel1) * 1. / float(nm)
                if (xm[i] < 0.5 * np.pi) | (xm[i] > 1.5 * np.pi):
                    ylab = ylabel2 - (j + 1) * mlabel12
                    rot  = np.rad2deg(-xm[i])
                else:
                    ylab = ylabel2 - (nm - j) * mlabel12
                    rot  = np.rad2deg(-xm[i]) + 180.
                label = sub.text(xm[i], ylab * ymax, m, rotation=rot,
                                 fontsize=ntextsize,
                                 horizontalalignment=imodhalign[i],
                                 verticalalignment=imodvalign[i])
            # class
            if docomp:
                label = sub.text(xm[i], ylabel2 * ymax, comp[i],
                                 fontsize=mtextsize, fontweight='bold',
                                 horizontalalignment='center',
                                 verticalalignment='center')
                if (xm[i] < 0.5 * np.pi) | (xm[i] > 1.5 * np.pi):
                    label.set_rotation(np.rad2deg(-xm[i]))
                else:
                    label.set_rotation(np.rad2deg(-xm[i])+180.)

    # y-axis
    # grid
    nyticks = 5
    dyy     = np.linspace(0, ymax, nyticks)
    gy      = np.delete(dyy[1:-1], nyticks // 2 - 1)
    npoints = 100
    gxx     = np.linspace(0, 2. * np.pi, npoints)
    for i in range(gy.size):
        grid = sub.plot(gxx, np.ones(npoints) * gy[i], linestyle='--',
                        color=mcol, linewidth=glwidth)
    # in "axis normal coordinates" for rectangular ticks, etc.
    dyy    = np.array([0, ymax])
    yy     = ((1. + 2. * bpar) * ymax + dyy) / ((2. + 2. * bpar) * ymax)
    yaxis  = sub.plot([0.5, 0.5], yy, transform=sub.transAxes,
                      linestyle='-', linewidth=alwidth, color=acol)
    nyticks = 5
    xx      = np.ones(nyticks)*0.5
    dyy     = np.linspace(0,ymax,nyticks)
    yy      = ((1.+2.*bpar)*ymax+dyy)/((2.+2.*bpar)*ymax)
    ytickwidth = 0.015
    for i in range(nyticks):
        yticks = sub.plot([xx[i],xx[i]+ytickwidth], [yy[i],yy[i]], transform=sub.transAxes,
                          linestyle='-', linewidth=alwidth, color=acol)
    # y-tickmarks at top and bottom
    tx = xx[0]+1.5*ytickwidth
    ty = yy[0]
    if usetex:
        tt = r'$\mathrm{0}$'
    else:
        tt = '0'
    label = sub.text(tx, ty, tt, transform=sub.transAxes,
                     fontsize=ytextsize, horizontalalignment='left', verticalalignment='bottom')
    bx = xx[-1]+1.5*ytickwidth
    by = yy[-1]
    if usetex:
        bt = r'$\mathrm{'+str(ymax)+'}$'
    else:
        bt = str(ymax)
    label = sub.text(bx, by, bt, transform=sub.transAxes,
                     fontsize=ytextsize, horizontalalignment='left', verticalalignment='top')

    # param numbers in center == x-tickmarks
    xticknames = [ str(i) for i in param[1::4] ]
    if usetex:
        xticknames = [ r'$\mathrm{'+i+'}$' for i in xticknames ]
    shiftx  = np.floor(1./(nsi+1)*10.)/10.
    pleft   = (param+(space4yaxis-1)+shiftx-0.5*fwb[nsi-1]+(nsi-1)/2.*fwb[nsi-1])*n2rad # center at middle of all stacks
    pwidth  = np.ones(nparam)*fwb[nsi-1]*n2rad
    tx = pleft[1::4]+0.5*pwidth[1::4]
    ty = -np.ones(tx.size)*bplabel*ymax
    for i in range(tx.size):
        if (tx[i] < np.pi):
            rot = np.rad2deg(-tx[i])+90.
        else:
            rot = np.rad2deg(-tx[i])-90.
        label = sub.text(tx[i], ty[i], xticknames[i], rotation=rot, fontsize=ptextsize,
                         horizontalalignment='center', verticalalignment='center')

    # Index stacks
    for n in range(nsi):
        # params on bottom
        pleft = (param+(space4yaxis-1)+shiftx-0.5*fwb[nsi-1]+n*fwb[nsi-1])*n2rad # center at 0.5 from param number
        pheight = isi[n,:]
        bar2    = sub.bar(pleft, pheight, pwidth, bottom=0.,
                          facecolor=mcols[2*n], hatch=hatches[2*n], edgecolor=lcols[2*n],
                          linewidth=plwidth)
        if sti is not None:
            # params on top
            pheight = idsi[n,:]
            pbottom = isi[n,:]
            bar2    = sub.bar(pleft, pheight, pwidth, bottom=pbottom,
                              facecolor=mcols[2*n+1], hatch=hatches[2*n+1], edgecolor=lcols[2*n+1],
                              linewidth=plwidth)
        if stierr is not None:
            # error bars
            xx      = pleft+0.5*pwidth
            if sti is not None:
                yy      = isti[n,:]
            else:
                yy      = isi[n,:]
            perr    = istierr[n,:]
            pewidth = 0.1*n2rad
            for i in range(xx.size):
                yerrm = sub.plot([xx[i],xx[i]], [yy[i]-perr[i],yy[i]+perr[i]], # middle line
                                 linestyle='-', linewidth=elwidth, color=ecol)
                yerrl = sub.plot([xx[i]-pewidth,xx[i]+pewidth], [yy[i]-perr[i],yy[i]-perr[i]], # lower bar
                                 linestyle='-', linewidth=elwidth, color=ecol)
                yerru = sub.plot([xx[i]-pewidth,xx[i]+pewidth], [yy[i]+perr[i],yy[i]+perr[i]], # upper bar
                                 linestyle='-', linewidth=elwidth, color=ecol)

    # Stars
    if star is not None:
        pleft = (param+(space4yaxis-1)+shiftx-0.5*fwb[nsi-1]+(nsi-1)/2.*fwb[nsi-1])*n2rad # same as xticklabels
        xstar = (pleft+0.5*pwidth)[star.astype(np.bool)]
        ystar = np.ones(xstar.shape[0]) * ymax * dystar
        star_mucm = sub.plot(xstar, ystar, linestyle='none',
                             marker=ssym, markeredgecolor=scol, markerfacecolor=sfcol,
                             markersize=ssize, markeredgewidth=swidth)

    # subplot numbering
    if doabc and (iplot is not None):
        from pyjams.abc2plot import abc2plot
        abc2plot(sub, dxabc, dyabc, iplot, transform=sub.transAxes,
                 lower=True, parenthesis='close',
                 bold=True, xlarge=True,
                 mathrm=True, usetex=usetex,
                 horizontalalignment='right', verticalalignment='bottom')

    # Signature
    if dosig:
        from pyjams.signature2plot import signature2plot
        signature2plot(sub, dxsig, dysig, sig, transform=sub.transAxes,
                       italic=True, small=True, mathrm=True, usetex=usetex)

    # General settings
    sub.set_xlim(xlim)
    sub.set_ylim(ylim)     # start at -bpar to get offset for bars
    sub.grid(False)
    sub.set_frame_on(False)
    sub.set_xticks([])
    sub.set_xticklabels([])
    sub.set_yticks([])
    sub.set_yticklabels([])

    if dolegend:
        # Fake subplot for legend and numbering
        spos = sub.get_position()
        fig  = sub.get_figure()
        lsub = fig.add_axes([spos.x0+llxbbox*spos.width, spos.y0+llybbox*spos.height, 0.5*spos.width, 0.1*spos.height])

        x1, y1 = lsub.transData.transform_affine(np.array([0,0]))
        x2, y2 = lsub.transData.transform_affine(np.array([1,1]))
        dpi = lsub.figure.dpi                         # pixels per inch
        import matplotlib as mpl
        ss  = mpl.rcParams['font.size']               # text size in points: 1 pt = 1/72 inch
        shifty = 1.0 * ss/72.*float(dpi)/float(y2-y1) # shift by 1.0 of textsize
        for n in range(nsi):
            dy1 = 1. - (n+1.)   * shifty
            dy2 = 1. - (n+0.01) * shifty
            # colour bar
            lsub.fill_between([0,0.3],   [dy1,dy1], [dy2,dy2], linewidth=plwidth, clip_on=False,
                              facecolor=mcols[2*n],   edgecolor=lcols[2*n], hatch=hatches[2*n])
            dx1 = 0.35
            if sti is not None:
                lsub.fill_between([0.3,0.6], [dy1,dy1], [dy2,dy2], linewidth=plwidth, clip_on=False,
                                  facecolor=mcols[2*n+1], edgecolor=lcols[2*n+1], hatch=hatches[2*n+1])
                dx1 = 0.65
            # Annotation to the right
            lsub.text(dx1, 0.5*(dy1+dy2), isaname[n], fontsize=ntextsize,
                      horizontalalignment='left', verticalalignment='center')
        # Annotation on top
        if type(indexname) is list:
            iindexname = indexname[:]
        else:
            iindexname = [indexname]
        t = iindexname[0]
        dy2 = 1. - 0.01 * shifty
        lsub.text(0.15, dy2+0.05, t, fontsize=ntextsize,
                  horizontalalignment='center', verticalalignment='bottom')
        if sti is not None:
            t = iindexname[1]
            lsub.text(0.45, dy2+0.05, t, fontsize=ntextsize,
                      horizontalalignment='center', verticalalignment='bottom')
        # Star
        if star is not None:
            if sti is not None:
                dxstar1 = 0.3
            else:
                dxstar1 = 0.15
            dystar1 = 1. - (2.*nsi+1.01)/2. * shifty
            lsub.plot([dxstar1], [dystar1], linestyle='none', clip_on=False,
                      marker=ssym, markeredgecolor=scol, markerfacecolor=sfcol,
                      markersize=ssize, markeredgewidth=swidth)
            lsub.text(dx1, dystar1, isaname[nsi], fontsize=ntextsize,
                      horizontalalignment='left', verticalalignment='center')

        lsub.set_xlim([0,1])
        lsub.set_ylim([0,1])

        lsub.set_title('')
        lsub.set_xlabel('')
        lsub.set_ylabel('')
        lsub.set_xticks([])
        lsub.set_yticks([])
        lsub.set_axis_off()


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # nn = 52
    # ymax = 0.7
    # si  = np.arange(nn)/np.float(nn-1) * ymax * 0.5
    # sti = np.arange(nn)/np.float(nn-1) * ymax
    # stierr = 0.1*sti

    # pngbase = 'clockplot_'
    # pdffile = '' # 'clockplot.pdf'
    # usetex  = True

    # if (pdffile != '') & (pngbase != ''):
    #     print('\nError: PDF and PNG are mutually exclusive. Only either -p or -g possible.\n')
    #     parser.print_usage()
    #     import sys
    #     sys.exit()

    # if (pdffile == ''):
    #     if (pngbase == ''):
    #         outtype = 'x'
    #     else:
    #         outtype = 'png'
    # else:
    #     outtype = 'pdf'

    # # Main plot
    # nrow        = 3           # # of rows of subplots per figure
    # ncol        = 2           # # of columns of subplots per figure
    # hspace      = 0.05        # x-space between subplots
    # vspace      = 0.09        # y-space between subplots
    # right       = 0.9         # right space on page
    # textsize    = 6           # standard text size
    # dxabc       = 2           # % of (max-min) shift to the right from left y-axis for a,b,c,... labels
    # dyabc       = 0.5           # % of (max-min) shift up from lower x-axis for a,b,c,... labels
    # dxsig       = 1.23        # % of (max-min) shift to the right from left y-axis for a,b,c,... labels
    # dysig       = -0.05       # % of (max-min) shift up from lower x-axis for a,b,c,... labels

    # lwidth      = 1.5         # linewidth
    # elwidth     = 1.0         # errorbar line width
    # alwidth     = 1.0         # axis line width
    # glwidth     = 0.5         # grid line width
    # msize       = 1.0         # marker size
    # mwidth      = 1.0         # marker edge width
    # mcol1       = '0.0'       # primary marker colour
    # mcol2       = '0.4'                     # secondary
    # mcol3       = '0.0' # third
    # mcols       = ['0.0', '0.4', '0.4', '0.7', '0.7', '1.0']
    # lcol1       = colours('blue')   # primary line colour
    # lcol2       = '0.4'
    # lcol3       = '0.0'
    # lcols       = ['None', 'None', 'None', 'None', 'None', '0.0']
    # hatches     = [None, None, None, None, None, '//']

    # # Legend
    # llxbbox     =  0.0        # x-anchor legend bounding box
    # llybbox     = 1.15       # y-anchor legend bounding box
    # llrspace    = 0.          # spacing between rows in legend
    # llcspace    = 1.0         # spacing between columns in legend
    # llhtextpad  = 0.4         # the pad between the legend handle and text
    # llhlength   = 1.5         # the length of the legend handles
    # frameon     = False       # if True, draw a frame around the legend. If None, use rc

    # # PNG
    # dpi           = 600
    # transparent   = False
    # bbox_inches   = 'tight'
    # pad_inches    = 0.035

    # # Clock options
    # ymax = 0.8
    # ntextsize   = 'medium'       # normal textsize
    # # modules
    # bmod        = 0.5            # fraction of ymax from center to start module colours
    # alphamod    = 0.7            # alpha channel for modules
    # fwm         = 0.05           # module width to remove at sides
    # ylabel1     = 1.15           # position of module names
    # ylabel2     = 1.35           # position of class names
    # mtextsize   = 'large'        # 1.3*textsize # textsize of module labels
    # # bars
    # bpar        = 0.4            # fraction of ymax from center to start with parameter bars
    # fwb         = [0.7,0.4,0.3]  # width of bars
    # plwidth     = 0.5
    # # parameters in centre
    # bplabel     = 0.1            # fractional distance of ymax of param numbers in centre from 0-line
    # ptextsize   = 'medium'       # 'small' # 0.8*textsize # textsize of param numbers in centre
    # # yaxis
    # space4yaxis = 2              # space for y-axis (integer)
    # ytextsize   = 'medium'       # 'small' # 0.8*textsize # textsize of y-axis

    # import matplotlib as mpl
    # if (outtype == 'pdf'):
    #     mpl.use('PDF') # set directly after import matplotlib
    #     import matplotlib.pyplot as plt
    #     from matplotlib.backends.backend_pdf import PdfPages
    #     # Customize: http://matplotlib.sourceforge.net/users/customizing.html
    #     mpl.rc('ps', papersize='a4', usedistiller='xpdf') # ps2pdf
    #     mpl.rc('figure', figsize=(8.27,11.69)) # a4 portrait
    #     if usetex:
    #         mpl.rc('text', usetex=True)
    #     else:
    #         #mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    #         mpl.rc('font',**{'family':'serif','serif':['times']})
    #     mpl.rc('text.latex', unicode=True)
    # elif (outtype == 'png'):
    #     mpl.use('Agg') # set directly after import matplotlib
    #     import matplotlib.pyplot as plt
    #     mpl.rc('figure', figsize=(8.27,11.69)) # a4 portrait
    #     if usetex:
    #         mpl.rc('text', usetex=True)
    #     else:
    #         #mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    #         mpl.rc('font',**{'family':'serif','serif':['times']})
    #     mpl.rc('text.latex', unicode=True)
    #     mpl.rc('savefig', dpi=dpi, format='png')
    # else:
    #     import matplotlib.pyplot as plt
    #     mpl.rc('figure', figsize=(4./5.*8.27,4./5.*11.69)) # a4 portrait
    # mpl.rc('font', size=textsize)
    # mpl.rc('lines', linewidth=lwidth, color='black')
    # mpl.rc('axes', linewidth=alwidth, labelcolor='black')
    # mpl.rc('path', simplify=False) # do not remove

    # if (outtype == 'pdf'):
    #     print('Plot PDF ', pdffile)
    #     pdf_pages = PdfPages(pdffile)
    # elif (outtype == 'png'):
    #     print('Plot PNG ', pngbase)
    # else:
    #     print('Plot X')

    # ifig = 0
    # ifig += 1
    # iplot = 0
    # print('Plot - Fig ', ifig)
    # fig = plt.figure(ifig)

    # iplot += 1
    # sub    = fig.add_axes(position(nrow,ncol,iplot,hspace=hspace,vspace=vspace), polar=True)
    # clockplot(sub, si, sti, usetex=usetex, dolegend=True)

    # iplot += 1
    # sub    = fig.add_axes(position(nrow,ncol,iplot,hspace=hspace,vspace=vspace), polar=True)
    # clockplot(sub, si, sti, stierr, llybbox=1.00, usetex=usetex)

    # iplot += 1
    # sub    = fig.add_axes(position(nrow,ncol,iplot,hspace=hspace,vspace=vspace), polar=True)
    # clockplot(sub, [si,si[::-1]], [sti,sti[::-1]], [stierr,stierr[::-1]], llybbox=1.1, doabc=True, dolegend=True)

    # if (outtype == 'pdf'):
    #     pdf_pages.savefig(fig)
    #     plt.close(fig)
    # elif (outtype == 'png'):
    #     pngfile = pngbase+"{0:04d}".format(ifig)+".png"
    #     fig.savefig(pngfile, transparent=transparent, bbox_inches=bbox_inches, pad_inches=pad_inches)
    #     plt.close(fig)

    # if (outtype == 'pdf'):
    #     pdf_pages.close()
    # elif (outtype == 'png'):
    #     pass
    # else:
    #     plt.show()
