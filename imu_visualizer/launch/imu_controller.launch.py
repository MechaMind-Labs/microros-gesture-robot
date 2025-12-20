import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    # Node to smooth the raw IMU data
    imu_smoother_node = Node(
        package='imu_visualizer',
        executable='imu_smoother',
        name='imu_smoother',
        parameters=[{'window_size': 15}]
    )

    # Node to apply the Madgwick filter for orientation
    imu_filter_node = Node(
        package='imu_filter_madgwick',
        executable='imu_filter_madgwick_node',
        name='imu_filter',
        parameters=[{
            'use_mag': False,
            'world_frame': 'odom',  
            'publish_tf': True,
            'gain': 0.05
        }],
        remappings=[
            ('/imu/data_raw', '/imu/data_filtered'),
            ('/imu/data', '/imu/data/filtered')
        ]
    )

    # Node to convert filtered IMU data to velocity commands
    imu_controller_node = Node(
        package='imu_visualizer',
        executable='imu_controller', # This should match the name in your setup.py
        name='imu_controller',
        parameters=[{
            'max_linear_speed': 0.5,
            'max_angular_speed': 1.0
        }]
    )

    # Launch all the nodes
    return LaunchDescription([
        imu_smoother_node,
        imu_filter_node,
        imu_controller_node,
    ])
