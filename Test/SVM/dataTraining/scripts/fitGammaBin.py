import svm
import pars

import numpy as np

import sys


import classifier 

import cv2



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

cfr = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE_FINE, cellSize=pars.CELL_SIZE_FINE, loc='pickle/test_multi', binary=True)

#Extract features binary
#sizes = []
#XList = []
#for i in range(nClasses):
	#new = cfr.getData(fol + '/' + str(i), cls=True)

	#XList.append(new)
	#sizes.append(len(new))

maxes = []


XList = load(fol+"/XFineList")

for i in range(1,nClasses):

	X = np.vstack((XList[0], XList[i]))
	y = [0]*len(XList[0]) + [i]*len(XList[i])

	((XT,XV),(YT,YV)) = getValidation(X,y, trainingSize)

	#Fit
	max = (-1,-1)
	for c in np.e**(np.arange(1,10)):
		for g in range(1,10):
			gamma = float(g)/10.0 * (end-start) + start

			cfr = svm.classifier(i, blockSize=pars.BLOCK_SIZE_FINE, cellSize=pars.CELL_SIZE_FINE, loc='pickle/test_multi_' + str(g), gamma=gamma. C=c, binary=True)
			cfr.svc.fit(XT,YT)

			score = cfr.svc.score(XV,YV)

			if(score> max[0]):
				max = (score, gamma, g)


	maxes.append(max)


cfr = classifier.classifier(19)
actualX, selection = cfr.train("Data")

for max in maxes:
	print max



print len(XList)

print cfr.fine_filter[selection-1].svc.gamma


for i in range(1, nClasses):
	ans = True
	shape =  XList[i].shape

	if shape != actualX.shape:
		ans = False
	else:
		for r in range(shape[0]):
			for c in range(shape[1]):
				local = actualX[r][c] == XList[i][r][c]
				ans = ans and local

	X = np.vstack((XList[0], XList[i]))
	y = [0]*len(XList[0]) + [1]*len(XList[i])

	X2 = np.vstack((XList[0], actualX))
	y2= [0]*len(XList[0]) + [1]*len(actualX)

	print str(i) + " - " + str(ans)  + " - "+ str(cfr.fine_filter[selection-1].svc.score(X,y)) + " - " + str(cfr.fine_filter[selection-1].svc.score(X2,y2))