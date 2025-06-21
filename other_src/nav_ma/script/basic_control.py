
import rospy
from geometry_msgs.msg import Twist
from math import pi


class Control:

    def __init__(self):
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        self.rate = 50
        self.r = rospy.Rate(self.rate)

    def back(self, dis):
        goal_distance = dis
        linear_speed = 0.2
        
        move_cmd = Twist()
        if(dis < 0):
            linear_speed = linear_speed*(-1)
        move_cmd.linear.x = linear_speed
        
        linear_duration = goal_distance/linear_speed
        ticks = int(linear_duration*self.rate)
        for t in range(ticks):
            # one node can publish msgs to different topics, here only publish
            # to /cmd_vel
            self.cmd_vel.publish(move_cmd)
            self.r.sleep()  # sleep according to the rate
        self.cmd_vel.publish(Twist())

    def rotate(self, angle):
        goal_angular = angle
        angular_speed = 0.5
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


if __name__ == "__main__":
    rospy.init_node("forward_back", anonymous=False)
    # print(pi)
    # Control().rotate(-pi)
    Control().back(-1.0)