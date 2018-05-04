import svm

import pars

class classifier:

	def __init__(self, nClasses):

		print "Initializing classifier"
		self.orientation = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='orientation')
		print "Initializing filters"
		
		self.coarse_filter = []
		self.fine_filter = []

		self.nClasses = nClasses

		for cls in range(1,nClasses):

			self.coarse_filter.append(svm.classifier(cls, blockSize=pars.BLOCK_SIZE_COARSE, cellSize=pars.CELL_SIZE_COARSE, binary=True, loc='coarse_'+str(cls)))
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
		return self.coarse_filter[cls].classifyImage(imgs, self.getInterestPoints(imgs))

	def getThirdOpinion(self, imgs, cls):
		return self.fine_filter[cls].classifyImage(imgs, self.getInterestPoints(imgs))

	def getInterestPoints(self, imgs):
		return pars.FIXED_LOCATION
	
	def train(self, fol, loc=True):
		self.orientation.train(fol, loc)
		
		for i in range(self.nClasses-1):
			self.coarse_filter[i].train(fol, loc)
			self.fine_filter[i].train(fol, loc)


	def save(self):
		self.orientation.save()

		for i in range(self.nClasses-1):
			self.coarse_filter[i].save()
			self.fine_filter[i].save()

	def load(self):
		self.orientation.load()

		for i in range(self.nClasses-1):
			self.coarse_filter[i].load()
			self.fine_filter[i].load()