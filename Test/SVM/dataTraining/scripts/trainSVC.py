import sys
import os

from sklearn.svm import SVC

import convertDataset as cd
import pars

def getTargetFol(fol,y):
	return fol+'/'+str(y)

if(len(sys.argv)==1 or sys.argv[1]=="-h" or sys.argv[1]=="-help"):
	
	print "Usage python convertDataset <FolderPath> <numberTargetClasses> (binaryClasses = True|False) [localPath = False|True]"

else:
	
	#Argument setting
	local = True 			#local path
	fol = sys.argv[1]		#folder path
	nClasses = sys.argv[2]	#number of target classes
	binary = sys.argv[3]	#turn the dataset to binary

	#Set local
	if(len(sys.argv)>4 and sys.argv[4]=="False"):
		local = False

	print "Converting folder to data-set Matrix"
	X,y = cd.getDataSet(fol, nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, local=local)


	print "Test case extracted\n\n"

	for example in range(nData)
		print "x: " + str(X[example]) + "\ty: " + str(y[example])

	print "\n\n"

	print "Instanciating classifier":
	print "Training SVC..."
