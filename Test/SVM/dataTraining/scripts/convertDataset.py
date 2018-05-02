import sys

import os
from os import listdir
from os.path import isfile, join

import featureExtraction as fe

from PIL import Image

import pars

#NP WRAPPERS
def addRows(M, r):
	if len(r.shape)==1:
		r = [r]

	return np.vstack((M, r))

#EXTRACT FILE LIST FROM FOLDER
def getImages(fol, target):
	#print (fol.split('/'))[-1]
	#target = int((fol.split('/'))[-1])

	files = [Image.open(fol+'/'+f) for f in listdir(fol) if isfile(join(fol, f))]

	return files


#EXTRACT TEST CASE NATRIX FROM FILE LIST
def getTestCase(img, blockSize = (2,2), cellSize = (8,8)):
	return fe.getBlockFeature(getImgFeat(img, blockSize=blockSize, cellSize=cellSize))

def getTestCases(imgs, blockSize = (2,2), cellSize = (8,8)):
	X = np.array([getTestCase(imgs[0], blockSize=blockSize, cellSize=cellSize)])

	for img in imgs[1:]:
		X = addRows(X,getTestCase(img, blockSize=blockSize, cellSize=cellSize))

	return X

#WRAPPERS
def folToMat(fol, target, blockSize = (2,2), cellSize = (8,8), prev=None):
	files = getImages(fol, target);

	inputs = getTestCases(files, blockSize=blockSize, cellSize=cellSize)
	targets = target*no.ones(inputs.shape[0])

	if prev:
		X,y = prev
		
		inputs = addRows(X,inputs)
		target = np.concatenate(y,targets)

	return (inputs, targets)
#MAIN

def getDataSet(fol, nClasses, blockSize = (2,2), cellSize = (8,8), local=True, binary=False):
	#Set full path
	if local:
		wd = os.path.dirname(os.path.realpath(__file__))
		fol = wd+"/"+fol


	X, y = folToMat(getTargetFol(0), 0)
	for t in range(1,nClasses):
		out = t if (not binary) else 1
		X,y = folToMat(getTargetFol(fol,t),t, blockSize=blockSize, cellSize=cellSize,prev=(X,y))

	return X,y