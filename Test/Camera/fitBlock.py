import numpy
import rospy
import cv2

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import sys
import numpy as np
import pars

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
	def __init__(self, square_size):
		self.image_topic = '/camera/rgb/image_raw'
		self.bridge = CvBridge()

		self.square_size = square_size
		print self.square_size

	def process(self):
		image_data = rospy.wait_for_message(self.image_topic, Image)
		self.cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")

		#print self.cv_image.shape

		self.draw_block()

		cv2.imshow('Kinect data', self.cv_image)
		cv2.waitKey(1)

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


block_size = int(sys.argv[1])
cell_size = int(sys.argv[2])

if __name__ == '__main__':
	rospy.init_node('kinect', anonymous=True)
	k = Kinect(block_size*cell_size)

	try:
		while True:
			k.process()

	except KeyboardInterrupt:
		print("Shutting down")
		cv2.destroyAllWindows()