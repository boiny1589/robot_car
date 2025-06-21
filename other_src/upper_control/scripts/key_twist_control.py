#!/usr/bin/env python
#-*- coding:utf-8   -*-
 
import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import Twist
 
# 定义按键定义
key_mapping={
    'w':[0,1],
    'x':[0,-1],
    'a':[-1,0],
    'd':[1,0], 
    's':[0,0] 
}
 
g_twist_pub=None
 
g_target_twist=None
g_last_twist=None
 
g_last_send_time=None
 
# 速度因子参数
g_vel_scals=[0.1,0.1]
g_vel_ramps=[1.0,1.0]
 
def fetch_params(name,default):
    # 判断是否有name参数 
    if rospy.has_param(name):
        return rospy.get_param(name)
    else:
        print("%s not provided,using %.1f"%(name,default))
        return default
 
 
def ramped_vel(v_prev,v_target,t_prev,t_now,ramp_rate):
    step=(t_now-t_prev).to_sec()*ramp_rate
    if v_target>v_prev:
        sign=1
    else:
        sign=-1
    if (math.fabs(v_target-v_prev))>step:
        return v_prev+step*sign
    else:
        return v_target
 
def ramped_twist(prev,target,t_prev,t_now,ramps):
    tw=Twist()
    tw.angular.z=ramped_vel(prev.angular.z,target.angular.z,t_prev,t_now,ramps[0])
    tw.linear.x=ramped_vel(prev.linear.x,target.linear.x,t_prev,t_now,ramps[1])
    return tw
 

def send_twist():
    global g_last_twist,g_target_twist,g_last_send_time,g_vel_ramps,g_twist_pub
 
    t_now=rospy.Time.now()
    g_last_twist=ramped_twist(g_last_twist,g_target_twist,g_last_send_time,t_now,g_vel_ramps)
    g_twist_pub.publish(g_last_twist)
    g_last_send_time=t_now

# 接收keys话题回调函数
def keys_callback(msg):
    global g_target_twist,g_vel_scals
    if len(msg.data)==0 or (not msg.data[0] in key_mapping):
        return
    vels=key_mapping[msg.data[0]]
    g_target_twist=Twist()
    g_target_twist.angular.z=vels[0]*g_vel_scals[0]
    g_target_twist.linear.x=vels[1]*g_vel_scals[0]
 
 
if  __name__ == '__main__':
    rospy.init_node('keys_to_twist')
    g_last_send_time=rospy.Time.now()
    g_twist_pub=rospy.Publisher('cmd_vel',Twist,queue_size=1)
    keys_sub=rospy.Subscriber('keys',String,keys_callback)
    
    g_last_twist=Twist()
    g_target_twist=Twist()
 
    g_vel_scals[1]=fetch_params('~linear_scale',g_vel_scals[1])
    g_vel_scals[0]=fetch_params('~angular_scale',g_vel_scals[0])
 
    g_vel_ramps[1]=fetch_params('~linear_accl',g_vel_ramps[1])
    g_vel_ramps[0]=fetch_params('~angular_accl',g_vel_ramps[0])
 
    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        send_twist()
        rate.sleep()