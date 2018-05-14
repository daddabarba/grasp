import sys

import os
from os import listdir
from os.path import isfile, join

import numpy as np
import featureExtraction as fe

import cv2

import pars

#NP WRAPPERS
def getTargetFol(fol,y):
	return fol+'/'+str(y)

def addRows(M, r):
	if len(r.shape)==1:
		r = [r]

	return np.vstack((M, r))

#EXTRACT FILE LIST FROM FOLDER
def getImages(fol, target):
	#print (fol.split('/'))[-1]
	#target = int((fol.split('/'))[-1])

	files = [cv2.imread(fol+'/'+f) for f in listdir(fol) if isfile(join(fol, f))]

	return files


#EXTRACT TEST CASE NATRIX FROM FILE LIST
def getTestCase(img, location, blockSize = (2,2), cellSize = (8,8)):
	return fe.getBlockFeature(fe.getImgFeat(img, blockSize=blockSize, cellSize=cellSize), block = location)

def getTestCases(imgs, locations, blockSize = (2,2), cellSize = (8,8)):
	X = np.array([getTestCase(imgs[0], location=locations[0], blockSize=blockSize, cellSize=cellSize)])

	for i in range(1, len(imgs)):
		X = addRows(X,getTestCase(imgs[i], location=locations[i], blockSize=blockSize, cellSize=cellSize))

	return X

#WRAPPERS
def folToMat(fol, locations, target, blockSize = (2,2), cellSize = (8,8), prev=None, files=None):
		
	if not files:
		print "\n Extracting from " + fol
		files = getImages(fol, target);
		print "extracted " + str(len(files)) + " files" 

	locations = [locations]*len(files)

	inputs = getTestCases(files, locations, blockSize=blockSize, cellSize=cellSize)
	targets = target*np.ones(inputs.shape[0], dtype=int)

	if prev:
		print "Adding to previous setting"
		X,y = prev
		
		print "Overwriting input and target"
		inputs = addRows(X,inputs)
		targets = np.concatenate((y,targets))

	return (inputs, targets)
#MAIN

def getDataSet(fol, location, nClasses, blockSize = (2,2), cellSize = (8,8), local=True, binary=False, cls=False, files=None):
	#Set full path
	if local:
		wd = os.path.dirname(os.path.realpath(__file__))
		fol = wd+"/"+fol

	if cls:
		return (folToMat(fol, locations=location, target=0, blockSize=blockSize, cellSize=cellSize, files=files))[0]

	X, y = folToMat(getTargetFol(fol,0), locations=location, target=0, blockSize=blockSize, cellSize=cellSize, files=files)


	if binary:
		X,y = folToMat(getTargetFol(fol,nClasses), locations=location, target=1, blockSize=blockSize, cellSize=cellSize, prev=(X,y), files=files)
	else:

		for t in range(1,nClasses):

			#t = t if (not binary) else 1
			X,y = folToMat(getTargetFol(fol,t),locations=location, target=t, blockSize=blockSize, cellSize=cellSize,prev=(X,y), files=files)

	return X,y