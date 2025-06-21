#!/usr/bin/env python3
#-*- coding: UTF-8 -*- 
from sys import argv,path
# path.insert(0, "/home/meroke/ros_catkin_ws/install/lib/python3/dist-packages")
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import sin, cos
import math
import rospy
import actionlib


# 欧拉数转四元数
def euler_to_quaternion(yaw, pitch, roll):
    qx = sin(roll / 2) * cos(pitch / 2) * cos(yaw / 2) - cos(roll / 2) * sin(
        pitch / 2
    ) * sin(yaw / 2)
    qy = cos(roll / 2) * sin(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * cos(
        pitch / 2
    ) * sin(yaw / 2)
    qz = cos(roll / 2) * cos(pitch / 2) * sin(yaw / 2) - sin(roll / 2) * sin(
        pitch / 2
    ) * cos(yaw / 2)
    qw = cos(roll / 2) * cos(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * sin(
        pitch / 2
    ) * sin(yaw / 2)

    return [qx, qy, qz, qw]

# 截断函数
def trunc(f, n):
    slen = len("%.*f" % (n, f))
    return float(str(f)[:slen])

class Navigation:
    """导航类"""
    def affect(self, coordinate):
        """投递点到map坐标系的变换"""
        coordinate[0] -= 0.67
        coordinate[1] -= 0.79

    def __init__(self):
        self.succeed = False
        self.locations = dict()

        #####################
        # 准备阶段
        #####################

        # # ros相关节点设置
        # disable_signals=True,否则ros会单独处理中断信号,而导致无法使得process处理键盘中断信号
        # rospy.init_node("navigation", anonymous=True,disable_signals=True)

        # 调用move_base前的准备工作
        self.move_base_prepare()

        # 初始化各点坐标
        self.coordinates_init()

        # 初始化各点位姿
        self.locations_init()

        # 确保有初始位置
        # while self.initial_pose.header.stamp == "":
        #     rospy.sleep(1)


    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        if not self.succeed:
            self.move_base.cancel_goal()
        # rospy.sleep(2)
        # self.cmd_vel_pub.publish(Twist())

    def coordinates_init(self):

        #######################################
        #   导航过程中各点的绝对坐标
        #######################################

        # 各投递点初始坐标
        self.coordinates = list()
        # self.coordinates.append([0.65, 1.95])  # p0
        # self.coordinates.append([1.25, 1.95])  # p1
        # self.coordinates.append([3.85, 1.95])  # p2
        # self.coordinates.append([4.5, 1.95])  # p3
        # self.coordinates.append([4.5, 0.60])  # p4
        # self.coordinates.append([3.85, 0.60])  # p5
        # self.coordinates.append([2.90, 0.60])  # p6
        # self.coordinates.append([2.35, 0.60])  # p7
        # self.coordinates.append([1.25, 0.60])  # p8
        # self.coordinates.append([0.70, 0.60])  # p9
        #每个分组第一个坐标为左侧箱子
        self.coordinates.append([0.65, 1.95])  # p0 #左上角
        self.coordinates.append([1.22, 1.95])  # p1 
        self.coordinates.append([1.22, 0.60])  # p2 #左下角
        self.coordinates.append([0.651, 0.60])  # p3 
        self.coordinates.append([2.83, 0.60])  # p4 #中间
        self.coordinates.append([2.29, 0.60])  # p5 
        
        self.coordinates.append([4.451, 0.60])  # p6 # 右下角
        self.coordinates.append([3.87, 0.60])  # p7
        

        self.coordinates.append([3.87, 1.95])  # p8 #右上角
        self.coordinates.append([4.46, 1.95])  # p9
        
        
        
        
        # 识别点
        # self.coordinates.append([0.925, 1.325])  # r0: 0 1
        # self.coordinates.append([4.200, 1.325])  # r1: 2 3
        # self.coordinates.append([4.200, 1.325])  # r2: 4 5
        # self.coordinates.append([2.600, 1.325])  # r3: 6 7
        # self.coordinates.append([0.925, 1.325])  # r4: 8 9
        self.coordinates.append([0.9251, 1.325])  # r0: 0 1
        self.coordinates.append([0.925, 1.325])  # r4: 8 9
        self.coordinates.append([2.500, 1.325])  # r3: 6 7
        self.coordinates.append([4.1701, 1.325])  # r2: 4 5
        self.coordinates.append([4.170, 1.325])  # r1: 2 3
        
        
        

        # 抓取点 1.5 ~ 3.5
        self.coordinates.append([1.60, 2.20])  # g0
        self.coordinates.append([1.90, 2.20])  # g1
        self.coordinates.append([2.20, 2.20])  # g2
        self.coordinates.append([2.50, 2.20])  # g3
        self.coordinates.append([2.80, 2.20])  # g4
        self.coordinates.append([3.10, 2.20])  # g5
        self.coordinates.append([3.30, 2.20])  # g6

        # self.coordinates.append([3.10, 1.95])    # start
        self.coordinates.append([1.0, 1.0])    # start
        self.coordinates.append([2.5, 1.75])    # middle

        # 对每个绝对坐标逐个施加变换,使之变成map坐标系下的坐标
        # for i in self.coordinates:
        #     self.affect(i)

    def locations_init(self):

        #######################################
        #   导航过程中各点的绝对位姿
        #######################################

        # 0~1投递点位姿确定
        for i in range(2):
            self.locations["p" + str(i)] = Pose(
                Point(self.coordinates[i][0], self.coordinates[i][1], 0.000),
                Quaternion(
                    0.000,
                    0.000,
                    euler_to_quaternion(math.radians(90), 0, 0)[2],
                    euler_to_quaternion(math.radians(90), 0, 0)[3],
                ),
            )
        # 2~7投递点位姿确定
        for i in range(2, 8):
            self.locations["p" + str(i)] = Pose(
                Point(self.coordinates[i][0], self.coordinates[i][1], 0.000),
                Quaternion(
                    0.000,
                    0.000,
                    euler_to_quaternion(math.radians(-90), 0, 0)[2],
                    euler_to_quaternion(math.radians(-90), 0, 0)[3],
                ),
            )
        # 7~8投递点位姿确定
        for i in range(8,10):
            self.locations["p" + str(i)] = Pose(
                Point(self.coordinates[i][0], self.coordinates[i][1], 0.000),
                Quaternion(
                    0.000,
                    0.000,
                    euler_to_quaternion(math.radians(90), 0, 0)[2],
                    euler_to_quaternion(math.radians(90), 0, 0)[3],
                ),
            )
        # 0识别点位姿确定
        for i in range(1):
            self.locations["r" + str(i)] = Pose(
                Point(self.coordinates[i + 10][0], self.coordinates[i + 10][1], 0.000),
                Quaternion(
                    0.000,
                    0.000,
                    euler_to_quaternion(math.radians(90), 0, 0)[2],
                    euler_to_quaternion(math.radians(90), 0, 0)[3],
                ),
            )
        # 1~3识别点位姿确定
        for i in range(1,4):
            self.locations["r" + str(i)] = Pose(
                Point(self.coordinates[i + 10][0], self.coordinates[i + 10][1], 0.000),
                Quaternion(
                    0.000,
                    0.000,
                    euler_to_quaternion(math.radians(-90), 0, 0)[2],
                    euler_to_quaternion(math.radians(-90), 0, 0)[3],
                ),
            )
        # 4识别点位姿确定
        for i in range(4,5):
            self.locations["r" + str(i)] = Pose(
                Point(self.coordinates[i + 10][0], self.coordinates[i + 10][1], 0.000),
                Quaternion(
                    0.000,
                    0.000,
                    euler_to_quaternion(math.radians(90), 0, 0)[2],
                    euler_to_quaternion(math.radians(90), 0, 0)[3],
                ),
            )
        # 0~6抓取点位姿确定
        for i in range(7):
            self.locations["g" + str(i)] = Pose(
                Point(self.coordinates[i + 15][0], self.coordinates[i + 15][1], 0.000),
                Quaternion(
                    0.000,
                    0.000,
                    euler_to_quaternion(math.radians(90), 0, 0)[2],
                    euler_to_quaternion(math.radians(90), 0, 0)[3],
                ),
            )
            # print("g"+str(i))
            # print(self.coordinates[i + 14][0])
            # print(self.coordinates[i + 14][1])
        # 开始点
        for i in range(1):
            self.locations["start"] = Pose(
                Point(self.coordinates[i + 22][0], self.coordinates[i + 22][1], 0.000),
                Quaternion(
                    0.000,
                    0.000,
                    euler_to_quaternion(math.radians(0), 0, 0)[2],
                    euler_to_quaternion(math.radians(0), 0, 0)[3],
                ),
            )
        for i in range(1):
            self.locations["middle"] = Pose(
                Point(self.coordinates[i + 23][0], self.coordinates[i + 23][1], 0.000),
                Quaternion(
                    0.000,
                    0.000,
                    euler_to_quaternion(math.radians(90), 0, 0)[2],
                    euler_to_quaternion(math.radians(90), 0, 0)[3],
                ),
            )
 
    def send_goal(self,target):

        """
        前往目标点:
        p(投递点):0-9
        g(抓取点):0-6
        r(投递盒识别点):0-4
        start: 起始点
        middle: 中点(定位用)
        """

        # 到达目标时的状态
        goal_states = [
            "PENDING",
            "ACTIVE",
            "PREEMPTED",
            "SUCCEEDED",
            "ABORTED",
            "REJECTED",
            "PREEMPTING",
            "RECALLING",
            "RECALLED",
            "LOST",
        ]

        # 决定要前往的位置
        location = self.locations[target]

        # 设定当前目标点
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = location
        self.goal.target_pose.header.frame_id = "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.succeed = False

        # 向当前位置进发
        self.move_base.send_goal(self.goal)

        # 五分钟时间限制
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(1200))

        # 查看是否成功到达
        if not finished_within_time:
            self.move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("Goal succeeded!")
                self.succeed=True
            else:
                rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))

    def move_base_prepare(self):

        # 订阅move_base服务器的消息
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # 60s等待时间限制
        self.move_base.wait_for_server(rospy.Duration(60))

# 退出时的回调函数
def shutdown():
    rospy.loginfo("navigation finished")

if __name__ == "__main__":
    try:
        Navigation()
        # rospy.on_shutdown(shutdown)

    except rospy.ROSInterruptException:
        rospy.loginfo("Random navigation finished.")