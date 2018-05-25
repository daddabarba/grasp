TARGET_SIZE = [0.06, 0.06, 0.1] #[0.05, 0.16, 0.06]  # Box size

TARGET_POSE = {
	"x": 0.2007, #0.24
	"y": -0.332, #-0.32
	"z": 0.04,
	"w": 1.0
}


ORIENTATIONS = {}

for i in range(1,11):

	ORIENTATIONS[i] = {
		"yaw": ((i-1)*20)%180,
		"pitch": 90,
		"roll": 0
	}


ORIENTATIONS_GRASP = copy(ORIENTATIONS)

ORIENTATIONS_GRASP[10] = { 
	"yaw": 90,
	"pitch": 0,
	"roll": 0
}

APPROACH_DIRECTION = (0.08, 0.15)  #(0.03, 0.08) #(0.08, 0.15)
RETREAT_DIRECTION = (0.1, 0.11)