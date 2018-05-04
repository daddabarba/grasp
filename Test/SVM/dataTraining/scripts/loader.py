import classifier 

import cv2


cfr = classifier.classifier(19)
cfr.train("Data")

cfr.classifyImage("Data/1/img1.png")