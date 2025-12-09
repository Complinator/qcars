---
date: 2025-09-12
estimated-date: 2025-09-26
task: We had to work on the nodes related to QCAR movement, but software lag made it nearly impossible to work on it in an optimal way. The team need to enhance the virtual environment performance in order to make it usable during it's usage, that involved having to take 1 step back to make 2 step forward.
terms:
  - WSL
  - XServer
  - GPU
  - Optimization
---
## Overview

At this stage of development, the team was focused on implementing and refining the QCar nodes necessary for enabling autonomous functionalities within the simulation environment. Progress had been made with the successful creation and validation of two sensor nodes and two execution nodes, establishing a solid foundation for the system’s architecture. However, one critical component, the movement node, presented significant challenges. Although it was partially functional, the vehicle was not responding as expected to movement commands. Specifically, the speed/acceleration parameter was not being correctly applied, resulting in a car that remained stationary despite command inputs. This was a major concern, given that the ability to control movement is a fundamental requirement for the system’s operation.

In an effort to resolve this issue, the team investigated existing resources and encountered several pre-existing nodes within the _bchampp_ autonomous driving repository, an open-source project which also leverages the QCar model. It was noted, however, that many of these nodes were dependent on proprietary Quanser libraries, which are not publicly available. This introduced an additional line of inquiry: determining whether those libraries were essential for movement functionality or if alternative, open-source approaches could be pursued. Should the libraries prove indispensable, the team would need to explore the means of obtaining access to them through appropriate channels.

Compounding the technical issues was the performance bottleneck encountered in the virtual environment. The system’s graphical interface, particularly the visualization tools such as Gazebo and RViz, was being rendered through an XServer implementation, which proved to be highly inefficient. The interface ran at approximately 3 frames per second while placing heavy demands on CPU resources, making it impractical for continued use in development or testing. Given the importance of a responsive and stable simulation environment, the team redirected its efforts toward optimizing this aspect of the system.

This documentation outlines the steps taken to address these problems, with a particular focus on the migration of the current XServer-based visualization approach to a more modern and performant alternative, integrated within the existing Dockerized architecture. The goal was to achieve a smoother and more efficient simulation workflow, capable of supporting the ongoing development of the autonomous QCar system.
## Knowledge and Terms
#### XServer and How It Works

The X Window System, commonly known as **X11** or simply **XServer**, is a display server protocol that provides the fundamental framework for managing graphical displays on UNIX-like operating systems, including most Linux distributions. Its primary role is to mediate communication between graphical applications (clients) and the graphical hardware (display output). While XServer has been the standard for decades, it is increasingly seen as outdated due to performance limitations and lack of native support for modern rendering technologies.

When a graphical application is launched, it sends **drawing commands** to the XServer, which then processes and renders those commands to the screen. These commands can include anything from drawing windows and buttons to rendering 3D scenes or video playback. The XServer handles input (keyboard, mouse, etc.) and output (drawing to the screen), making it central to the graphical user experience.

In many virtualized environments, such as Docker containers or remote desktops, XServer is implemented using software rendering methods due to the lack of direct hardware (GPU) access. One of the most common rendering backends used in such scenarios is **LLVMpipe**.
#### LLVMpipe: Software-Based Rendering

**LLVMpipe** is a **Gallium3D** driver that performs rendering entirely on the **CPU** rather than the **GPU**. It is part of the **Mesa 3D Graphics Library**, which serves as an open-source implementation of the OpenGL specification. LLVMpipe utilizes the **LLVM compiler infrastructure** to dynamically generate highly optimized CPU instructions for rendering operations. However, despite its flexibility, LLVMpipe is fundamentally constrained by the CPU’s architecture and bandwidth, which are not optimized for parallel pixel processing.

As a result, software rendering through LLVMpipe is significantly slower than hardware-accelerated rendering. In practice, this leads to **low frame rates**, **high CPU utilization**, and general sluggishness in graphical applications, especially those involving real-time simulations or complex 3D models, such as **Gazebo** or **RViz** in robotic environments.

The problem becomes more evident in Docker-based workflows, where containers operate in isolated environments and typically lack direct access to the host GPU unless explicitly configured. When graphical output is routed through XServer using software rendering like LLVMpipe, the performance bottleneck becomes a major concern. In the team’s specific case, this approach yielded rendering speeds as low as **3 frames per second (FPS)**, which made the development and debugging of visual simulation tools almost impractical.
#### Alternatives to XServer

As the industry has moved toward more performance-sensitive and security-conscious computing environments, several alternatives to the traditional XServer architecture have emerged:

