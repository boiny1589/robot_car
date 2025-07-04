    joint_state_publisher (joint_state_publisher/joint_state_publisher)
    map_server (map_server/map_server)
    move_base (move_base/move_base)
    robot_state_publisher (robot_state_publisher/robot_state_publisher)
    rviz (rviz/rviz)
    urdf_spawner (gazebo_ros/spawn_model)

auto-starting new master
process[master]: started with pid [14788]
ROS_MASTER_URI=http://localhost:11311

setting /run_id to d27fd3d4-5900-11f0-a75f-1bb384d8b202
process[rosout-1]: started with pid [14805]
started core service [/rosout]
process[gazebo-2]: started with pid [14813]
process[gazebo_gui-3]: started with pid [14816]
process[urdf_spawner-4]: started with pid [14822]
process[joint_state_publisher-5]: started with pid [14824]
process[robot_state_publisher-6]: started with pid [14825]
process[map_server-7]: started with pid [14826]
process[amcl-8]: started with pid [14827]
process[move_base-9]: started with pid [14833]
process[rviz-10]: started with pid [14839]
[INFO] [1751652052.447720, 0.000000]: Loading model XML from ros parameter robot_description
[INFO] [1751652052.451269, 0.000000]: Waiting for service /gazebo/spawn_urdf_model
[ INFO] [1751652052.507978805]: Finished loading Gazebo ROS API Plugin.
[ INFO] [1751652052.510504475]: waitForService: Service [/gazebo/set_physics_properties] has not been advertised, waiting...
[ INFO] [1751652052.529446670]: Finished loading Gazebo ROS API Plugin.
[ INFO] [1751652052.530515768]: waitForService: Service [/gazebo_gui/set_physics_properties] has not been advertised, waiting...
[INFO] [1751652053.055337, 0.000000]: Calling service /gazebo/spawn_urdf_model
[INFO] [1751652053.066019, 0.000000]: Spawn status: SpawnModel: Entity pushed to spawn queue, but spawn service timed out waiting for entity to appear in simulation under the name robot
[ERROR] [1751652053.067062, 0.000000]: Spawn service failed. Exiting.
[ INFO] [1751652053.068763589, 4347.965000000]: waitForService: Service [/gazebo/set_physics_properties] is now available.
[ INFO] [1751652053.088075881, 4347.982000000]: Physics dynamic reconfigure ready.
[urdf_spawner-4] process has died [pid 14822, exit code 1, cmd /opt/ros/noetic/lib/gazebo_ros/spawn_model -urdf -model robot -param robot_description -z 0.05 __name:=urdf_spawner __log:=/home/ubuntu/.ros/log/d27fd3d4-5900-11f0-a75f-1bb384d8b202/urdf_spawner-4.log].
log file: /home/ubuntu/.ros/log/d27fd3d4-5900-11f0-a75f-1bb384d8b202/urdf_spawner-4*.log
[ INFO] [1751652054.995377462, 4348.104000000]: Camera Plugin: Using the 'robotNamespace' param: '/'
[ INFO] [1751652054.998382186, 4348.104000000]: Camera Plugin (ns = /)  <tf_prefix_>, set to ""
[ INFO] [1751652055.003342954, 4348.104000000]: Camera Plugin: Using the 'robotNamespace' param: '/'
[ INFO] [1751652055.007361627, 4348.104000000]: Camera Plugin (ns = /)  <tf_prefix_>, set to ""
[ INFO] [1751652055.241757624, 4348.104000000]: Laser Plugin: Using the 'robotNamespace' param: '/'
[ INFO] [1751652055.241892249, 4348.104000000]: Starting Laser Plugin (ns = /)
[ INFO] [1751652055.242878260, 4348.104000000]: Laser Plugin (ns = /)  <tf_prefix_>, set to ""
[ INFO] [1751652055.249005031, 4348.104000000]: <initialOrientationAsReference> is unset, using default value of false to comply with REP 145 (world as orientation reference)
[ INFO] [1751652055.249143365, 4348.104000000]: <robotNamespace> set to: //
[ INFO] [1751652055.249170431, 4348.104000000]: <topicName> set to: imu
[ INFO] [1751652055.249186477, 4348.104000000]: <frameName> set to: imu_link
[ INFO] [1751652055.249254550, 4348.104000000]: <updateRateHZ> set to: 100
[ INFO] [1751652055.249330099, 4348.104000000]: <gaussianNoise> set to: 0
[ INFO] [1751652055.249364911, 4348.104000000]: <xyzOffset> set to: 0 0 0
[ INFO] [1751652055.249439526, 4348.104000000]: <rpyOffset> set to: 0 -0 0
context mismatch in svga_surface_destroy
context mismatch in svga_surface_destroy
[ WARN] [1751652055.355536822, 4348.104000000]: GazeboRosSkidSteerDrive Plugin (ns = //) missing <covariance_x>, defaults to 0.000100
[ WARN] [1751652055.355620149, 4348.104000000]: GazeboRosSkidSteerDrive Plugin (ns = //) missing <covariance_y>, defaults to 0.000100
[ WARN] [1751652055.355638403, 4348.104000000]: GazeboRosSkidSteerDrive Plugin (ns = //) missing <covariance_yaw>, defaults to 0.010000
[ INFO] [1751652055.355690733, 4348.104000000]: Starting GazeboRosSkidSteerDrive Plugin (ns = //)
[ WARN] [1751652055.363920248, 4348.106000000]: Timed out waiting for transform from base_footprint to map to become available before running costmap, tf error: canTransform: target_frame map does not exist.. canTransform returned after 4348.11 timeout was 0.1.
[ INFO] [1751652056.144245730, 4348.817000000]: global_costmap: Using plugin "static_layer"
[ INFO] [1751652056.150242156, 4348.822000000]: Requesting the map...
[ INFO] [1751652056.379173815, 4349.024000000]: Resizing costmap to 320 X 256 at 0.050000 m/pix
[ INFO] [1751652056.489316165, 4349.124000000]: Received a 320 X 256 map at 0.050000 m/pix
[ INFO] [1751652056.492416422, 4349.126000000]: global_costmap: Using plugin "obstacle_layer"
[ INFO] [1751652056.495164945, 4349.130000000]:     Subscribed to Topics: scan
[ INFO] [1751652056.508986091, 4349.140000000]: global_costmap: Using plugin "inflation_layer"
[ INFO] [1751652056.559863705, 4349.189000000]: local_costmap: Using plugin "obstacle_layer"
[ INFO] [1751652056.563856303, 4349.193000000]:     Subscribed to Topics: scan
[ INFO] [1751652056.585789996, 4349.214000000]: local_costmap: Using plugin "inflation_layer"
[ INFO] [1751652056.630613261, 4349.253000000]: Created local_planner dwa_local_planner/DWAPlannerROS
[ INFO] [1751652056.633419707, 4349.256000000]: Sim period is set to 0.10
[ INFO] [1751652056.848063330, 4349.452000000]: Recovery behavior will clear layer 'obstacles'
[ INFO] [1751652056.854761905, 4349.458000000]: Recovery behavior will clear layer 'obstacles'
[ INFO] [1751652056.892186838, 4349.493000000]: odom received!

libcurl: (6) Could not resolve host: fuel.gazebosim.org

libcurl: (6) Could not resolve host: fuel.ignitionrobotics.org

