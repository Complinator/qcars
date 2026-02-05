FROM osrf/ros:humble-desktop-full

# Install basics
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    wget \
    curl \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-xacro \
    ros-humble-ackermann-msgs \
    ros-humble-cv-bridge \
    python3-matplotlib \
    python3-opencv \
    python3-tk \
    dos2unix \
    build-essential \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    && rm -rf /var/lib/apt/lists/*

# Update rosdep
RUN rosdep init || true && rosdep update

# Create colcon workspace
RUN mkdir -p /root/ros2_ws/src
WORKDIR /root/ros2_ws/src

# Note: The QCar simulation repo (autonomous-driving) is ROS 1 based.
# It is excluded here. To use it, you'd need to migrate it or use ros1_bridge.
# RUN git clone https://github.com/bchampp/autonomous-driving.git qcar

# Copy your nodes package
COPY nodes /root/ros2_ws/src/my_qcar_nodes

# Copy migrated simulation packages (and exclude ROS 1 legacy packages)
COPY simulation/qcar/src/qcar_gazebo /root/ros2_ws/src/qcar_gazebo
COPY simulation/qcar/src/qcar_control /root/ros2_ws/src/qcar_control
COPY simulation/qcar/src/realsense2_description /root/ros2_ws/src/realsense2_description
COPY simulation/qcar/src/qcar_interface /root/ros2_ws/src/qcar_interface

# Build workspace
WORKDIR /root/ros2_ws

# Fix line endings
RUN find src -name "*.py" -exec dos2unix {} \; || true
RUN chmod +x src/my_qcar_nodes/my_qcar_nodes/*.py || true

# Install dependencies
RUN apt-get update && rosdep install --from-paths src --ignore-src -r -y --skip-keys "ament_python ament_cmake"
RUN apt-get install -y \
    xterm \
    ros-humble-gazebo-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-xacro \
    ros-humble-joint-state-publisher-gui \
    ros-humble-joint-state-broadcaster \
    ros-humble-velocity-controllers \
    ros-humble-position-controllers

# Build (symlink install for development)
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build --symlink-install"

# Source ROS every time a shell opens
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
RUN echo "source /root/ros2_ws/install/setup.bash" >> /root/.bashrc

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
