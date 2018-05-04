import classifier 
from skimage import data

import cv2

img = data.astronaut() #Just a test image
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Convert to grayscale image


cfr = classifier.classifier(4)

cfr.train("ExData")

print cfr.classifyImage(img)