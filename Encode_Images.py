from PIL import Image
import os
import numpy as np
from numpy import array

#Gets directory this file is run from. Define the Directory it gets the images from, relatively to this files directory
cwd = os.getcwd()
source_directory = ''.join([cwd,"\Supersampled_Dataset"])

#Defines the directory with the images you wish to encode
source_directory_path = os.fsencode(source_directory)

combinedArray = []
print(combinedArray)
counter = 0

#Iterates through directory only considering 'png' and 'jpeg' files.
for file in os.listdir(source_directory_path):
	filename = os.fsdecode(file)
	if filename.endswith(".png") or filename.endswith(".jpeg"): 
		filepath = ''.join([source_directory,"\\",filename])
		
		#Open reworked and supersampled images
		img = Image.open(filepath)

		#Transform image to array and cast it to float type
		arr = np.array(img)
		arr = arr.astype(np.float32, copy=False)

		#Change array values from 0 - 255 to 0 - 1 (0 == black, 1 == white)
		for x in np.nditer(arr, op_flags=['readwrite']):
			x[...] = x / 255

		arr = arr.ravel()
		combinedArray.append(arr)
		
		#Test prints to see if everything is working correctly
		#print("Shape: ",arr.shape)
		#print(arr)
		#print(img.format, img.size, img.mode)
		#print(filepath)
		#img.show()	
		continue
	else:
		continue

#Change array type to Numpy array
combinedArray = np.array(combinedArray)

#Print out the shape of the final array
print(combinedArray.shape)

#Save encoded image in current working directory with specified name as text and csv file
cwd = os.getcwd()
np.savetxt(''.join([cwd,"\Encoded_Dataset\Encoded_Image_List"]), combinedArray, delimiter = ",")
np.savetxt(''.join([cwd,"\Encoded_Dataset\Encoded_Image_List.csv"]), combinedArray, delimiter = ",")


