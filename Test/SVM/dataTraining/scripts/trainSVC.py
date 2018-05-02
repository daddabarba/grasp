import sys
import os

import cPickle

from sklearn.svm import SVC

import classifier
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

	
	clf = classifier.classifier(nClasses, binary=binary)

	clf.train(fol)
	clf.save()