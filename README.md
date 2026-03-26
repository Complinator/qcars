# IMPORTANT
- PS1 file is intended to use on windows only, as this is the first push of this version I am not going to get into much details on how to set up for linux and MacOS, but it was already done, just not documented, so will be implemented in future work
- In order to run this you MUST have installed an [X Server](https://sourceforge.net/projects/xming/), otherwise, you will be able to open the docker container, but you won't see any app opening from it
- Note that `example.ps1` requires you to modify the path on the 2nd line to the path to your `config.xlaunch` file
- The app takes a while to run the gazebo model, so don't worry if it seems frozen
- The model used cames from an open-source repo called [autonomus-driving](https://github.com/bchampp/autonomous-driving)
- Remember to create the container using `docker build -t qcar-wsl .` (use that code inside this folder)
- In order to run nodes you would need to run another terminal using `docker exec -it qcar-wsl bash`
- To start running a node/bridge use `rosrun my_qcar_nodes <node_name.py>` inside scripts folder (src/nodes/scripts/)
- To start running gazebo + rviz simulation use `roslaunch qcar_gazebo qcar_world.launch` inside qcar_gazebo folder (src/qcar/src/qcar_gazebo/launch/)

# Update
- Start by using `colcon build --symlink-install`
- Then `source install/setup.bash`
- Finally, to run the simulation `ros2 launch qcar_gazebo qcar_world.launch.py`
- To run nodes `ros2 launch my_qcar_nodes basic_movement.launch.py`

## ROS2 perception (now available)

This repository now includes ROS2-native lane and object detection nodes in `my_qcar_nodes`:

- `my_qcar_nodes/lane_detection_node.py`
- `my_qcar_nodes/object_detection_node.py`
- Launch files:
	- `nodes/launch/lane_detection.launch.py`
	- `nodes/launch/object_detection.launch.py`
	- `nodes/launch/perception.launch.py`

### Run in ROS2

1. Build and source:

```bash
cd /root/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

2. Start simulation:

```bash
ros2 launch qcar_gazebo qcar_world.launch.py
```

3. In another terminal, run both detectors:

```bash
source /opt/ros/humble/setup.bash
source /root/ros2_ws/install/setup.bash
ros2 launch my_qcar_nodes perception.launch.py image_topic:=/qcar/csi_front/image_raw
```

### Run each detector separately

```bash
ros2 launch my_qcar_nodes lane_detection.launch.py image_topic:=/qcar/csi_front/image_raw
ros2 launch my_qcar_nodes object_detection.launch.py image_topic:=/qcar/csi_front/image_raw confidence_threshold:=0.45
```

### Topics published

- Lane detector:
	- `/perception/lane/overlay` (`sensor_msgs/msg/Image`)
	- `/planning/center_offset` (`std_msgs/msg/Float64`)
	- `/planning/waypoints` (`std_msgs/msg/Float64MultiArray`)
- Object detector:
	- `/perception/object/overlay` (`sensor_msgs/msg/Image`)
	- `/perception/object/detections` (`std_msgs/msg/String`, JSON array)

### Quick verification

```bash
ros2 topic list | grep perception
ros2 topic echo /planning/center_offset
ros2 topic echo /perception/object/detections
```