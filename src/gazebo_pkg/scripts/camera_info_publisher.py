#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import CameraInfo

def publish_camera_info():
    rospy.init_node('temp_camera_info_publisher', anonymous=True)
    
    # 根据您当前的话题结构发布
    pub_rgb = rospy.Publisher('/camera/camera_info', CameraInfo, queue_size=10)
    pub_depth = rospy.Publisher('/camera/depth/camera_info', CameraInfo, queue_size=10)
    
    rate = rospy.Rate(30)
    
    camera_info = CameraInfo()
    camera_info.header.frame_id = "camera_link"
    camera_info.height = 480
    camera_info.width = 640
    
    # 基于您的相机配置计算内参
    # 水平FOV = 1.047弧度 ≈ 60度
    # fx = fy = (width/2) / tan(hfov/2)
    import math
    fx = fy = (640/2) / math.tan(1.047/2)
    cx = 640/2
    cy = 480/2
    
    camera_info.K = [fx, 0.0, cx, 
                     0.0, fy, cy, 
                     0.0, 0.0, 1.0]
    camera_info.D = [0.0, 0.0, 0.0, 0.0, 0.0]
    camera_info.R = [1.0, 0.0, 0.0, 
                     0.0, 1.0, 0.0, 
                     0.0, 0.0, 1.0]
    camera_info.P = [fx, 0.0, cx, 0.0, 
                     0.0, fy, cy, 0.0, 
                     0.0, 0.0, 1.0, 0.0]
    
    rospy.loginfo("Publishing camera info to match your current topics...")
    
    while not rospy.is_shutdown():
        try:
            camera_info.header.stamp = rospy.Time.now()
            pub_rgb.publish(camera_info)
            pub_depth.publish(camera_info)
        except Exception as e:
            rospy.logwarn(f"Error publishing: {e}")
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_camera_info()
    except rospy.ROSInterruptException:
        pass