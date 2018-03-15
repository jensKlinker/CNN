Script flow:
1. Resize and Grayscale from -> Source Data: 
Resize_Grayscale_Images.py
2. Super Sample from -> Resized Data: 
Supersample_Images.py
3. Encode and Standardize from -> Super Sampled Data: 
Encode_Images.py / Encode_Number_Data.py
4. Create Train / Test Sets from -> Encoded and Standardized Data: Create_Train_Test_Sets.r
5. Create Model from -> Created Train / Test Sets: 
Create_Model.r

Examples:
1. Example_Eyes: Execute order -> Resize_Grayscale_Images.py -> Supersample_Images.py -> Encode_Images.py -> Create_Train_Test_Sets.r (Adapt code before) -> Create_Model.r
2. Example_SemeionNumbers: Execure order -> Encode_Number_Data.py -> Create_Train_test_Sets.r (Adapt code before) -> Create_Model.r

Required Libraries:
- Python 3.6.3 or newer
- Pip or Anaconda (used for installing python packages) I prefer Pip.
- PIL (python library for managing images)
- Numpy (python library)
- R 3.3.3 or newer
- Mxnet (R library for neural networks)

Important Tutorials:
https://mxnet.incubator.apache.org/tutorials/

Getting Started:
The starting point mostly depends on the source data’s form and what you want to do with it. Therefore it is very important that you first understand the data you are intending to analyze and how (if at all) it is labelled. Once you understand your data you may start adapting it to your needs making use of these scripts. All scripts have been documented to help understanding the code.
1. Resize and Grayscale:
This script searches a given directory (“Original_Images”) for all jpg/jpeg/png files and creates a resized and gray scaled copy of each image, placing them in the “Reworked_Images” folder. You may adapt the target folder and the resize dimensions to your own preferences. 
This script was written to standardize all pictures and also lower their dimensions, as most CPUs won’t be able to run a CNN on datasets consisting of images with a resolution greater than 64x64 pixels. However what size you want your images to be is up to you. I personally would recommend to start testing with a very low resolution and work your way up to higher resolutions.
If the dataset you are working on has already been encoded it will most likely also have been downsized as well. If you still want to downsize it you could either write your own script to manually downsize the encoded data, or otherwise write a script to translate the encoded data back into image files. You could then use the “Resize_Grayscale_Images.py” script to downsize (and if necessary grayscale) the images.
--------------------

2. Super Sample:
After resizing and gray scaling is done, you might want to artificially increase the amount of data. Again it is very important that you really understand your dataset and its labelling before super sampling it. Otherwise you might find yourself altering your data in ways that will only slow down or even harm the training process.
The script for super sampling takes all images inside the “Rewoked_Images” folder and creates altered copies and one unaltered copy of the original and stores them in the “Supersampled_Dataset” folder. The “Supersample_Images.py” script currently focuses on an example super sampling images alone, additionally altering the corresponding labels in the “Single_Labels.txt” file in the “Original_Labels” folder. This is merely a demonstration on how this could be done as it is most likely that your dataset and labelling will be quite differently structured. Therefore you might have to adapt the script to fit to your data structure. In this example case we originally had 27 images showing human eyes, while the labels marked the very center of the left eye (x/y position of pixel). This of course, is a horrible dataset and an even worse way to label it, but it helps create an understanding for datasets and their labelling. Have a look at the “Supersample_Images.py” file and read its documentation to see which parts of the code are generic and which should be adapted.
--------------------

3. Encode and Standardize:
After super sampling the next step is to encode and standardize the datasets, preparing them for the following R scripts. For this purpose I created two examples. “Encode_Images.py” continues where we last stopped, now encoding the previously super sampled dataset and saving it into a csv and a text file. If you prefer a different file format that is rather easily adapted. Also, in preparation for the next step the labels are “Encode_Number_Data.py” is the starting point for a different data set, used to identify handwritten digits. It uses a .data file stored in the “Datasets\SemeionNumberDataset” folder. The R script we will use in the next step expects the data to be ordered in a specific way with one file consisting of the dataset and a second file with the corresponding labels. If you take a look at the source file in the “Datasets\SemeionNumberDataset” folder, you will realize that it contains 1593 rows each representing a single encoded image with its label. Each row consists of 256 values that are either 1 or 0 (16x16 pixels) followed by10 more values also varying from 1 to 0. The first 256 values form the dataset file, while the following 10 entries will create the labels file. Additionally, as the R script currently expects a single value label for each data element the 10 entries are transformed into a number varying from 0-9.
--------------------
4. Create Train / Test Sets:
The “Create_Train_Test_Sets.r” script takes the previously created encoded dataset file and the labels file as inputs to merge them into a train and a test file (.csv). The train file contains 90% of the data while the remaining 10% are saved for testing the model.
--------------------

5. Create Model:
The “Create_Model.r” file uses the mxnet library and the previously created train and test sets to create a model. Currently the underlying code is a Convolutional Neural Network. The mxnet library offers a great variety of analyzation and model creating methods, so I would advise you to take some time reading the documentation and going through some of the tutorials.
