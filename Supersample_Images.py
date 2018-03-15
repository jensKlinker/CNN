from PIL import Image
from PIL import ImageFilter
import os
import numpy as np
from numpy import array

#Gets directory this file is run from. Define the Directory it gets the images from, relatively to this files directory
cwd = os.getcwd()

#Makes sure these file paths are correct, they alter on different operating systems
path_labels = ''.join([cwd,"\Original_Labels\Single_Labels.txt"])
path_images = ''.join([cwd,"\Reworked_Images"])
target_directory = "Supersampled_Dataset\ "

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
		
		#Just for file naming purposes
		if filename.endswith('_gray.png'):
			filename = filename[:-9]
		
		#Defines the degree range by which images will be rotated (adapt these to the problem domain)	
		blur_range = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1]
		for x in blur_range:
			blurred_img = img.filter(ImageFilter.GaussianBlur(radius=x))
			print("Blurred: ",filename,"by",x)
			
			#Saves blurred images to "Supersampled_Dataset\" folder. The nameing is quite important to ensure the stay in the same order.
			blurred_img.save(''.join([target_directory,str(counter),"_",filename,"_Blurred_",str(x),"°_gray.png"]))
			
			#simply adding unchanged label to newly created image
			#if you get an error out of bounds error, it means you have too many pictures compared to the amount of labels. (look into the image folder then)
			supersampled_labels.append(label_array[label_counter])
			counter = counter + 1
		
		#Same as previously, just for translating images.
		transform_range = [-4,-3,-2,-1,1,2,3,4]
		for x in transform_range:	
			#Formula behind this is(ax+by+c, dx+ey+f), with x and y being the x and y value of the image's pixel matrix, so it is fine to only change the c and f values to translate the image.
			a = 1
			b = 0
			c = x #x-axis (left/right)
			d = 0
			e = 1 
			f = x #y-axis (up/down)
			print("Transformed: ",filename,"by",x,(-1*x))
			print("Transformed: ",filename,"by",x,x)
			transform_img = img.transform(img.size, Image.AFFINE, (a, b, c, d, e, f))
			transform_img.save(''.join(["Supersampled_Dataset\ ",str(counter),"_",filename,"_translated_",str(x),"_",str(x),"°_gray.png"]))		
			counter = counter + 1		
			f = (-1)*x
			transform_img = img.transform(img.size, Image.AFFINE, (a, b, c, d, e, f))
			transform_img.save(''.join(["Supersampled_Dataset\ ",str(counter),"_",filename,"_translated_",str(x),"_",str(f),"°_gray.png"]))	
		#You can alter the images in many more ways, these are just two examples of how this could be done!
		#The following code additionally adapts the labels, super sampling them accordingly.
		#This entirely depends on how these images were encoded. Therefore, this code will have to be adapted for different data sets.
		#There are many datasets where the labelling is independent from any changes to the picture (e.g a "cat" image won't become a "dog" image).
		#These labels though define the position of a certain pixel in the images.
		#While blurring the images won't affect the position the corresponding label, translating the images does.
		#Consequently this code also translates the labels of those images that were translated, by the same degree.
		#As many more labelling classes are created this way it would be advisable to also cluster them.
		#The clustering hasn't been done here, yet.
		#Start - Label rework
			label_x = (100*x+label_array[label_counter])/100
			label_y = (label_array[label_counter]%100)+x
			if label_x < 0:
				label_x = 0
			if label_y < 0:
				label_y = 0
			supersampled_labels.append(label_x*100+label_y)
			label_x = (100*x+label_array[label_counter])/100
			label_y = (label_array[label_counter]%100)+f
			if label_x < 0:
				label_x = 0
			if label_y < 0:
				label_y = 0
			supersampled_labels.append(label_x*100+label_y)
		#End - Label rework
			counter = counter + 1
		
		label_counter = label_counter + 1
		continue
	else:
		continue

print(counter," images and labels were created. \nStored at",(''.join([cwd," \ ",target_directory,"."])))

#fmt parameter can be adapted to adjust variable type. (See @ https://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html)
np.savetxt(''.join([cwd,"\Supersampled_Labels\Encoded_Single_Label_List"]), supersampled_labels, delimiter = ",", fmt='%d')
np.savetxt(''.join([cwd,"\Supersampled_Labels\Encoded_Single_Label_List.csv"]), supersampled_labels, delimiter = ",", fmt='%d')