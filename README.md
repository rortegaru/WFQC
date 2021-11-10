# WFQC  Programs for quality control using ANN's

## INSTALL

Install git and anaconda


Clone the repository

`git clone https://github.com/rortegaru/WFQC.git`


## CREATE THE ENVIRONMENT

`conda create --name wfqc --file requirements.txt`

Activate the environment

`conda activate wfqc`


## EXAMPLE DATASET

The example dataset is available at:

[SmallEvts_Part1.tar.gz](https://drive.google.com/file/d/1APb5U7axND7CCPqIlPkgyQVqfrfRup2Z/view?usp=sharing)

 
 We organized the directory tree in sac files with incremental order.
  

Each directory contains one event with multplie station.

Data may or may not be corrected by instrument, however we prefer to detrend and demean. Also we recommend to add location and P and S arrival, but it is not mandatory,

![](./filessubs.png)

##Trained weights and models

 We organized the workspace in a tree structure, in this case the Data are not seismic waveforms but spectrograms. In the notebook examples we show how to create the spectrograms and to write in the `Extracted_Spectrogram_Full_Analysis` 
folder.

```
.
├── Data
│   ├── Extracted_Spectrogram
│   ├── Extracted_Spectrogram_Augmented
│   ├── Extracted_Spectrogram_Full_Analysis
│   └── Output_Spectrogram_Vector
├── Model
│   ├── DenseNet121_architecture_all_data.json
│   ├── DenseNet121_weights_all_data.h5
│   ├── ResNet50_architecture_all_data.json
│   ├── ResNet50_weights_all_data.h5
│   ├── cnn_architecture_all_data.json
│   ├── cnn_weights_all_data.h5
│   ├── vgg16_architecture_all_data.json
│   └── vgg16_weights_all_data.h5
└── Output
    ├── opt_weights.xlsx
    └── output_predicted.xlsx

```

[WFQCMODEL.tar.gz](https://drive.google.com/file/d/1aIRceq_qBk0zDI8EdXLEtP4vEouuU4Bn/view?usp=sharing)

## Output

At the Output folder, there are excel files for the ensemble weights _opt___weights.xlsx_ and there is an output of the example dataset.


## RUNNING
The easiest way to run the example is usin the Jupyter notebook in the notebooks folder.
## COMMENTS
ortega@cicese.mx