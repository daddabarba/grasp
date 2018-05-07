import svm
import pars

import numpy as np

import sys

nClasses = int(sys.argv[1])
fol = sys.argv[2]

start = float(sys.argv[3])
end = float(sys.argv[4])

cfr = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='pickle/test_multi')


#Extract Features
X = cfr.getData(fol + '/' + str(1), cls=True)
y = [1]*len(X)

for i in range(2,nClasses):
	new = cfr.getData(fol + '/' + str(i), cls=True)

	X = np.vstack((X,new))
	y += [i]*len(new)



max = (-1,-1)
for g in range(1,10):
	gamma = float(g)/10.0 * (end-start) + start

	cfr = svm.classifier(nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, loc='pickle/test_multi_' + str(g), gamma=gamma)
	cfr.svc.fit(X,y)

	score = cfr.svc.score(X,y)

	if(score> max[0]):
		max = (score, gamma, g)


print max
