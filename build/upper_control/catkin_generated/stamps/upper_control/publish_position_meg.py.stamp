'''
Description: 
Version: 2.0
Date: 2022-04-23 10:45:49
LastEditors: Meroke
LastEditTime: 2022-04-23 16:48:17
'''
from  nav_msgs.msg  import Odometry
import rospy

if __name__ == "__main__":
    rospy.init_node("publish_odom")
    while(1):
        var=rospy.wait_for_message('/odom',Odometry,timeout=5)         #(topic,topic_type,timeout)
        print(format(var.pose.pose.position.x,'.9f'), format(var.pose.pose.position.y,'.9f'))
        rospy.sleep(1.)