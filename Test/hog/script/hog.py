from skimage import exposure
from skimage import feature
from skimage import data

import cv2
import numpy as np

import time

img = data.astronaut() #Just a test image
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Convert to grayscale image

b = time.time()

#Just get the Features
H = feature.hog(img, orientations=9, pixels_per_cell=(8, 8),
cells_per_block=(2, 2), transform_sqrt=True, block_norm="L2-Hys",
visualise=False)

#Get the Features and also the image showing the HoG features
H, hog_image = feature.hog(img, orientations=9, pixels_per_cell=(8, 8),
cells_per_block=(2, 2), transform_sqrt=True, block_norm="L2-Hys",
visualise=True)

cv2.imshow("Image", img)
cv2.imshow("HoG Image", hog_image)
cv2.waitKey(0)