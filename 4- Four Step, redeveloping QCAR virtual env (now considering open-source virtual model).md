---
date: 2025-07-25
estimated-date: 2025-08-29
task: Based on various difficulties when setting up the virtual env + gazebo model of the official qcar2 model, and the oportunity to move to a completelly open-source model, the team has decided to pivot our efforts into rebuild the environment in order to set up the open-source model rather than the official (private) one.
terms:
  - Containerization
  - Docker
  - Gazebo
  - Open-Source
---
## Overview

As the team advanced in the development of a robust simulation environment for the QCar2 model developed by Quanser, several unforeseen challenges emerged. Initially, the primary goal was to replicate the behavior of the QCar2 within a virtual environment, enabling a scalable, cost-effective, and safe platform for development, testing, and experimentation with autonomous driving algorithms. However, despite the theoretical simplicity of this objective, the team encountered substantial practical roadblocks that required both strategic redirection and technical adaptation.

One of the earliest and most persistent issues was the **scarcity of official documentation** detailing the necessary steps for configuring a custom simulation environment specifically tailored to the QCar2. This lack of formal guidance significantly complicated the integration process. Moreover, access to the QCar2 model itself presented logistical difficulties; acquiring the model, ensuring compatibility with existing tooling, and achieving functional execution added further complexity. These obstacles introduced a bottleneck in the workflow, impeding the team's progress in deploying a digital twin of the QCar2.

However, amidst these challenges, a **notable opportunity surfaced**: the discovery of an open-source QCar simulation model developed by an external community. Unlike the proprietary Quanser solution, this model was fully transparent and specifically designed to operate within customizable simulation environments (but it was not actively maintained, so it was and older qcar version with no recent updates). This development aligned strongly with the team’s broader open-source philosophy and project goals. After careful evaluation, the team **unanimously agreed to pivot** toward this open-source solution, recognizing its potential to streamline development and reduce dependency on proprietary technologies.

Before fully committing to the open-source model, the team conducted a series of validation tests using a set of **executables provided by the official Quanser team**. These executables were deployed within a Windows 11 virtual machine in an attempt to initialize and configure a simulation environment. The tests confirmed that these tools primarily served to prepare physical QCar hardware for operation, including the installation of key drivers, low-level controller interfaces (such as HAL and PAL layers), and other runtime dependencies, but **did not contribute meaningfully** to the construction of a standalone simulation (digital twin) of the QCar2. Thus, while informative, the outcome further reinforced the team's decision to adopt the open-source model as the simulation foundation moving forward.

It is important to note that the open-source model being adopted **corresponded to the original QCar**, not the QCar2, which introduced a generational gap in terms of hardware abstraction and software compatibility. After a careful technical assessment, the team concluded that this discrepancy was acceptable at the current stage of development, given that the primary objectives were exploratory and foundational in nature. Nonetheless, this decision carried several implications. Specifically, it necessitated **a downgrade in multiple software components** to ensure compatibility with the older QCar model. These included reverting from ROS 2 to the original ROS framework, and utilizing older versions of Gazebo and RViz, all of which operate under the **Catkin build system** as opposed to more modern alternatives like Colcon.

Moreover, attempts to modify or upgrade the simulation environment to accommodate newer model definitions proved increasingly error-prone and unstable. Numerous dependency conflicts, API mismatches, and integration issues arose when trying to retrofit the existing environment. As a result, it became evident that **retrofitting the original environment was not viable**. Rather than continuing to apply incremental fixes to a structurally flawed system, the team chose to initiate a **complete redevelopment of the simulation environment**, grounded on the foundations of a cleaner architecture.

The remainder of this report documents the process of designing and implementing a **completely new simulation environment**, based on the **Gazebo-based autonomous driving simulation framework maintained in the open-source `bchampp` repository**. This repository served as the foundation for a new, containerized development ecosystem, one that is robust, reproducible, and flexible for future expansion.

The newly developed environment is structured around a **Docker-based architecture**, ensuring cross-platform compatibility and ease of deployment. It includes:

- A base Docker image encapsulating all essential dependencies for QCar simulation.
- Templates and executable scripts to automate the container build and runtime process across both Linux and Windows systems.
- A modular file structure facilitating rapid development and integration of future ROS nodes, scenarios, or model enhancements.

Through this new architecture, the team establishes a sustainable path forward for QCar simulation, one that accommodates the current capabilities of the open-source model, while remaining extensible for future improvements or eventual migration to a more accurate QCar2 digital twin.
## Terms and knowledge

