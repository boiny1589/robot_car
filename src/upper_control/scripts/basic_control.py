
import rospy
from geometry_msgs.msg import Twist
from math import pi
from navigation import *

class Control:

    def __init__(self):
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        self.rate = 50
        self.r = rospy.Rate(self.rate)

    def back(self,dis):
        goal_distance = dis
        linear_speed = 0.2
        linear_duration = goal_distance/linear_speed
        move_cmd = Twist()
        move_cmd.linear.x = -1 * linear_speed
        ticks = int(linear_duration*self.rate)
        for t in range(ticks):
            # one node can publish msgs to different topics, here only publish
            # to /cmd_vel
            self.cmd_vel.publish(move_cmd)
            self.r.sleep() # sleep according to the rate
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)


    def rotate(self,angle):
        goal_angular = angle
        angular_speed = 1
        mvoe_cmd = Twist()
        if(angle < 0):
            angular_speed *= -1
        mvoe_cmd.angular.z = angular_speed

        angular_duration = goal_angular/angular_speed
        ticks = int(angular_duration*self.rate)
        for t in range(ticks):
            self.cmd_vel.publish(mvoe_cmd)
            self.r.sleep()

        self.cmd_vel.publish(Twist())

    def send_control(self):
        
        rate = 50
        r = rospy.Rate(rate)
         
        move_cmd = Twist()
        move_cmd.linear.x = self.linear_speed # 
        ticks = int(self.linear_duration*rate)
        for t in range(ticks):
            # one node can publish msgs to different topics, here only publish
            # to /cmd_vel 
            self.cmd_vel.publish(move_cmd)
            r.sleep() # sleep according to the rate
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

        move_cmd = Twist()
        move_cmd.angular.z = self.angular_speed
        ticks = int(self.angular_duration*rate)
        for t in range(ticks):
            self.cmd_vel.publish(move_cmd)
            r.sleep()

        self.cmd_vel.publish(Twist())
        rospy.sleep(1)




if __name__ == "__main__":
    rospy.init_node("forward_back",anonymous=False)
    # Control().back(0.3)
    # Control().rotate(pi*8)

    na = Navigation()
    na.send_position([-0.617,0.070])
    Control().rotate(pi*8)
    na.send_position([-0.525,1.176])
    Control().rotate(pi*8)
    na.send_position([3.846,0.142])
    Control().rotate(pi*8)
    na.send_position([3.884,1.022])
    Control().rotate(pi*8)
    na.send_goal("start")         

    """
    3.846,0.142       -0.617,0.070
    3.884,1.022       -0.525,1.176
    """