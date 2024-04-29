#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
from py_eddy_tracker.dataset.grid import RegularGridDataset
from matplotlib import pyplot as plt
import numpy as np
import os
import sys
from netCDF4 import Dataset
from time import ctime

dirin = sys.argv[1]
dirout = sys.argv[2]
filepattern = np.str(sys.argv[3])
fmt = np.str(sys.argv[4])
vname = sys.argv[5]
d1 = sys.argv[6]
d2 = sys.argv[7]
tile = sys.argv[8]
do_save_nc = np.int32(sys.argv[9])
do_plot_fig = np.int32(sys.argv[10])
x_name = sys.argv[11]
y_name = sys.argv[12]
fp = sys.argv[13]
wave_length = np.float32(sys.argv[14])
radius_MIN = np.float32(sys.argv[15])
amplitude_MIN = np.float32(sys.argv[16])

if vname == 'sla':
    v1n, v2n = 'ugosa', 'vgosa'
elif vname == 'adt':
    v1n, v2n = 'ugos', 'vgos'
else:
    raise ValueError('check vname !!!')
    
dt_now = dt.datetime.now()
dt_now_str = dt_now.strftime('%Y-%m-%dT%H%M')
date_Start = dt.datetime.strptime(d1, fmt)
date_End = dt.datetime.strptime(d2, fmt)
datelist = np.arange(date_Start, 
                     date_End+dt.timedelta(days=1),
                     dt.timedelta(days=1),
                     dtype=dt.datetime)
dirAC = dirout+'{:}.AC.{:}'.format(vname, tile)
dirCC = dirout+'{:}.CC.{:}'.format(vname, tile)
dirfig = dirout+'{:}.jpgs.{:}'.format(vname, tile)
filetmp = dirout+'tmp.{:}.nc'
filetmp = filetmp.format(dt.datetime.now().strftime('%y%m%dT%H%M'))

# print info

info = []
info.append('======= {:} ======='.format(ctime()))
info.append('{:16s}: {:}'.format('Input Dir',dirin))
info.append('{:16s}: {:}'.format('Output Dir', dirout))
info.append('{:16s}: {:}'.format('File Pattern', filepattern))
info.append('{:16s}: {:}'.format('Tile', tile))
info.append('{:16s}: {:}'.format('fmt', fmt))
info.append('{:16s}: {:}'.format('Variable', vname))
info.append('{:16s}: {:}'.format('X name', x_name))
info.append('{:16s}: {:}'.format('Y name', y_name))
info.append('{:16s}: from {:} to {:}'.format('Dates',
                                             date_Start.strftime(fmt),
                                             date_End.strftime(fmt)))
info.append('{:16s}: {:}'.format('Save NC', do_save_nc==1))
info.append('{:16s}: {:}'.format('Plot Figs', do_plot_fig==1))
info.append('{:16s}: {:}'.format('Tmp NC', filetmp))
info.append('{:16s}: {:}km'.format('Wave Length', wave_length))
info.append('{:16s}: {:}km'.format('Radius MIN', radius_MIN))
info.append('{:16s}: {:}m'.format('Amplitude MIN', amplitude_MIN))
for i in info:
    print(i)
while(True):
    print('!!! NOTE !!! Please confirm the above information.')
    in_content = input('Continue/Exit [Y/N]: ')
    if in_content == 'N':
        print('{:} Exit'.format(ctime()))
        exit(0)
    elif in_content == 'Y':
        if do_save_nc == 1:
            jAC = os.path.exists(dirAC)
            if jAC:
                print('!!! WARNING !!! {:} exists'.format(dirAC))
                while(True):
                    dirAC_ic = input('Overwrite/Exit [Y/N]: ')
                    if dirAC_ic == 'N':
                        print('{:} Exit'.format(ctime()))
                        exit(0)
                    elif dirAC_ic == 'Y':
                        os.system('rm -r {:}'.format(dirAC))
                        os.system('mkdir {:}'.format(dirAC))
                        print('{:12s}: {:}'.format('Dir Re-Created', dirAC))
                        break
                    else:
                        print('Wrong input, Y/N only')
            else:
                os.system('mkdir {:}'.format(dirAC))
                print('{:12s}: {:}'.format('Dir Created', dirAC))
            jCC = os.path.exists(dirCC)
            if jCC:
                print('!!! WARNING !!! {:} exists'.format(dirCC))
                while(True):
                    dirCC_ic = input('Overwrite/Exit [Y/N]: ')
                    if dirCC_ic == 'N':
                        print('{:} Exit'.format(ctime()))
                        exit(0)
                    elif dirCC_ic == 'Y':
                        os.system('rm -r {:}'.format(dirCC))
                        os.system('mkdir {:}'.format(dirCC))
                        print('{:12s}: {:}'.format('Dir Re-Created', dirCC))
                        break
                    else:
                        print('Wrong input, Y/N only')
            else:
                os.system('mkdir {:}'.format(dirCC))
                print('{:12s}: {:}'.format('Dir Created', dirCC))
        if do_plot_fig == 1:
            jfg = os.path.exists(dirfig)
            if jfg:
                print('!!! WARNING !!! {:} exists'.format(dirfig))
                while(True):
                    dirfig_ic = input('Overwrite/Exit [Y/N]: ')
                    if dirfig_ic == 'N':
                        print('{:} Exit'.format(ctime()))
                        exit(0)
                    elif dirfig_ic == 'Y':
                        os.system('rm -r {:}'.format(dirfig))
                        os.system('mkdir {:}'.format(dirfig))
                        print('{:12s}: {:}'.format('Dir Re-Created', dirfig))
                        break
                    else:
                        print('Wrong input, Y/N only')
            else:
                os.system('mkdir {:}'.format(dirfig))
                print('{:12s}: {:}'.format('Dir Created', dirfig))
        break
    else:
        print('Wrong input, Y/N only')

