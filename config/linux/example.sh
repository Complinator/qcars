#!/bin/bash

# Allow Docker containers to access X11
xhost +local:docker

# Run Docker container
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /c/Path/to/nodes/scripts:/root/catkin_ws/src/nodes/scripts \
    --name qcar \
    qcar-sim

# Revoke permissions after container exits (optional, more secure)
xhost -local:docker
