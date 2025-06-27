#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import torch

class MoveWithDetection:
    def __init__(self):
        rospy.init_node('move_with_detection', anonymous=True)
        self.bridge = CvBridge()
        # 加载yolov5模型（假设你已下载好.pt文件）
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/ubuntu/Desktop/smartcar_xunfei_simulation/weights/best.pt', source='local')
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
        # 显示检测结果（可选，调试用）
        cv2.imshow("Detection", cv_image)
        cv2.waitKey(1)

if __name__ == '__main__':
    try:
        MoveWithDetection()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
