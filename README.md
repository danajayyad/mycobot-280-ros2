# MyCobot 280 ROS 2 Workspace

This is a **ROS 2 Jazzy workspace** containing the MyCobot 280 robot packages, including:

1. **mycobot_description** – URDF/Xacro description of the robot and adaptive gripper  
2. **mycobot_ros2** – Main ROS 2 package for nodes, controllers, and future development

The workspace is structured for modular development, RViz visualization, and future Gazebo or MoveIt 2 integration.

---

## Visualizing the MyCobot 280 in RViz (URDF / Xacro)

This package provides a **URDF/Xacro** description of the MyCobot 280 robot arm and enables visualization in RViz using ROS 2 tools.

---

## Installation & Dependencies

The MyCobot description package depends on the **URDF tutorial package** (`urdf_tutorial`) for launch and visualization tools.

### How Dependencies Are Managed

- `CMakeLists.txt` of `mycobot_description` package includes:

```cmake
find_package(urdf_tutorial REQUIRED)
```

- `package.xml` of `mycobot_description` package includes:

```xml
<buildtool_depend>urdf_tutorial</buildtool_depend>
```

### Build Instructions

From the workspace root:

```bash
# Install dependencies automatically
rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y

# Build workspace
colcon build
source install/setup.bash
```

---

## Launching the Robot Visualization

Run:

```bash
ros2 launch urdf_tutorial display.launch.py \
model:=/root/robotic_arm_ws/src/mycobot_ros2/mycobot_description/urdf/robots/mycobot_280.urdf.xacro
```

### What This Command Does

- Launches a predefined launch file from the `urdf_tutorial` package  
- Loads the MyCobot 280 Xacro file  
- Converts the Xacro file into a URDF internally  
- Starts RViz with an interactive robot model  

---

## Nodes That Are Launched

| Node                        | Function                                                                  |
|-----------------------------|---------------------------------------------------------------------------|
| `joint_state_publisher_gui` | Provides sliders for each joint and publishes angles to `/joint_states`   |
| `robot_state_publisher`     | Subscribes to `/joint_states` and computes link transforms using the URDF |
| `rviz2`                     | Visualizes the robot using TF data and updates the pose in real time      |

---

## Behind the Scenes

- **Xacro Processing:** The `.urdf.xacro` file is processed to expand macros, conditions, and arguments  
- **URDF Generation:** The output is a plain URDF XML used by the `robot_state_publisher`  
- **Joint Control Flow:**
  1. `joint_state_publisher_gui` → publishes to `/joint_states`
  2. `robot_state_publisher` → computes transforms and publishes to `/tf`
  3. `rviz2` → listens to `/tf` and updates the 3D model

> **Important:** This setup is for **visualization only**. It does not include physics, controllers, or real robot motion.

---

