#!/usr/bin/env python
# coding: utf-8

# In[1]:


#
# full_analysis_scoring_for_new_dataset.py
#
# Run trained models on a new data set for which spectrograms have already
# been generated.
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
#

#%% Imports

import pandas as pd
import numpy as np
import glob
import os
import cv2
from keras.models import model_from_json


# In[2]:


current_dir = "/home/roberto/notebooks/WFQC/"

model_dir = current_dir + "Model/"
data_dir = current_dir + "Data/"
spectrogram_dir = data_dir + "Extracted_Spectrogram_Full_Analysis/" 
output_dir = current_dir + "Output/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# In[3]:


spectrogram_filenames = glob.glob(spectrogram_dir + '/*.png')


# In[4]:



with open(model_dir + 'cnn_architecture_all_data.json', 'r') as f:
    model_cnn = model_from_json(f.read())
model_cnn.load_weights(model_dir + 'cnn_weights_all_data.h5')

with open(model_dir + 'vgg16_architecture_all_data.json', 'r') as f:
    model_vgg16 = model_from_json(f.read())
model_vgg16.load_weights(model_dir + 'vgg16_weights_all_data.h5')

with open(model_dir + 'ResNet50_architecture_all_data.json', 'r') as f:
    model_ResNet50 = model_from_json(f.read())
model_ResNet50.load_weights(model_dir + 'ResNet50_weights_all_data.h5')

with open(model_dir + 'DenseNet121_architecture_all_data.json', 'r') as f:
    model_DenseNet121 = model_from_json(f.read())
model_DenseNet121.load_weights(model_dir + 'DenseNet121_weights_all_data.h5')


# In[5]:



ncol, nrow = 300, 300

full_analysis_score = pd.DataFrame()
full_analysis_score['spectrogram_filename'] = spectrogram_filenames
full_analysis_score['waveform_filename'] = ''
full_analysis_score['spectrogram_start_second'] = ''
full_analysis_score['predicted_probability'] = 0.0


# In[13]:



opt_weights = pd.read_excel(output_dir + 'opt_weights.xlsx', header = None, engine='openpyxl')[0].values.tolist()


# In[14]:


print(opt_weights)


# In[25]:


res_data = []

for index, row in full_analysis_score.iterrows():
    if (index % 10000 == 0):
        print([index,row])
    simplefile=os.path.basename(row['spectrogram_filename'])
    sta,chan,sub,sti=simplefile.split('_')
    stim,ext=sti.split('.')
    stim=stim[1:]
    #print(stim)
    waveform_file=sub+'/'+sta+'.'+chan+'.vel'
    #print(waveform_file)
    img = cv2.imread(row['spectrogram_filename'])
    img = cv2.resize(img, (ncol, nrow))
    img_reshaped = []
    img_reshaped.append(img)
    predict_prob_cnn = model_cnn.predict(np.asarray(img_reshaped) / 255.0).tolist()[0][0]
    predict_prob_vgg16 = model_vgg16.predict(np.asarray(img_reshaped) / 255.0).tolist()[0][0]
    predict_prob_ResNet50 = model_ResNet50.predict(np.asarray(img_reshaped) / 255.0).tolist()[0][0]
    predict_prob_DenseNet121 = model_DenseNet121.predict(np.asarray(img_reshaped) / 255.0).tolist()[0][0]
    predicted_probability = sum([x*y for x,y in zip([predict_prob_cnn, predict_prob_vgg16, predict_prob_ResNet50, predict_prob_DenseNet121], opt_weights)]) 
        ## the opmized weight for each model was computed in previous step
    res_data.append([simplefile,waveform_file,stim,predicted_probability])


# In[26]:


df = pd.DataFrame(res_data, columns=['Filename', 'Waveform', 'Initial_time','Prob'])


# In[27]:


df.to_excel(output_dir + 'full_analysis_ouptut_predicted_scores.xlsx', index=False,engine='openpyxl')


# In[28]:


df


# In[32]:


df.sort_values(by=['Prob'],ascending=False)


# In[ ]:




