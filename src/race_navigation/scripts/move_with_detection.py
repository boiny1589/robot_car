#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import torch
import sys

sys.path.append('/home/ubuntu/robot_car/yolov5/yolov5')

class MoveWithDetection:
    def __init__(self):
        rospy.init_node('move_with_detection', anonymous=True)
        self.bridge = CvBridge()
        # 加载yolov5模型（假设你已下载好.pt文件）
        self.model = torch.hub.load(
            '/home/ubuntu/robot_car/yolov5/yolov5',  # 本地yolov5源码路径
            'custom',
            path='/home/ubuntu/robot_car/yolov5/yolov5/best.pt',  # 你的权重文件
            source='local'
        )
        self.model.conf = 0.5  # 置信度阈值，可调整

        # 订阅摄像头话题
        self.image_sub = rospy.Subscriber('/cam', Image, self.image_callback)
        rospy.loginfo("YOLOv5目标检测节点已启动，等待图像话题...")

    def image_callback(self, msg):
        # ROS图像转OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        # 推理
        results = self.model(cv_image)
        # 解析结果
        detections = results.pandas().xyxy[0]
        for i, row in detections.iterrows():
            x1, y1, x2, y2, conf, cls, name = row[['xmin','ymin','xmax','ymax','confidence','class','name']]
            cv2.rectangle(cv_image, (int(x1),int(y1)), (int(x2),int(y2)), (0,255,0), 2)
            cv2.putText(cv_image, f"{name} {conf:.2f}", (int(x1),int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        # 缩放到宽640，高自动等比例
        scale = 0.5  # 缩放比例（0.5为缩小一半）
        small_img = cv2.resize(cv_image, (0, 0), fx=scale, fy=scale)
        cv2.imshow("Detection", small_img)
        cv2.waitKey(1)

if __name__ == '__main__':
    try:
        MoveWithDetection()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
