---
date: 2025-08-29
estimated-date: 2025-09-12
task: At this point we already have a functioning and fully open-source environment, So we need to move on into exploring this workspace. For that, we will start creating nodes that will alter the behavior of the digital QCar, being able to control it like "remote controlled", also getting familiarized with the pub-sub scheme
terms:
  - Pub/Sub
  - Docker
  - Gazebo
  - Nodes
---
## Overview

At this stage, significant progress has been made in the development of the simulation environment for the QCar model. After overcoming various hurdles related to setting up the environment, including the challenges of adapting to an open-source QCar model, the team succeeded in deploying a fully operational QCar simulation within the Gazebo environment. This marked the completion of the most technically demanding phase of the project. However, the simulation, while functional, currently lacks the ability to perform dynamic actions such as turning, accelerating, or responding to control inputs. The next major task, therefore, involves transitioning from a passive simulation to an actively controlled system, where the QCar can perform tasks autonomously or in response to user commands.

To achieve this, the team now faces the challenge of developing custom ROS nodes from scratch to enable the QCar to interact with its environment and execute control commands. A key realization in this phase is that the development effort will not be limited to creating subscription nodes to receive sensor or control data, but will also involve the creation of communication bridges. This is because the existing publish/subscribe (pub/sub) model, which works for physical QCars, needs to be adapted for the simulated environment. Consequently, the team must not only focus on understanding the ROS pub/sub model but also gain a deep understanding of how Gazebo simulations work, particularly in terms of the physics engine that drives the virtual car’s movement and behavior.

In order to gain the necessary knowledge and insight, the team undertook extensive research into both the theoretical and practical aspects of QCar systems. A crucial part of this knowledge acquisition was a visit to the _Universidad Técnica Federico Santa María_ (UTFSM), where the team had the opportunity to examine physical QCars2 in action. This visit proved invaluable, as the team observed the official Quanser QCars2 performing various tasks, including line detection, joystick control, and communication with other systems. This firsthand experience allowed the team to gain a deep understanding of the QCar’s capabilities, including its powerful onboard CPU, sensor integration, and control over various commands and interactions with its environment.

During the visit, the team also had the chance to observe the physical structure of the QCar, including its size, components, and the positioning of essential sensors such as cameras and LIDAR. These observations provided the team with crucial insights into the vehicle’s design, which would later inform their decisions regarding the development of control and decision-making modules within the simulated environment. Furthermore, conversations with the team at UTFSM provided valuable networking opportunities and detailed insights into the various use cases of the QCar platform, as well as ongoing research in autonomous driving and robotic systems.

One of the key takeaways from the visit was the realization that while the QCar offers an excellent platform for research and development in autonomous driving, its primary role is to provide a modern vehicle's hardware workspace, rather than offering pre-built decision-making functionality. As a result, the focus of the project shifted towards the development of internal control systems, decision-making algorithms, and AI that would enable the QCar to make autonomous decisions and interact intelligently with its environment. This insight highlighted the complexity of the path forward, particularly when the team plans to integrate a physical QCar into the simulation and research workflows.

For the time being, the project remains focused on the simulated QCar, which offers an ideal environment for testing and refining control algorithms before physical deployment. Building on the insights gained from the UTFSM visit and the continued research, the team has begun the process of developing several modules that will allow the QCar to interact with the simulation. These initial modules focus on simple tasks such as gathering basic information from the vehicle’s sensors and controlling fundamental movements like turning or accelerating. While these functionalities are relatively simple, their implementation revealed important insights into the communication protocols and internal structure of the simulation environment, as well as the necessary steps for scaling up to more advanced behaviors in the future.

The development of these modules has not only required adjustments to the existing environment structure but has also provided valuable lessons in how to effectively communicate with and control the QCar within the simulation. As the team continues to refine these control modules, the process of simulating the QCar’s movement and behavior will become more sophisticated, gradually paving the way for the eventual integration of a physical QCar into the system. This phase of the project, while challenging, has laid the groundwork for the next steps in developing a fully autonomous QCar system, both in simulation and eventually in the real world.
## Knowledge and Terms
#### Create Nodes Using Publish/Subscribe model in ROS