- **Wayland**: A modern replacement for X11, Wayland is a protocol that simplifies the graphical stack by delegating responsibilities traditionally handled by XServer (such as compositing) to the display compositor itself. It allows for better performance, less code overhead, lower latency, and improved security. However, Wayland is not yet fully adopted across all desktop environments or toolkits, which limits its use in specialized setups like robotics simulation.
 
- **Vulkan with Direct Rendering**: Vulkan is a low-level graphics API that allows direct, fine-grained control over the GPU. It bypasses the older abstraction layers used by OpenGL and X11, which results in better performance and efficiency. It’s commonly used in game engines and high-performance visualization systems but requires deep integration and is not trivial to adapt for all graphical applications (Applying this solution could feel like it is like killing a fly with a machine gun as the virtual environment itself is not the main objective to fulfill, but it is part of it).

- **VirtualGL**: This approach allows applications running in a remote or containerized environment to use the host’s GPU for rendering, then stream the resulting images back to a local XServer for display. While it bridges some of the performance gap, it introduces its own set of complexities in setup and can still be limited by network or memory bandwidth.

- **NoMachine and VNC**: Remote desktop protocols like NoMachine or VNC provide full desktop access across systems and are sometimes used to run graphical applications in headless or virtualized setups. However, these tools are generally not optimized for 3D rendering and still suffer from latency and image quality issues.
#### WSL and WSLg: A Modern, GPU-Aware Environment

**WSL** (Windows Subsystem for Linux) is a compatibility layer developed by Microsoft that enables Linux binaries to run natively on Windows. With **WSL 2**, the system evolved to run a full Linux kernel inside a lightweight virtual machine, enabling full system call compatibility and improving overall performance and compatibility with Linux software.

Building on top of WSL 2, Microsoft introduced **WSLg** (Windows Subsystem for Linux GUI). WSLg integrates a Wayland-based compositor into WSL, which allows GUI-based Linux applications to run seamlessly alongside native Windows applications without requiring users to set up an XServer manually.

One of the most significant advantages of WSLg is **hardware-accelerated GPU sharing**. It uses **GPU paravirtualization** to allow Linux applications running inside WSL to access the **Windows host’s GPU resources**, including through technologies like **GPU-PV (GPU Paravirtualization)** for Windows 11. This drastically improves the performance of graphical applications such as RViz or Gazebo when compared to traditional XServer + software-rendering pipelines.

With WSLg, GPU access can be extended **into Docker containers** running inside the WSL environment. This means that simulation and robotics tools running within Docker can benefit from **direct GPU acceleration**, resulting in significant performance gains, smoother graphical rendering, and reduced CPU overhead.

WSLg’s architecture is also more modern and maintainable than the legacy XServer-based approaches. It supports Wayland by default, falls back gracefully to X11 when needed, and includes support for PulseAudio and other desktop integration features. In development environments that rely on high-performance visualization, WSLg represents a forward-looking solution that aligns with current hardware capabilities and software trends.
#### AMD vs. NVIDIA in GPU Passthrough

While WSLg offers the capability of GPU sharing, the process of enabling and leveraging GPU acceleration within containerized environments (such as Docker) depends heavily on the specific **GPU vendor** in use.

For **NVIDIA GPUs**, the situation is relatively mature and well-documented. NVIDIA provides **WSL-compatible drivers**, including **CUDA and OpenGL support**, along with Docker integrations through **NVIDIA Container Toolkit** and **nvidia-docker**. This allows for a smoother and more standardized setup process, especially for projects that rely on GPU computation or visualization.

In contrast, the situation with **AMD GPUs** is more fragmented. While AMD has made strides in open-source support through the **Mesa** drivers and **ROCm** (Radeon Open Compute), its integration with WSL and Docker environments remains limited. The documentation is sparse, community support is less established, and there are frequent compatibility issues—particularly in scenarios involving OpenGL or Vulkan in containerized Linux environments.

This created a specific challenge for the team, as the machine used for development was equipped with an **AMD GPU**. Unlike NVIDIA, where enabling GPU passthrough involved following well-defined procedures, setting up AMD GPU acceleration required significant manual configuration and experimentation, often without official documentation or community-tested best practices. This added complexity to the process of modernizing the virtual environment and underscored the need for a flexible, maintainable, and hardware-agnostic solution moving forward.
## Results

