import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('imu_visualizer')

    rviz_config_path = os.path.join(
        pkg_share,
        'rviz',
        'imu_config.rviz'
    )


    urdf_path = os.path.join(
        get_package_share_directory('imu_visualizer'),
        'urdf',
        'imu_cube.urdf'
    )

    # 1. IMU smoother node
    imu_smoother_node = Node(
        package='imu_visualizer',
        executable='imu_smoother',
        name='imu_smoother',
        parameters=[{'window_size': 15}]
    )

    # 2. IMU filter (Madgwick) → publishes odom -> imu_link
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

    # 3. Robot state publisher (reads URDF)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': open(urdf_path).read()}]
    )

    # 4. RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
    )

    return LaunchDescription([
        imu_smoother_node,
        imu_filter_node,
        robot_state_publisher_node,
        rviz_node
    ])
