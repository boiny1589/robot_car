#!/bin/bash

# 这个脚本用于检查深度相机的点云话题状态

echo "正在检查深度相机话题..."
echo "=========================================="

# 列出所有与深度相机相关的话题
echo "相关话题列表:"
rostopic list | grep camera/depth
echo ""

# 检查深度图像是否发布
if rostopic info /camera/depth/image_raw > /dev/null 2>&1; then
    echo "✓ 深度图像话题 (/camera/depth/image_raw) 已发布"
    echo "  消息类型: $(rostopic type /camera/depth/image_raw)"
    echo "  发布频率: $(rostopic hz /camera/depth/image_raw -w 5 2>/dev/null | grep average | awk '{print $3}') Hz"
else
    echo "✗ 深度图像话题 (/camera/depth/image_raw) 未发布"
fi
echo ""

# 检查相机信息是否发布
if rostopic info /camera/depth/camera_info > /dev/null 2>&1; then
    echo "✓ 相机信息话题 (/camera/depth/camera_info) 已发布"
    echo "  消息类型: $(rostopic type /camera/depth/camera_info)"
else
    echo "✗ 相机信息话题 (/camera/depth/camera_info) 未发布"
fi
echo ""

# 检查原始点云话题
if rostopic info /camera/depth/points > /dev/null 2>&1; then
    echo "✓ 原始点云话题 (/camera/depth/points) 已发布"
    echo "  消息类型: $(rostopic type /camera/depth/points)"
    echo "  发布频率: $(rostopic hz /camera/depth/points -w 5 2>/dev/null | grep average | awk '{print $3}') Hz"
    echo "  点云大小: $(rostopic echo /camera/depth/points -n1 | grep width | head -1 | awk '{print $2}' | sed 's/,//' ) x $(rostopic echo /camera/depth/points -n1 | grep height | head -1 | awk '{print $2}' | sed 's/,//' ) 点"
else
    echo "✗ 原始点云话题 (/camera/depth/points) 未发布"
fi
echo ""

# 检查转换后的点云话题
if rostopic info /camera/depth/points_converted > /dev/null 2>&1; then
    echo "✓ 转换点云话题 (/camera/depth/points_converted) 已发布"
    echo "  消息类型: $(rostopic type /camera/depth/points_converted)"
    echo "  发布频率: $(rostopic hz /camera/depth/points_converted -w 5 2>/dev/null | grep average | awk '{print $3}') Hz"
else
    echo "✗ 转换点云话题 (/camera/depth/points_converted) 未发布"
fi
echo ""

# 检查XYZ点云话题
if rostopic info /camera/depth/points_xyz > /dev/null 2>&1; then
    echo "✓ XYZ点云话题 (/camera/depth/points_xyz) 已发布"
    echo "  消息类型: $(rostopic type /camera/depth/points_xyz)"
    echo "  发布频率: $(rostopic hz /camera/depth/points_xyz -w 5 2>/dev/null | grep average | awk '{print $3}') Hz"
else
    echo "✗ XYZ点云话题 (/camera/depth/points_xyz) 未发布"
fi
echo ""

# 检查TF变换是否正确
echo "检查TF变换..."
if rosrun tf tf_echo /map /camera_link > /dev/null 2>&1; then
    echo "✓ 相机链接在TF树中"
else
    echo "✗ 相机链接不在TF树中，这可能导致点云定位问题"
fi
echo ""

# 检查依赖
echo "检查深度相机依赖包..."
if dpkg -l | grep ros-noetic-depth-image-proc > /dev/null 2>&1; then
    echo "✓ depth_image_proc包已安装"
else
    echo "✗ depth_image_proc包未安装，请运行:"
    echo "  sudo apt-get install ros-noetic-depth-image-proc"
fi

if dpkg -l | grep ros-noetic-pcl-ros > /dev/null 2>&1; then
    echo "✓ pcl_ros包已安装"
else
    echo "✗ pcl_ros包未安装，请运行:"
    echo "  sudo apt-get install ros-noetic-pcl-ros"
fi
echo "=========================================="
echo "检查完成。如果有问题，请根据上面的信息进行排查。"
