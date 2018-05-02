import os

import convertDataset as cd
#import featureExtraction as fe

import Image

import cPickle

class classifier:

	def __init__(self, nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SEIZE, loc=None, binary=False):
		self.nClasses = nClasses

		self.blockSize = blockSize
		self.cellSize = cellSize

		self.binary = binary

		self.loc = os.path.dirname(os.path.realpath(__file__)) + '/svc_pickle'

		self.svc = SVC()

		if loc:
			self.loc = os.path.dirname(os.path.realpath(__file__)) + '/' + loc

		if os.path.exists(self.loc):
			self.load()



	def getData(fol, local=True):
		return cd.getDataSet(fol, self.nClasses, self.blockSize, self.cellSize, local=local, binary=self.binary)

	def train(fol, local=True):
		X,y = self.getData()

		self.svc.fit(X,y)


	def classifyImage(imgs):
		if type(imgs) == type(""):
			imgs =  os.path.dirname(os.path.realpath(__file__)) + '/' + imgs
			imgs = [Image.open(imgs+'/'+f) for f in listdir(imgs) if isfile(join(imgs, f))]

		if type(imgs) != type([]):
			imgs = [imgs]

		return self.predict(cd.getTestCases(imgs, blockSize=self.blockSize, cellSize=self.cellSize))

	def predict(x):
		if len(x.shape)==1:
			x = [x]

		return self.svc.predict(x)

	def save():
		with open(self.loc, 'wb') as fid:
			cPickle.dump(self.svc, fid)


	def load():
		with open(self.loc, 'rb') as fid:
			self.svc = cPickle.load(fod)