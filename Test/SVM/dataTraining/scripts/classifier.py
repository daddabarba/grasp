import os

import svm
import numpy as np

import cv2
import convertDataset as cd

import pars

class classifier:

	def __init__(self, nClasses):

		print "Initializing classifier"
		self.orientation = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='pickle/orientation')
		print "Initializing filters"
		
		self.intermediate_filter = []
		self.fine_filter = []

		self.nClasses = nClasses

		for cls in range(1,nClasses):

			self.intermediate_filter.append(svm.classifier(cls, blockSize=pars.BLOCK_SIZE_INTERMEDIATE, cellSize=pars.CELL_SIZE_INTERMEDIATE, binary=True, loc='pickle/int/intermediate_'+str(cls), gamma=pars.GAMMA_INTERMEDIATE[cls-1]))
			self.fine_filter.append(svm.classifier(cls, blockSize=pars.BLOCK_SIZE_FINE, cellSize=pars.CELL_SIZE_FINE, binary=True, loc='pickle/fine/fine_'+str(cls), gamma=pars.GAMMA_FINE[cls-1]))


	def classifyImage(self, imgs):
		if type(imgs) == type(""):
			imgs =  os.path.dirname(os.path.realpath(__file__)) + '/' + imgs
			print "Extracting images from path " + imgs
			imgs = [cv2.imread(imgs)]

		if type(imgs) != type([]):
			print "Converting to list"
			imgs = [imgs]

		raw_location = self.getInterestPoints(imgs)

		location = [tuple(self.blockTrainPosition(pars.BLOCK_SIZE, pars.CELL_SIZE, loc)) for loc in raw_location]
		locationI = [tuple(self.blockTrainPosition(pars.BLOCK_SIZE_INTERMEDIATE, pars.CELL_SIZE_INTERMEDIATE, loc)) for loc in raw_location]
		locationF = [tuple(self.blockTrainPosition(pars.BLOCK_SIZE_FINE, pars.CELL_SIZE_FINE, loc)) for loc in raw_location]

		x = cd.getTestCases(imgs, locations = location, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE)
		xi = cd.getTestCases(imgs, locations = locationI, blockSize=pars.BLOCK_SIZE_INTERMEDIATE, cellSize=pars.CELL_SIZE_INTERMEDIATE)
		xf = cd.getTestCases(imgs, locations = locationF, blockSize=pars.BLOCK_SIZE_FINE, cellSize=pars.CELL_SIZE_FINE)

		return self.classifyVector(x,xi,xf)

	def classifyVector(self, x, xi, xf):
		#activations = self.orientation.getImageDF(imgs, self.getInterestPoints(imgs))[0]
		activations = self.orientation.getDF(x)
		activations = sorted(list(enumerate(activations)), key=lambda tup: tup[1])[::-1]

		#print list(activations)

		best_guess = 0
		while(best_guess<len(activations) and (self.getSecondOpinion(xi, best_guess)==0 or self.getThirdOpinion(xf, best_guess)==0)):
			best_guess += 1

		if(best_guess>=len(activations)):
			print "No match found "
			return 0
		else:
			return activations[best_guess][0] + 1

	def getSecondOpinion(self, x, cls):
		return self.intermediate_filter[cls].predict(x)

	def getThirdOpinion(self, x, cls):
		return self.fine_filter[cls].predict(x)

	def getInterestPoints(self, imgs):
		return [pars.FIXED_LOCATION]
	
	def train(self, fol, loc=True):
		#self.orientation.train(fol, loc)
		X, XInt, XFine, sizes = self.getData(fol)

		y = []
		for i in range(1,len(sizes)):
			y += [i]*sizes[i]
			
		self.orientation.svc.fit(X,y)

		for i in range(self.nClasses-1):
			self.intermediate_filter[i].svc.fit(np.vstack((XInt[0], XInt[i])), [0]*sizes[0] + [1]*sizes[i])
			self.fine_filter[i].svc.fit(np.vstack((XFine[0], XFine[i])), [0] * sizes[0] + [1] * sizes[i])

		'''
		for i in range(self.nClasses-1):
			self.intermediate_filter[i].train(fol, loc)
			self.fine_filter[i].train(fol, loc)
		'''

	def getData(self, fol):
		X, XInt, XFine = self.orientation.getData(fol + '/' + str(1), cls=True), [], []

		sizes = []

		for i in range(2,self.nClasses):
			X = np.vstack((X,self.orientation.getData(fol + '/' + str(i), cls=True)))

		for i in range(self.nClasses):
			newInt = self.intermediate_filter[0].getData(fol + '/' + str(i), cls=True)
			newFine = self.fine_filter[0].getData(fol + '/' + str(i), cls=True)

			XInt.append(newInt)
			XFine.append(newFine)

			sizes.append(len(newFine))



		return X,XInt,XFine, sizes


	def save(self):
		self.orientation.save()

		for i in range(self.nClasses-1):
			self.intermediate_filter[i].save()
			self.fine_filter[i].save()

	def load(self):
		self.orientation.load()

		for i in range(self.nClasses-1):
			self.intermediate_filter[i].load()
			self.fine_filter[i].load()

	def blockTrainPosition(self, cells_per_block, pixel_per_cell, position):
		ppc = np.array(pixel_per_cell)
		cpb = np.array(cells_per_block)
		size = ppc * cpb
		p = np.array(position)
		return (p - size / 2) // ppc
