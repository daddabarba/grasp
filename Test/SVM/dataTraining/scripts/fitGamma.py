import svm
import pars

import numpy as np

import sys

import random as rand

import  matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import cPickle

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
	return x[:nPatterns], x[nPatterns:]

def getValidation(X,y, size):
	X,y = shufflePatterns(X,y)
	return getSub(X, size), getSub(y, size)

def load(loc):
	print "Loading from " +  loc
	with open(loc, 'rb') as fid:
		return cPickle.load(fid)




#nClasses = int(sys.argv[1])
fol = sys.argv[1]

start = float(sys.argv[2])
end = float(sys.argv[3])

XList = load(fol+"/XList")
nClasses = len(XList)

cfr = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='pickle/test_multi')

trainingSize = 0.8

#Extract Features



X = XList[1]
y = [1]*len(XList[1])

for t in list(XList.keys()):
	if t!= 1:
		X = np.vstack((X,XList[t]))
		y += [t]*len(XList[t])


#X = cfr.getData(fol + '/' + str(1), cls=True)
#y = [1]*len(X)

#for i in range(2,nClasses):
	#new = cfr.getData(fol + '/' + str(i), cls=True)

	#X = np.vstack((X,new))
	#y += [i]*len(new)

((XT,XV),(YT,YV)) = getValidation(X,y, trainingSize)

maxVal = (-1,-1, -1)

costV = []
costT = []

cVals = np.e**(np.arange(1,3))
gammaVals = (np.arange(1,3,dtype='float'))/10.0*(end-start) + start


trialC = 0
for c in cVals:

	trialG = 0

	for gamma in gammaVals:
		#gamma = float(g)/10.0 * (end-start) + start

		cfr = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='pickle/test_multi_' + str(trialG) + '_' + str(trialC), gamma=gamma, C=c)
		cfr.svc.fit(XT,YT)

		score = cfr.svc.score(XV,YV)

		costV.append( score )
		costT.append( cfr.svc.score(XT,YT) )

		if(score> maxVal[0]):
			maxVal = (score, c, gamma)

		trialG += 1
	trialC += 1


print maxVal

pointsC, pointsG = np.meshgrid(cVals, gammaVals)

plotV = np.reshape(costV, pointsC.shape)
plotT = np.reshape(costT, pointsC.shape)

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot_surface(pointsC, pointsG, plotV, label='Validation', linewidth=0, antialiased=False, color='blue')
ax.plot_surface(pointsC, pointsG, plotT, label='Training', linewidth=0, antialiased=False, color='red')
ax.plot([maxVal[1]]*(2*int(maxVal[0])+1), [maxVal[2]]*(2*int(maxVal[0])+1), np.arange(-maxVal[0], maxVal[0]+1))

#ax.legend()

plt.show()