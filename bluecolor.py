#opencv basic color thresholding example - BLUE Screen

import matplotlib.pyplot as plt
import numpy as np
import cv2

image = cv2.imread('testimage1.jpg')

print('this image is:', type(image), 'with dimensions', image.shape)

image_copy = np.copy(image)

image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)

plt.imshow(image_copy)

#need to adjust to isolate blue background
lower_blue = np.array[0,0,200]
upper_blue = np.array[250,250,255]

#Create mask

mask = cv2.inRange(image_copy, lower_blue, upper_blue)

plt.imshow(mask, cmap='gray')

masked_image = np.copy(image_copy)
masked_image[mask != 0] = [0,0,0] #just the object is visible, blue background is masked

plt.imshow(masked_image)

#Mask and add background image

background_image = cv2.imread('testimage2.jpg')
background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)

crop_background[mask == 0] = [0,0,0]

plt.imshow(crop_background)

complete = masked_image + crop_background

plt.imshow(complete)


