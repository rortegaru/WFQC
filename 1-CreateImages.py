#!/usr/bin/env python
# coding: utf-8


import glob
from obspy.core import read, UTCDateTime
from obspy.io.sac import SACTrace
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 

basedir="/home/roberto"
imagdir="IMAG"
waveformsdir="/INGVDATA/LUCA1"

foldername=os.path.join(basedir,imagdir)
def plotwaveyspec(spl1,fmin=0.1,fmax=20,filename='test.png'):
    from obspy.imaging.spectrogram import spectrogram
    beg = spl1[0].stats.starttime    
    end = spl1[0].stats.endtime
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.75, 0.7, 0.2]) #[left bottom width height]
    ax2 = fig.add_axes([0.1, 0.1, 0.7, 0.60], sharex=ax1)
    t = np.arange(spl1[0].stats.npts) / spl1[0].stats.sampling_rate
    ax1.plot(t, spl1[0].data, 'k')
    spl2 = spl1[0]
    fig = spl2.spectrogram(show=False, axes=ax2)
    mappable = ax2.images[0]
    ax2.set_ylim(fmin, fmax)
    plt.savefig(filename)
    plt.close()



rev=glob.glob(waveformsdir+'/????')
for dirs in rev:
    os.chdir(dirs)
    for file in glob.glob('*.vel'):
        st=read(file)
        stats=st[0].stats
        sac = SACTrace.read(file, headonly=True)
        dist=sac.dist
        t0=sac.t0
        a=sac.a
        b=sac.b
        #st.plot()
        tr=st[0]
        msg=tr.stats.station+" Dist = "+str(dist)
        sttime1=stats.starttime
        sttime2=sttime1+60
        st = st.slice(sttime1, sttime2)
        st[0].normalize()
        base=os.path.basename(file)
        rest=os.path.basename(dirs)          
        ofile3=foldername+'/'+'PM_'+rest+'_'+base+'.jpg'
        plotwaveyspec(st,filename=ofile3)
    os.chdir('..')

