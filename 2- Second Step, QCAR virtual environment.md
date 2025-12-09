---
date: 2025-07-11
estimated-date: 2025-07-18
task: Now that the technologies to be used are known, it is important to clarify the virtual space in use, the idea is to research different ways to create this dockerized space, defining cons and pros on each one.
terms:
  - Docker
  - VM
  - Containerization
  - Virtual-env
---
## Overview

When aiming to simulate a robot like the QCar 2 using **Ubuntu**, **ROS 2**, and **Gazebo**, there are various ways to **virtualize** or create isolated environments to run these tools. Virtualization provides the flexibility to run multiple operating systems or software setups in an isolated manner without interfering with your host system.

The goal is to explore different methods of setting up **Ubuntu (Linux)**, **ROS 2**, and **Gazebo** on a machine to ensure you can simulate your robot effectively. We need a solution that allows for the full stack — from running **Ubuntu** as the operating system to **ROS 2** for robot control and **Gazebo** for simulation. The methods we will explore include:

1. **Virtual Machines (VMs)**: Using platforms like VirtualBox or VMware to create a virtualized instance of Ubuntu with ROS and Gazebo.

2. **Windows Subsystem for Linux 2 (WSL2)**: A solution for running Ubuntu directly on Windows with the ability to execute graphical applications like Gazebo.

3. **Docker Containers**: Running Ubuntu, ROS 2, and Gazebo within isolated containers for lightweight, portable simulations.

4. **Cloud-based Virtualization**: Using cloud platforms like AWS or Google Cloud to run virtual machines with ROS and Gazebo, without consuming local resources.


Each of these methods has its own set of pros and cons, affecting system performance, ease of setup, flexibility, and resource usage. Our task is to explore each option in-depth, examining how each technology works and how they can be configured to run ROS 2 and Gazebo simulations smoothly.

Finally, we will compare all these options and offer recommendations based on different use cases. Understanding these technologies will allow you to select the most appropriate solution for your simulation environment.

## Terms and knowledge

Before diving into the comparison of each virtualization method, it’s important to understand the key terms and technologies involved in this process. Here's an overview of the essential concepts:

#### Virtual Machine (VM)

A **Virtual Machine** (VM) is a software emulation of a physical computer that runs an operating system (OS) and applications just like a real computer. A VM can run an OS such as Ubuntu on top of your existing host OS (such as Windows or macOS). VMs are managed by hypervisors like **VirtualBox** or **VMware**.

- **Use Case**: Ideal for running complete operating systems isolated from your host system, ensuring that ROS 2 and Gazebo run in a controlled, consistent environment.

#### Windows Subsystem for Linux 2 (WSL2)

**WSL2** is a compatibility layer for running Linux binary executables natively on Windows. Unlike the previous version (WSL1), WSL2 uses a full Linux kernel and is more efficient at running Linux software like Ubuntu, ROS, and Gazebo. WSL2 enables developers to run Linux distributions directly on Windows without needing a full VM.

- **Use Case**: Ideal for users running Windows who want to seamlessly run Linux-based tools and libraries without the overhead of a full virtual machine.

#### X11 and X11 Forwarding

**X11** is a protocol that manages the display of graphical applications over a network. When running graphical applications on a virtual machine or container, **X11 forwarding** allows the graphical interface of the application (like Gazebo or RViz) to be displayed on your local system. For example, with Docker, X11 is often used to display GUI applications running in containers to your local machine.

- **Use Case**: When running GUI-based applications like Gazebo from Docker or a VM, X11 forwarding is necessary to view the graphical outputs on your screen.

#### Docker Containers

**Docker** is a platform for developing, shipping, and running applications inside isolated **containers**. Containers package the application and its dependencies, including libraries, settings, and runtime, in a consistent environment. Docker allows you to run Ubuntu, ROS 2, and Gazebo as separate services within a single container.

- **Use Case**: Great for lightweight, portable setups where you need to run Ubuntu and ROS 2 without setting up a full VM or system. Ideal for deploying on different systems and cloud environments.

#### Cloud Virtualization (e.g., AWS, Google Cloud, Azure)

Cloud virtualization refers to running virtual machines or containers on remote cloud platforms like **Amazon Web Services (AWS)**, **Google Cloud**, or **Microsoft Azure**. These platforms allow you to set up high-performance virtual environments remotely, providing scalability and high availability for running simulations, including complex tasks that require significant resources.

- **Use Case**: Best for high-performance needs or when local resources are insufficient, and you need scalability or the ability to access your simulation from multiple locations.

## Results