In the Robot Operating System (ROS), **nodes** are fundamental building blocks. Each node is essentially a small, modular, and independent unit of computation responsible for performing a specific task, such as controlling motors, reading sensors, or processing data. Nodes in ROS communicate with each other using a **publish/subscribe model** that facilitates a decoupled interaction between different parts of the system. This design promotes modularity, scalability, and ease of debugging, as nodes are loosely coupled and can function independently without needing to know the internal details of other nodes.

The **publish/subscribe** model is based on the concept of **topics**. Topics are named communication channels that allow nodes to send and receive messages. The two main roles in this communication pattern are **publishers** and **subscribers**:

- **Publishers** are nodes that send information (or messages) to a specific topic.
- **Subscribers** are nodes that listen for messages on that topic.

This model enables flexibility because nodes only interact with the topic name and the message format, not with each other directly. The publisher does not need to know how many subscribers are listening, and vice versa. As long as the message type remains consistent, new nodes can be added without disrupting existing communication.

The **QCar** simulation leverages this model for controlling and interacting with the car, as well as handling sensory data. For example, a control node might publish velocity commands (such as speed and steering angle) to a topic, while the QCar's simulation node subscribes to those commands to update the car's movement. Similarly, the car’s simulation can publish sensor data (e.g., camera feeds, LIDAR scans) to topics, which other nodes may subscribe to in order to process the data for decision-making tasks like path planning, obstacle detection, or behavior control.

This model is critical for the QCar simulation because the car needs to be able to dynamically respond to external inputs, such as control commands, and also provide feedback, such as sensor readings, to other parts of the system. For instance, the QCar will receive velocity and steering commands through the subscription model, and, in turn, it will publish real-time sensor data, such as LIDAR readings or camera images, to enable other nodes to process and react accordingly.

The **importance of the pub/sub model** in QCar simulations cannot be overstated. It allows for the separation of concerns between different subsystems (e.g., motion control, perception, planning, etc.), making it easier to modify, extend, or replace components without disrupting the entire system. For instance, new sensor modules or control algorithms can be added without requiring changes to the existing nodes. Additionally, the asynchronous nature of ROS communication ensures that the system can scale well, especially in real-time applications like autonomous driving, where responsiveness and low latency are essential.
#### Physics in Gazebo and QCar's Cinematic Model

Gazebo, as a powerful robotics simulation tool, uses a physics engine to simulate the real-world dynamics of robots in virtual environments. This engine is responsible for computing the interaction between objects based on physical principles such as force, torque, friction, and gravity. Gazebo supports several physics engines, with the most commonly used being **ODE (Open Dynamics Engine)**, **Bullet**, and **Simbody**. These engines resolve how objects move, collide, and interact within the simulated world by solving the equations of motion that govern physical systems.

However, the complexity of a robot’s behavior is not only determined by the physics engine but also by how the robot’s **kinematic and dynamic models** are defined. In the case of the QCar simulation, the **Ackermann steering model** is used to represent the car's motion. Understanding how this model works is crucial for controlling the car’s behavior in simulation, as it defines how the car’s wheels move in response to steering commands.

The **Ackermann model** is a widely used **kinematic model** for vehicles that incorporates a set of physical principles that define how a car with four wheels moves. The most notable feature of the Ackermann steering geometry is the fact that the car’s front wheels turn at an angle to allow the car to follow a curved path, while the rear wheels remain fixed. This model uses the concept of a **steering angle** to control the vehicle's trajectory, and the car's turning radius is governed by the angle of the front wheels.

At its core, the Ackermann model is described by the following principles:

