#!/usr/bin/env python3 
#-*- coding: UTF-8 -*- 
import sys
# sys.path.insert(0, "/home/tdb1/build_dir/tf_ws/devel/lib/python3/dist-packages/")
# sys.path.insert(0, "/usr/lib/python3/dist-packages")

import rospy
from geometry_msgs.msg import Twist, Quaternion, Point
from laser_line_extraction.msg import LineSegment, LineSegmentList
from nav_msgs.msg import Odometry

import time
import numpy as np

from math import radians, copysign
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from math import pi, sqrt, pow
import math

import tf2_ros

def quat_to_angle(quat):
    rot = euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
    # rot = PyKDL.Rotation.Quaternion(quat.x, quat.y, quat.z, quat.w)
    return rot[2]


def normalize_angle(angle):
    res = angle
    while res > pi:
        res -= 2.0 * pi
    while res < -pi:
        res += 2.0 * pi
    return res


def get_foot(start, end):
    '''
    计算线段和机器人中心点作垂线的垂足坐标
    机器人中心点为[0,0]
    '''
    if start == end:
        return start
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    ap = -start
    ab = end - start
    result = start + np.dot(ap, ab)/np.dot(ab, ab)*ab

    return result


def get_distance(point):

    return sqrt(pow((point[0]-0.30), 2) +
                pow((point[1]), 2))


