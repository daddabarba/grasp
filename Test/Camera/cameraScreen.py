import numpy
import rospy
import cv2
import threading

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import sys
import os

class Kinect:
	def __init__(self, class_name, initial_value = 0):
		self.image_topic = '/camera/rgb/image_raw'
		self.bridge = CvBridge()
		self.counter = initial_value
		self.class_name = class_name

	def process(self):
		image_data = rospy.wait_for_message(self.image_topic, Image)
		self.cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")

		#self.draw_block()

		cv2.imshow('Kinect data', self.cv_image)
		key = cv2.waitKey(1)
		if key == 13:
			self.save()

	def save(self):
		fileName = "../img/%s/img%d.png" % (self.class_name, self.counter)
		dirName = os.path.dirname(fileName)
		if not os.path.exists(dirName):
			os.makedirs(os.path.dirname(fileName))
		self.counter = self.counter + 1
		cv2.imwrite(fileName, self.cv_image)

	def draw_block(self):
		shape = self.cv_image.shape
		center = numpy.array([348,318])

		print shape[:-1]
		print center

		z = center[0]
		center[0] = center[1]
		center[1] = z

		topLeft = tuple(center - self.square_size / 2);
		bottomRight = tuple(center + self.square_size / 2);

		print topLeft;
		print bottomRight;

		#print topLeft

		self.cv_image = cv2.rectangle(img=self.cv_image, pt1=topLeft[::-1], pt2=bottomRight[::-1], color=(255,0,0), thickness=3)
		#print cv2.__version__

# def saveThread(self, kinect):
# 	cv2.waitKey(0)
# 	kinect.save()

if __name__ == '__main__':
	rospy.init_node('kinect', anonymous=True)
	if len(sys.argv) >= 2:
		class_name = sys.argv[1]
	if len(sys.argv) >= 3:
		initial_value = int(sys.argv[2])
	else:
		initial_value = 0

	k = Kinect(class_name = class_name, initial_value = initial_value)
	# screenThread = threading.Thread(args = (k))
	# screenThread.run = saveThread

	try:
		while True:
			k.process()

	except KeyboardInterrupt:
		print("Shutting down")
		cv2.destroyAllWindows()

