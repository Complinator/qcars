FROM osrf/ros:noetic-desktop-full-focal

# Install basics
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    wget \
    curl \
    python3-pip \
    python3-rosdep \
    python3-catkin-tools \
    ros-noetic-ackermann-msgs \
    ros-noetic-gazebo-msgs \
    ros-noetic-velocity-controllers \
    dos2unix \
    build-essential \
    mesa-utils \
    mesa-va-drivers \
    mesa-vulkan-drivers \
    && rm -rf /var/lib/apt/lists/*

# Update rosdep
RUN rosdep update

# Create catkin workspace
RUN mkdir -p /root/catkin_ws/src
WORKDIR /root/catkin_ws/src

# Clone QCar repo (open-source one by bchampp)
RUN git clone https://github.com/bchampp/autonomous-driving.git qcar

# Copy your nodes package (contains package.xml/CMakeLists.txt)
COPY nodes /root/catkin_ws/src/nodes

# Build workspace
WORKDIR /root/catkin_ws
RUN find src/nodes -name "*.py" -exec dos2unix {} \; || true
RUN find src/nodes -name "*.sh" -exec dos2unix {} \; || true
RUN chmod +x src/nodes/scripts/*.py || true

RUN rosdep install --from-paths src --ignore-src -r -y
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"

# Source ROS every time a shell opens
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc
RUN echo "source /root/catkin_ws/devel/setup.bash" >> /root/.bashrc

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

# Default command is handled by entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