The new simulation environment adopted by the team is based on the **open-source repository [autonomous-driving](https://github.com/bchampp/autonomous-driving/blob/main/src/qcar/src/qcarnode.py)**, created by the GitHub user **bchampp**. This repository provides a robust and modular framework for simulating autonomous vehicle behavior using ROS (Robot Operating System), **Gazebo** for 3D simulation, and a series of custom ROS nodes that simulate core autonomous driving functionalities.

Unlike the proprietary Quanser QCar2 environment, this open-source environment is designed with **transparency, simplicity, and portability** in mind. It allows researchers and developers to work with virtualized vehicles in a realistic physics-based environment, making it especially suitable for projects involving autonomy, perception, and planning.
### Catkin Workspace

The `autonomous-driving` repo is built on top of a **Catkin workspace**, which is a ROS-native build system. A **Catkin workspace** is the standard directory structure used in ROS (pre-ROS2) for organizing and compiling packages. It typically consists of the following core directories:

- `src/`: Contains all source code (ROS packages).
- `build/`: Temporary build files generated during compilation.
- `devel/`: Stores built executable binaries, libraries, and setup scripts for environment sourcing.

Catkin is a CMake-based system, meaning it provides fine-grained control over dependencies, compilation order, and build configuration. This structure makes the environment **highly modular and extensible**, enabling developers to add or modify packages without altering the entire system.

> **Comparison Note**: The official Quanser model partially adopted ROS2, and instead of `.launch` files, it used **hybrid Python launch scripts** (typically `.launch.py`), which add complexity, particularly for those unfamiliar with ROS2's newer paradigms. In contrast, the `bchampp` environment uses standard `.launch` files written in XML — more accessible, mature, and better documented, thereby simplifying integration and debugging.
### Repository Structure

The `autonomous-driving` repository is well-structured and separated into ROS packages, each responsible for a key functionality in the autonomous driving stack. These are located in the `src/` directory of the Catkin workspace and include the following:
##### **1. `qcar_gazebo/`**

This package provides the **Gazebo simulation environment** for the QCar model.

- Includes the `qcar_world.launch` file, which spawns a **digital twin** of the QCar inside a Gazebo world. This launch file initializes the vehicle model, sensor configurations, and physics parameters.
- Loads SDF (Simulation Description Format) and URDF (Unified Robot Description Format) files, which describe the robot’s structure, dynamics, sensors, and actuators.
- Contains plugin configurations for vehicle dynamics, differential drive, cameras, LiDAR, and IMU.

**This is the central package being used by the team** to initialize and run the simulated vehicle.
##### **2. `qcar_carla/`**

A bridge or placeholder package for integrating the QCar model into the **CARLA Simulator**, another high-fidelity open-source autonomous driving simulator. This is not used in the current phase of the project..
##### **3. `qcar_control/`**

Responsible for implementing **control algorithms** that drive the vehicle:

- Includes PID controllers, velocity controllers, and possibly low-level actuator interfacing within the simulation.
- Nodes here translate high-level navigation commands into steering and throttle actions that drive the QCar in Gazebo.
##### **4. `qcar_interface/`**

Acts as a middleware or **ROS interface** between various modules and the simulated (or physical) QCar, Defines ROS topics, services, and TF frames, ensuring coherent message passing between perception, planning, and control modules.
##### **5. `qcar_mapping/`**

Implements **SLAM (Simultaneous Localization and Mapping)** and **mapping algorithms**.

- Likely integrates packages such as GMapping, Hector SLAM, or Cartographer.
- Provides real-time 2D/3D map generation based on sensor data, useful for navigation and localization tasks.
##### **6. `qcar_perception/`**

Handles **environmental awareness** using simulated sensors like:

- Cameras
- LiDAR
- IMU
- Possibly radar or ultrasonic sensors

Contains nodes that process this data to detect lanes, obstacles, or other vehicles. Potential for future development includes object detection using machine learning models.
##### **7. `qcar_planning/`**

It performs **local planning** by interpreting **lane waypoints** and optionally **object detection** data (like stop signs) to control the car’s **steering and throttle**, enabling **autonomous lane following** and **basic stop sign handling**. (Apparently still on development)
### Hal/Pal Role

The official Quanser QCar environment depends heavily on two hardware abstraction libraries: **HAL** and **PAL**.

- **HAL (Hardware Abstraction Layer)**: Provides a unified interface for accessing low-level hardware components such as GPIO pins, motors, and sensors.
- **PAL (Platform Abstraction Layer)**: Abstracts the operating system layer, allowing cross-platform hardware interactions and real-time control.

These libraries are crucial for **physical hardware deployment**, as they handle real-time communication with the car’s embedded systems.
However, in the current context of **pure simulation**, such libraries are:

- **Unnecessary**: All hardware behavior is simulated via Gazebo plugins and ROS interfaces.
- **Unsupported** in open environments: HAL/PAL are proprietary to Quanser and are not designed for use outside their own ecosystem.

This is a major advantage of the open-source approach — the simulation runs **entirely in software**, eliminating the complexity of hardware drivers and proprietary layers.
## Results

This section presents all artifacts, configurations, and commands used in the successful construction and execution of the Dockerized simulation environment for this new open-source QCar model.
#### Project Structure

A new folder was created to hold all Docker-related artifacts:

```bash
qcar_docker/ 
	├──	config/ # Contain excecutable templates for different OS
		├──	linux/
			└── example.sh
		└── windows/
			├──	config.xlaunch # Contain parameters for xsrvr to launch
			└── example.ps1
	├──	nodes/ # Contain nodes and requirements
	├── .gitattributes # To prevent future CRLF issues
	├── .gitignore # Ignore unnecessary files during push
	├── Dockerfile # Script to build the environment
	├── entrypoint.sh # Bash script to initialize ROS inside container 
	├── Readme.md # Holds information about the container
	└── .dockerignore # Ignore unnecessary files during image build
```
#### Dockerfile – Full Content and Explanation

The Dockerfile used for this stage is reproduced below:

```dockerfile
FROM osrf/ros:noetic-desktop-full

# Install basics
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    python3-pip \
    python3-rosdep \
    python3-catkin-tools \
    ros-noetic-ackermann-msgs \
    ros-noetic-gazebo-msgs \
    build-essential \
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
```

This Dockerfile defines a containerized development environment based on the `osrf/ros:noetic-desktop-full` image, which provides a complete installation of ROS Noetic along with Gazebo and various graphical tools preconfigured. The base image is ideal for ROS1-based robotics projects and provides a stable foundation for simulation and development tasks. The Dockerfile begins by installing a set of essential packages, including `git`, `wget`, `curl`, and `python3-pip`, which are commonly used for downloading repositories and managing Python-based tooling. It also includes `python3-rosdep` and `python3-catkin-tools`, which are necessary for dependency resolution and building Catkin workspaces. Specific ROS packages like `ros-noetic-ackermann-msgs` (for vehicle control messages) and `ros-noetic-gazebo-msgs` (for Gazebo communication) are included to ensure compatibility with the QCar simulation. The `build-essential` package is also installed to provide compiler tools needed for building C++-based ROS packages. To reduce image size, the package cache is cleared after installation.

Following the installation of dependencies, the Dockerfile updates `rosdep`, which is a ROS tool for resolving and installing system dependencies listed in `package.xml` files. It then creates a standard Catkin workspace at `/root/catkin_ws/src`, which will serve as the development root for the simulation environment. The working directory is switched to this location to prepare for the cloning of necessary packages. The Dockerfile clones the `autonomous-driving` repository by `bchampp` into a subdirectory named `qcar`, which contains the complete open-source QCar simulation environment, including the Gazebo model, control nodes, and associated ROS packages. Additionally, a local package named `nodes` (presumably developed by the user) is copied into the workspace's `src` directory. This local package should include a `package.xml` and `CMakeLists.txt`, indicating it's a ROS-compatible package ready for integration into the build process.

The next step in the Dockerfile involves building the entire Catkin workspace. The working directory is changed to the workspace root (`/root/catkin_ws`), and a Bash command is executed to source the base ROS environment (`/opt/ros/noetic/setup.bash`) before running `catkin_make`, which compiles all packages found within the `src` directory and links them into the `devel` folder. To ensure that the ROS environment is properly configured each time a new shell is opened within the container, two lines are appended to the root user’s `.bashrc`: one to source the ROS Noetic installation, and another to source the workspace's own setup script. This ensures that ROS tools and environment variables are always available inside the container, without needing to source them manually.

Finally, the Dockerfile includes an `entrypoint.sh` script, which is copied into the container’s root filesystem and marked as executable. This script is specified as the container's `ENTRYPOINT`, meaning it will be executed whenever the container starts. The `CMD ["bash"]` statement provides the default command to run inside the container, allowing interactive shell access. This structure allows for clean container startup, environment setup, and interactive development, making the Docker container suitable for both automated simulation launches and manual ROS/Gazebo experimentation.
#### entrypoint.sh

```bash
#!/bin/bash
set -e

# Source ROS setup
source /opt/ros/noetic/setup.bash
source /root/catkin_ws/devel/setup.bash

# Start roscore in the background
roscore &
sleep 5   # give roscore time to start

# Launch QCar Gazebo
exec "$@" # here run 'roslaunch qcar_gazebo qcar_world.launch' This takes some time, so no worries if it seems stuck
```

This `entrypoint.sh` script is designed to set up the environment and start essential ROS services when the Docker container is launched. First, it sources the necessary ROS setup files to ensure the environment is configured correctly. After that, it starts `roscore` in the background. `roscore` is the central communication hub in any ROS system, and it needs to be running before launching other ROS nodes. The script waits for a few seconds (`sleep 5`) to give `roscore` time to initialize. Finally, it executes the command passed to the Docker container (`exec "$@"`), which in this case would typically be a command like `roslaunch qcar_gazebo qcar_world.launch` to start the QCar Gazebo simulation. This allows the user to launch the simulation or any other ROS-based process when the container starts. The `exec` ensures that the passed command takes over the script's process, which is useful for managing the lifecycle of ROS nodes.
#### .gitattributes

```bash
*.py text eol=lf
*.sh text eol=lf
*.launch text eol=lf
*.xml text eol=lf
*.txt text eol=lf
Dockerfile text eol=lf
```

Used to configure Git’s handling of files in a repository, particularly in terms of **end-of-line (EOL) normalization**. The attributes specified here set the EOL behavior for specific file types to ensure consistent handling across different operating systems (Windows, Linux, macOS).
#### Other files

Finally, there is the **.dockerignore**, which specifies files ignored in the docker containerization process, **.gitignore**, which contains files ignored when committing progress via git, and **Readme.md**, holding general info on how to run the container.  
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
# Run VcXsrv from saved config
Start-Process 'C:\Path\to\config.xlaunch'

# Wait a bit to ensure VcXsrv starts
Start-Sleep -Seconds 2

# Set DISPLAY variable for Docker
$env:DISPLAY = "host.docker.internal:0.0" 

# Run the Docker container with ROS1
docker run -it --rm `
    -e DISPLAY=$env:DISPLAY `
    -v /tmp/.X11-unix:/tmp/.X11-unix `
    --name qcar `
    qcar-sim
    
# Kill VcXsrv after Docker container exits
Get-Process vcxsrv -ErrorAction SilentlyContinue | Stop-Process
```

This file is used to open the x server via the **config.xlaunch**, then launching the container, having defined the x server variable, and finally, on close, not only removing the container, but also closing the x server. To run this make sure to have the **config.xlaunch** file.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<XLaunch WindowMode="MultiWindow" ClientMode="NoClient" LocalClient="False" Display="-1" LocalProgram="xcalc" RemoteProgram="xterm" RemotePassword="" PrivateKey="" RemoteHost="" RemoteUser="" XDMCPHost="" XDMCPBroadcast="False" XDMCPIndirect="False" Clipboard="True" ClipboardPrimary="True" ExtraParams="-ac -nowgl -multiwindow -clipboard +iglx" Wgl="False" DisableAC="True" XDMCPTerminate="False"/>
```

---
### Linux (not tested):

1. Run xhost +local:docker to allow container connections to X server.

2. Run the container:

```bash
#!/bin/bash

# Allow Docker containers to access X11
xhost +local:docker

# Run Docker container
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --name qcar \
    qcar-sim
    
# Revoke permissions after container exits (optional, more secure)
xhost -local:docker
```

---
#### Environment Testing

To verify the graphical environment inside the container, let's launch the gazebo simulation, for that, make sure to navigate to the gazebo launch folder:

```bash
cd src/qcar/src/qcar_gazebo/launch
```

Now you can launch the model by simply running

```bash
roslaunch qcar_gazebo qcar_world.launch
```

#### Final remarks

This phase concludes with a fully functional ROS based simulation container that includes:

- Ubuntu 22.04 (by default with ros)
- ROS and Catkin workspace (with Gazebo and RViz)
- GUI support over X11 for all major platforms
- Basic environment to implement future nodes

All software and configuration are isolated from the host system, ensuring reproducibility and consistency across team members’ environments. This forms a stable foundation for further development, including simulation control, robot modeling, and ROS 2 node programming.

>  _**Next phase**: Implementation of custom ROS nodes and bridges for QCar simulation control and sensor interaction (not covered in this log)._

>  _All of this information and progress is being constantly updated in the github repository [qcars](https://github.com/Complinator/qcars/tree/updated), branch **"updated"**_