#!/bin/bash

# Start XQuartz in background (if not already running)
open -a XQuartz

# Give it a moment to start up
sleep 2

# Set DISPLAY
export DISPLAY=host.docker.internal:0

# Run Docker container
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --network host \
    --name qcar_sim qcar_sim bash
