#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory, GripperCommand
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from enum import Enum



# State definition
class ArmState(Enum):
    MOVE_1 = 1
    MOVE_2 = 2
    MOVE_3 = 3
    MOVE_4 = 4
    GRASP = 5
    LIFT = 6
    MOVE_PLACE = 7
    LOWER = 8
    RELEASE = 9
    RETURN_HOME = 10
    DONE = 11





class ArmGripperController(Node):
    """
    A ROS 2 node for controlling robot arm and gripper.
    Executes a single pick-and-place sequence with specific positions.
    """
    def __init__(self):
        super().__init__('arm_gripper_controller')

        # Action clients for arm and gripper
        self.arm_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/arm_controller/follow_joint_trajectory'
        )


        self.gripper_client = ActionClient(
            self,
            GripperCommand,
            '/gripper_action_controller/gripper_cmd'
        )

        # Wait for action servers
        self.get_logger().info('Waiting for action servers...')
        self.arm_client.wait_for_server()
        self.gripper_client.wait_for_server()
        self.get_logger().info('Action servers connected!')

        # Joint names
        self.joint_names = [
            'link1_to_link2', 'link2_to_link3', 'link3_to_link4',
            'link4_to_link5', 'link5_to_link6', 'link6_to_link6_flange'
        ]

        self.motion_map = {
            ArmState.MOVE_1: [-0.85, 0, 0, 0, 0, 0],
            ArmState.MOVE_2: [-0.85, -0.4, 0, 0, 0, 0],
            ArmState.MOVE_3: [-0.85, -0.4, 0, -0.2, 0, 0],
            ArmState.MOVE_4: [-0.85, -0.4, -0.3, -0.2, 0, 0],
            ArmState.LIFT: [-0.85, -0.4, -0.1, -0.2, 0, 0],
            ArmState.MOVE_PLACE: [0.0, -0.2, -0.1, -0.2, 0, 0],
            ArmState.LOWER: [0.0, -0.2, -0.33, -0.2, 0, 0],
            ArmState.RETURN_HOME: [0.0, 0, 0, 0, 0, 0],
        }

        # per state lock
        self.busy = False
        # Initial State
        self.state = ArmState.MOVE_1
        # Time-driven state machine autonomy loop
        self.timer = self.create_timer(3.0, self.state_machine_callback)


    # Arm Control
    def send_arm_command(self, positions: list):
        """Send arm to a specified joint positions."""
        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start = Duration(sec=2)

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = self.joint_names
        goal_msg.trajectory.points = [point]

        self.arm_client.send_goal_async(goal_msg)

    # Gripper Control
    def send_gripper_command(self, position: float):
        """Open or close the gripper."""
        goal_msg = GripperCommand.Goal()
        goal_msg.command.position = position
        goal_msg.command.max_effort = 5.0
        self.gripper_client.send_goal_async(goal_msg)


    def finish_step(self):
        self.busy = False


    def state_machine_callback(self):

        if self.busy:
            return  # wait until motion finishes

        self.busy = True

        if self.state in self.motion_map:
            self.get_logger().info(f"STATE: {self.state.name}")
            self.send_arm_command(self.motion_map[self.state])
            self.create_timer(2.5, self.finish_step)
            self.state = ArmState(self.state.value + 1)

        elif self.state == ArmState.GRASP:
            self.get_logger().info("STATE: GRASP")
            self.send_gripper_command(-0.3)
            self.create_timer(0.5, self.finish_step)
            self.state = ArmState.LIFT

        elif self.state == ArmState.RELEASE:
            self.get_logger().info("STATE: RELEASE")
            self.send_gripper_command(0.0)
            self.create_timer(0.5, self.finish_step)
            self.state = ArmState.RETURN_HOME

        elif self.state == ArmState.DONE:
            self.get_logger().info("Pick-and-place completed autonomously")






def main(args=None):
    rclpy.init(args=args)
    controller = ArmGripperController()
    
    rclpy.spin(controller)

    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()