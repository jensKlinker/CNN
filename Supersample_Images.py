from PIL import Image
from PIL import ImageFilter
import os
import numpy as np
from numpy import array

#Gets directory this file is run from. Define the Directory it gets the images from, relatively to this files directory
cwd = os.getcwd()
path_labels = ''.join([cwd,"\Original_Labels\Single_Labels.txt"])
path_images = ''.join([cwd,"\Reworked_Images"])

#Open labels and adapt filename (just for nameing purposes)
label_array = np.loadtxt(path_labels)
print(label_array)

#Defines the directory with the images you wish to encode
directory = os.fsencode(path_images)

label_counter = 0
counter = 0
supersampled_labels = []

#Iterates through directory only considering 'png' and 'jpeg' files.
for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith("jpg"): 
		filepath = ''.join([path_images,"\\",filename ])
		
		#Open images and adapt filename (just for nameing purposes)
		img = Image.open(filepath)
		
		if filename.endswith('_gray.png'):
			filename = filename[:-9]
		
		
		#Defines the degree range by which images will be rotated (adapt these to the problem domain)
		#rotate_range = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
		
		#Rotate each image by every value saved in "rotate_range"
		#for x in rotate_range:
		#	rotated_img = img.rotate(x)
			
			#Enable this print to see if function is working
		#	print("Rotated: ",filename,"by",x,'degrees')
			
			#Saves rotated images to "Supersampled_Dataset\" folder. (Make sure to create one)
		#	rotated_img.save(''.join(["Supersampled_Dataset\ ",filename,"_Rotated_",str(x),"°_gray.png"]))
		#	counter = counter + 1
			
		#Same as rotate, just for blurring images	
		blur_range = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1]
		for x in blur_range:
			blurred_img = img.filter(ImageFilter.GaussianBlur(radius=x))
			print("Blurred: ",filename,"by",x)
			blurred_img.save(''.join(["Supersampled_Dataset\ ",str(counter),"_",filename,"_Blurred_",str(x),"°_gray.png"]))
			supersampled_labels.append(label_array[label_counter])
			counter = counter + 1
		
		#Same as previously, just for translating images
		transform_range = [-4,-3,-2,-1,1,2,3,4]
		for x in transform_range:	
			#Formula behind this is(ax+by+c, dx+ey+f), with x and y being the x and y value of the image's pixel matrix, so it is fine to only change the c and f values to translate the image.
			a = 1
			b = 0
			c = x #left/right (i.e. 5/-5)
			d = 0
			e = 1 
			f = x #up/down (i.e. 5/-5)
			print("Transformed: ",filename,"by",x,(-1*x))
			print("Transformed: ",filename,"by",x,x)
			transform_img = img.transform(img.size, Image.AFFINE, (a, b, c, d, e, f))
			transform_img.save(''.join(["Supersampled_Dataset\ ",str(counter),"_",filename,"_translated_",str(x),"_",str(x),"°_gray.png"]))		
			counter = counter + 1		
			f = (-1)*x
			transform_img = img.transform(img.size, Image.AFFINE, (a, b, c, d, e, f))
			transform_img.save(''.join(["Supersampled_Dataset\ ",str(counter),"_",filename,"_translated_",str(x),"_",str(f),"°_gray.png"]))	
			
					
		#Start - Specially adpated to this kind of label. Will need adation for different labelling method!
			label_x = (100*x+label_array[label_counter])/100
			label_y = (label_array[label_counter]%100)+x
			if label_x < 0:
				label_x = 0
			if label_y < 0:
				label_y = 0
			supersampled_labels.append(label_x*100+label_y)
		#Second run
			label_x = (100*x+label_array[label_counter])/100
			label_y = (label_array[label_counter]%100)+f
			if label_x < 0:
				label_x = 0
			if label_y < 0:
				label_y = 0
			supersampled_labels.append(label_x*100+label_y)
		#End
		
			counter = counter + 1
		
		label_counter = label_counter + 1
		continue
	else:
		continue

print(counter," images and labels were created!")

#fmt parameter can be adapted to adjust variable type. (See @ https://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html)
np.savetxt(''.join([cwd,"\Supersampled_Labels\Encoded_Single_Label_List"]), supersampled_labels, delimiter = ",", fmt='%d')
np.savetxt(''.join([cwd,"\Supersampled_Labels\Encoded_Single_Label_List.csv"]), supersampled_labels, delimiter = ",", fmt='%d')