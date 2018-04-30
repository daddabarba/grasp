import numpy as np
import rospy
import cv2

from skimage import exposure
from skimage import feature
from skimage import data

import time

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


class Kinect:
	def __init__(self):
		self.image_topic = '/camera/rgb/image_raw'
		self.bridge = CvBridge()

	def process(self):
		image_data = rospy.wait_for_message(self.image_topic, Image)
		self.cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")

		self.cv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY) #Convert to grayscale image

		H, hog_image = feature.hog(self.cv_image , orientations=9, pixels_per_cell=(8, 8),
cells_per_block=(2, 2), transform_sqrt=True, block_norm="L2-Hys",
visualise=True)


		cv2.imshow('Kinect data', hog_image)
		cv2.waitKey(1)


if __name__ == '__main__':
	rospy.init_node('kinect', anonymous=True)
	k = Kinect()

	try:
		while True:
			k.process()

	except KeyboardInterrupt:
		print("Shutting down")
		cv2.destroyAllWindows()