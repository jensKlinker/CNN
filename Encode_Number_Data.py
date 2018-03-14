from PIL import Image
from PIL import ImageFilter
import os
import numpy as np
from numpy import array

#Gets directory this file is run from. Define the Directory it gets the images from, relatively to this files directory
cwd = os.getcwd()
path_data = ''.join([cwd,"\Datasets\SemeionNumberDataset\semeion.data"])

#Open labels and adapt filename (just for nameing purposes)
data_array = np.loadtxt(path_data)
number_of_samples = len(data_array)
sample_length = len(data_array[0])

labels_array = []
images_array = []
counter = 0

for sample in data_array:
	images_array.append(sample[:-10])
	temp = sample[(sample_length-10):sample_length]
	index = 0
	
	while temp[index] != 1 and index <= 10:
		index = index + 1
		#print(index)
	else:
		labels_array.append(index)
	
	#print(counter+1," out of ",number_of_samples," done!")
	counter = counter + 1
	

print(counter," images and labels were created!")

#fmt parameter can be adapted to adjust variable type. (See @ https://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html)
np.savetxt(''.join([cwd,"\Encoded_Dataset\Encoded_Simeion_Set"]), images_array, delimiter = ",", fmt='%d')
np.savetxt(''.join([cwd,"\Encoded_Dataset\Encoded_Simeion_Set.csv"]), images_array, delimiter = ",", fmt='%d')

np.savetxt(''.join([cwd,"\Encoded_Labels\Encoded_Simeion_Set"]), labels_array, delimiter = ",", fmt='%d')
np.savetxt(''.join([cwd,"\Encoded_Labels\Encoded_Simeion_Set.csv"]), labels_array, delimiter = ",", fmt='%d')