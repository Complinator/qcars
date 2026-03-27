#!/bin/bash
set -e

# Configure GPU acceleration for WSL2
export LIBGL_ALWAYS_INDIRECT=0
export MESA_D3D12_DEFAULT_ADAPTER_NAME=AMD
export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH

# Source ROS setup
source /opt/ros/humble/setup.bash
source /root/ros2_ws/install/setup.bash

# Auto-build workspace on container startup unless explicitly disabled.
# This keeps mounted source changes available without manual build steps.
if [ "${QCAR_SKIP_AUTOBUILD}" != "1" ]; then
    echo "[entrypoint] Running colcon build --symlink-install ..."
    cd /root/ros2_ws
    colcon build --symlink-install
    source /root/ros2_ws/install/setup.bash
fi

# Fix line endings if volume mounted
if [ -d /root/ros2_ws/src/my_qcar_nodes ]; then
    find /root/ros2_ws/src/my_qcar_nodes -name "*.py" -exec dos2unix {} \; 2>/dev/null || true
fi

exec "$@"
