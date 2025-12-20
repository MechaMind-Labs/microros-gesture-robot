#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
import math

def quaternion_to_euler(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    
    return roll_x, pitch_y, yaw_z

class ImuToTwist(Node):
    """
    A ROS 2 node that converts IMU data into Twist commands.
    It calibrates to the initial IMU orientation on startup.
    - Forward/backward motion is controlled by orientation around the Y-axis (pitch).
    - Left/right turning is controlled by angular velocity around the Z-axis (yaw rate).
    """
    def __init__(self):
        super().__init__('imu_to_twist_controller')

        # --- Parameters ---
        # Threshold for pitch angle (in radians) to control linear motion.
        self.pitch_threshold = self.declare_parameter('pitch_threshold', 0.1).get_parameter_value().double_value
        # Threshold for angular velocity (in rad/s) to control turning.
        self.ang_vel_threshold_z = self.declare_parameter('ang_vel_threshold_z', 0.1).get_parameter_value().double_value

        # Maximum speed scaling factor.
        self.max_linear_speed = self.declare_parameter('max_linear_speed', 2.0).get_parameter_value().double_value  # m/s
        self.max_angular_speed = self.declare_parameter('max_angular_speed', 1.0).get_parameter_value().double_value # rad/s

        # --- Calibration Variables ---
        self.is_calibrated = False
        self.pitch_offset = 0.0
        self.ang_vel_offset_z = 0.0

        # --- Publisher and Subscriber ---
        self.publisher_ = self.create_publisher(Twist, '/wheel_controller/cmd_vel_unstamped', 10)
        self.subscription = self.create_subscription(
            Imu,
            '/imu/data/filtered',
            self.imu_callback,
            10)
        
        self.get_logger().info(f"IMU to Twist Controller started. Waiting for IMU data to calibrate...")
        self.get_logger().info(f"-> Pitch Threshold: {self.pitch_threshold} rad | Z Ang Vel Threshold: {self.ang_vel_threshold_z} rad/s")

    def imu_callback(self, msg):
        """
        This function is called every time a new IMU message is received.
        """
        # --- Calibration Step ---
        if not self.is_calibrated:
            # Get the initial orientation as a quaternion
            q = msg.orientation
            # Convert to Euler angles to find the initial pitch
            _, initial_pitch, _ = quaternion_to_euler(q.x, q.y, q.z, q.w)
            
            # Store the initial pitch and Z angular velocity as offsets
            self.pitch_offset = initial_pitch
            self.ang_vel_offset_z = msg.angular_velocity.z
            self.is_calibrated = True
            self.get_logger().info(f"IMU calibrated with Pitch Offset: {self.pitch_offset:.2f} rad, Z Ang Vel Offset: {self.ang_vel_offset_z:.2f} rad/s")
            return

        # --- Calculate Relative Orientation and Velocity ---
        # Get current orientation
        q_current = msg.orientation
        _, current_pitch, _ = quaternion_to_euler(q_current.x, q_current.y, q_current.z, q_current.w)
        
        # Subtract the initial offset to get relative tilt
        relative_pitch = current_pitch - self.pitch_offset
        
        # Z-axis logic remains the same, using angular velocity
        relative_ang_vel_z = msg.angular_velocity.z - self.ang_vel_offset_z

        self.get_logger().info(f"Relative Pitch: {relative_pitch:7.2f} rad | Relative Ang Vel Z: {relative_ang_vel_z:7.2f} rad/s")

        # Create a new Twist message
        twist = Twist()

        # --- Forward/Backward Motion (from Pitch Angle) ---
        if abs(relative_pitch) > self.pitch_threshold:
            # A positive relative pitch (tilted down) means move forward.
            # A negative relative pitch (tilted up) means move backward.
            # We normalize by a reasonable tilt angle, e.g., 45 deg = pi/4 rad
            twist.linear.x = -self.max_linear_speed * (relative_pitch / (math.pi / 4.0))
        else:
            twist.linear.x = 0.0

        # --- Left/Right Turning (from Angular Vel Z) ---
        if abs(relative_ang_vel_z) > self.ang_vel_threshold_z:
            # This logic is unchanged as requested.
            twist.angular.z = self.max_angular_speed * (relative_ang_vel_z / (math.pi / 2.0))
        else:
            twist.angular.z = 0.0

        # Publish the calculated velocity command
        self.publisher_.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    imu_to_twist_node = ImuToTwist()
    try:
        rclpy.spin(imu_to_twist_node)
    except KeyboardInterrupt:
        pass
    finally:
        imu_to_twist_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