This section documents the successful migration from a laggy, software-rendered graphical environment based on XServer, to a modern, GPU-accelerated development setup using **WSL2 + Docker + GPU passthrough**, enabling significant performance gains for graphical applications like **Gazebo** and **RViz**. The steps below detail the process of configuring the WSL2 environment, integrating Docker, enabling GPU access from within containers, and resolving critical errors encountered during setup.
#### Installing and Setting Up WSL2
##### Install WSL2 on Windows

The first requirement was to move the development environment from a traditional Linux VM to **WSL2**, taking advantage of Microsoft’s native support for Linux GUI applications via **WSLg**, and hardware-accelerated GPU access.

Run the following command in an **elevated PowerShell terminal**:

```powershell
wsl --install
```

This installs:
- WSL2 engine (including a real Linux kernel)
- A default Linux distribution (Ubuntu)
- WSLg (Graphical Linux support)

Once installed, restart your system. You can then verify installation with:

```powershell
wsl --version
```

Ensure that the version is **WSL 2**, not WSL 1.
##### Checking GPU Access in WSL2

WSL2 supports GPU acceleration by sharing the Windows GPU with the Linux environment. To verify GPU availability:

Start by installing Mesa Utilities

```bash
sudo apt update && sudo apt install mesa-utils
```

Run `glxinfo`

```bash
glxinfo -B
```

If working correctly, you should see an output such as:

```bash
OpenGL renderer string: AMD Radeon XYZ
OpenGL core profile version string: ...
```

If the renderer is listed as **llvmpipe** (software rendering), it means GPU access is not working. This typically happens when:
- You are not using WSLg
- Environment variables aren't properly set
- The container lacks access to `/dev/dxg`, the GPU interface
##### Setting Up Docker in WSL2

Although Docker Desktop was already installed in the development environment, additional configuration was necessary to make Docker function **natively inside WSL2**, which is a prerequisite for GPU sharing and compatibility with WSLg.

###### Step-by-step setup:

1. **Open Docker Desktop GUI**.
2. Go to **Settings > General** and ensure:
	 - "Use the WSL 2 based engine" is **enabled**.
3. Navigate to **Settings > Resources > WSL Integration**:
    - Enable integration with your selected Linux distribution (e.g., Ubuntu).
    - This ensures that Docker CLI commands in WSL directly access the Docker engine.
4. Restart Docker Desktop and then restart WSL:
```bash
wsl --shutdown
```
5. Open WSL and verify Docker is available:
```bash
docker --version
```

Now Docker is correctly set up to run within WSL2, using the Windows host's engine while enabling GPU passthrough and filesystem performance optimizations.
##### Enabling GPU Usage Inside Docker (with WSLg)

This was the most complex part. Sharing GPU access from WSL into Docker containers requires very specific mounts and environment variables. Otherwise, OpenGL applications will fall back to software rendering and produce errors like:

```bash
name of display: :0 
libGL error: failed to create dri screen
libGL error: failed to load driver: swrast
X Error of failed request: BadValue (integer parameter out of range for operation)
```

This error indicates:
- GPU drivers are not accessible
- The container cannot communicate with WSLg's Wayland/X11 compositor
- `libGL` falls back to **swrast** (software rasterizer), which fails inside the Docker context

To solve this, the following launch script was created:

##### New Docker Launch Script

```bash
#!/bin/bash

# Build the docker image
echo "Building docker image..."
docker build -t qcar-sim-wsl .

# Run the Docker container with ROS1 and WSLg
echo "Running docker container..."

docker run -it --rm \
    --privileged \
    -e DISPLAY=$DISPLAY \
    -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
    -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
    -e PULSE_SERVER=$PULSE_SERVER \
    -e LIBGL_ALWAYS_INDIRECT=1 \
    -e LD_LIBRARY_PATH=/usr/lib/wsl/lib \
    -e MESA_D3D12_DEFAULT_ADAPTER_NAME=AMD \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /mnt/wslg:/mnt/wslg \
    -v /usr/lib/wsl:/usr/lib/wsl:ro \
    -v /dev/dri:/dev/dri \
    --device=/dev/dxg \
    -v $(pwd)/nodes/scripts:/root/catkin_ws/src/nodes/scripts \
    --name qcar-wsl \
    qcar-sim-wsl
```

Why This Works (especially for AMD GPUs):
- `--device=/dev/dxg`: Mounts the GPU interface exposed by Windows.
- `-v /usr/lib/wsl:/usr/lib/wsl:ro`: Gives the container access to WSLg's shared libraries, including Direct3D-to-Mesa translation layers.
- `MESA_D3D12_DEFAULT_ADAPTER_NAME=AMD`: Explicitly tells Mesa to use the AMD adapter, solving an issue where it defaults to "Microsoft Basic Adapter".
- `LD_LIBRARY_PATH=/usr/lib/wsl/lib`: Ensures the dynamic linker can find WSLg's OpenGL implementation.
- `LIBGL_ALWAYS_INDIRECT=1`: Required for indirect rendering under certain container conditions.