fw = 190
nlef, nrig = 10, 15
ntop, nbot = 10, 5
nha = (fw - nlef*2 - nrig)/2
nva = nha * 28 / 30
fh = nbot + ntop + nva
ha, va = nha/fw, nva/fh
xloc = [nlef/fw, (nlef*2+nha)/fw]
cloc = [(fw-nrig+2)/fw, nbot/fh, 2/fw, va]

def plotax1(ax, h,
            xlim=[70, 100],
            ylim=[-5, 23],
            vmin=-0.3, vmax=0.3,
            var='sla',
            uname='u',
            vname='v',
            title='date',
            cmap='coolwarm',
            scale=10,
            sstep=2):
    
    im = h.display(ax, var, vmin=vmin, vmax=vmax, cmap=cmap)
    u, v = h.grid(uname).T, h.grid(vname).T
    ax.quiver(h.x_c[::sstep], h.y_c[::sstep], 
              u[::sstep,::sstep], 
              v[::sstep,::sstep], 
              scale=scale, pivot='mid', color='gray')
    ax.text(0.01, 1.02, title, transform=ax.transAxes)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.tick_params(axis='both',pad=0.5,length=2)

    return im

def plotax2(ax, h, a, c,
            xlim=[70, 100],
            ylim=[-5, 23],
            vmin=-0.3, vmax=0.3,
            var='sla',
            title='date',
            cmap='coolwarm',
            show_circle=False):
    
    kwargs_a = dict(lw=0.5, 
                    label="AC ({nb_obs})", 
                    color="b")
    kwargs_c = dict(lw=0.5, 
                    label="CC ({nb_obs})", 
                    color="r")
    
    im = h.display(ax, var, vmin=vmin, vmax=vmax, cmap=cmap)
    if show_circle:
        a.circle_contour()
        c.circle_contour()
    a.display(ax, **kwargs_a)
    c.display(ax, **kwargs_c)
    ax.legend(loc='upper left')
    ax.text(0.01, 1.02, title, transform=ax.transAxes)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.tick_params(axis='both',pad=0.5,length=2)

    return im

for date in datelist:
    datestr = date.strftime(fmt)
    print('-- processing {:}'.format(datestr))
    filein = dirin+'{:}/{:}'.format(date.year,
                                    filepattern.replace(fp, datestr))
#    filetmp = dirout+'tmp.{:}.nc'
#    filetmp = filetmp.format(dt.datetime.now().strftime('%y%m%dT%H%M'))
    cmd = ('cdo -s -b 32 -f nc copy -sellonlatbox,70,100,-5,23 ' +
           '{:} '.format(filein) +
           '{:}'.format(filetmp))
    os.system(cmd)
    h = RegularGridDataset(filetmp,
                           x_name,
                           y_name,
                           centered=True)
    h.copy(vname, vname+'_high')
    h.bessel_high_filter(vname+'_high',
                         wave_length=wave_length,
                         order=1)
    a, c = h.eddy_identification(vname+'_high', v1n, v2n, date,
                                step=0.002,
                                shape_error=55)
    a_req = a.extract_with_mask(a.radius_e > radius_MIN)
    a_req = a_req.extract_with_mask(a_req.amplitude > amplitude_MIN)
    c_req = c.extract_with_mask(c.radius_e > radius_MIN)
    c_req = c_req.extract_with_mask(c_req.amplitude > amplitude_MIN)

    savename = '{:}/PET.{:}.{:}.jpg'.format(dirfig,
                                            vname,
                                            datestr)
    if do_plot_fig == 1:
        fig = plt.figure(figsize=(fw/25.4, fh/25.4))
        ax1 = fig.add_axes([xloc[0], nbot/fh, ha, va])
        im = plotax1(ax1, h,
                     var=vname,
                     uname=v1n,
                     vname=v2n,
                     title=vname,
                     cmap='coolwarm')
        ax2 = fig.add_axes([xloc[1], nbot/fh, ha, va])
        im = plotax2(ax2, h, a_req, c_req,
                     var=vname+'_high',
                     title=vname+'_high',
                     show_circle=True,
                     cmap='coolwarm')
        ax2.text(1, 1.02, datestr, ha='right', transform=ax2.transAxes,
                fontsize='x-large')
        cax = plt.axes(cloc)
        cbar = plt.colorbar(im, cax=cax,)
        cbar.ax.tick_params(direction='in')
        plt.savefig(savename, dpi=600)
        plt.close()
    if do_save_nc == 1:
        with Dataset('{:}/AC.all.{:}.nc'.format(dirAC, datestr), 'w') as nc:
            a.to_netcdf(nc)
        with Dataset('{:}/AC.req.{:}.nc'.format(dirAC, datestr), 'w') as nc:
            a_req.to_netcdf(nc)
        with Dataset('{:}/CC.all.{:}.nc'.format(dirCC, datestr), 'w') as nc:
            c.to_netcdf(nc)
        with Dataset('{:}/CC.req.{:}.nc'.format(dirCC, datestr), 'w') as nc:
            c_req.to_netcdf(nc)
print('======= {:} DONE ======='.format(ctime()))