- **Steering Angle**: The angle at which the front wheels are turned relative to the car’s body.
- **Turning Radius**: The radius of the circular arc that the car follows as it turns. The turning radius is determined by the steering angle and the wheelbase (distance between the front and rear axles).
- **Velocity**: The speed at which the car moves forward along the trajectory defined by the turning radius.

When controlling a QCar in simulation, nodes that publish velocity commands typically define the car’s **linear velocity** (forward speed) and **steering angle**. The QCar simulation will then compute the required wheel velocities to achieve the specified speed and steering behavior. This is where the car's **internal controllers** come into play. These controllers, which are part of the simulation’s kinematic model, compute the necessary speeds of the **individual wheels** (front and rear) based on the desired linear velocity and steering angle. Essentially, the Ackermann model resolves the car’s motion by breaking down the car's velocity into wheel velocities, ensuring the wheels rotate at the correct speeds to achieve the car's intended movement.

It is important to note that the **velocity defined in the node** is the **car's velocity**, i.e., the speed at which the center of the car’s mass is moving along its path. The kinematic model does not directly command the individual wheel speeds; rather, it calculates the required wheel velocities based on the desired motion. For example, if a command is issued to the QCar to move at a certain speed, the model internally computes how fast each wheel should rotate to move the car at the specified speed while maintaining the correct turning radius based on the steering angle. This decoupling of car-level velocity and wheel-level velocity is what enables more realistic and scalable simulations, as it mimics how physical vehicles would respond to control commands.

Understanding how Gazebo’s physics engine, combined with the Ackermann model, simulates the motion of the QCar is critical for developers working on the control algorithms. It not only informs how the vehicle’s movement will behave in response to commands but also shapes how developers design and implement control nodes that interact with the QCar simulation. When developing velocity controllers or implementing complex behaviors like lane-following or obstacle avoidance, the developers must account for these physics constraints and ensure that the simulation closely mirrors real-world behavior, both in terms of how the car moves and how it interacts with its environment.
## Results

In order to create the final nodes, several parts of the previously defined structure had to be modified/improved. This section cover every change and addition made to the original structure, considering also nodes and bridges added.
#### Project Structure

Several changes had been made inside of  `nodes/` folder, the new project structure looks like:

```bash
qcar_docker/ 
	├──	config/ # Contain excecutable templates for different OS
		├──	linux/
			└── example.sh
		└── windows/
			├──	config.xlaunch # Contain parameters for xsrvr to launch
			└── example.ps1
	├──	nodes/ # Contain nodes and requirements
		├──	scripts/ # Contain .py nodes, this folder is mounted to the container
			└── custom_node.py
		├──	CMakeLists.txt
		└── package.xml
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
    dos2unix \
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
```

The updated Dockerfile introduces several key modifications to enhance the functionality, compatibility, and efficiency of the development environment. One of the main changes is the addition of the **`dos2unix`** tool, which ensures proper handling of file line endings between Windows and Linux systems. This tool is particularly important when working with scripts that may have been developed or modified across different operating systems, preventing issues with incorrect line endings that could cause script failures in the container. 
In addition to this, the Dockerfile now includes commands to automatically convert all Python and Shell scripts inside the `src/nodes` directory to Unix-style line endings, ensuring smooth execution of these files. 
Furthermore, **`rosdep install`** has been added to resolve and install any missing dependencies for the ROS packages. This step ensures that all external libraries required by the QCar repository and custom ROS nodes are automatically installed, reducing the potential for errors related to unresolved dependencies. Additionally, the Dockerfile includes permissions handling for the entrypoint script, ensuring that it is executable and properly formatted, preventing any issues when the container starts. The general cleanup command (`rm -rf /var/lib/apt/lists/*`) has also been retained, which reduces the overall size of the Docker image by removing unnecessary package cache files.
#### Dockerfile – Full Content and Explanation

