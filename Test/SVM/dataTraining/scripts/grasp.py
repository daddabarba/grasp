import rospy
import moveit_commander
from moveit_commander import MoveGroupCommander, PlanningSceneInterface
from moveit_msgs.msg import PlanningScene, ObjectColor
from moveit_msgs.msg import Grasp, GripperTranslation
from moveit_msgs.msg import MoveItErrorCodes
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from geometry_msgs.msg import PoseStamped, Pose
import sys
import math
import numpy as np

import graspPars as pars

import sys
import copy

class grasp(object):
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("grasp_tutorial")
        
        self.scene = PlanningSceneInterface()
        self.scene_pub = rospy.Publisher("planning_scene", PlanningScene, queue_size=10)
        self.gripper_pose_pub = rospy.Publisher("target_pose", Pose, queue_size=10)

        self.arm = MoveGroupCommander("arm")
        gripper = MoveGroupCommander("gripper")

        end_effector_link = self.arm.get_end_effector_link()

        self.arm.allow_replanning(True)
        self.arm.set_pose_reference_frame("world")

        self.arm.set_planning_time(5)
    
        rospy.sleep(2)
        
        self.box1_id = "box1"
        self.target_id = "target"

        self.scene.remove_world_object(self.box1_id)
        self.scene.remove_world_object(self.target_id)

        self.scene.remove_attached_object("m1n6s200_end_effector", self.target_id)

        rospy.sleep(1)


    def act_grasp(self, nClass):
        self.nClass = nClass

        target_size = copy.copy(pars.TARGET_SIZES[nClass])
        target_pose = PoseStamped()
        target_pose.header.frame_id = "/world"
        target_pose.pose.position.x = pars.TARGET_POSES[nClass]["x"]
        target_pose.pose.position.y = pars.TARGET_POSES[nClass]["y"]
        target_pose.pose.position.z = pars.TARGET_POSES[nClass]["z"]
        target_pose.pose.orientation.w = pars.TARGET_POSES[nClass]["w"]

       	target_pose = self.rotate(target_pose, pars.ORIENTATIONS[nClass]["yaw"], pars.ORIENTATIONS[nClass]["pitch"], pars.ORIENTATIONS[nClass]["roll"])

        self.scene.add_box(self.target_id, target_pose, target_size)
        rospy.sleep(0.5)

        grasp_pose = copy.copy(target_pose)
        grasp_pose.pose.position.z = pars.GRASPING_HEIGHT

        print "x: " + str(grasp_pose.pose.position.x) + " y: " + str(grasp_pose.pose.position.y) + " z: " + str(grasp_pose.pose.position.z)
        print "x: " + str(target_pose.pose.position.x) + " y: " + str(target_pose.pose.position.y) + " z: " + str(target_pose.pose.position.z)


        '''
        grasp_pose = PoseStamped()
        grasp_pose.header.frame_id = "/world"
        grasp_pose.pose.position.x = 0.2007 #0.24
        grasp_pose.pose.position.y = -0.332 #-0.32
        grasp_pose.pose.position.z = 0.07
        grasp_pose.pose.orientation.w = 1.0 
        '''

        grasps = self.make_grasps(grasp_pose, [self.target_id])
             
        result = self.arm.pick(self.target_id, grasps)
        if result == MoveItErrorCodes.SUCCESS:
            print 'Success'
        else:
            print 'Failed'
    
        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

    def rotate(self, pose, yaw, pitch, roll):
    	q = quaternion_from_euler(math.radians(pitch) + math.pi / 2, math.radians(roll), math.radians(yaw))

        pose.pose.orientation.x = q[0]
        pose.pose.orientation.y = q[1]
        pose.pose.orientation.z = q[2]
        pose.pose.orientation.w = q[3]

        return pose


    def open_gripper(self):
        t = JointTrajectory()
        t.header.stamp = rospy.get_rostime()
        t.joint_names = ["m1n6s200_joint_finger_1", "m1n6s200_joint_finger_2"]

        tp = JointTrajectoryPoint()
        tp.positions = [0, 0]
        tp.time_from_start = rospy.Duration(5.0)
        t.points.append(tp)
        return t

    def close_gripper(self):
        t = JointTrajectory()
        t.header.stamp = rospy.get_rostime()
        t.joint_names = ["m1n6s200_joint_finger_1", "m1n6s200_joint_finger_2"]

        tp = JointTrajectoryPoint()
        tp.positions = [1.2, 1.2] # Might need to change for real arm?
        tp.time_from_start = rospy.Duration(5.0)
        t.points.append(tp)
        return t

    def make_gripper_translation_approach(self, min_dist, desired):
        # Initialize the gripper translation object
        g = GripperTranslation()

        # Set the direction vector components to the input
        g.direction.vector.x = 0
        g.direction.vector.y = 0
        g.direction.vector.z = -1

        # The vector is relative to the gripper frame
        g.direction.header.frame_id = "world"

        # Assign the min and desired distances from the input
        g.min_distance = min_dist
        g.desired_distance = desired

        return g

    def make_gripper_translation_retreat(self, min_dist, desired):
        # Initialize the gripper translation object
        g = GripperTranslation()

        # Set the direction vector components to the input
        g.direction.vector.x = 0
        g.direction.vector.y = 0
        g.direction.vector.z = 1

        # The vector is relative to the gripper frame
        g.direction.header.frame_id = "world"

        # Assign the min and desired distances from the input
        g.min_distance = min_dist
        g.desired_distance = desired

        return g


    def make_grasps(self, initial_pose_stamped, allowed_touch_objects):

    	yaw = pars.ORIENTATIONS_GRASP[self.nClass]["yaw"]
        pitch = pars.ORIENTATIONS_GRASP[self.nClass]["pitch"]
        roll = pars.ORIENTATIONS_GRASP[self.nClass]["roll"]

        grasps = []
                    
        g = Grasp()
        
        g.pre_grasp_posture = self.open_gripper()
        g.grasp_posture = self.close_gripper()

        g.grasp_pose = initial_pose_stamped
        
        g.grasp_pose = self.rotate(g.grasp_pose, yaw, pitch, roll)

        g.pre_grasp_approach = self.make_gripper_translation_approach(*pars.APPROACH_DIRECTION)
        g.post_grasp_retreat = self.make_gripper_translation_retreat(*pars.RETREAT_DIRECTION)
        g.allowed_touch_objects = allowed_touch_objects    
        grasps.append(g)

        return grasps