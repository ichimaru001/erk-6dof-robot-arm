# Erk Robotic Arm: ROS 2 & Gazebo Harmonic Simulation

An end-to-end ROS 2 package for **Erk**, a 3D-printed 5-DOF/6-DOF robotic arm. This repository contains the complete robot description, URDF/Xacro models, 3D mesh visual/collision geometries, RViz2 visualization setups, and Gazebo Harmonic physics simulation integration.

---

## 📌 Overview & Features

- **Robot Description (`erk_description`)**: Modular Xacro-based URDF with precise joint limits, link transforms, mass/inertia parameters, and STL visual/collision meshes.
- **RViz2 Visualization**: Interactive joint control using `joint_state_publisher_gui` and `robot_state_publisher`.
- **Gazebo Harmonic Simulation**: Physics simulation setup integrated with `gz_ros2_control`, joint state broadcasters, and position trajectory controllers.

---

## 🛠️ Prerequisites

- **OS**: Ubuntu 24.04 LTS (Noble Numbat)
- **ROS 2 Version**: Jazzy Jalisco
- **Simulator**: Gazebo Harmonic (`ros-jazzy-ros-gz`)
- **Key Dependencies**: `robot_state_publisher`, `joint_state_publisher_gui`, `xacro`, `ros2_control`, `gz_ros2_control`

---

## 📂 Repository Structure

```text
erk_ws/
└── src/
    └── erk_description/
        ├── config/             # Controller configurations (gazebo_controllers.yaml)
        ├── launch/             # Launch files (display.launch.py, gazebo.launch.py)
        ├── meshes/             # Visual and collision STL files
        ├── urdf/               # Robot description files (erk.urdf.xacro, etc.)
        ├── CMakeLists.txt      # Build configuration
        └── package.xml         # ROS 2 package manifest
```

---

## 🚀 Building & Launching

### 1. Build the Workspace

```bash
cd ~/erk_ws
colcon build --symlink-install
source install/setup.bash
```

### 2. Visualize in RViz2 (Manual Joint Control)

To inspect the robot model and test joint movements using sliders in RViz2:

```bash
ros2 launch erk_description display.launch.py
```

### 3. Launch Gazebo Harmonic Simulation

To launch the physics simulation environment in Gazebo with active controllers:

```bash
ros2 launch erk_description gazebo.launch.py
```

---

## 📽️ Video Demonstration

A screen recording demonstrating the robot arm running in Gazebo Harmonic and RViz2 is included in the repository:
- **File Location**: `simulation_demo.mp4` (placed in the repository root directory)
- **Contents**: Showcases launching the simulation via terminal and controlling/observing joint movements in Gazebo and RViz2.
