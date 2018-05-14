import svm
import pars

import numpy as np

import sys

import random as rand



def shufflePatterns(X,y):
	nPatterns = len(X)

	indexes = list(range(nPatterns))
	rand.shuffle(indexes)

	newX, newY = [], []

	for r in indexes:
		newX.append(X[r])
		newY.append(y[r])

	return np.array(newX), np.array(newY)

def getSub(x, p):
	nPatterns = int(len(x)*p)
	return x[:nPatterns]

def getValidation(X,y, size):
	X,y = shufflePatterns(X,y)
	return getSub(X, size), getSub(y, size)

def load(loc):
	print "Loading from " +  loc
	with open(loc, 'rb') as fid:
		return cPickle.load(fid)




nClasses = int(sys.argv[1])
fol = sys.argv[2]

start = float(sys.argv[3])
end = float(sys.argv[4])

cfr = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='pickle/test_multi')

trainingSize = 0.8

#Extract Features

XList = load(fol+"/XList")

X = XList[1]
y = [1]*len(XList[1])

for t in range(2,nClasses):
	X = np.vastack((X,XList[t]))
	y += [t]*len(XList[t])


#X = cfr.getData(fol + '/' + str(1), cls=True)
#y = [1]*len(X)

#for i in range(2,nClasses):
	#new = cfr.getData(fol + '/' + str(i), cls=True)

	#X = np.vstack((X,new))
	#y += [i]*len(new)

((XT,XV),(YT,YV)) = getValidation(X,y, trainingSize)

max = (-1,-1)

for c in np.e**(np.arange(1,10)):
	for g in range(1,10):
		gamma = float(g)/10.0 * (end-start) + start

		cfr = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='pickle/test_multi_' + str(g), gamma=gamma, C=c)
		cfr.svc.fit(XT,YT)

		score = cfr.svc.score(XV,YV)

		if(score> max[0]):
			max = (score, gamma, g)


print max
