#!/usr/bin/env python
# coding: utf-8
#
# model_vgg16.py
#
# Train the VGG-16 model
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
#

#%% Imports

from sklearn.model_selection import train_test_split
import csv
import numpy as np
import matplotlib.pyplot as plt

# Keras imports
from tensorflow.keras import models, layers, optimizers
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc


#%% Path configuration

current_dir = "/INGVDATA/WFQC/"
model_dir = current_dir + "Model/"
data_dir = current_dir + "Data/"
spectrogram_dir = data_dir + "Extracted_Spectrogram/"
output_spectrogram_vector_dir = "Output_Spectrogram_Vector/"


ncol, nrow = 300, 300

spectrograms_B_sample = np.load(data_dir + output_spectrogram_vector_dir + "spectrograms_B_sample_300_300.npy")
spectrograms_F_sample = np.load(data_dir + output_spectrogram_vector_dir + "spectrograms_F_sample_300_300.npy")
spectrograms_N_sample = np.load(data_dir + output_spectrogram_vector_dir + "spectrograms_N_sample_300_300.npy")

filenames_B_sample = []
with open(data_dir + output_spectrogram_vector_dir + "filenames_B_sample.csv", newline='') as f:
    for row in csv.reader(f):
        filenames_B_sample.append(row[0])

filenames_F_sample = []
with open(data_dir + output_spectrogram_vector_dir + "filenames_F_sample.csv", newline='') as f:
    for row in csv.reader(f):
        filenames_F_sample.append(row[0])

filenames_N_sample = []
with open(data_dir + output_spectrogram_vector_dir + "filenames_N_sample.csv", newline='') as f:
    for row in csv.reader(f):
        filenames_N_sample.append(row[0])
                    
spectrograms_B_train_validation, spectrograms_B_test, filenames_B_train_validation, filenames_B_test = train_test_split(spectrograms_B_sample, filenames_B_sample, test_size = 0.3, random_state = 1)
spectrograms_F_train_validation, spectrograms_F_test, filenames_F_train_validation, filenames_F_test = train_test_split(spectrograms_F_sample, filenames_F_sample, test_size = 0.3, random_state = 1)
spectrograms_N_train_validation, spectrograms_N_test, filenames_N_train_validation, filenames_N_test = train_test_split(spectrograms_N_sample, filenames_N_sample, test_size = 0.3, random_state = 1)

spectrograms_train_validation = np.concatenate((spectrograms_B_train_validation, spectrograms_F_train_validation, spectrograms_N_train_validation), axis=0)
labels_train_validation = np.array([1] * len(spectrograms_B_train_validation) + [0] * len(spectrograms_F_train_validation) + [0] * len(spectrograms_N_train_validation))

X_train, X_validation, y_train, y_validation = train_test_split(spectrograms_train_validation, labels_train_validation, test_size = 0.3, random_state = 1)

X_train = X_train / 255.0
X_validation = X_validation / 255.0



#print(X_train.shape)   
#print(X_validation.shape)   
#print(spectrograms_B_test.shape)   
#print(spectrograms_F_test.shape)
#print(spectrograms_N_test.shape)



from tensorflow.keras.applications import VGG16

# Load the VGG model
vgg_conv = VGG16(weights='imagenet', include_top=False, input_shape=(nrow, ncol, 3))

# Freeze the layers except the last 3 layers
for layer in vgg_conv.layers[:-3]:
    layer.trainable = False
 

for layer in vgg_conv.layers:
    print(layer, layer.trainable)

model = models.Sequential()
model.add(vgg_conv)

model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1, activation='sigmoid'))


# Compile the model
optimizer = optimizers.Adam(learning_rate=0.0001, decay=1e-7)
model.compile(loss='binary_crossentropy',optimizer=optimizer,metrics=['accuracy'])

# Show a summary of the model. Check the number of trainable parameters
model.summary()



model_history = model.fit(X_train, y_train, batch_size=64, epochs=15, verbose=1, validation_data=(X_validation, y_validation))



model.save_weights(model_dir +'vgg16_weights_all_data.h5')



plt.figure()
plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['training', 'validation'], loc='upper left')
plt.savefig(model_dir+"Model_TrainHist_Accuracy_VGG16.pdf")



# Save the model architecture
with open(model_dir + 'vgg16_architecture_all_data.json', 'w') as f:
    f.write(model.to_json())


del X_train
del X_validation
del spectrograms_B_train_validation
del spectrograms_F_train_validation
del spectrograms_N_train_validation
plt.figure()
spectrograms_B_test_predict = model.predict(spectrograms_B_test / 255.0)
spectrograms_B_test_wrong_predictions = [i for i,v in enumerate(spectrograms_B_test_predict) if v < 0.5]
plt.hist(spectrograms_B_test_predict)
#print(1 - len(spectrograms_B_test_wrong_predictions) / len(spectrograms_B_test_predict))

spectrograms_F_test_predict = model.predict(spectrograms_F_test / 255.0)
spectrograms_F_test_wrong_predictions = [i for i,v in enumerate(spectrograms_F_test_predict) if v > 0.5]
plt.hist(spectrograms_F_test_predict)
#print(1 - len(spectrograms_F_test_wrong_predictions) / len(spectrograms_F_test_predict)) 

spectrograms_N_test_predict = model.predict(spectrograms_N_test / 255.0)
spectrograms_N_test_wrong_predictions = [i for i,v in enumerate(spectrograms_N_test_predict) if v > 0.5]
plt.hist(spectrograms_N_test_predict)
plt.savefig(model_dir+"HistBFN_test.pdf")
#print(1 - len(spectrograms_N_test_wrong_predictions) / len(spectrograms_N_test_predict))

tp = len([i for i,v in enumerate(spectrograms_B_test_predict) if v >= 0.5])
fn = len([i for i,v in enumerate(spectrograms_B_test_predict) if v < 0.5])
tn = len([i for i,v in enumerate(spectrograms_F_test_predict) if v < 0.5])
fp = len([i for i,v in enumerate(spectrograms_F_test_predict) if v >= 0.5])
precision = tp / (tp + fp)
recall = tp / (tp + fn) 
accuracy = (tp + tn) / (tp + fp + tn + fn)

y_true = [1] * len(spectrograms_B_test_predict) + [0] * len(spectrograms_F_test_predict)
y_scores = spectrograms_B_test_predict.tolist() + spectrograms_F_test_predict.tolist()



# Calculate ROC and AUC
AUC = roc_auc_score(y_true, y_scores) 
#print('AUC: %.4f' % AUC)

# Calculate ROC Curve
plt.figure()
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
plt.plot(fpr, tpr, marker='.')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.savefig(model_dir+'True_Falsepositiv_VGG16.pdf',format='pdf')


# Calculate precision-recall curve
precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
precision_recall_auc = auc(recall, precision)
#print('Precesion Recall AUC: %.4f' % precision_recall_auc)

# Plot precision-recall curve
plt.figure()
plt.plot(recall, precision, marker='.')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.legend()
plt.savefig(model_dir+'Precision_VGG16.pdf', format='pdf')

