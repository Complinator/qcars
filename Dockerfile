FROM osrf/ros:noetic-desktop-full

# Install basics
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    python3-pip \
    python3-rosdep \
    python3-catkin-tools \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Update rosdep
RUN rosdep update

# Create catkin workspace
RUN mkdir -p /root/catkin_ws/src
WORKDIR /root/catkin_ws/src

# Clone QCar repo (open-source one by bchampp)
RUN git clone https://github.com/bchampp/autonomous-driving.git qcar

# Build workspace
WORKDIR /root/catkin_ws
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"

# Source ROS every time a shell opens
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc
RUN echo "source /root/catkin_ws/devel/setup.bash" >> /root/.bashrc

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Default command is handled by entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
