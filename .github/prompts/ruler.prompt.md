---
mode: ask
---
Define the task to achieve, including specific requirements, constraints, and success criteria.
# 🚀 Task Definition

## 1. Context（上下文）
说明背景或工件，例如：
- 使用的语言 / 框架（如 Python + ROS Noetic + Yolov5 等）
- 我现在在做什么：
    - 我现在在做一个ROS小车 Gazebo仿真项目，用来做一个教学示范作用，因为目前大多数人学习ROS并没有一个完整的好的项目让自己能够内化ROS相关的知识，我的大致思路是：仅用 Gazebo 进行仿真，让小车实现自主建图，用DWA，TEB等算法进行优化"/home/ubuntu/robot_car/src/race_navigation/launch", 小车车模建立好了"/home/ubuntu/robot_car/src/gazebo_pkg/urdf/waking_robot.xacro"，地图也建好了"/home/ubuntu/robot_car/src/gazebo_pkg/world/xinjian.world"，之前大致实现的是建图，路径规划，自主导航行驶，行驶的同时可以调用yolov5推理模型对路上摄像头拍到的图像进行物体检测“/home/ubuntu/robot_car/src/race_navigation/scripts/move_with_detection.py”，我现在打算将原来的RGB摄像头换成深度相机进行环境感知，让这个项目更加完善，而且正在探索如何使用深度相机和原来那些结合在一起。
        

## 2. Requirements（具体需求）
列出明确的功能或约束，例如：
- 使用深度相机进行环境感知，替换原有的RGB摄像头

## 3. Constraints（约束条件）
说明不得超过的限制，例如：
- 风格要求：必须注释、变量命名规范、支持国际化等

## 4. Success Criteria（成功标准）


