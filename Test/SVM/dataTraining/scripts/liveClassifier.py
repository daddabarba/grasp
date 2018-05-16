import numpy
import rospy
import cv2
import threading

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import sys
import os

import classifier

import cPickle

class Kinect:
	def __init__(self, cfr=None):
		self.image_topic = '/camera/rgb/image_raw'
		self.bridge = CvBridge()

		self.cfr = cfr

	def process(self):
		image_data = rospy.wait_for_message(self.image_topic, Image)
		self.cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")

		#self.draw_block()

		cv2.imshow('Kinect data', self.cv_image)
		key = cv2.waitKey(1)
		if key == 13:
			print self.classify()

	def classify(self):
		return self.cfr.classifyImage(self.cv_image)

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

	XList, XIntList, XFineList = load(fol+"/XList"), load(fol+"/XIntList"), load(fol+"/XFineList")
	nClasses = len(XList)

	cfr = classifier.classifier(nClasses, loc="live_cfr")
	cfr.train("", data=(XList, XIntList, XFineList))

	k = Kinect(cfr=cfr)
	# screenThread = threading.Thread(args = (k))
	# screenThread.run = saveThread

	try:
		while True:
			k.process()

	except KeyboardInterrupt:
		print("Shutting down")
		cv2.destroyAllWindows()

