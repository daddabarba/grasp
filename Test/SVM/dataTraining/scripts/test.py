import classifier

import convertDataset as cd

if(len(sys.argv)==1 or sys.argv[1]=="-h" or sys.argv[1]=="-help"):
	
	print "Usage python convertDataset <pickle_path> <test_set_path> (binaryClasses = True|False) [localPath = False|True]"

else:
	
	#Argument setting
	pickle_path = sys.argv[1]
	test_batch = os.path.dirname(os.path.realpath(__file__)) + '/' + sys.argv[2]



	clf = classifier.classifier(nClasses, loc=pickle_path, binary=binary)

	X,y = clf.getData(test_batch)
	print clf.predict(test_batch)