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

class MoveItTutorial(object):
    def __init__(self):
    
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("grasp_tutorial")
        
        self.scene = PlanningSceneInterface()
        self.scene_pub = rospy.Publisher("planning_scene", PlanningScene, queue_size=10)
        self.gripper_pose_pub = rospy.Publisher("target_pose", Pose, queue_size=10)

        arm = MoveGroupCommander("arm")
        gripper = MoveGroupCommander("gripper")

        end_effector_link = arm.get_end_effector_link()

        arm.allow_replanning(True)
        arm.set_pose_reference_frame("world")

        arm.set_planning_time(5)
    
        rospy.sleep(2)
        
        box1_id = "box1"
        target_id = "target"

        self.scene.remove_world_object(box1_id)
        self.scene.remove_world_object(target_id)

        self.scene.remove_attached_object("m1n6s200_end_effector", target_id)

        rospy.sleep(1)


        target_size = [0.06, 0.06, 0.1] #[0.05, 0.16, 0.06]  # Box size

        target_pose = PoseStamped()
        target_pose.header.frame_id = "/world"
        target_pose.pose.position.x = 0.2007 #0.24
        target_pose.pose.position.y = -0.332 #-0.32
        target_pose.pose.position.z = 0.04
        target_pose.pose.orientation.w = 1.0

        self.scene.add_box(target_id, target_pose, target_size)
        rospy.sleep(0.5)

        grasp_pose = PoseStamped()
        grasp_pose.header.frame_id = "/world"
        grasp_pose.pose.position.x = 0.2007 #0.24
        grasp_pose.pose.position.y = -0.332 #-0.32
        grasp_pose.pose.position.z = 0.07
        grasp_pose.pose.orientation.w = 1.0 

        grasps = self.make_grasps(grasp_pose, [target_id])
             
        result = arm.pick(target_id, grasps)
        if result == MoveItErrorCodes.SUCCESS:
            print 'Success'
        else:
            print 'Failed'
    
        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

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

        yaw = 0 # Change orientation of gripper 
        pitch = 90
        roll = 0

        grasps = []
                    
        q = quaternion_from_euler(math.radians(pitch) + math.pi / 2, math.radians(roll), math.radians(yaw))
        g = Grasp()
        
        g.pre_grasp_posture = self.open_gripper()
        g.grasp_posture = self.close_gripper()

        g.grasp_pose = initial_pose_stamped
        
        g.grasp_pose.header.frame_id = "/world"
        g.grasp_pose.pose.orientation.x = q[0]
        g.grasp_pose.pose.orientation.y = q[1]
        g.grasp_pose.pose.orientation.z = q[2]
        g.grasp_pose.pose.orientation.w = q[3]

        g.pre_grasp_approach = self.make_gripper_translation_approach(0.08, 0.15)  #(0.03, 0.08) #(0.08, 0.15)
        g.post_grasp_retreat = self.make_gripper_translation_retreat(0.1, 0.11)
        g.allowed_touch_objects = allowed_touch_objects    
        grasps.append(g)

        return grasps



if __name__ == "__main__":
    moveit_tutorial = MoveItTutorial()
