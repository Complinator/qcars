#!/bin/bash
set -e

# Source ROS setup
source /opt/ros/noetic/setup.bash
source /root/catkin_ws/devel/setup.bash

# Start roscore in the background
roscore &
sleep 5   # give roscore time to start

# Launch QCar Gazebo
exec "$@" # here run 'roslaunch qcar_gazebo qcar_world.launch' This takes some time, so no worries if it seems stuck