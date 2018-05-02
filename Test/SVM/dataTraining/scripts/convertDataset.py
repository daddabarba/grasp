import sys

import os
from os import listdir
from os.path import isfile, join

import featureExtraction as fe

from PIL import Image


def getImages(fol, target):
	#print (fol.split('/'))[-1]
	#target = int((fol.split('/'))[-1])

	files = [Image.open(fol+'/'+f) for f in listdir(fol) if isfile(join(fol, f))]

	return files


local = True
fol = sys.argv[1]
nClasses = sys.argv[2]

if(len(sys.argv)>2 and sys.argv[3]=="False"):
	local = False

if local:
	wd = os.path.dirname(os.path.realpath(__file__))
	fol = wd+"/"+fol


for y in range(nClasses):
	getImages(fol+'/'+str(y), y)