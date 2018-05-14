import numpy
import rospy
import cv2

import convertDataset as cd

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import os
from os import listdir
from os.path import isfile, join

import sys
import numpy as np
import pars

import copy

from scipy.ndimage import interpolation

LM = 20

wd = os.path.dirname(os.path.realpath(__file__))
fol = wd+'/'+(sys.argv)[1]

print "Looking at " + fol

reflection = { 0:0, 1:1, 2:9, 3:8, 4:7, 5:6, 6:5, 7:4, 8:3, 9:2 }

angles = [-10,10]

gitterSize = range(1,5)
gitterSize = [(sr,sc) for sr in gitterSize for sc in gitterSize]

gitterDirections = [(r,c) for r in range(-1,2) for c in range(-1,2)]
del gitterDirections[gitterDirections.index((0,0))]

def blockTrainPosition(cells_per_block, pixel_per_cell, position):
	ppc = np.array(pixel_per_cell)
	cpb = np.array(cells_per_block)
	size = ppc * cpb
	p = np.array(position)
	return (p - size / 2) // ppc

def getBlock(ppc, cpb, center):
	center = blockTrainPosition(cpb, ppc, center);

	#print center

	ppc = np.array(ppc)
	cpb = np.array(cpb)

	size = ppc*cpb;

	#print size

	return (center*ppc, size)

block_size = (pars.BLOCK_SIZE)[0]
cell_size = (pars.CELL_SIZE)[0]

print "block size: " + str(block_size) + " cell size " + str(cell_size)

square_size = block_size*cell_size

print "Square size: " + str(square_size)

#shape = self.cv_image.shape
center = numpy.array(pars.FIXED_LOCATION)

#topLeft = tuple((center-(self.square_size/2.0)).astype(int))
topLeft = getBlock(pars.CELL_SIZE, pars.BLOCK_SIZE, pars.FIXED_LOCATION)[0]
bottomRight = tuple((topLeft+(square_size)).astype(int))
topLeft = tuple(topLeft)

print "Top left: " + str(topLeft) + " bottom right: " + str(bottomRight)

def cropImg(img):
	return (img[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0], :]).copy()

def flipCrop(img):
	return cv2.flip(img, 1).copy()

def gitterCrop(img, cr, cc):
	return (img[topLeft[1]+cr:bottomRight[1]+cr, topLeft[0]+cc:bottomRight[0]+cc, :]).copy()

def replaceCrop(img, crop):
	img = img.copy()

	for r in range(len(crop)):
			for c in range(len(crop[0])):
				img[r+topLeft[1]][c+topLeft[0]] = crop[r][c]

	return img

def replaceLargeCrop(img, crop):
	img = img.copy()

	for r in range(len(crop)):
			for c in range(len(crop[0])):
				if crop[r][c][0]>0 and crop[r][c][1]>0 and crop[r][c][2]>0:
					img[r+topLeft[1]-LM][c+topLeft[0]-LM] = crop[r][c]

	return img

def flip(img):
	crop = flipCrop(cropImg(img))
	return replaceCrop(img, crop)

def gitter(img, cr, cc):
	crop = gitterCrop(img, cr, cc)
	return replaceCrop(img, crop)

def cropLarger(img):
		return (img[topLeft[1]-LM:bottomRight[1]+LM, topLeft[0]-LM:bottomRight[0]+LM, :]).copy()

def rotate(img, angle):
	crop = cropLarger(img)
	rotated = interpolation.rotate(crop, angle, reshape=False)

	return replaceLargeCrop(img, rotated)

def augment(img):
	rotated = [img.copy()]

	for angle in angles:
		rotated.append(rotate(img, angle))

		#cv2.imshow('Gittered image', imgs[-1])
		#cv2.waitKey(1)

	imgs = copy.copy(rotated)


	for pic in rotated:

		visited = []

		for (sr,sc) in gitterSize:
			for (dr,dc) in gitterDirections:

				location = (pic,dr*sr,dc*sc)

				if not location in visited:
					imgs.append(gitter(pic,dr*sr,dc*sc))
					#cv2.imshow('Gittered image', imgs[-1])
					#cv2.waitKey(1)

					visited.append(location)


	flipped = []
	for pic in imgs:
		flipped.append(flip(pic))

	return (imgs, flipped)

#EXTRACT FILE LIST FROM FOLDER
def getImages(fol, target):
	#print (fol.split('/'))[-1]
	#target = int((fol.split('/'))[-1])
	fol += '/' + str(target)

	files = [cv2.imread(fol+'/'+f) for f in listdir(fol) if isfile(join(fol, f))]

	return files

def getName(target):
	serial = 0

	while( os.path.isfile("./aug/%d/aug%d.png" % (target, serial)) ):
		serial+=1

	return serial

def save(target, serial, img):
	fileName = "./aug/%d/aug%d.png" % (target, serial)
	dirName = os.path.dirname(fileName)
	if not os.path.exists(dirName):
		print "Making " + dirName
		os.makedirs(os.path.dirname(fileName))

	cv2.imwrite(fileName, img)

def saveList(target, imgs):
	serial = getName(target)
	for img in imgs:
		save(target, serial, img)
		serial += 1

	return serial

def storeHOG(List, X, target):
	if target in list(List.keys()):
		List[target] = np.vstack((List[target], X))
	else:
		List[target] = X

	return List



def save(loc, obj):
	print "Saving at " + loc
	with open(loc, 'wb') as fid:
		cPickle.dump(obj, fid)


def load(loc):
	print "Loading from " + loc
	with open(loc, 'rb') as fid:
		return cPickle.load(fid)


def blockTrainPosition( pixel_per_cell, cells_per_block, position, target=1):
	ppc = np.array(pixel_per_cell)
	cpb = np.array(cells_per_block)
	size = ppc * cpb
	p = np.array(position)
	return (p - size / 2) // ppc

def getHOGs(files, ppc, cpb, target=1):
	location = blockTrainPosition(ppc, cpb, pars.TRAINING_LOCATION)
	return cd.folToMat("", location, target, blockSize=cpb, cellSize=ppc, files=files)[0]

def getAll(files, target=1):
	course = getHOGs(files, pars.CELL_SIZE, pars.BLOCK_SIZE, target)
	inter = getHOGs(files, pars.CELL_SIZE_INTERMEDIATE, pars.BLOCK_SIZE_INTERMEDIATE, target)
	fine = getHOGs(files, pars.CELL_SIZE_FINE, pars.BLOCK_SIZE_FINE, target)

	return course, inter, fine

nClasses = len(listdir(fol))
print "nClasses: " + str(nClasses)


XList, XIntList, XFineList = {}, {}, {}

for t in range(1,nClasses):
	files = getImages(fol, t)
	print "Target: %d" % (t)
	print "Files: " + str(len(files))

	for img in files:
		print "Generating augmented data"
		generated, opposite = augment(img)
		print "Data generated"

		#saveList(t, generated)
		#saveList(reflection[t], opposite)

		print "Extracting HOG features"
		X, XInt, XFine = getAll(generated)
		XR, XIntR, XFineR = getAll(opposite)
		print "HOG extracted"

		XList = storeHOG(XList, X, t)
		XList = storeHOG(XList, XR, reflection[t])

		XIntList = storeHOG(XIntList, XInt, t)
		XIntList = storeHOG(XIntList, XIntR, reflection[t])

		XFineList = storeHOG(XFineList, XFine, t)
		XFineList = storeHOG(XFineList, XFine, t)
		

save("XList" , XList)
save("XIntList" , XIntList)
save("XFineList" , XFineList)