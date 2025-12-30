# mycobot_description #
# MyCobot 280 ROS 2 Package

This repository contains a **ROS 2 Jazzy description package** for the **MyCobot 280** robotic arm with an **adaptive gripper**.

It provides a modular, Xacro-based URDF structure and meshes for visualization and collision. The package is ready for integration with RViz, Gazebo, or MoveIt in the future.

---

## Features

- Modular **Xacro-based URDF** for easy customization  
- **Adaptive gripper** with mimic joints for coordinated finger movement  
- Meshes for **visualization** and **collision detection**  
- Fully modular structure for base, arm, and gripper  

---
## Repository Structure

mycobot_description/
├── urdf/ # Xacro files for the robot, arm, and gripper
│ ├── mech/ # Modular parts (base, arm, gripper)
│ ├── robots/ # Full robot Xacro file
├── meshes/ # 3D models (dae/stl) for visualization and collision
├── package.xml
└── CMakeLists.txt