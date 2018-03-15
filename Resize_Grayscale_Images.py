from PIL import Image
import os
import numpy as np
from numpy import array

#Gets directory this file is run from. Defines the "source_directory" it gets the images from, relatively to this files directory
cwd = os.getcwd()

#If you intend to change your file path, do it here.
source_directory = ''.join([cwd,"\Original_Images"])
print("\nPath to source_directory: ",source_directory)

#Encoded version of source path
source_directory_path = os.fsencode(source_directory)

counter = 0

#Iterates through directory only considering files ending with 'png', 'jpeg' and 'jpg'.
for file in os.listdir(source_directory_path):
	filename = os.fsdecode(file)
	if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith("jpg"): 
		filepath = ''.join([source_directory,"\\",filename])
		
		#Open and convert each image to 'grayscale'
		img = Image.open(filepath).convert('L')

		#Resize the image to a 'width' and aspect height given in pixels
		width = 28
		height = width
		img = img.resize((width,height), Image.ANTIALIAS)
		
		#If you want to save a copy of the reworked image. Currently saved to folder 'Reworked_Images' in current working directory
		target_directory = "Reworked_Images\ "
		img.save(''.join([target_directory,filename,"_",str(width),"_",str(height),"_gray.png"]))
		
		#Only for printing purposes
		counter += 1
		
		continue
	else:
		continue

print("Resizing and grayscaling done.","\nReworked",counter,"images and stored at",(''.join([cwd," \ ",target_directory,"."])))