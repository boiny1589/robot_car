/*
 * @Description: 
 * @Version: 2.0
 * @Date: 2022-04-22 21:38:06
 * @LastEditors: Meroke
 * @LastEditTime: 2022-04-22 21:47:34
 */
#include "ros/ros.h"
#include "std_msgs/String.h"
#include <iostream>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
#include <geometry_msgs/PointStamped.h>
#include <geometry_msgs/PoseStamped.h>

void chatterCallback(const geometry_msgs::PoseStamped::ConstPtr& msg)
{
  double x = msg->pose.position.x;
  double y = msg->pose.position.y;
  ROS_INFO("x: %f y: %f",x,y);
}

void chatterCallback1(const geometry_msgs::PointStamped::ConstPtr& msg)
{
  double x=msg->point.x;
  double y=msg->point.y;
  //double theta=msg->pose.pose.orientation;
  
  std::cout<<x<<y<<std::endl;
}
int main(int argc, char **argv)
{
  ros::init(argc, argv, "sub2");
  ros::NodeHandle nh;
  ROS_INFO("subscribe:");
  ros::Subscriber sub = nh.subscribe("/initialpose", 1000, chatterCallback);
 ros::Subscriber sub2 = nh.subscribe("/clicked_point", 1000, chatterCallback1);
while(1)
{
  ros::spinOnce();
}
  std::cout<<"........................."<<std::endl;

  return 0;
}