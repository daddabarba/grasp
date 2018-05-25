TARGET_SIZE = [0.07, 0.16, 0.07] #[0.05, 0.16, 0.06]  

TARGET_POSE = {
	"x": 0.201, #0.2007, #0.24
	"y": -0.34, #-0.332, #-0.32
	"z": -0.015,
	"w": 1.0
}


GRASPING_HEIGHT = 0.02

ORIENTATIONS = {}
TARGET_SIZES = {}
TARGET_POSES = {}

for i in range(1,11):

	ORIENTATIONS[i] = {
		"yaw": -((i-1)*20)%180,
		"pitch": 90,
		"roll": 0
	}

	TARGET_SIZES[i] = TARGET_SIZE
	
TARGET_SIZES[10] = [0.06, 0.06, 0.15]


for i in range(1,11):
	TARGET_POSES[i] = {
		"x": TARGET_POSE["x"],
		"y": TARGET_POSE["y"],
		"z": TARGET_POSE["z"] + TARGET_SIZES[i][2]/2.0,
		"w": TARGET_POSE["w"]
	}

ORIENTATIONS_GRASP = ORIENTATIONS.copy()

ORIENTATIONS_GRASP[10] = { 
	"yaw": 90,
	"pitch": 0,
	"roll": 0
}

APPROACH_DIRECTION = (0.08, 0.15)  #(0.03, 0.08) #(0.08, 0.15)
RETREAT_DIRECTION = (0.1, 0.11)