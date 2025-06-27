import torch
import cv2
import numpy as np
from pathlib import Path

# 1. 加载模型（默认 yolov5s，可换成人脸专用模型）
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # 或 yolov5s-face.pt

# 如果你有本地人脸检测模型：
# model = torch.load('path/to/yolov5s-face.pt')['model'].float().fuse().eval()

# 设置只检测人脸（yolov5s默认训练的是COCO，类别0是person）
model.conf = 0.25  # 置信度阈值
model.classes = [0]  # 只检测类别0：person（不是face，除非你用的是人脸专用模型）

# 2. 加载图片或视频
source = 0  # 0表示使用摄像头；可以换成'image.jpg'或'video.mp4'
cap = cv2.VideoCapture(source)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv5 推理（注意：模型自动处理 BGR -> RGB）
    results = model(frame)

    # 3. 获取预测结果
    for *box, conf, cls in results.xyxy[0]:  # xyxy: 左上、右下坐标
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'{model.names[int(cls)]} {conf:.2f}', 
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (0, 255, 0), 2)

    # 4. 显示结果
    cv2.imshow('YOLOv5 Face Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
