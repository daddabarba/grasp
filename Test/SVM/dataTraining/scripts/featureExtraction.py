from skimage import exposure
from skimage import feature

import cv2
import numpy as np

from skimage import data


def getImgFeat(img, blockSize = (2,2), cellSize = (8,8)):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	return feature.hog(img, orientations=9, pixels_per_cell=cellSize,
cells_per_block=blockSize, transform_sqrt=True, block_norm="L2-Hys",
visualise=False, feature_vector=False)

def getBlockFeature(H, block="mid"):
	vBlocks, hBlocks, vCells, hCells, histSize = H.shape	

	if block=="mid":
		block = (int(vBlocks/2), int(hBlocks/2))

	return H[block[0]][block[1]].flatten()