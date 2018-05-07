import classifier 

import cv2


cfr = classifier.classifier(19)
#cfr.train("Data")

print cfr.classifyImage("Data/6/img1.png")
print cfr.classifyImage("Data/15/img1.png")
