import classifier 
from skimage import data

import cv2

img = data.astronaut() #Just a test image


cfr = classifier.classifier(4)

cfr.train("ExData")

print cfr.classifyImage(img)