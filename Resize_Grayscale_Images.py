from PIL import Image
import os
import numpy as np
from numpy import array

#Gets directory this file is run from. Defines the "source_directory" it gets the images from, relatively to this files directory
cwd = os.getcwd()
source_directory = ''.join([cwd,"\Original_Images"])

#Defines the directory with the images you wish to encode
source_directory_path = os.fsencode(source_directory)

combinedArray = []
print(combinedArray)
counter = 0

#Iterates through directory only considering 'png' and 'jpeg' files.
for file in os.listdir(source_directory_path):
	filename = os.fsdecode(file)
	if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith("jpg"): 
		filepath = ''.join([source_directory,"\\",filename])
		
		#Open and convert each image to 'grayscale'
		img = Image.open(filepath).convert('L')

		#Resize the image to a 'basewidth' and aspect ratio height
		basewidth = 28
		wpercent = (basewidth/float(img.size[0]))
		
		#If required, a fixed 'hsize' can be defined, but be aware that this might distort the images
		hsize = int((float(img.size[1])*float(wpercent)))
		hsize = basewidth
		img = img.resize((basewidth,hsize), Image.ANTIALIAS)
		
		#If you want to save a copy of the reworked image. Currently saved to folder 'Reworked_Images' in current working directory
		img.save(''.join(["Reworked_Images\ ",filename,"_",str(basewidth),"_",str(hsize),"_gray.png"]))
		
		#Only for printing number of reworked images
		counter += 1
		
		continue
	else:
		continue

print("Resizing and grayscaling done.",counter,"images have been reworked.")