```bash
#!/bin/bash
set -e

# Source ROS setup
source /opt/ros/noetic/setup.bash
source /root/catkin_ws/devel/setup.bash

# Fix line endings and permissions for mounted volumes (if any)
if [ -d /root/catkin_ws/src/nodes/scripts ]; then
    find /root/catkin_ws/src/nodes -name "*.py" -exec dos2unix {} \; 2>/dev/null || true
    chmod +x /root/catkin_ws/src/nodes/scripts/*.py 2>/dev/null || true
fi

# Start roscore in the background
roscore &
sleep 5   # give roscore time to start

# Launch QCar Gazebo
exec "$@" # here run 'roslaunch qcar_gazebo qcar_world.launch' This takes some time, so no worries if it seems stuck
```

The `entrypoint.sh` script plays a crucial role in setting up the environment and ensuring the proper initialization of the ROS workspace and QCar simulation within the Docker container. In its initial form, the script starts by sourcing the necessary ROS environment setup files, specifically `setup.bash` for both ROS Noetic and the local catkin workspace. This step ensures that all the required ROS environment variables and dependencies are correctly set up before executing any ROS-related commands.

The script then proceeds to start **`roscore`** in the background. **`roscore`** is the central component of any ROS-based system, responsible for managing the communication between different nodes and topics in the ROS network. The `sleep 5` command ensures that the system gives `roscore` enough time to initialize before proceeding to the next step. This is important because starting other nodes or launching simulations requires `roscore` to be fully operational.

Next, the script executes the **`roslaunch`** command to launch the QCar Gazebo simulation. The `exec "$@"` part is a placeholder that allows any additional commands passed to the container to be executed, making the script versatile for launching different ROS launch files based on the needs of the user or system. In this case, the default is to run `roslaunch qcar_gazebo qcar_world.launch`, which starts the Gazebo simulation with the QCar model. Since the launch process can take some time, the user should not be concerned if the container appears to "freeze" at this point, as Gazebo initializes and loads the simulation environment.

The updated version of the `entrypoint.sh` script introduces a few important changes aimed at improving compatibility and ensuring smooth operation, especially when handling files from external sources or mounted volumes. It begins with the same ROS setup and initialization process but adds steps to address potential issues with file formats and permissions for Python and Shell scripts within the `src/nodes` directory. Specifically, it runs **`dos2unix`** on any Python and Shell scripts to ensure they have the correct Unix-style line endings, which is particularly important when files are transferred from a Windows environment. The script also ensures that these Python scripts are made executable by running **`chmod +x`**, a necessary step for any scripts that need to be run in a Linux-based environment.
#### Package.xml – Full Content and Explanation

```xml
<?xml version="1.0"?>
<package format="2">
  <name>my_qcar_nodes</name>
  <version>0.0.1</version>
  <description>Basic QCar demo nodes (cmd, sensors)</description>
  <maintainer email="you@example.com">you</maintainer>
  <license>MIT</license>
  <buildtool_depend>catkin</buildtool_depend>

  <build_depend>rospy</build_depend>
  <build_depend>std_msgs</build_depend>
  <build_depend>geometry_msgs</build_depend>
  <build_depend>sensor_msgs</build_depend>
  <build_depend>ackermann_msgs</build_depend>
  <build_depend>gazebo_msgs</build_depend>

  <exec_depend>rospy</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <exec_depend>geometry_msgs</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>
  <exec_depend>ackermann_msgs</exec_depend>
  <exec_depend>gazebo_msgs</exec_depend>
</package>
```

The `package.xml` file is a critical component in any ROS (Robot Operating System) package, as it serves to define essential metadata about the package and its dependencies. This file helps the ROS build system to correctly interpret, manage, and resolve the necessary resources for both building and executing the package. It begins with an XML declaration and is structured in a way that allows ROS to automatically handle dependencies, ensuring the package integrates smoothly with other parts of the ROS ecosystem.