This specific configuration is **essential for AMD** cards, where support and documentation are less mature than NVIDIA.
##### Dockerfile Changes for GPU Compatibility

The Dockerfile was based on the standard `osrf/ros:noetic-desktop-full-focal`, but modifications were required to make GPU rendering possible:

```bash
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
    dos2unix \
    build-essential \
    mesa-utils \ # Enables glxinfo/glxgears
    mesa-va-drivers \ # VAAPI drivers for video acceleration
    mesa-vulkan-drivers \ # Vulkan support for Mesa
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

Why These Additions Matter:
- `mesa-utils`: Provides tools like `glxinfo` to test GPU rendering.
- `mesa-va-drivers` and `mesa-vulkan-drivers`: Required for hardware-accelerated rendering via Vulkan/VAAPI.
- These enable compatibility with WSLg’s Direct3D-to-OpenGL translation pipeline, which uses Mesa under the hood to interact with Linux apps.
##### Entrypoint.sh Changes for GPU Compatibility

```bash
#!/bin/bash
set -e

# Configure GPU acceleration for WSL2
export LIBGL_ALWAYS_INDIRECT=0
export MESA_D3D12_DEFAULT_ADAPTER_NAME=AMD
export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH

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

Key Changes:
- `LIBGL_ALWAYS_INDIRECT=0`: Allows direct rendering if possible, improving performance.
- `MESA_D3D12_DEFAULT_ADAPTER_NAME=AMD`: Forces Mesa to select the correct GPU.
- `LD_LIBRARY_PATH`: Ensures the container uses WSLg's GPU-rendering libraries.

These variables **must be set at container startup**, otherwise applications may silently fall back to software rendering, leading to poor performance or outright failure.

The script also:
- Fixes file permissions (`chmod +x`) and line endings (`dos2unix`)
- Starts `roscore` in the background before launching the main simulation
##### NVIDIA GPU Setup: A Plug-and-Play Experience

Compared to AMD, **NVIDIA's integration with WSL and Docker** is significantly more streamlined, thanks to dedicated tools and documentation. With the **NVIDIA WSL2-compatible driver** and **NVIDIA Container Toolkit**, GPU access inside containers becomes nearly plug-and-play.

```bash
#!/bin/bash

# Build the docker image
echo "Building docker image for NVIDIA..."

# Usaríamos un Dockerfile específico para NVIDIA
docker build -f Dockerfile.nvidia -t qcar-sim-nvidia .

# Run the Docker container with NVIDIA GPU support
echo "Running docker container..."

docker run -it --rm \
    --gpus all \
    -e DISPLAY=$DISPLAY \
    -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
    -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR \
    -e PULSE_SERVER=$PULSE_SERVER \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /mnt/wslg:/mnt/wslg \
    -v $(pwd)/nodes/scripts:/root/catkin_ws/src/nodes/scripts \
    --name qcar-nvidia \
    qcar-sim-nvidia
```

Why This Works:
- `--gpus all` activates GPU sharing automatically, assuming drivers are installed.
- No need to manually manage `/dev/dxg`, `LD_LIBRARY_PATH`, or adapter names. 
- No extra Dockerfile or entrypoint modifications are required—**the same logic used for AMD works**, but with fewer complications.

NVIDIA’s ecosystem (driver, runtime, and toolkit) is tightly integrated with both Docker and WSL2, significantly reducing setup time and debugging.
##### Final Results and Impact

The migration to WSL2 with Docker and GPU passthrough had a **profound impact on both performance and usability** of the QCar simulation environment.
#### Before Optimization:

- **Rendering performance:** 2–3 FPS
- **CPU utilization:** Reach high CPU usage spikes.
- **Responsiveness:** Severe input lag; RViz and Gazebo nearly unusable
- **Development friction:** Testing and debugging were highly inefficient due to laggy GUI and lack of feedback

#### After Optimization:
- **Rendering performance:** Increased to **50–60 FPS**, achieving near-native responsiveness
- **CPU utilization:** CPU is now free for other ROS-related tasks (e.g., sensor emulation, path planning)
- **GPU utilization:** Fully leveraged via WSLg, leading to hardware-accelerated OpenGL rendering
- **Developer experience:** Significant improvement in feedback loop, ease of testing, and simulation realism