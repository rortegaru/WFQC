#!/usr/bin/env python
# coding: utf-8

# In[98]:


import pandas as pd
from datetime import datetime, timedelta
import glob
import os
import wave
import pylab
#from matplotlib import plt
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import multiprocessing
import gc
import random


# In[99]:


current_dir = "/WFQC/"
data_dir = current_dir + "Data/"
seism_dir = os.path.join('/users','LUCADATA2')
output_spectrogram_dir = data_dir + "Extracted_Spectrogram_Full_Analysis/" 

if not os.path.exists(output_spectrogram_dir):
    os.makedirs(output_spectrogram_dir)


# In[100]:


seis_filenames = glob.glob(seism_dir + '/????')


# In[101]:


new_list=[]
i=1
for subs in seis_filenames:
    new2=os.path.basename(subs)
    velfil=glob.glob(subs+'/*.vel')
    for file in velfil:
        sub=os.path.basename(file)
        cont=os.path.dirname(file)
#
        last=os.path.basename(cont)
        new_list.append([i,sub,last])
        i=i+1


# In[102]:


df = pd.DataFrame(new_list, columns =['Num', 'Waveform','Sub']) 


# In[103]:


#print("Total number of New Audio Files to Score:", len(audio_filenames))


# In[111]:


def graph_spectrogram(wav_file, sub, serial):
#    fig=pyplot.figure(num=None, figsize=(19, 12))   
#    ax = pyplot.axes()
#    ax.set_axis_off()
    st = read(wav_file)
    tr=st[0]
    tr.normalize()
    fig = plt.figure()
    #ax = plt.Axes(fig,[0.,0.,.8,.8])
    ax = plt.Axes(fig,[0.1, 0.1, 0.7, 0.6])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_axis_off() 
    begin_TimeStamp=tr.stats.starttime
    audio_begin_TimeStamp=str(begin_TimeStamp.year)+'-'+str(begin_TimeStamp.month)+'-'+str(begin_TimeStamp.day)+'T'+str(begin_TimeStamp.hour)+'-'+str(begin_TimeStamp.minute)
    start_second=str(begin_TimeStamp.second)
    filename=output_spectrogram_dir + serial + '-' + audio_begin_TimeStamp + '-' + str(start_second)  + '.png'
#    print(filename)
    fig = tr.spectrogram(show=False,axes=ax)
#   # filename=output_spectrogram_dir+"AAA"+".png"
    plt.savefig(filename)
    plt.close()
 


# In[112]:


dirwave="/users/LUCADATA2/"


# In[113]:


def generate_spectrogram(i):
    try:
        Filenam = df.loc[i, 'Waveform'] 
        Sub = df.loc[i, 'Sub']
        Fileall=dirwave+Sub+'/'+Filenam
        serial,comp,ty=Filenam.split('.')
        serial=serial+'_'+comp+'_'+Sub+'_' 
#        print([serial,Sub,Fileall])
        return graph_spectrogram(Fileall,Sub,serial)
    except:
        pass


# In[114]:


num_cores = multiprocessing.cpu_count()


# In[115]:


nums=random.sample(range(1, len(df)), 10)


# In[116]:


from obspy.core import read, UTCDateTime


# In[117]:


output_spectrogram_dir = data_dir + "Extracted_Spectrogram_Full_Analysis/" 
#print(output_spectrogram_dir)


# In[118]:


#graph_spectrogram('/users/LUCADATA2/3814/AOI.HHN.vel','3814','AOI_HHN_3814_')


# In[119]:


spectrograms = Parallel(n_jobs=num_cores)(delayed(generate_spectrogram)(i) for i in (nums))


# In[ ]:




