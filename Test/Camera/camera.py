import numpy
import rospy
import cv2

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


class Kinect:
	def __init__(self):
		self.image_topic = '/camera2/rgb/image_raw'
		self.bridge = CvBridge()

	def process(self):
		image_data = rospy.wait_for_message(self.image_topic, Image)
		self.cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")

		cv2.imshow('Kinect data', self.cv_image)
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