class Slide():
    def __init__(self):
        # Give the node a name
        # rospy.init_node('calibrate_angular', anonymous=True,disable_signals=True)

        # Set rospy to execute a shutdown function when terminating the script
        # rospy.on_shutdown(self.shutdown)

        self.lock = True  # 是否继续执行
        self.slid = False  # 是否滑动
        self.finished = True

        self.max_rot_speed = 0.3  # radians per second
        self.min_rot_speed = 0.05  # radians per second
        self.max_trans_speed = 0.2  # meters per second
        self.min_trans_speed = 0.05  # meters per second
        # self.tolerance = radians(rospy.get_param('tolerance', 0.035)) # degrees converted to radians
        self.rot_tolerance = 0.01  # radians
        self.trans_tolerance = 0.025  # meter
        # Publisher to control the robot's speed
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        # Subscribe line detection result
        self.line_sub = rospy.Subscriber(
            "/line_segments", LineSegmentList, self.line_call, queue_size=2)

        # The base frame is usually base_link or base_footprint
        self.base_frame = rospy.get_param('~base_frame', 'base_footprint')

        # The odom frame is usually just /odom
        # self.odom_frame = rospy.get_param('~odom_frame', 'odom_combined')
        self.odom_frame = rospy.get_param('~odom_frame', 'odom')
        # Initialize the tf listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        self.target_angle = 0
        self.target_position = [1.80, 2.20]
        self.start_position = [1.80, 2.20]
        
        self.positions= [1.80, 2.20],[2.10, 2.20],[2.40, 2.20],[2.70, 2.20],[3.00, 2.20],[3.30, 2.20]
        self.end_position = [3.40, 2.20]
        self.current_position = [0,0]

        # Give tf some time to fill its buffer
        rospy.sleep(1)

    def stop(self):
        self.cmd_vel.pub(Twist())

    # def line_call(self, lines_msg:LineSegmentList()):
    def line_call(self, lines_msg: LineSegmentList()):

        rot_v = 0
        trans_v = 0
        # print("recived")
        line = LineSegment()
        line.start = [100.0, 100.0]
        line.end = [100, 100]
        line.radius = 0
        angles = []
        for temp_line in lines_msg.line_segments:
            angles.append(temp_line.angle)
            if math.fabs(temp_line.angle) < 0.5 and get_distance(get_foot(temp_line.start, temp_line.end)) < get_distance(get_foot(line.start, line.end)) and temp_line.radius > line.radius:
                line = temp_line
        # print(self.target_angle)
        self.target_angle = line.angle -0.03 #激光雷达误差
        # Get the current rotation angle from tf
        # 过机器人中心点作与货物放置台边缘的垂线的垂足坐标
        foot_point = get_foot(line.start, line.end)
        # 距离
        trans_distance = sqrt(pow((foot_point[0]-0.24), 2) +
                              pow((foot_point[1]), 2))
        if self.finished:
            return
        self.finished = True
        move_cmd = Twist()
        if rospy.is_shutdown():
            return
        
        # 处理旋转误差
        if abs(self.target_angle) > self.rot_tolerance:
            self.finished = False
            # Rotate the robot to reduce the error

            rot_v = self.target_angle

            if math.fabs(rot_v) >= self.max_rot_speed:
                rot_v = self.max_rot_speed
            elif math.fabs(rot_v) < self.min_rot_speed:
                rot_v = self.min_rot_speed

            move_cmd.angular.z = copysign(math.fabs(rot_v), self.target_angle)
        
        #处理x方向误差
        if abs(trans_distance) > self.trans_tolerance:
            self.finished = False
            trans_v_x = (foot_point[0]-0.24)*0.3
            # trans_v_y = -(foot_point[1])
            if math.fabs(trans_v_x) >= self.max_trans_speed:
                trans_v_x = copysign(self.max_trans_speed, trans_v_x)
            elif math.fabs(trans_v_x) < self.min_trans_speed:
                trans_v_x = copysign(self.min_trans_speed, trans_v_x)
            # if math.fabs(trans_v_y) >= self.max_trans_speed:
            #     trans_v_y = copysign(self.max_trans_speed, trans_v_y)
            # elif math.fabs(trans_v_y) < self.min_trans_speed:
            #     trans_v_y = copysign(self.min_trans_speed, trans_v_y)

            move_cmd.linear.x = trans_v_x
        # 处理y方向与目标点间误差
        if math.fabs(self.get_position()[0]-self.target_position[0]) > self.trans_tolerance:
            self.finished = False
            trans_v_y = self.get_position()[0]-self.target_position[0]
            # trans_v_y *= 0.3
            if math.fabs(trans_v_y) >= self.max_trans_speed:
                trans_v_y = copysign(self.max_trans_speed, trans_v_y)
            elif math.fabs(trans_v_y) < self.min_trans_speed:
                trans_v_y = copysign(self.min_trans_speed, trans_v_y)

            # move_cmd.linear.x = trans_v_x
            move_cmd.linear.y = trans_v_y

        self.cmd_vel.publish(move_cmd)
        return

    def get_odom_angle(self):
        # Get the current transform between the odom and base frames
        try:
            trans = self.tf_buffer.lookup_transform(
                self.odom_frame, self.base_frame, rospy.Time(0))
        except (tf2_ros.ExtrapolationException, tf2_ros.ConnectivityException, tf2_ros.LookupException):
            rospy.loginfo("TF Exception")
            return

        # Convert the rotation from a quaternion to an Euler angle
        return quat_to_angle(Quaternion(trans.transform.rotation.x, trans.transform.rotation.y, trans.transform.rotation.z, trans.transform.rotation.w))

    def get_position(self):
        # Get the current transform between the odom and base frames
        try:
            trans = self.tf_buffer.lookup_transform(
                "map", self.base_frame, rospy.Time(0))
        except (tf2_ros.ExtrapolationException, tf2_ros.ConnectivityException, tf2_ros.LookupException):
            rospy.loginfo("TF Exception")
            return

        return [trans.transform.translation.x, trans.transform.translation.y, trans.transform.translation.z]

    def shutdown(self):
        # Always stop the robot when shutting down the node
        rospy.loginfo("Stopping the robot...")
        self.line_sub.unregister()
        rospy.sleep(1)
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
    
    def lock(self):
        self.cmd_vel.publish(Twist())
        self.lock = True
        # self.current_position = self.get_position()

    def to(self,index):
        self.target_position = self.positions[index]
        self.finished = False
        try:
            while not self.finished:
                time.sleep(0.2)
        except:
            self.finished = True
        return 
    
    


if __name__ == '__main__':
    try:
        rospy.init_node("Slide")
        slide = Slide()
        # time.sleep(2)
        # cal.slid = True
        for i in range(6):
            time.sleep(3)
            print("Moving to point " + str(i))
            slide.to(i)
            print("Finished")
        # slide.target_position = slide.end_position
        # cal.slid = False
        # while not rospy.is_shutdown():
        #     rospy.spin()
    except Exception as e :
        # rospy.on_shutdown()
        print(e)
        slide.line_sub.unregister()

        slide.shutdown()
    # finally:
    #     rospy.on_shutdown()
    #     slide.line_sub.unregister()

    #     slide.shutdown()
