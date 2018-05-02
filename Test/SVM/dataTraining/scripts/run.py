import sys

import convertDataset as cd
import pars

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

	X,y = cd.getDataSet(fol, nClasses, blockSize=pars.BLOCK_SIZE, cellSize=pars.CELL_SIZE, local=local)

	nData = X.shape[0]

	for example in range(nData)
		print "x: " + str(X[example]) + "\ty: " + str(y[example])