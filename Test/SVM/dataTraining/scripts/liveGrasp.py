import grasper
import numpy
import rospy
import cv2
import threading

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import sys
import os

import numpy as np

import grasper
import pars
import cPickle

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

class Kinect:
	def __init__(self, square_size = 0, cfr=None):
		self.image_topic = '/camera/rgb/image_raw'
		self.bridge = CvBridge()

		self.square_size = square_size

		self.cfr = cfr

	def process(self):
		image_data = rospy.wait_for_message(self.image_topic, Image)
		self.cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")

		#self.draw_block()

		
		key = cv2.waitKey(1)
		if key == 13:
			print self.classify()

		self.draw_block()
		cv2.imshow('Kinect data', self.cv_image)


	def classify(self):
		return self.cfr.getObject(self.cv_image)

	def draw_block(self):
		#shape = self.cv_image.shape
		center = numpy.array(pars.FIXED_LOCATION)

		#topLeft = tuple((center-(self.square_size/2.0)).astype(int))
		topLeft = getBlock(pars.CELL_SIZE, pars.BLOCK_SIZE, pars.FIXED_LOCATION)[0]
		bottomRight = tuple((topLeft+(self.square_size)).astype(int))
		topLeft = tuple(topLeft)


		#print topLeft
		#print bottomRight

		#print self.cv_image.shape

		#print topLeft
		#self.cv_image = cv2.rectangle(img=self.cv_image, pt1=(231,189), pt2 = (231+210, 189+210), color=(255,0,0), thickness=3)
		
		self.cv_image = cv2.rectangle(img=self.cv_image, pt1=topLeft, pt2=bottomRight, color=(255,0,0), thickness=3)
		#print cv2.__version__

		#print cv2.__version__

block_size = pars.BLOCK_SIZE[0]
cell_size = pars.CELL_SIZE[0]

def load(loc):
	print "Loading from " +  loc
	with open(loc, 'rb') as fid:
		return cPickle.load(fid)

# def saveThread(self, kinect):
# 	cv2.waitKey(0)
# 	kinect.save()

if __name__ == '__main__':
	rospy.init_node('kinect', anonymous=True)
	
	'''
	if len(sys.argv) >= 2:
		class_name = sys.argv[1]
	if len(sys.argv) >= 3:
		initial_value = int(sys.argv[2])
	else:
		initial_value = 0
	'''

	fol = sys.argv[1]

	#XList, XIntList, XFineList = load(fol+"/XList"), load(fol+"/XIntList"), load(fol+"/XFineList")
	XList = load(fol+"/XList")
	nClasses = len(XList)

	cfr = grasper.grasper(nClasses, loc="live_cfr")
	#cfr.train("", data=(XList, XIntList, XFineList))

	#cfr.save()

	k = Kinect(square_size = block_size*cell_size, cfr=cfr)
	# screenThread = threading.Thread(args = (k))
	# screenThread.run = saveThread

	try:
		while True:
			k.process()

	except KeyboardInterrupt:
		print("Shutting down")
		cv2.destroyAllWindows()