At its core, the `package.xml` file specifies important details such as the package name (`my_qcar_nodes`), version (`0.0.1`), and a brief description of its functionality. This information helps developers quickly understand the package’s purpose, which in this case, relates to controlling basic QCar functionalities such as movement and sensor readings. Additionally, the file identifies the package's maintainer and provides an email address for communication, ensuring that users can contact the responsible party for maintenance or issues. The inclusion of the software license (MIT in this case) defines the terms under which the package can be shared and modified.

One of the most significant sections of the `package.xml` is the dependency management system. ROS packages are often built upon or interact with other packages, and this section ensures that all required libraries are available during both the build and execution phases. The file specifies build dependencies like `rospy` (for Python-based ROS nodes), `std_msgs` (for standard message types such as strings or integers), and `geometry_msgs` (for handling geometric data like poses and velocity). These dependencies are required during the build process to compile the code and ensure that the necessary libraries are available for the package to function correctly. The `build_depend` tags are critical here, as they list the necessary libraries and message types needed to complete the build process.

In addition to build-time dependencies, the `exec_depend` tags outline the libraries required when running the package. This ensures that all necessary resources are available when the package is executed in a runtime environment. The execution dependencies mirror the build dependencies, with key libraries such as `ackermann_msgs` (used to control the QCar's Ackermann steering mechanism), `gazebo_msgs` (which allows interaction with the Gazebo simulation), and others. By listing these dependencies under both build and execution categories, the `package.xml` guarantees that the package will operate as intended both during development and when deployed for use in a simulated or real environment.
#### CMakeLists.txt – Full Content and Explanation

```cmake
cmake_minimum_required(VERSION 3.0.2)
project(my_qcar_nodes)
find_package(catkin REQUIRED COMPONENTS
  rospy std_msgs geometry_msgs sensor_msgs ackermann_msgs gazebo_msgs
)
catkin_package()
install(PROGRAMS
  scripts/move_cmd_vel.py
  scripts/move_ackermann.py
  scripts/print_joint_states.py
  scripts/print_model_states.py
  scripts/basic_move.py
  scripts/qcar_targets_bridge.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```

The `CMakeLists.txt` file is an integral part of a ROS (Robot Operating System) package, functioning as the configuration file for the build system. It is responsible for defining the build process, specifying dependencies, and guiding the compilation of the package's code and scripts. In this case, the `CMakeLists.txt` file is set up to build the package `my_qcar_nodes`, which contains nodes for interacting with the QCar, particularly its movement and sensor capabilities.

The file starts by defining the minimum required version of CMake (`cmake_minimum_required(VERSION 3.0.2)`). This ensures that the build system is compatible with the specified version of CMake or newer. CMake is a cross-platform build system that ROS uses to automate the compilation process. Next, the `project(my_qcar_nodes)` command defines the name of the project, which helps CMake organize and manage the build process under this specific name.

The core functionality of the `CMakeLists.txt` file lies in the `find_package(catkin REQUIRED COMPONENTS ...)` command. This command specifies the dependencies that the package needs to function properly. In this case, it lists the required ROS packages such as `rospy`, `std_msgs`, `geometry_msgs`, `sensor_msgs`, `ackermann_msgs`, and `gazebo_msgs`. These dependencies are essential for the package to interact with the ROS ecosystem, communicate with other nodes, and interface with the Gazebo simulation environment. By listing these dependencies in the `find_package` command, CMake ensures that the necessary libraries are located and included in the build process.

Following the dependency resolution, the `catkin_package()` command is invoked. This is a macro provided by the `catkin` build system (the standard build system for ROS) that declares this package as a ROS package. This macro essentially flags the package as a valid ROS package, enabling it to be built, tested, and installed within a ROS workspace. The `catkin_package()` command simplifies the process of linking this package to other ROS packages and makes it compatible with the overall ROS ecosystem.

Lastly, the `install()` command is used to specify which files should be installed when the package is built. In this case, it lists several Python scripts (located in the `scripts` directory), such as `move_cmd_vel.py`, `move_ackermann.py`, `print_joint_states.py`, and others. These scripts are likely the primary nodes used to interact with the QCar, sending commands for movement or reading sensor data. By specifying them in the `install()` command, these scripts are made executable and will be installed to a specific destination in the ROS workspace, which is defined by the `CATKIN_PACKAGE_BIN_DESTINATION` variable. This ensures that the package's nodes are placed in the appropriate location for execution within the ROS environment.
#### Windows and Linux executables

Both Linux and Windows executable files received a change on how the docker is being run in order to mount the scripts folder inside of the container, allowing live changes inside the container.

```bash
docker run -it --rm `
    -e DISPLAY=$env:DISPLAY `
    -v /tmp/.X11-unix:/tmp/.X11-unix `
    -v /c/Path/to/nodes/scripts:/root/catkin_ws/src/nodes/scripts `
    --name qcar `
    qcar-sim
```
#### Nodes/Bridges created
##### 1. Movement Bridge (`qcar_bridge.py`)

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

class QCarTargetsBridge:
    def __init__(self):
        rospy.init_node('qcar_targets_bridge')
        
        # Subscribe to QCar target topics
        rospy.Subscriber('/qcar/velocity_target', Float64, self.velocity_callback)
        rospy.Subscriber('/qcar/steering_target', Float64, self.steering_callback)

        # Publishers to Gazebo controllers
        self.rl_pub = rospy.Publisher('/qcar/rl_controller/command', Float64, queue_size=10)
        self.rr_pub = rospy.Publisher('/qcar/rr_controller/command', Float64, queue_size=10)
        self.fl_pub = rospy.Publisher('/qcar/base_fl_controller/command', Float64, queue_size=10)
        self.fr_pub = rospy.Publisher('/qcar/base_fr_controller/command', Float64, queue_size=10)

        # Parameters
        self.wheel_radius = rospy.get_param('~wheel_radius', 0.05)  # meters
        self.max_steering = rospy.get_param('~max_steering', 0.6)   # radians
        rospy.loginfo("QCar targets bridge started")
        
    def velocity_callback(self, msg):
        # Convert velocity (m/s) to wheel angular velocity (rad/s)
        wheel_speed = msg.data / self.wheel_radius

        # Send to rear wheel controllers
        self.rl_pub.publish(Float64(data=wheel_speed))
        self.rr_pub.publish(Float64(data=wheel_speed))

    def steering_callback(self, msg):
        # Clamp steering angle
        steering_angle = max(-self.max_steering, min(self.max_steering, msg.data))

        # Send to front wheel controllers
        self.fl_pub.publish(Float64(data=steering_angle))
        self.fr_pub.publish(Float64(data=steering_angle))

if __name__ == '__main__':
    try:
        bridge = QCarTargetsBridge()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
```

The script provided is a ROS (Robot Operating System) node written in Python that acts as a bridge between high-level target commands (such as velocity and steering) and the low-level wheel controllers of a QCar simulation model in Gazebo. This node listens for velocity and steering target messages and publishes appropriate commands to control the QCar's wheels.

When the node is initialized, it subscribes to two topics: `/qcar/velocity_target` and `/qcar/steering_target`, both of which expect messages of type `Float64`. These topics represent the desired target velocity and steering angle for the QCar. The node also sets up four publishers that send control commands to the Gazebo simulation: one for each wheel (right and left rear wheels, front left and front right wheels). These publishers send messages of type `Float64`, which specify the desired speed or steering angle for each wheel.

The core functionality of the node is divided into two callback functions. The first callback, `velocity_callback`, takes the target velocity (in meters per second) and converts it into the corresponding wheel angular velocity (in radians per second), using the wheel radius as a conversion factor. This calculated angular velocity is then published to the rear wheel controllers. The second callback, `steering_callback`, takes the desired steering angle and ensures it stays within a predefined limit (clamping it between `-max_steering` and `max_steering` radians). It then publishes this clamped value to the front wheel controllers.

The node also defines some parameters, such as `wheel_radius` and `max_steering`, which are retrieved using `rospy.get_param`. These parameters control the physical characteristics of the QCar model, such as the size of the wheels and the maximum steering angle allowed.

##### 2. Basic Move (`basic_move.py`)

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

def main():
    rospy.init_node('basic_move')
    
    # Publishers to the same topics the QCar hardware node expects
    vel_pub = rospy.Publisher('/qcar/velocity_target', Float64, queue_size=10)
    steer_pub = rospy.Publisher('/qcar/steering_target', Float64, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    # Movement parameters (adjustable via rosparam)
    velocity = rospy.get_param('~velocity', 1.0)    # m/s
    steering = rospy.get_param('~steering', 20.0)    # radians
    rospy.loginfo(f"Publishing velocity: {velocity} m/s, steering: {steering} rad")

    while not rospy.is_shutdown():
        vel_pub.publish(Float64(data=velocity))
        steer_pub.publish(Float64(data=steering))
        rate.sleep()

if __name__ == '__main__':
    try:
        main()

    except rospy.ROSInterruptException:
        pass
```

This script is a basic ROS node written in Python that controls the movement of the QCar by publishing velocity and steering target commands to specific topics. It is designed to send commands for simple movement based on parameters for velocity and steering.

Upon initialization, the node creates two publishers: one for publishing the target velocity (`/qcar/velocity_target`) and one for publishing the target steering angle (`/qcar/steering_target`). Both of these publishers use the `Float64` message type, which is appropriate for sending numeric values like velocity (in meters per second) and steering angle (in radians). The node runs at a frequency of 10 Hz, controlled by `rospy.Rate(10)`.

The node also retrieves two parameters from the ROS parameter server, `velocity` and `steering`, which represent the desired speed and steering angle for the QCar. These parameters can be adjusted dynamically via `rosparam` to control the car's behavior without modifying the code directly. If the parameters are not set, default values of `1.0 m/s` for velocity and `20.0 radians` for steering are used. The `rospy.loginfo()` function logs the current parameters to provide feedback in the ROS logs.

The main loop of the script continuously publishes the `velocity` and `steering` values to their respective topics as long as the node is running. This loop allows the QCar to receive commands and maintain a steady movement at the specified speed and steering angle. The rate at which the messages are sent is controlled by `rate.sleep()`, ensuring the loop runs at the set frequency of 10 Hz.

##### 3. Basic Join Read (`basic_read_joint.py`)

```python
#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState

last = 0.0

def cb(msg: JointState):
    global last
    now = rospy.Time.now().to_sec()
    if now - last < 0.5:
        return

    last = now
    pairs = list(zip(msg.name, msg.position))
    rospy.loginfo_throttle(0.5, f'Joint positions (sample): {pairs[:6]}')

  

def main():
    rospy.init_node('qcar_print_joint_states')
    topic = rospy.get_param('~topic', '/joint_states')
    rospy.Subscriber(topic, JointState, cb, queue_size=10)
    rospy.loginfo(f'Subscribed to {topic}')
    rospy.spin()

if __name__ == '__main__':
    main()
```

This Python script defines a simple ROS node that subscribes to the `/joint_states` topic (or another topic specified via the `rosparam`), listens for `JointState` messages, and logs joint positions at a throttled rate to avoid flooding the console with too many messages.

The `main()` function initializes the ROS node with the name `qcar_print_joint_states` and subscribes to the specified topic (defaulting to `/joint_states`). The subscription is tied to a callback function, `cb()`, which processes incoming `JointState` messages. The `JointState` message contains the names and positions of various joints, typically representing different parts of a robot's structure, including wheels or actuators.

In the callback function (`cb()`), the current time is checked against the last processed time (stored in the `last` variable) to ensure that the joint state data is not printed more frequently than every 0.5 seconds, preventing excessive logging. This is managed by the `rospy.Time.now().to_sec()` function, which returns the current time in seconds. If less than 0.5 seconds have passed since the last message, the function returns early and doesn't process the new message. Otherwise, it proceeds to update the `last` time and logs a sample of the joint positions, specifically the first six pairs of joint names and positions, using `rospy.loginfo_throttle()`. This method ensures that the joint positions are logged at a throttled rate of once every 0.5 seconds, avoiding overwhelming the log output.

In the `main()` function, once the node is initialized and the subscription is set up, the node enters a spinning loop with `rospy.spin()`, which keeps the node alive, waiting for incoming messages. The `rospy.loginfo()` call logs a message indicating that the node has successfully subscribed to the `topic` (either `/joint_states` or another user-defined topic).
##### 4. Basic Pose Read (`basic_read_pose.py`)

```python
#!/usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelStates

name = rospy.get_param('/qcar_model_name', 'qcar')

def cb(msg: ModelStates):
    try:
        idx = msg.name.index(name)
        pose = msg.pose[idx]
        p = pose.position
        o = pose.orientation
        rospy.loginfo_throttle(0.5, f'{name} pos=({p.x:.2f},{p.y:.2f},{p.z:.2f}) yaw(qz)={o.z:.2f}')
        
    except ValueError:
        pass

def main():
    rospy.init_node('qcar_print_model_states')
    topic = rospy.get_param('~topic', '/gazebo/model_states')
    rospy.Subscriber(topic, ModelStates, cb, queue_size=5)
    rospy.loginfo(f'Subscribed to {topic} (qcar_model_name param controls which model to track)')
    rospy.spin()

if __name__ == '__main__':
    main()
```

This Python script creates a ROS node that subscribes to the `/gazebo/model_states` topic, listens for `ModelStates` messages, and logs the position and yaw (orientation in the z-axis) of a specific model (in this case, a QCar) in the Gazebo simulation environment. The specific model to track is determined by the `qcar_model_name` ROS parameter.

The `main()` function initializes the ROS node with the name `qcar_print_model_states` and subscribes to the topic specified in the ROS parameter `~topic` (defaulting to `/gazebo/model_states`). The subscription is tied to the callback function (`cb()`), which processes the incoming `ModelStates` messages.

In the callback function (`cb()`), the `ModelStates` message contains information about all the models in the Gazebo environment, including their names, poses, and orientations. The `name` of the model to track is obtained from the `qcar_model_name` ROS parameter, which is set to `'qcar'` by default. The callback attempts to find the index of this model name within the `msg.name` list, which holds the names of all models currently in the Gazebo simulation.

If the specified model name (`qcar`) is found, the script extracts the pose and orientation of the model by accessing the corresponding index in the `msg.pose` list. The pose consists of a `position` (with x, y, and z coordinates) and an `orientation` (represented by a quaternion). In this case, the script logs the position (x, y, z) and the yaw (the z-component of the quaternion orientation, which represents rotation around the vertical axis). The data is logged at a throttled rate of 0.5 seconds using `rospy.loginfo_throttle()`, ensuring that the log messages do not flood the console with updates too frequently.

If the specified model is not found in the `msg.name` list, a `ValueError` is raised, but the script catches this exception and silently ignores it, preventing any errors from halting the node.

The `main()` function also logs a message indicating that the node has successfully subscribed to the specified `topic` and explains that the `qcar_model_name` parameter controls which model is being tracked. The node then enters the `rospy.spin()` loop, keeping the node alive and waiting for incoming messages.

#### Environment Testing

To finally test the nodes in action, you have to run the simulation via 

```bash
cd src/qcar/src/qcar_gazebo/launch
roslaunch qcar_gazebo qcar_world.launch
```

Then, open a new docker terminal using

```bash
docker exec -it qcar bash
```

Finally, run the node that you want using

```bash
cd src/nodes/scripts/
rosrun my_qcar_nodes <node_name.py>
```

> _If you want to use the movement functionality, you will have to open 2 new terminals, one for the bridge and other for the sub_

> _For some reason this version of the node was unable to resolve movement itself, but it will be resolved in future updates_