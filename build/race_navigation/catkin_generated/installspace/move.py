#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import roslib
import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# 节点初始化
rospy.init_node('move_test', anonymous=True)

# 订阅move_base服务器的消息
move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

rospy.loginfo("Waiting for move_base action server...")

# 等待连接服务器，5s等待时间限制
while move_base.wait_for_server(rospy.Duration(5.0)) == 0:
    rospy.loginfo("Connected to move base server")

# 设定目标点
target = Pose(Point(-0.25, -5.3, 0.000), Quaternion(0.000, 0.000, 1.000, 0.000))
goal = MoveBaseGoal()
goal.target_pose.pose = target
goal.target_pose.header.frame_id = 'map'
goal.target_pose.header.stamp = rospy.Time.now()

rospy.loginfo("Going to: " + str(target))

start_time = rospy.Time.now()  

# 向目标进发
move_base.send_goal(goal)

# 五分钟时间限制
finished_within_time = move_base.wait_for_result(rospy.Duration(300))

# 运行所用时间  
running_time = rospy.Time.now() - start_time  
running_time = running_time.secs

# 查看是否成功到达
if not finished_within_time:
    move_base.cancel_goal()
    rospy.loginfo("Timed out achieving goal")
else:
    state = move_base.get_state()
    if state == GoalStatus.SUCCEEDED:
        rospy.loginfo("Goal succeeded! Time Result: %f", running_time)
    else:
        rospy.loginfo("Goal failed！ ")
