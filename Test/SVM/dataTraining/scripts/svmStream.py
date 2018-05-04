import numpy as np
import rospy
import cv2

import classifier

import time

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


class Kinect:
	def __init__(self):
		self.image_topic = '/camera/rgb/image_raw'
		self.bridge = CvBridge()

		self.cfr = classifier.classifier(4)

	def process(self):
		image_data = rospy.wait_for_message(self.image_topic, Image)
		self.cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")

		print self.cfr.classifyImage(self.cv_image)


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