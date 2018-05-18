import classifier 

import cv2
import cPickle

import sys

def load(loc):
	print "Loading from " +  loc
	with open(loc, 'rb') as fid:
		return cPickle.load(fid)

fol = sys.argv[1]

cfr = classifier.classifier(11)
#cfr.train("Data")


XList = load(fol+'/XList')
XIntList = load(fol+'/XIntList')
XFineList = load(fol+'/XFineList')

cfr.train("", data=(XList, XIntList, XFineList))

print cfr.classifyImage("Data/6/img1.png")
print cfr.classifyImage("Data/10/img1.png")
print cfr.classifyImage("Data/3/img1.png")
