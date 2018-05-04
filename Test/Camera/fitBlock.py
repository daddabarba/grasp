import numpy
import rospy
import cv2

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import sys

import pars

class Kinect:
	def __init__(self, square_size):
		self.image_topic = '/camera/rgb/image_raw'
		self.bridge = CvBridge()

		self.square_size = square_size

	def process(self):
		image_data = rospy.wait_for_message(self.image_topic, Image)
		self.cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")

		print self.cv_image.shape

		self.draw_block()

		cv2.imshow('Kinect data', self.cv_image)
		cv2.waitKey(1)

	def draw_block(self):
		shape = self.cv_image.shape
		center = numpy.array(pars.FIXED_LOCATION)

		topLeft = tuple((center-(self.square_size/2.0)).astype(int))
		bottomRight = tuple((center+(self.square_size/2.0)).astype(int))

		#print topLeft

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