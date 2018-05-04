import os

from sklearn.svm import SVC
import convertDataset as cd
#import featureExtraction as fe

import pars

import numpy as np

import cv2
import cPickle

class classifier:

	def __init__(self, nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc=None, binary=False):
		print "setting nuber of classes to " + str(nClasses)
		self.nClasses = nClasses

		print "setting block size to " + str(blockSize) + " cells, and cell size to " + str(cellSize)
		self.blockSize = blockSize
		self.cellSize = cellSize

		print "The class is " + ("binary" if binary else "not binary")
		self.binary = binary

		self.loc = os.path.dirname(os.path.realpath(__file__)) + '/svc_pickle'
		

		print "Adding Support Vector Machine"
		self.svc = SVC()

		if loc:
			self.loc = os.path.dirname(os.path.realpath(__file__)) + '/' + loc

		print "classifier location: " + self.loc

		if os.path.exists(self.loc):
			print "Loading previous version"
			self.load()
		else:
			print "No jar found"



	def getData(self, fol, local=True):
		location = self.getBlockPos(pars.TRAINING_LOCATION)
		
		print "retreiving data from folder " + fol
		return cd.getDataSet(fol, location, self.nClasses, self.blockSize, self.cellSize, local=local, binary=self.binary)

	def train(self, fol, local=True):
		print "Retreiving training data"
		X,y = self.getData(fol, local=local)

		print "Fitting data"
		self.svc.fit(X,y)


	def classifyImage(self, imgs, locations):
		imgs, locations = self.format(imgs, locations)

		print "Classifying"
		return self.predict(cd.getTestCases(imgs, locations = locations, blockSize=self.blockSize, cellSize=self.cellSize))

	def getImageDF(self, imgs, locations):
		imgs, locations = self.format(imgs, locations)

		print "Classifying"
		return self.getDF(cd.getTestCases(imgs, locations = locations, blockSize=self.blockSize, cellSize=self.cellSize))

	def format(self, imgs, locations):
		if type(imgs) == type(""):
			imgs =  os.path.dirname(os.path.realpath(__file__)) + '/' + imgs
			print "Extracting images from path " + imgs
			imgs = [cv2.imread(imgs)]

		if type(imgs) != type([]):
			print "Converting to list"
			imgs = [imgs]

		if type(locations) != type([]):
			locations = [locations]

		locations = [self.getBlockPos(loc) for loc in locations]

		return (imgs, locations)

	def predict(self, x):
		print "Predicting class"
		if len(x.shape)==1:
			print "Making x a list"
			x = [x]

		return self.svc.predict(x)

	def getDF(self, x):
		print "Predicting class"
		if len(x.shape)==1:
			print "Making x a list"
			x = [x]

		return self.svc.decision_function(x)


	def getBlockPos(self, position):
		return self.blockTrainPosition(self.cellSize, self.blockSize, position)

	def blockTrainPosition(self, pixel_per_cell, cells_per_block, position):
		ppc = np.array(pixel_per_cell)
		cpb = np.array(cells_per_block)
		size = ppc * cpb
		p = np.array(position)
		return (p - size / 2) // ppc


	def save(self):
		print "Saving at " + self.loc
		with open(self.loc, 'wb') as fid:
			cPickle.dump(self.svc, fid)


	def load(self):
		print "Loading from " + self.loc
		with open(self.loc, 'rb') as fid:
			self.svc = cPickle.load(fid)