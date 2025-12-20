#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from collections import deque
import numpy as np

class ImuSmoother(Node):
    def __init__(self):
        super().__init__('imu_smoother_node')

        # Declare a parameter for the window size of the moving average filter
        self.declare_parameter('window_size', 10)
        window_size = self.get_parameter('window_size').get_parameter_value().integer_value
        self.get_logger().info(f'Using moving average window size of {window_size}')

        # Create deques (double-ended queues) to store recent IMU readings
        self.accel_x_buffer = deque(maxlen=window_size)
        self.accel_y_buffer = deque(maxlen=window_size)
        self.accel_z_buffer = deque(maxlen=window_size)
        self.gyro_x_buffer = deque(maxlen=window_size)
        self.gyro_y_buffer = deque(maxlen=window_size)
        self.gyro_z_buffer = deque(maxlen=window_size)

        # Create subscriber to the raw IMU topic
        self.subscription = self.create_subscription(
            Imu,
            '/imu/data_raw',
            self.imu_callback,
            10)
        
        # Create publisher for the filtered IMU topic
        self.publisher = self.create_publisher(Imu, '/imu/data_filtered', 10)

    def imu_callback(self, msg):
        # Add current sensor readings to their respective buffers
        self.accel_x_buffer.append(msg.linear_acceleration.x)
        self.accel_y_buffer.append(msg.linear_acceleration.y)
        self.accel_z_buffer.append(msg.linear_acceleration.z)
        self.gyro_x_buffer.append(msg.angular_velocity.x)
        self.gyro_y_buffer.append(msg.angular_velocity.y)
        self.gyro_z_buffer.append(msg.angular_velocity.z)

        # Create a new Imu message for the filtered data
        filtered_msg = Imu()
        # Copy header and orientation from the original message
        filtered_msg.header = msg.header
        filtered_msg.orientation = msg.orientation
        filtered_msg.orientation_covariance = msg.orientation_covariance
        filtered_msg.linear_acceleration_covariance = msg.linear_acceleration_covariance
        filtered_msg.angular_velocity_covariance = msg.angular_velocity_covariance

        # Calculate the average (mean) of the values in each buffer
        filtered_msg.linear_acceleration.x = np.mean(self.accel_x_buffer)
        filtered_msg.linear_acceleration.y = np.mean(self.accel_y_buffer)
        filtered_msg.linear_acceleration.z = np.mean(self.accel_z_buffer)
        filtered_msg.angular_velocity.x = np.mean(self.gyro_x_buffer)
        filtered_msg.angular_velocity.y = np.mean(self.gyro_y_buffer)
        filtered_msg.angular_velocity.z = np.mean(self.gyro_z_buffer)

        # Publish the filtered message
        self.publisher.publish(filtered_msg)


def main(args=None):
    rclpy.init(args=args)
    imu_smoother = ImuSmoother()
    rclpy.spin(imu_smoother)
    imu_smoother.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
