import svm
import numpy as np

import pars

class classifier:

	def __init__(self, nClasses):

		print "Initializing classifier"
		self.orientation = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='orientation')
		print "Initializing filters"
		
		self.intermediate_filter = []
		self.fine_filter = []

		self.nClasses = nClasses

		for cls in range(1,nClasses):

			self.intermediate_filter.append(svm.classifier(cls, blockSize=pars.BLOCK_SIZE_INTERMEDIATE, cellSize=pars.CELL_SIZE_INTERMEDIATE, binary=True, loc='intermediate_'+str(cls)))
			self.fine_filter.append(svm.classifier(cls, blockSize=pars.BLOCK_SIZE_FINE, cellSize=pars.CELL_SIZE_FINE, binary=True, loc='fine_'+str(cls)))


	def classifyImage(self, imgs):
		activations = self.orientation.getImageDF(imgs, self.getInterestPoints(imgs))
		activations = sorted(list(enumerate(activations)), key=lambda tup: tup[1])[::-1]

		best_guess = 0

		while(best_guess<len(activations) and self.getSecondOpinion(imgs, best_guess)==0 and self.getThirdOpinion(imgs, best_guess)==0):
			best_guess += 1

		if(best_guess>=len(activations)):
			print "No match found "
			return 0
		else:
			return activations[best_guess][0]

	def getSecondOpinion(self, imgs, cls):
		return self.intermediate_filter[cls].classifyImage(imgs, self.getInterestPoints(imgs))

	def getThirdOpinion(self, imgs, cls):
		return self.fine_filter[cls].classifyImage(imgs, self.getInterestPoints(imgs))

	def getInterestPoints(self, imgs):
		return pars.FIXED_LOCATION
	
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