Here’s a detailed comparison of the different methods for virtualizing Ubuntu, ROS 2, and Gazebo. Each method has its strengths and trade-offs. Let’s break down their **pros and cons** and how they can be implemented for our needs.

#### 1. Virtual Machine (VM)

##### Pros:
- **Fully Isolated Environment**: Can install a complete OS (e.g., Ubuntu) with ROS 2, Gazebo, and other dependencies without affecting your host OS.

- **Supports GUI Applications**: Since the VM runs a full operating system, you can run graphical applications like Gazebo and RViz without additional configuration.

- **Complete Control**: Full control over the environment and can tweak settings or install additional software freely.

##### Cons:
- **High Resource Consumption**: VMs require significant CPU, memory, and disk resources, which can slow down your system, especially on machines with limited resources.

- **Slower Performance**: The virtualization layer introduces overhead, meaning applications will not run as efficiently as they would on a native system.

- **Requires Virtualization Software**: You need tools like **VirtualBox** or **VMware**, which can add complexity (or at least some annoying installation steps).

##### Implementation:
- Set up **VirtualBox** or **VMware** on the host system (in my case, I have VirtualBox already installed).

- Create a virtual machine with **Ubuntu** as the OS (For that you will also need the image file, which you can download from some web sites).

- Install **ROS 2** and **Gazebo** inside the VM.

- Use the virtualized environment as a sandbox for robot simulations.

---

#### 2. Windows Subsystem for Linux 2 (WSL2)

##### Pros:
- **Efficient and Integrated**: WSL2 runs a full Linux kernel and is tightly integrated with Windows, allowing seamless operation between both environments.

- **Lightweight**: WSL2 uses fewer resources than a VM, making it more efficient for machines with limited resources.

- **Direct Access to Windows Files**: You can access and modify files between Linux and Windows without issues.

##### Cons:
- **Limited Hardware Support**: Some hardware devices might not be fully supported, particularly those requiring low-level hardware access (this is not a really big drawback in this case as we are not using hardware devices that require low-level hardware access).

- **Configuration for GUI**: Running GUI applications (like Gazebo) in WSL2 requires configuring an X server (X11), which can be tricky.

##### Implementation:
- Install **WSL2** and set up **Ubuntu**.

- Install **ROS 2** and **Gazebo** within Ubuntu in WSL2.

- Configure **VcXsrv** or **X410** for GUI support to display Gazebo and RViz.

---

#### 3. Docker Containers

##### Pros:
- **Lightweight**: Docker containers are more resource-efficient than VMs and allow you to isolate only the necessary components (Ubuntu, ROS 2, Gazebo).

- **Portability**: Docker containers can be easily moved between machines or cloud platforms, ensuring a consistent environment (this is really good, as we are a group working in different machines, the fact that we can share our containers is actually efficient).

- **Modular and Scalable**: You can run each part of your setup (e.g., ROS nodes, Gazebo simulation) in separate containers (which I personally like the most about using docker).

##### Cons:
- **Complex Setup for GUI**: Running graphical applications like Gazebo inside Docker requires configuring **X11 forwarding**, which can be complex.

- **Not a Full OS**: Docker containers do not provide a complete OS, so certain hardware-related tasks or complex setups may not work as expected (in this case, we are not needing too much hardware related process as we are just simulating the behavior of the robot inside gazebo with the assistance of ROS).

##### Implementation:
- Create a **Dockerfile** to define your container environment (Ubuntu, ROS 2, Gazebo).

- Build and run the container using Docker commands.

- Set up **X11 forwarding** to display Gazebo's GUI.

---

#### 4. Cloud-based Virtualization (AWS, Google Cloud, Azure)

##### Pros:
- **Scalable Resources**: Cloud services provide access to high-performance computing power, including GPU instances for heavy simulations.

- **Remote Access**: You can access your simulation environment from anywhere, which is useful for collaborative work or running long-term experiments.

- **No Local Resource Usage**: The cloud handles resource-intensive tasks, meaning your local machine remains unaffected.

##### Cons:
- **Cost**: Cloud-based instances can be expensive, especially if you need powerful machines or are running simulations continuously (this is actually a big drawback, specially considering the fact that we want to make this with open-source technologies).

- **Dependency on Internet Connection**: You must have a reliable internet connection to access the cloud environment.

- **Latency**: Graphical applications like Gazebo can experience delays when accessed remotely, especially with large-scale simulations.

##### Implementation:
- Create a virtual machine (VM) in a cloud platform like **AWS EC2**.

- Install **Ubuntu**, **ROS 2**, and **Gazebo** on the cloud VM.