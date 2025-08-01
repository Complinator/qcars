FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt upgrade -y && \
    apt install -y \
    x11-apps \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-rviz2 \
    ros-humble-demo-nodes-cpp \
    ros-humble-demo-nodes-py \
    python3-colcon-common-extensions \
    git \
    curl \
    net-tools \
    nano

# Configuración de ROS2
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
