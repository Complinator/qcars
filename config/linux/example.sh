#!/bin/bash

# Allow Docker containers to access X11
xhost +local:docker

# Run Docker container
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --name qcar_sim qcar_sim bash

# Revoke permissions after container exits (optional, more secure)
xhost -local:docker
