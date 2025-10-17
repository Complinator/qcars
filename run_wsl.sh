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
    -v $(pwd)/nodes/scripts:/root/catkin_ws/src/nodes/scripts \
    --name qcar-wsl \
    qcar-sim-wsl