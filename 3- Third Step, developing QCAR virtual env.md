---
date: 2025-07-18
estimated-date: 2025-07-25
task: At this point , the team has decided the technologies to use inside the simulation, and where the virtual environment for that simulation is going to be, so now with everything on our hands, it is time to start developing the virtual environment.
terms:
  - Containerization
  - Docker
  - Gazebo
---
## Overview

The present entry documents the initial phase of constructing a modular and reproducible simulation environment for the Quanser QCar 2 robotic platform. The core objective of this milestone is to establish a fully functional virtual environment using Docker containers, enabling simulation, visualization, and experimentation of QCar-related robotic functionalities in isolation from the host operating system.

In this phase, the emphasis lies on laying the technological foundation required for upcoming development stages. This includes the selected base operating system, middleware, visualization tools, and container configuration. All tooling and dependencies are to be packaged inside a Docker container for consistency, version control, and portability across various host platforms (Windows, macOS, Linux).

As a critical architectural decision, ROS 1 was deprecated in favor of ROS 2, specifically the Humble Hawksbill distribution. This transition, agreed upon during the previous project meeting, was motivated by two factors:
- ROS 2 is the middleware utilized in actual QCar 2 deployments, thus improving the fidelity of our simulated environment.
- ROS 2 offers improved modularity, real-time capabilities, and native DDS (Data Distribution Service) integration, which are essential for modern robotic applications.

The present document includes a theoretical and practical walkthrough of the container construction, package installation, graphical interface enablement, and platform-specific considerations. The culmination of this stage results in a fully functional Docker container capable of running Gazebo and RViz with ROS 2, providing the basis for robotic control node development in future phases.
## Terms and knowledge

Docker is a platform designed to automate the deployment of applications within lightweight, portable containers. These containers are similar to virtual machines but differ in that they share the host OS kernel and are thus significantly more efficient.

In our simulation context, Docker is used to isolate the full robotics development environment, ensuring:
- Independence from host operating system and libraries.
- Encapsulation of all simulation and visualization tools (ROS 2, Gazebo, RViz).
- Portability across different systems with minimal setup.
#### Docker Workflow for Simulation

The creation of the QCar simulation environment using Docker follows a sequential development model:

**Step 1**: Create a Dockerfile – A declarative script that defines the OS base image, packages, tools, and configuration steps needed.

**Step 2**: Build the Docker image – This process compiles the Dockerfile instructions into a binary image, which is a read-only blueprint of the desired environment.

**Step 3**: Launch a Docker container – A container is a writable, runtime instance of an image. It runs all software as defined in the Dockerfile.

**Step 4 (optional)**: Mount volumes – Data persistence and interoperation with the host can be enabled via volumes, but are not used in this specific stage.

**Step 5**: Enable graphical support – Since ROS simulation tools are graphical (Gazebo, RViz), special configuration is needed to support GUI output from within containers using the host's X server.

The following practical section maps each of these conceptual steps to specific commands and files used to build and run the simulation container.
## Results

This section presents all artifacts, configurations, and commands used in the successful construction and execution of the Dockerized simulation environment for QCar 2.
#### Project Structure

A new folder was created to hold all Docker-related artifacts:

```bash
qcar_docker/  
	├── Dockerfile # Script to build the environment  
	├── entrypoint.sh # Bash script to initialize ROS 2 inside container  
	└── .dockerignore # Ignore unnecessary files during image build
```
#### Dockerfile – Full Content and Explanation

The Dockerfile used for this stage is reproduced below:

```dockerfile
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

# ROS2 setup
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

The Dockerfile serves as a blueprint for constructing a self-contained virtual environment capable of running a ROS 2-based robotics simulation—specifically tailored for the QCar 2 platform. It begins by selecting a foundational image that already includes ROS 2 Humble along with essential desktop tools like RViz and Gazebo. This provides a solid starting point, reducing the need for extensive manual setup.

To ensure the environment remains non-interactive and automated—crucial for containerized builds—the script configures the APT package manager to suppress prompts. It then installs a comprehensive set of packages required for development and simulation. These include graphical tools for interacting with X11 (enabling GUI forwarding), Gazebo integration packages for ROS 2, the RViz visualization environment, demo ROS nodes, and development tools such as Git, curl, and colcon (ROS 2’s primary build system).

The container's shell is explicitly set to Bash to ensure compatibility with ROS 2 environment sourcing commands. A line is also appended to the shell configuration to make the ROS environment available by default in every terminal session within the container. To streamline how the container is launched and to ensure it’s always “ROS 2 ready,” a custom entrypoint script is included and designated to execute by default whenever the container starts.

#### entrypoint.sh

```bash
#!/bin/bash  
source /opt/ros/humble/setup.bash  
exec "$@"
```

This script sources the ROS 2 environment and then executes the command passed to the container (e.g., ros2 launch ... or bash). It ensures every container session is ROS 2-ready.

#### .dockerignore

.dockerignore helps speed up the image build by excluding irrelevant files:

```bash
*.log  
*.tmp
```
#### Image Build

Inside qcar_docker/, the following command was used to build the image:

```bash
cd qcar_docker/
docker build -t qcar_sim .
```

> The -t flag tags the resulting image as qcar_sim for easier reference during container runs.

#### Running the Container with GUI (OS-specific)

To support GUI applications like Gazebo and RViz from inside the container, special host configuration is required.

---
### Windows (with VcXsrv):

Steps:

1. Install and launch [VcXsrv](https://sourceforge.net/projects/vcxsrv/).
    - Use “Multiple windows” mode.
    - Enable “Disable access control”.

2. Set DISPLAY environment variable and run container (PowerShell):

```powershell
$env:DISPLAY="host.docker.internal:0.0"  
docker run -it --rm -e DISPLAY=$env:DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --network host --name qcar_sim qcar_sim bash
```

---
### macOS (with XQuartz, not tested):

1. Install and open XQuartz.
    - Enable “Allow connections from network clients”.
    - Run xhost + from the terminal.

2. Execute:

```bash
export DISPLAY=host.docker.internal:0  
docker run -it --rm \ 
	-e DISPLAY=$DISPLAY \
	-v /tmp/.X11-unix:/tmp/.X11-unix \  
	--network host \
	--name qcar_sim qcar_sim bash \
```

---
### Linux (not tested):

1. Run xhost +local:docker to allow container connections to X server.

2. Run the container:

```bash
xhost +local:docker
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --name qcar_sim qcar_sim bash
```

---
#### Environment Testing

To verify the graphical environment inside the container, let's launch gazebo:

```bash
ros2 launch gazebo_ros <gazebo_model_to_use>
```

or just simply launch the application:

```bash
gazebo
```

also you can try the same with RViz

```bash
rviz2
```

#### Final remarks

This phase concludes with a fully functional ROS 2-based simulation container that includes:

- Ubuntu 22.04 (by default with ros)
- ROS 2 Humble (with Gazebo and RViz)
- GUI support over X11 for all major platforms
- Developer utilities and ROS 2 build tooling

All software and configuration are isolated from the host system, ensuring reproducibility and consistency across team members’ environments. This forms a stable foundation for further development, including simulation control, robot modeling, and ROS 2 node programming.

>  _**Next phase**: Implementation of custom ROS 2 nodes for QCar simulation control and sensor interaction (not covered in this log)._