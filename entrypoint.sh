#!/bin/bash
set -e

# Source ROS setup
source /opt/ros/noetic/setup.bash
source /root/catkin_ws/devel/setup.bash

# Fix line endings and permissions for mounted volumes (if any)
if [ -d /root/catkin_ws/src/nodes/scripts ]; then
    find /root/catkin_ws/src/nodes -name "*.py" -exec dos2unix {} \; 2>/dev/null || true
    chmod +x /root/catkin_ws/src/nodes/scripts/*.py 2>/dev/null || true
fi

# Start roscore in the background
roscore &
sleep 5   # give roscore time to start

# Launch QCar Gazebo
exec "$@" # here run 'roslaunch qcar_gazebo qcar_world.launch' This takes some time, so no worries if it seems stuck