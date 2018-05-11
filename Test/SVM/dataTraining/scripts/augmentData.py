import numpy
import rospy
import cv2

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import os
from os import listdir
from os.path import isfile, join

import sys
import numpy as np
import pars

wd = os.path.dirname(os.path.realpath(__file__))
fol = wd+'/'+(sys.argv)[1]

print "Looking at " + fol

reflection = { 0:0, 1:1, 2:9, 3:8, 4:7, 5:6, 6:5, 7:4, 8:3, 9:2 }

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

def flip(img):
	crop = flipCrop(cropImg(img))
	return replaceCrop(img, crop)

def gitter(img, cr, cc):
	crop = gitterCrop(img, cr, cc)
	return replaceCrop(img, crop)

def augment(img):
	imgs = []

	for (sr,sc) in gitterSize:
		for (dr,dc) in gitterDirections:
			imgs.append(gitter(img,dr*sr,dc*sc))
			cv2.imshow('Gittered image', imgs[-1])
			cv2.waitKey(1)

	imgs.append(img)

	flipped = []
	for pic in imgs:
		flipped.append(flip(pic))
	flipped.append(flip(img))

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

nClasses = len(listdir(fol))
print "nClasses: " + str(nClasses)

for t in range(1,nClasses+1):
	files = getImages(fol, t)
	print "Target: %d" % (t)
	print "Files: " + str(len(files))

	for img in files:
		generated, opposite = augment(img)

		saveList(t, generated)
		saveList(reflection[t], opposite)
		
