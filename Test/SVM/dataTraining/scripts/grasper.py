import classifier
import grasp

class grasper:

	def __init__(self, nClasses, loc):
		self.nClasses = nClasses

		self.cfr = classifier.classifier(nClasses, loc=loc)
		self.grasp = grasp.grasp()

	def train(self, fol, loc=True, files=None, data=None):
		self.cfr.train(fol, loc, files, data)

	def getObject(self, imgs):
		nClass = self.cfr.classifyImage(imgs)

		if nClass!=0:			
			self.grasp.act_grasp(nClass)

		return nClass
