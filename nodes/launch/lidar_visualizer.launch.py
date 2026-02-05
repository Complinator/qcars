from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_qcar_nodes',
            executable='lidar_visualizer',
            name='lidar_visualizer',
            output='screen',
            emulate_tty=True
        )
    ])
