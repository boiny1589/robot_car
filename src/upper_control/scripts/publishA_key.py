#!/usr/bin/env python
#-*- coding:utf-8   -*-
 
import sys
import select 
import tty
import termios 
import rospy
from std_msgs.msg import String
 
key_pub=rospy.Publisher('keys',String,queue_size=1)
rospy.init_node('keyboard_driver')
rate=rospy.Rate(100)
 
# 保存原来属性
old_attr=termios.tcgetattr(sys.stdin)
# 设置为单字符响应模式
tty.setcbreak(sys.stdin.fileno())
print("Publishing keystrokes. Press Ctrl+C to exit...")
 
while not rospy.is_shutdown():
    if select.select([sys.stdin],[],[],0)[0]==[sys.stdin]:
        # 发布按键
        key_pub.publish(sys.stdin.read(1))
    rate.sleep()
#恢复属性
termios.tcsetattr(sys.stdin,termios.TCSADRAIN,old_attr)