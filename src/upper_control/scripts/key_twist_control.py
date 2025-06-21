#!/usr/bin/env python
#-*- coding:utf-8   -*-
 
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
 
# Global publishers
g_linear_pub = None
g_angular_pub = None

# Key mappings: [angular_velocity, linear_velocity]
key_mapping = {
    'w': [0, 1],   # Forward
    'x': [0, -1],  # Backward
    'a': [-1, 0],  # Turn Left
    'd': [1, 0],   # Turn Right
    's': [0, 0]    # Stop
}
 
def keys_callback(msg):
    global g_linear_pub, g_angular_pub
    if len(msg.data) == 0 or (not msg.data[0] in key_mapping):
        return

    vels = key_mapping[msg.data[0]]

    # Create separate Twist messages for linear and angular velocities
    angular_twist = Twist()
    linear_twist = Twist()
    
    # Populate the messages based on key press
    angular_twist.angular.z = vels[0] * 0.5  # Angular speed scale
    linear_twist.linear.x = vels[1] * 0.2    # Linear speed scale

    # Publish the messages to their respective topics
    g_angular_pub.publish(angular_twist)
    g_linear_pub.publish(linear_twist)
 
if __name__ == '__main__':
    rospy.init_node('keys_to_twist_decoupled')
    
    # Publishers for separate linear and angular command topics
    g_linear_pub = rospy.Publisher('cmd_vel_linear', Twist, queue_size=1)
    g_angular_pub = rospy.Publisher('cmd_vel_angular', Twist, queue_size=1)
    
    # Subscriber for the key presses
    rospy.Subscriber('keys', String, keys_callback)
    
    rospy.loginfo("Decoupled Keys to Twist node started. Press keys in the other terminal.")
    rospy.spin()