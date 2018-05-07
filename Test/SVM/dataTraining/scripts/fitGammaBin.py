import svm
import pars

import numpy as np

import sys

nClasses = int(sys.argv[1])
fol = sys.argv[2]

start = float(sys.argv[3])
end = float(sys.argv[4])

cfr = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE_INTERMEDIATE, cellSize=pars.CELL_SIZE_INTERMEDIATE, loc='pickle/test_multi', binary=True)

#Extract features binary
sizes = []
XList = []
for i in range(nClasses):
	new = cfr.getData(fol + '/' + str(i), cls=True)

	XList.append(new)
	sizes.append(len(new))

maxes = []

for i in range(1,nClasses):

	X = np.vstack((XList[0], XList[i]))
	y = [0]*len(XList[0]) + [i]*len(XList[i])

	#Fit
	max = (-1,-1)
	for g in range(1,10):
		gamma = float(g)/10.0 * (end-start) + start

		cfr = svm.classifier(i, blockSize=pars.BLOCK_SIZE_INTERMEDIATE, cellSize=pars.CELL_SIZE_INTERMEDIATE, loc='pickle/test_multi_' + str(g), gamma=gamma, binary=True)
		cfr.svc.fit(X,y)

		score = cfr.svc.score(X,y)

		if(score> max[0]):
			max = (score, gamma, g)


	maxes.append(max)


for max in maxes:
	print max
