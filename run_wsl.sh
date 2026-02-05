#!/bin/bash

# Build the docker image
echo "Building docker image..."
docker build -t qcar-sim-wsl .

# Run the Docker container with ROS1 and WSLg
echo "Running docker container..."
docker run -it --rm \
    --privileged \
    -e DISPLAY=$DISPLAY \
    -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
    -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
    -e PULSE_SERVER=$PULSE_SERVER \
    -e LIBGL_ALWAYS_INDIRECT=1 \
    -e LD_LIBRARY_PATH=/usr/lib/wsl/lib \
    -e MESA_D3D12_DEFAULT_ADAPTER_NAME=AMD \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /mnt/wslg:/mnt/wslg \
    -v /usr/lib/wsl:/usr/lib/wsl:ro \
    -v /dev/dri:/dev/dri \
    --device=/dev/dxg \
    -v $(pwd)/nodes:/root/ros2_ws/src/my_qcar_nodes \
    -v $(pwd)/simulation/qcar/src/qcar_gazebo:/root/ros2_ws/src/qcar_gazebo \
    -v $(pwd)/simulation/qcar/src/qcar_control:/root/ros2_ws/src/qcar_control \
    -v $(pwd)/simulation/qcar/src/realsense2_description:/root/ros2_ws/src/realsense2_description \
    -v $(pwd)/simulation/qcar/src/qcar_interface:/root/ros2_ws/src/qcar_interface \
    --name qcar-wsl \
    qcar-sim-wsl