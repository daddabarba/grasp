import svm

import pars

class classifier:

	def __init__(self, nClasses):

		print "Initializing classifier"
		self.orientation = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='orientation')
		print "Initializing filters"
		self.coarse_filter = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE_COARSE, cellSize=pars.CELL_SIZE_COARSE, binary=True, loc='coarse')
		self.fine_filter = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE_FINE, cellSize=pars.CELL_SIZE_FINE, binary=True, loc='fine')


	def classifyImage(self, imgs):
		if type(imgs) != type([]):
			imgs = [imgs]

		return self.orientation.classifyImage(imgs, self.getInterestPoints(imgs))

	def getInterestPoints(self, imgs):
		return [self.extractLocation(img) for img in imgs]

	def extractLocation(self, img):
		return pars.FIXED_LOCATION

	
	def train(self, fol, loc=True):
		self.orientation.train(fol, loc)
		self.coarse_filter.train(fol, loc)
		self.fine_filter.train(fol, loc)


	def save(self):
		self.orientation.save()
		self.coarse_filter.save()
		self.fine_filter.save()

	def load(self):
		self.orientation.load()
		self.coarse_filter.load()
		self.fine_filter.load()